import re

import spacy
import typer
from spacy.language import Doc

app = typer.Typer()


# class RESTCountriesComponent(object):
#     name = 'countries'
#     def __init__(self, nlp, label='GPE'):
#         self.countries = [u'MyCountry', u'MyOtherCountry']
#         self.label = nlp.vocab.strings[label]
#         patterns = [nlp(c) for c in self.countries]
#         self.matcher = PhraseMatcher(nlp.vocab)
#         self.matcher.add('COUNTRIES', None, *patterns)
#     def __call__(self, doc):
#         matches = self.matcher(doc)
#         spans = []
#         for _, start, end in matches:
#             entity = Span(doc, start, end, label=self.label)
#             spans.append(entity)
#         doc.ents = list(doc.ents) + spans
#         for span in spans:
#             span.merge()
#         return doc


class UrlsMatcher(object):
    name = "urls_matcher"

    def __init__(self, nlp):
        pass

    def __call__(self, doc):
        # http://www.noah.org/wiki/RegEx_Python
        expression = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        urls = re.findall(expression, doc.text)
        Doc.set_extension("urls", default=True, force=True)
        doc._.urls = re.findall(expression, doc.text)
        return doc


# def urls_matcher_(doc):


@app.command()
def urls_matcher(model: str, dest: str = None):
    """Add custom component matching urls based on regex"""
    nlp = spacy.blank(model) if len(model) == 2 else spacy.load(model)
    nlp.add_pipe(UrlsMatcher, last=True)
    if dest:
        nlp.to_disk(dest)
