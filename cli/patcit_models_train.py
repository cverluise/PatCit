import os
import random
from glob import glob

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import spacy
import typer
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
from spacy.util import minibatch, compounding
from wasabi import Printer

msg = Printer()

LABELS = {
    4: "BIBLIOGRAPHICAL_REFERENCE",
    5: "SEARCH_REPORT",
    6: "OFFICE_ACTION",
    7: "DATABASE",
    8: "WEBPAGE",
    9: "PATENT",
    10: "OTHERS",
    11: "NA",
    12: "PRODUCT_DOCUMENTATION",  # seems that we need NER-PROD to distinguish 8 and 12
    1752: "NORM_STANDARD",
    1773: "LITIGATION",
}

CATS = [cat for cat in list(LABELS.values()) if cat != "OTHERS"]  # we skip OTHERS


def load_data(path):
    """
    Load data from files in <PATH>
    Nb: input files should be labeled according to the LABELS (local var)
    :param path: str, wildcard enabled
    :return: pd.DataFrame
    """
    files = glob(path)

    l = []
    for file in files:
        tmp = pd.read_csv(file).reset_index()
        tmp["label"] = tmp["label"].apply(lambda x: LABELS[x])
        l.append(tmp)
    df = pd.concat(l, axis=0, ignore_index=True)
    df = df.drop("index", axis=1)
    print(df.groupby("label").count().sort_values("text", ascending=False)["text"])
    tmp = df.query("label not in ['OTHERS']")
    msg.info(title=f"Loaded data: {len(tmp)} rows (excl 'OTHERS')")
    return df


def prep_data(df, train_share=0.8):
    """
    Return the data in a proper format for spaCy multi-class textCategorizer training
    See dicussion here https://github.com/explosion/spaCy/issues/1997
    :param df: pd.DataFrame, from load_data()
    :param train_share: float, share of the data used in the training task
    :return: list (4), train_texts, train_cats, dev_texts, dev_gold
    """
    tmp = df.query("label not in ['OTHERS']")
    tmp = tmp.sample(frac=1, random_state=42)  # shuffle

    n = int(len(tmp) * train_share)

    texts = tmp["text"].values.tolist()
    gold = tmp["label"].values.tolist()

    cats = [{k: False for k in CATS} for _ in range(len(gold))]
    for i in range(len(gold)):
        cats[i].update({gold[i]: True})

    # We format the cats as
    # {'BIBLIOGRAPHICAL_REFERENCE':False, 'SEARCH_REPORT': False, 'OFFICE_ACTION': True, ...}
    # where the value True is the gold label. Nb, gold is a list of the gold labels
    # ['OFFICE_ACTION', ..]
    # see discussion here https://github.com/explosion/spaCy/issues/1997
    train_texts = texts[:n]
    dev_texts = texts[n:]
    train_cats = cats[:n]
    dev_gold = gold[n:]

    msg.info(f"{n} training samples and {len(tmp) - n} dev samples.")

    return train_texts, train_cats, dev_texts, dev_gold


def train_model(
    train_texts,
    train_cats,
    spacy_model="en_core_web_sm",
    architecture="ensemble",
    n_iter: int = 100,
    min_delta: float = 1e-3,
    path=None,
):
    """
    Return a <spacy_model> with an additional text-categorizer pipe
    Based on https://spacy.io/usage/training/
    :param train_texts: list, list of texts for training (["text"])
    :param train_cats: list, list of cats for training ({LABEL:bool})
    :param spacy_model: spacy.lang.xx.XX
    :param architecture: str, architecture of the classifier ["ensemble", "simple_cnn", "bow"]
    :param n_iter: int, nb of training iteration
    :param min_delta: float, if the loss does not decline by at least <min_delta>, we stop
    :param path: str, path for saving the model (if not None)
    :return: spacy.lang.xx.XX
    """
    # if path:
    #     assert os.path.exists(path)

    # Load baseline model
    try:
        nlp = spacy.load(spacy_model)
    except IOError as e:
        raise (
            e,
            f"To load a spacy model by its name, run 'python -m "
            f"spacy download {spacy_model}'.",
        )

    # Create textcat pipe
    # Warning, if the model already has a textcat pipe, it will be overwritten
    # TODO: improve based on online example
    textcat = nlp.create_pipe(
        "textcat", config={"exclusive_classes": True, "architecture": architecture}
    )
    nlp.add_pipe(textcat, last=True)

    # Add labels
    for cat in CATS:
        textcat.add_label(cat)

    # Format training data
    train_data = list(zip(train_texts, [{"cats": cats} for cats in train_cats]))

    # Disable other pipes
    pipe_exceptions = ["textcat", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

    early_stoping = []
    # Train textcat
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        print("Training the model...")
        print("{:^5}".format("LOSS"))
        batch_sizes = compounding(4.0, 32.0, 1.001)
        loss = 1e6
        for i in range(n_iter):
            losses = {}
            # Batch up the examples using spaCy's minibatch
            random.shuffle(train_data)
            batches = minibatch(train_data, size=batch_sizes)
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=0.2, losses=losses)
            print("{0:.3f}\t".format(losses["textcat"]))

            # callback
            delta_loss = loss - losses["textcat"]
            loss = losses["textcat"]
            if min_delta > delta_loss:
                early_stoping += [i]
                if len(early_stoping) >= 2:
                    if early_stoping[-1] - early_stoping[-2] == 1:
                        # we stop if the loss does not decline by at least 1e-3 twice consecutively
                        break

    # Save the model
    if path:
        file = os.path.join(path)
        nlp.to_disk(file)
        msg.good(f"Model saved: {file}")

    return nlp


def clip_score(score, threshold=0.5):
    bool = True if score > threshold else False
    return bool


def get_pred(dev_texts, nlp, threshold=0.5):
    """
    Return the predicted labels for the texts in dev_texts
    :param dev_texts: ["3GPP, Third Generation...", "US Application ...."]
    :param nlp:
    :param threshold: float
    :return:
    """
    # TODO: use nlp.pipe
    pred = []
    for text in dev_texts:
        doc = nlp(text)
        pred_cats = {k: clip_score(v, threshold) for k, v in doc.cats.items()}
        pred_cat = [k for k, v in pred_cats.items() if v]
        # TODO: report score
        pred += pred_cat if pred_cat else ["None"]
    return pred


def plot_confusion(confusion_matrix, labels, file):
    """
    Wrapper for plotly ff.create_annotated_heatmap
    """
    fig = ff.create_annotated_heatmap(
        z=np.matrix.round(confusion_matrix, 1),
        x=labels,
        y=labels,
        colorscale="RdBu",
        reversescale=True,
        font_colors=["white", "black"],
    )
    fig.write_image(file)


def evaluate(gold, pred, path):
    """
    Return a series of evaluation objects (confusion matrix, multi-class
    precision-recall-f1-support, average accuracy-precision-recall-f1)
    :param gold: list, gold labels []
    :param pred: list, predicted labels []
    :param path: str, path to save evaluation objects
    :return:
    """
    for normalize in ["pred", "true", None]:
        file = os.path.join(
            path, f"confusion{'_norm-' + normalize if normalize else ''}.png"
        )
        confusion_norm = np.matrix.round(
            confusion_matrix(gold, pred, labels=CATS, normalize=normalize), 2
        )
        plot_confusion(confusion_norm, CATS, file)
        msg.good(f"{file} saved")

    # Multiclass precision recall f1 support
    multi_prfs = precision_recall_fscore_support(gold, pred, labels=CATS)
    df_multi_prfs = pd.DataFrame(
        multi_prfs, columns=CATS, index=["precision", "recall", "f1", "support"]
    ).round(decimals=2)
    file = os.path.join(path, f"multi_prfs.csv")
    df_multi_prfs.to_csv(file)
    msg.good(f"{file} saved")

    # Average accuracy precision recall f1
    file = os.path.join(path, f"aprf.csv")
    confusion = confusion_matrix(gold, pred, labels=CATS)
    accuracy = sum([confusion[i, i] for i in range(len(confusion))]) / np.sum(confusion)
    prfs = precision_recall_fscore_support(gold, pred, labels=CATS, average="weighted")
    aprf = [accuracy] + list(prfs[:-1])
    df_aprf = pd.DataFrame(data=aprf, index=["accuracy", "precision", "recall", "f1"]).T
    df_aprf.to_csv(file, index=False)
    msg.good(f"{file} saved")


def main(
    data_path: str,
    train_share: float = typer.Option(
        default=0.8, help="Share of the data dedicated to training"
    ),
    spacy_model: str = typer.Option(
        default="en_core_web_sm", help="Name of the spaCy model"
    ),
    architecture: str = typer.Option(
        default="ensemble", help="Architecture of the model"
    ),
    model_path: str = typer.Option(
        default=None,
        help="Path to save the spaCy model with the trained text categorizer",
    ),
    eval_path: str = typer.Option(default=None, help="Path to save evaluation objects"),
):
    """
    Train a multi-class text classifier using spaCy textCategorizer

    NB: Wildcard enabled for argument DATA-PATH
    """
    model_name = f"{spacy_model}_npl-class-{architecture}-{train_share}"
    df = load_data(data_path)
    train_texts, train_cats, dev_texts, dev_gold = prep_data(
        df, train_share=train_share
    )
    nlp = train_model(
        train_texts,
        train_cats,
        spacy_model=spacy_model,
        architecture=architecture,
        path=os.path.join(model_path, model_name),
    )
    preds = get_pred(dev_texts, nlp)
    if eval_path:
        if train_share == 1:
            raise typer.Abort("Model cannot be evaluated with train-share=1")
        try:
            os.mkdir(os.path.join(eval_path, model_name))
        except FileExistsError:
            msg.warn(f"{model_name} already exists in {eval_path}.")
            overwrite = typer.confirm("Overwrite existing files?")
            if not overwrite:
                raise typer.Abort()
        evaluate(dev_gold, preds, os.path.join(eval_path, model_name))


if __name__ == "__main__":
    typer.run(main)
