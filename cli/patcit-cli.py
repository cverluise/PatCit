import patcit_bq
import patcit_npl
import patcit_schema
import typer

app = typer.Typer()

app.add_typer(patcit_bq.app, name="bq")
app.add_typer(patcit_npl.app, name="npl")
app.add_typer(patcit_schema.app, name="schema")

if __name__ == "__main__":
    app()
