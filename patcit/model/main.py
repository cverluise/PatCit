from patcit.model import finetune
from patcit.model import evaluate
import typer

app = typer.Typer()

app.add_typer(evaluate.app, name="evaluate")
app.add_typer(finetune.app, name="finetune")

if __name__ == "__main__":
    app()
