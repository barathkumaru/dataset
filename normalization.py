"""
Text Normalization Module
Handles entity text cleaning and standardization.
Production-optimized with caching and regex compilation.
"""

import re
from typing import Set, Optional
from functools import lru_cache


class TextNormalizer:
    """Handles text normalization for entity matching."""
    
    # Compiled regex patterns for performance
    TITLE_PATTERN = re.compile(
        r'\b(mr|mrs|ms|dr|prof|sir|lady|lord|king|queen|prince|princess|'
        r'judge|senator|governor|mayor|commissioner|general|colonel|captain|'
        r'lieutenant|sergeant|officer|reverend|bishop|rabbi|imam|fr|esq)\b',
        re.IGNORECASE | re.UNICODE
    )
    
    COMPANY_SUFFIX_PATTERN = re.compile(
        r'\b(pvt|ltd|llc|inc|corp|corporation|company|co|lp|llp|pa|pllc|'
        r'a\.g|gmbh|sa|sarl|limited|plc|nv|bv|ag|kft|spd|sp\.a|s\.r\.l|'
        r'inc\.|corp\.|co\.|ltd\.|llc\.|pte|pty|limited\.?)*\b',
        re.IGNORECASE | re.UNICODE
    )
    
    PUNCTUATION_PATTERN = re.compile(r'[^\\w\s]', re.UNICODE)
    WHITESPACE_PATTERN = re.compile(r'\s+')
    
    @staticmethod
    @lru_cache(maxsize=10000)
    def remove_titles(text: str) -> str:
        """Remove titles from text (Mr, Mrs, Dr, etc)."""
        if not text or not isinstance(text, str):
            return ""
        return TextNormalizer.TITLE_PATTERN.sub('', text).strip()
    
    @staticmethod
    @lru_cache(maxsize=10000)
    def remove_company_suffixes(text: str) -> str:
        """Remove company suffixes (Inc, Ltd, LLC, etc)."""
        if not text or not isinstance(text, str):
            return ""
        return TextNormalizer.COMPANY_SUFFIX_PATTERN.sub('', text).strip()
    
    @staticmethod
    @lru_cache(maxsize=10000)
    def remove_punctuation(text: str) -> str:
        """Remove all punctuation from text."""
        if not text or not isinstance(text, str):
            return ""
        return TextNormalizer.PUNCTUATION_PATTERN.sub('', text)
    
    @staticmethod
    @lru_cache(maxsize=10000)
    def normalize_whitespace(text: str) -> str:
        """Normalize multiple spaces to single space."""
        if not text or not isinstance(text, str):
            return ""
        return TextNormalizer.WHITESPACE_PATTERN.sub(' ', text).strip()
    
    @staticmethod
    def normalize_person(text: str) -> str:
        """Normalize person name."""
        if not text or not isinstance(text, str):
            return ""
        
        # Remove titles
        text = TextNormalizer.remove_titles(text)
        # Remove punctuation
        text = TextNormalizer.remove_punctuation(text)
        # Normalize whitespace
        text = TextNormalizer.normalize_whitespace(text)
        # Lowercase
        text = text.lower()
        
        return text.strip()
    
    @staticmethod
    def normalize_company(text: str) -> str:
        """Normalize company name."""
        if not text or not isinstance(text, str):
            return ""
        
        # Remove company suffixes
        text = TextNormalizer.remove_company_suffixes(text)
        # Remove punctuation
        text = TextNormalizer.remove_punctuation(text)
        # Normalize whitespace
        text = TextNormalizer.normalize_whitespace(text)
        # Lowercase
        text = text.lower()
        
        return text.strip()
    
    @staticmethod
    def extract_tokens(text: str) -> list[str]:
        """Extract individual tokens from normalized text."""
        if not text or not isinstance(text, str):
            return []
        return text.split()
    
    @staticmethod
    def extract_first_last(text: str) -> tuple[Optional[str], Optional[str]]:
        """Extract first and last name from person text."""
        tokens = TextNormalizer.extract_tokens(text)
        if len(tokens) == 0:
            return None, None
        elif len(tokens) == 1:
            return tokens[0], None
        else:
            return tokens[0], tokens[-1]
    
    @staticmethod
    def get_core_name(text: str) -> str:
        """Get core company name (just tokens, no suffixes)."""
        # Already removes suffixes, return as is
        return text
