import re
from difflib import SequenceMatcher
from coreapi.services.product_grouping.normalizers.base import BaseNormalizer
from coreapi.domain.product import ProductSpecs
from coreapi.constants import CATEGORIES
import logging

logger = logging.getLogger("backend.services")

class GPUNormalizer(BaseNormalizer):
    def __init__(self, rules_path):
        super().__init__(rules_path)
        self.category = CATEGORIES["GPU"]
    
    def normalize(self, title: str) -> ProductSpecs:
        clean_title = self.clean_title(title)
        
        # Extract the main components
        chipset_info = self._extract_chipset_and_model(clean_title)
        partner = self._extract_board_partner(clean_title)
        vram = self._extract_vram(clean_title)
        
        # Build canonical name
        canonical_name = f"{chipset_info["full_model_name"]}"
        if vram > 1:
            canonical_name += f" {vram} GB"
        canonical_name += f" - {partner}"
        
        # remaining text for the fuzzy matching
        remaining_title_text = self._extract_remaining_title(clean_title, chipset_info, partner, vram)
        
        return ProductSpecs(
            category=self.category,
            brand=chipset_info['brand'],
            model=canonical_name,  # "RTX 4090 - ASUS"
            key_specs={
                'chipset': chipset_info['chipset'],       # "RTX"
                'vram': vram,
                'model_number': chipset_info['model'],    # "4090"
                'model_variant': chipset_info['variant'], # "Ti" or None
                'board_partner': partner,                 # "ASUS"
                'sub_brand_text': remaining_title_text    # "rog strix gaming"
            },
            raw_title=title
        )

    
    def _extract_chipset_and_model(self, title: str) -> dict:
        """Extract chipset + model e.g. RTX 5060 TI"""
        chipset_patterns: dict = self.rules.get("chipset_patterns", {})
        
        for name, chip in chipset_patterns.items():
            brand = chip["brand"]
            model_extraction = chip["model_extraction"]
            
            match = re.search(model_extraction, title)
            
            if match:
                
                if name == "nvidia":
                    chipset = match.group(1).upper()
                    model_num = match.group(2) 
                    variant = match.group(3) if len(match.groups()) >= 3 else None
                    
                elif name == "amd":
                    chipset = "RX"
                    model_num = match.group(1)
                    variant = match.group(2) if len(match.groups()) >= 2 else None
                    
                elif name == "intel":
                    chipset = "ARC"
                    model_num = match.group(1).upper()
                    variant = None  # Intel doesn't have variants like Ti/Super yet
                
                else:
                    continue  # Unknown chipset type
                
                # Build full model name
                full_model_name = f"{chipset} {model_num}"
                if variant:
                    full_model_name += f" {variant.upper()}"
                    
                return {
                    "brand": brand,
                    "chipset": chipset,
                    "model": model_num,
                    "variant": variant.upper() if variant else None,
                    "full_model_name": full_model_name
                }
        
        # No match found
        return {
            'brand': 'Unknown',
            'chipset': 'Unknown',
            'model': 'Unknown',
            'variant': None,
            'full_model_name': 'Unknown'
        }

    
    def _extract_board_partner(self, title: str) -> dict:
        """Extract board partner based on a list"""
        known_partners = self.rules["board_partners"]
        for partner in known_partners:
            if partner in title:
                return partner
        return "UNKNOWN"
        
        
    def _extract_vram(self, title: str) -> int:
        """Extract VRAM in GB"""
        vram_patterns = self.rules.get("vram_patterns", [])
        for pattern in vram_patterns:
            match = re.search(rf"{pattern}", title)
            if match:
                vram = int(match.group(1))
                # Sanity check - GPU VRAM typically between 1-128GB
                if 1 <= vram <= 128:
                    return vram
        
        return 0  # Unknown/not found


    def _extract_remaining_title(self, title: str, chipset_info :dict, partner: str, vram: int) -> str:
        """Remove the core components and returning what's left"""

        remaining_title = title
        # Remove the chipset information
        for key, value in chipset_info.items():
            if value:
                remaining_title = re.sub(rf"\b{re.escape(value.lower())}\b", "", remaining_title)
        
        # Remove board partner
        if partner != "UNKNOWN":
            remaining_title = re.sub(rf"\b{partner.lower()}\b", "", remaining_title)
        
        # Remove VRAM
        if vram > 0:
            for pattern in self.rules.get("vram_patterns", []):
                remaining_title = re.sub(rf"{pattern}", "", remaining_title)
        
        # collapse multiple spaces
        remaining_title = re.sub(r"\s+", " ", remaining_title).strip()
        
        return remaining_title
    
    
    def calculate_similarity(self, specs1: ProductSpecs, specs2: ProductSpecs) -> float:
        """Calculate similarity between 2 products: exact core match + fuzzy sub-brand"""
        if specs1.category != specs2.category:
            return 0.0 # different category exit right away
        
        core_match = (
            specs1.key_specs['chipset'] == specs2.key_specs['chipset'] and
            specs1.key_specs['model_number'] == specs2.key_specs['model_number'] and
            specs1.key_specs['model_variant'] == specs2.key_specs['model_variant'] and
            specs1.key_specs['board_partner'] == specs2.key_specs['board_partner']
        )
        
        if not core_match:
            return 0.0 # key component dosent match
        
        # calculate fuzzy on the extra text in the titles
        text1 = specs1.key_specs.get("sub_brand_text", "")
        text2 = specs2.key_specs.get("sub_brand_text", "")
        
        if not text1 and not text2:
            fuzzy_score = 1.0  # Both have no sub-brand text
        elif not text1 or not text2:
            fuzzy_score = 0.5  # One has sub-brand, other doesn't
        else:
            fuzzy_score = SequenceMatcher(None, text1, text2).ratio()

        weights = self.rules["similarity_weights"]
        total_score = weights["core_match"] + (weights["sub_brand_fuzzy"] * fuzzy_score)
        
        return min(total_score, 1.0)
    
    
    def should_group(self, specs1: ProductSpecs, specs2: ProductSpecs) -> dict:
        """Determine if products should be grouped together"""
        similarity = self.calculate_similarity(specs1, specs2)
            # Core components match exactly
        core_match = (
            specs1.key_specs['chipset'] == specs2.key_specs['chipset'] and
            specs1.key_specs['model_number'] == specs2.key_specs['model_number'] and
            specs1.key_specs['model_variant'] == specs2.key_specs['model_variant'] and
            specs1.key_specs['board_partner'] == specs2.key_specs['board_partner']
        )
        
        if core_match and similarity >= self.rules["grouping_score_threshold"]:
            return {
                "decision": "group",
                "confidence": similarity,
                "reason": f"Same core product or high similarity score"
            }
        else:
            return {
                "decision": "separate",
                "confidence": similarity,
                "reason": "Low similarity score"
            }
                
        
