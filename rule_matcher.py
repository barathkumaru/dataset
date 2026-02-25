import re

class RuleMatcher:
    def __init__(self, rules):
        """
        Initializes RuleMatcher with a given set of rules.
        Each rule is a tuple containing a regex pattern and its associated weight.
        
        :param rules: List of tuples [(regex_pattern, weight), ...]
        """
        self.rules = rules

    def match(self, text):
        """
        Matches the given text against the rules and returns a weighted score.
        
        :param text: The text to match against the rules.
        :return: Total weighted score of matched rules.
        """
        total_score = 0
        for pattern, weight in self.rules:
            if re.search(pattern, text):
                total_score += weight
        return total_score

# Example usage:
if __name__ == '__main__':
    rules = [
        (r'\berror\b', 5),  # Matches 'error' with a weight of 5
        (r'\bwarning\b', 3),  # Matches 'warning' with a weight of 3
        (r'\binfo\b', 1)  # Matches 'info' with a weight of 1
    ]
    matcher = RuleMatcher(rules)
    score = matcher.match('This is an error message. Check warning.')
    print(f'Total Score: {score}')