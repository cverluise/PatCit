import patcit_bq
import typer

app = typer.Typer()

app.add_typer(patcit_bq.app, name="bq")

if __name__ == "__main__":
    app()
