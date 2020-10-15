from patcit.model import add_component
from patcit.model import finetune
from patcit.model import evaluate
import typer

app = typer.Typer()

app.add_typer(add_component.app, name="add_component")
app.add_typer(evaluate.app, name="evaluate")
app.add_typer(finetune.app, name="finetune")

if __name__ == "__main__":
    app()
