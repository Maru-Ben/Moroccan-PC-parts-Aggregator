
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class ProductSpecs:
    """Standardized product specifications"""
    category: str
    brand: str
    model: str
    key_specs: Dict[str, Any]
    raw_title: str
    
    def to_canonical_key(self) -> str:
        """Generate deterministic key for exact matching"""
        key_parts = [self.category, self.brand, self.model]
        key_parts.extend(str(v) for v in sorted(self.key_specs.values()))
        return "_".join(key_parts).upper().replace(" ", "_")
