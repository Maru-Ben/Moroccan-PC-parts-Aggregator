from abc import ABC, abstractmethod
from coreapi.domain.product import ProductSpecs
from typing import Dict
import re
import logging

logger = logging.getLogger("backend.services")

class BaseNormalizer(ABC):
    def __init__(self, rules_path: str):
        self.rules = self._load_rules(rules_path)

    @abstractmethod
    def normalize(self, title: str) -> ProductSpecs:
        """Extract structured specs from product title"""
        pass
    
    
    def _load_rules(self, path: str) -> Dict:
        import json
        with open(f"./coreapi/services/product_grouping/rules/{path}", 'r') as f:
            return json.load(f)
    
    def _extract_by_patterns(self, text: str, patterns: Dict[str, str]) -> str:
        """Helper: extract value using regex patterns"""
        import re
        text_lower = text.lower()
        for pattern, normalized_value in patterns.items():
            if re.search(pattern, text_lower):
                return normalized_value
        return "Unknown"
    
    def clean_title(self, title: str) -> str:
        # remove parentheses 
        title = re.sub(r"[()]", "", title)
        
        title = title.lower().strip()
        
        # remove ignored tokens
        ignore_tokens = self.rules.get("ignore_tokens", [])
        for token in ignore_tokens:
            title = re.sub(rf"\b{re.escape(token)}\b", "", title)
            
        # collapse multiple spaces
        title = re.sub(r"\s+", " ", title).strip()
        
        return title
            
        