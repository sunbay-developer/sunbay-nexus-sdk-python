"""
Common value objects shared across multiple requests and responses.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Amount:
    """
    Generic amount information.

    This mirrors the Java Amount class and is mainly used in responses.

    All amount fields are in the smallest currency unit (e.g., cents for USD, fen for CNY).
    """

    price_currency: Optional[str] = None
    trans_amount: Optional[int] = None
    order_amount: Optional[int] = None
    tax_amount: Optional[int] = None
    surcharge_amount: Optional[int] = None
    tip_amount: Optional[int] = None
    cashback_amount: Optional[int] = None


@dataclass
class SaleAmount:
    """
    Amount information for sale transactions.
    Supports: order_amount, tip_amount, tax_amount, surcharge_amount, cashback_amount.
    All amount fields are in the smallest currency unit (e.g., cents for USD, fen for CNY).
    """

    order_amount: int
    tip_amount: Optional[int] = None
    tax_amount: Optional[int] = None
    surcharge_amount: Optional[int] = None
    cashback_amount: Optional[int] = None
    price_currency: str


@dataclass
class AuthAmount:
    """
    Amount information for auth/forced auth/incremental auth.

    All amount fields are in the smallest currency unit (e.g., cents for USD, fen for CNY).
    """

    order_amount: int
    price_currency: str


@dataclass
class PostAuthAmount:
    """
    Amount information for post authorization.

    All amount fields are in the smallest currency unit (e.g., cents for USD, fen for CNY).
    """

    order_amount: int
    price_currency: str
    tip_amount: Optional[int] = None
    tax_amount: Optional[int] = None
    surcharge_amount: Optional[int] = None


@dataclass
class RefundAmount:
    """
    Amount information for refund.

    All amount fields are in the smallest currency unit (e.g., cents for USD, fen for CNY).
    """

    order_amount: int
    price_currency: str
    tip_amount: Optional[int] = None
    tax_amount: Optional[int] = None
    surcharge_amount: Optional[int] = None
    cashback_amount: Optional[int] = None


@dataclass
class PaymentMethodInfo:
    """
    Basic payment method information.

    The exact fields may evolve over time. This class focuses on properties
    that are generally useful to expose to callers. Additional fields can be
    added in a backward compatible way.
    """

    network_type: Optional[str] = None
    card_last4: Optional[str] = None
    entry_mode: Optional[str] = None


@dataclass
class BatchQueryItem:
    """
    Batch query item information.

    Statistics grouped by channel code and price currency.

    All amount fields are in the smallest currency unit (e.g., cents for USD, fen for CNY).
    """

    batch_no: Optional[str] = None
    start_time: Optional[str] = None
    channel_code: Optional[str] = None
    price_currency: Optional[str] = None
    total_count: Optional[int] = None
    net_amount: Optional[int] = None
    tip_amount: Optional[int] = None
    surcharge_amount: Optional[int] = None
    tax_amount: Optional[int] = None


