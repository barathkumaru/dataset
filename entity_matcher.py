import spacy
from spacy.matcher import Matcher

class EntityMatcher:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.matcher = Matcher(self.nlp.vocab)

    def add_rule(self, rule_id, pattern):
        self.matcher.add(rule_id, [pattern])

    def rule_based_matching(self, text):
        doc = self.nlp(text)
        matches = self.matcher(doc)
        return matches

    def validate_with_ner(self, text):
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities

    def hybrid_matcher(self, text, rule_id, pattern):
        self.add_rule(rule_id, pattern)
        rule_matches = self.rule_based_matching(text)
        ner_matches = self.validate_with_ner(text)
        return rule_matches, ner_matches

# Example usage:
# entity_matcher = EntityMatcher()
# rule_id = 'COMPANY_NAME'
# pattern = [{'LOWER': 'openai'}]
# text = "I work at OpenAI."
# rule_matches, ner_matches = entity_matcher.hybrid_matcher(text, rule_id, pattern)
# print(rule_matches)
# print(ner_matches)