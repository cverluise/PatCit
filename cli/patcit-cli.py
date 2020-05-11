import patcit_bq
import patcit_npl
import typer

app = typer.Typer()

app.add_typer(patcit_bq.app, name="bq")
app.add_typer(patcit_npl.app, name="npl")

if __name__ == "__main__":
    app()
