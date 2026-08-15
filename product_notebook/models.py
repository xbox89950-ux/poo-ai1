"""Product Notebook domain models for AI 1."""
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ProductRecord:
    product_id: str
    product_name: str
    category: str
    product_code: Optional[str] = None
    supplier_information: str = ""
    supplier_cost_bdt: Optional[float] = None
    market_price_bdt: Optional[float] = None
    possible_selling_price_bdt: Optional[float] = None
    demand_trend: str = ""
    target_customer: str = ""
    competitor_information: str = ""
    benefits: List[str] = field(default_factory=list)
    potential_problems: List[str] = field(default_factory=list)
    why_sell: str = ""
    confidence_level: str = "মাঝারি"
    sources_context: List[str] = field(default_factory=list)
    personal_notes: str = ""
    last_researched_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
