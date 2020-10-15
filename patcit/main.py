from patcit.bq import main as patcit_bq
from patcit.brew import main as patcit_brew
from patcit.data import main as patcit_data
from patcit.grobid import main as patcit_grobid
from patcit.model import main as patcit_model
from patcit.serialize import main as patcit_serialize
import typer

app = typer.Typer()

app.add_typer(patcit_bq.app, name="bq")
app.add_typer(patcit_brew.app, name="brew")
app.add_typer(patcit_data.app, name="data")
app.add_typer(patcit_grobid.app, name="grobid")
app.add_typer(patcit_model.app, name="model")
app.add_typer(patcit_serialize.app, name="serialize")

if __name__ == "__main__":
    app()
