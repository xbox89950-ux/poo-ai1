"""Shared-Connector contracts for AI 1 — Product Trend AI.

Natural-language fields/messages are Bangla by design. JSON keys remain stable
machine-readable identifiers so other AI apps can integrate without coupling to
AI 1's internal implementation.
"""
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

CONTRACT_VERSION = "1.0"
AI_ID = "ai1-product-trend"


@dataclass
class ProductResearch:
    product_id: str
    product_name: str
    category: str
    research_date: str
    demand_trend: str = ""
    target_customer: str = ""
    market_price_bdt: Optional[float] = None
    supplier_cost_bdt: Optional[float] = None
    possible_selling_price_bdt: Optional[float] = None
    supplier_information: str = ""
    competitor_information: str = ""
    benefits: List[str] = field(default_factory=list)
    potential_problems: List[str] = field(default_factory=list)
    why_sell: str = ""
    confidence_level: str = "মাঝারি"
    sources_context: List[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ConnectorMessage:
    message_id: str
    sender_ai: str
    receiver_ai: str
    message_type: str
    created_at: str
    payload: Dict[str, Any]
    language: str = "bn"
    contract_version: str = CONTRACT_VERSION

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def new_message(receiver_ai: str, message_type: str, payload: Dict[str, Any]) -> ConnectorMessage:
    now = datetime.now(timezone.utc).isoformat()
    return ConnectorMessage(
        message_id=f"{AI_ID}-{int(datetime.now(timezone.utc).timestamp() * 1000)}",
        sender_ai=AI_ID,
        receiver_ai=receiver_ai,
        message_type=message_type,
        created_at=now,
        payload=payload,
    )
