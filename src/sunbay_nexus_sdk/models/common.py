"""
Common value objects shared across multiple requests and responses.
"""

from dataclasses import dataclass
from typing import List, Optional


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
class TipSuggestions:
    """
    Tip suggestions configuration.

    fee_mode: RATE or AMOUNT.
      - RATE: values represent percentage (e.g., [15, 18, 20] means 15%, 18%, 20%).
      - AMOUNT: values represent fixed amounts in smallest currency unit.
    """

    fee_mode: str
    values: List[int]


@dataclass
class TipConfig:
    """
    Tip configuration for on-screen tipping.

    on_screen_tip: Whether to show tip screen on terminal.
    tip_mode: ON_SALE (tip during sale) or AFTER_SALE (tip after sale/adjust).
    tip_with_tax: Whether tip is calculated with tax included.
    suggestions: Optional tip suggestions shown to customer.
    """

    on_screen_tip: bool = True
    tip_mode: str = "ON_SALE"
    tip_with_tax: bool = False
    suggestions: Optional[TipSuggestions] = None


@dataclass
class SaleAmount:
    """
    Amount information for sale transactions.
    Supports: order_amount, tip_amount, tax_amount, surcharge_amount, cashback_amount.
    All amount fields are in the smallest currency unit (e.g., cents for USD, fen for CNY).
    """

    order_amount: int
    price_currency: str
    tip_amount: Optional[int] = None
    tax_amount: Optional[int] = None
    surcharge_amount: Optional[int] = None
    cashback_amount: Optional[int] = None
    tip_config: Optional[TipConfig] = None


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
    tip_config: Optional[TipConfig] = None


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

    sub_id: Sub payment method. When category=CARD, must not be set. When
    category=EBT and id=EBT only, may be set to SNAP, VOUCHER, or BENEFIT.
    """

    network_type: Optional[str] = None
    card_last4: Optional[str] = None
    entry_mode: Optional[str] = None
    # Sub payment method: SNAP, VOUCHER, BENEFIT. Only when category=EBT and id=EBT.
    sub_id: Optional[str] = None


@dataclass
class CheckoutAmount:
    """
    Amount for online checkout APIs (create-session and /checkout/sale).

    Payable / charged total = order_amount + tax_amount + surcharge_amount.
    All amount fields are in the smallest currency unit (e.g., cents for USD, fen for CNY).
    """

    order_amount: int
    price_currency: str
    tax_amount: Optional[int] = None
    surcharge_amount: Optional[int] = None


@dataclass
class CheckoutProductItem:
    """
    Line item for checkout productList.

    If product_list is sent, sum(amount * num) must equal amount.order_amount.
    """

    amount: int
    name: str
    num: int


@dataclass
class CheckoutAddress:
    """
    Billing or shipping address for direct online payment (POST /v1/checkout/sale).
    """

    line_1: Optional[str] = None
    line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None


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


