import spacy
from spacy.tokens import Span

class SpacyValidator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SpacyValidator, cls).__new__(cls)
            cls.nlp = spacy.load('en_core_web_sm')
        return cls._instance

    def validate(self, text, expected_entities):
        doc = self.nlp(text)
        found_entities = [Span(doc, ent.start, ent.end, label=ent.label_) for ent in doc.ents]

        # Check if expected entities are found
        return all(entity.label_ in [ent.label_ for ent in found_entities] for entity in expected_entities)

# Example usage:
# validator = SpacyValidator()
# text = 'Apple is looking at buying U.K. startup for $1 billion'
# expected_entities = [Span(doc, 0, 1, label='ORG'), Span(doc, 8, 9, label='GPE')]
# result = validator.validate(text, expected_entities)

