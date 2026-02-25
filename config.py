"""
Configuration Module
Central configuration for the Entity Matching system.
Production-ready with environment variable support.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict


class EntityType(Enum):
    """Supported entity types."""
    PERSON = "PERSON"
    COMPANY = "COMPANY"

@dataclass
class WeightConfig:
    """Weight configuration for entity matching scores."""
    
    # PERSON weights
    PERSON_FULL_NAME: float = 1.0
    PERSON_FIRST_LAST: float = 0.9
    PERSON_MIDDLE_COMBINATIONS: float = 0.75
    PERSON_FIRST_ONLY: float = 0.4
    PERSON_LAST_ONLY: float = 0.6
    
    # COMPANY weights
    COMPANY_FULL_NAME: float = 1.0
    COMPANY_CORE_NAME: float = 0.9
    COMPANY_ACRONYM: float = 0.85
    COMPANY_STRONG_TOKENS: float = 0.5

@dataclass
class ThresholdConfig:
    """Threshold configuration for hybrid matching."""
    weak_threshold: float = 0.6
    strong_threshold: float = 0.9

@dataclass
class SpacyConfig:
    """spaCy model configuration."""
    model_name: str = "en_core_web_sm"
    enable_gpu: bool = False
    batch_size: int = 50

class ProductionConfig:
    """Main production configuration."""
    
    ENTITY_TYPES = EntityType
    WEIGHTS = WeightConfig()
    THRESHOLDS = ThresholdConfig()
    SPACY = SpacyConfig()
    
    CACHE_SIZE = 10000
    REGEX_OPTIMIZATION = True
    BATCH_PROCESSING = True
    PARALLEL_WORKERS = 4
    
    LOG_LEVEL = "INFO"
    ENABLE_METRICS = True
    METRICS_WINDOW = 300
    
    USE_SINGLE_COMPILED_REGEX = True
    REGEX_SORT_BY_LENGTH = True
    
    MIN_TEXT_LENGTH = 2
    MAX_TEXT_LENGTH = 500
    
    @classmethod
    def get_weight_for_person_component(cls, component_type: str) -> float:
        component_map = {
            "full_name": cls.WEIGHTS.PERSON_FULL_NAME,
            "first_last": cls.WEIGHTS.PERSON_FIRST_LAST,
            "middle_combinations": cls.WEIGHTS.PERSON_MIDDLE_COMBINATIONS,
            "first_only": cls.WEIGHTS.PERSON_FIRST_ONLY,
            "last_only": cls.WEIGHTS.PERSON_LAST_ONLY,
        }
        return component_map.get(component_type, 0.0)
    
    @classmethod
    def get_weight_for_company_component(cls, component_type: str) -> float:
        component_map = {
            "full_name": cls.WEIGHTS.COMPANY_FULL_NAME,
            "core_name": cls.WEIGHTS.COMPANY_CORE_NAME,
            "acronym": cls.WEIGHTS.COMPANY_ACRONYM,
            "strong_tokens": cls.WEIGHTS.COMPANY_STRONG_TOKENS,
        }
        return component_map.get(component_type, 0.0)
    
    @classmethod
    def is_in_weak_strong_range(cls, score: float) -> bool:
        return cls.THRESHOLDS.weak_threshold <= score <= cls.THRESHOLDS.strong_threshold
