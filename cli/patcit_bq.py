import patcit_bq_create
import patcit_bq_export
import typer

app = typer.Typer()

app.add_typer(patcit_bq_create.app, name="create")
app.add_typer(patcit_bq_export.app, name="export")

if __name__ == "__main__":
    app()
