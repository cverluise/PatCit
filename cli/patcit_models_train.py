import json
import os
import random


import spacy
import typer

from spacy.util import minibatch, compounding
from wasabi import Printer

msg = Printer()
app = typer.Typer()


@app.command()
def textcat(
    train_texts: str,
    train_cats: str,
    model_dir: str = typer.Option(None, help="Dir for saving the model (if not None)"),
    spacy_model: str = typer.Option("en_core_web_sm", help="spaCy Model to build on"),
    architecture: str = typer.Option(
        "ensemble",
        help="Architecture of the classifier ['ensemble', " "'simple_cnn', 'bow']",
    ),
    n_iter: int = typer.Option(100, help="Nbr of training iteration"),
    min_delta: float = typer.Option(
        1e-3,
        "Early stopping. If the loss does not decline by at "
        "least <min_delta>, we stop",
    ),
):
    """
    Save a spaCy model with an additional text-categorizer pipe trained on TRAIN-TEXTS,
    TRAIN-CATS
    Based on https://spacy.io/usage/training/

    Notes:
        Expect TRAIN-TEXTS to be a list of texts for training (["text",]) and TRAIN-CATS to be list
        of cats dict for training ([{LABEL:bool, },])
    """

    def load_data(file):
        with open(file, "r") as fin:
            return json.loads(fin.read())  # now a list

    train_texts = load_data(train_texts)
    train_cats = load_data(train_cats)

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
    for cat in set(train_cats):  # CATS:
        textcat.add_label(cat)

    # Format training data
    train_data = list(zip(train_texts, [{"cats": cats} for cats in train_cats]))

    # Disable other pipes
    pipe_exceptions = ["textcat", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

    # Train textcat
    early_stoping = []
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
    if model_dir:
        file = os.path.join(model_dir)
        nlp.to_disk(file)
        msg.good(f"Model saved: {file}")


if __name__ == "__main__":
    app()
