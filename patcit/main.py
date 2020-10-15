import patcit_bq
import patcit_schema
import patcit_serialize
import patcit_grobid
import patcit_models
import typer

app = typer.Typer()

app.add_typer(patcit_bq.app, name="bq")
app.add_typer(patcit_schema.app, name="schema")
app.add_typer(patcit_serialize.app, name="serialize")
app.add_typer(patcit_grobid.app, name="grobid")
app.add_typer(patcit_models.app, name="models")

if __name__ == "__main__":
    app()
