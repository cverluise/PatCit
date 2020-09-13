import patcit_models_data
import patcit_models_evaluate
import patcit_models_process
import patcit_models_train
import patcit_models_finetune
import typer

app = typer.Typer()

app.add_typer(patcit_models_data.app, name="data")
app.add_typer(patcit_models_evaluate.app, name="evaluate")
app.add_typer(patcit_models_train.app, name="train")
app.add_typer(patcit_models_process.app, name="process")
app.add_typer(patcit_models_finetune.app, name="finetune")

if __name__ == "__main__":
    app()
