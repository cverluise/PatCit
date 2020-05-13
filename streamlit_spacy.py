# coding: utf-8
"""
Example of a Streamlit app for an interactive spaCy model visualizer. You can
either download the script, or point streamlit run to the raw URL of this
file. For more details, see https://streamlit.io.

Installation:
pip install streamlit
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
python -m spacy download de_core_news_sm

Usage:
streamlit run streamlit_spacy.py
"""
from __future__ import unicode_literals

import json
import random

import pandas as pd
import spacy
import streamlit as st
from glom import glom
from spacy import displacy

SPACY_MODEL_NAMES = ["./models/database/en_database_0.1/"]
EXAMPLE_FILES = ["./models/database/data/eval4spacy_01.json"]
DEFAULT_TEXT = "GenBank Accession No. AA705297 (Dec. 24, 1997 DATE)."
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius:
0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""


@st.cache(allow_output_mutation=True)
def load_model(name):
    return spacy.load(name)


@st.cache(allow_output_mutation=True)
def process_text(model_name, text):
    nlp = load_model(model_name)
    return nlp(text)


st.sidebar.title("Interactive spaCy model visualizer")
st.sidebar.markdown(
    """
Process text with [PatCit](https://github.com/cverluise/PatCit) models and visualize named
entities.
"""
)

spacy_model = st.sidebar.selectbox("Model name", SPACY_MODEL_NAMES)
example_file = st.sidebar.selectbox("Example file", EXAMPLE_FILES)
model_load_state = st.info(f"Loading model '{spacy_model}'...")
nlp = load_model(spacy_model)
model_load_state.empty()

examples_load_state = st.info(f"Loading examples from '{example_file}'...")
jdocs = json.loads(open(example_file, "r").read())
examples = [
    glom(jdocs[i], ("paragraphs", ["raw"]))[0]
    for i in random.choices(range(len(jdocs)), k=10)
]
examples_load_state.empty()

text = st.text_area("Text to analyze", DEFAULT_TEXT)
doc = process_text(spacy_model, text)

if "ner" in nlp.pipe_names:
    st.header("Named Entities")
    st.sidebar.header("Named Entities")
    label_set = nlp.get_pipe("ner").labels
    labels = st.sidebar.multiselect(
        "Entity labels", options=label_set, default=list(label_set)
    )
    html = displacy.render(doc, style="ent", options={"ents": labels})
    # Newlines seem to mess with the rendering
    html = html.replace("\n", " ")
    st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)
    attrs = ["text", "label_", "start", "end", "start_char", "end_char"]
    if "entity_linker" in nlp.pipe_names:
        attrs.append("kb_id_")
    data = [
        [str(getattr(ent, attr)) for attr in attrs]
        for ent in doc.ents
        if ent.label_ in labels
    ]
    df = pd.DataFrame(data, columns=attrs)
    st.dataframe(df)

# if "textcat" in nlp.pipe_names:
#     st.header("Text Classification")
#     st.markdown(f"> {text}")
#     df = pd.DataFrame(doc.cats.items(), columns=("Label", "Score"))
#     st.dataframe(df)

st.header("Examples")
st.write("  \n  \n".join(examples))

st.header("JSON model meta")
if st.button("Show JSON model meta"):
    st.json(nlp.meta)
