"""
Request models for Sunbay Nexus SDK.
"""

from dataclasses import dataclass
from typing import List, Optional

from .common import (
    AuthAmount,
    CheckoutAddress,
    CheckoutAmount,
    CheckoutProductItem,
    PaymentMethodInfo,
    PostAuthAmount,
    RefundAmount,
    SaleAmount,
)


@dataclass
class SaleRequest:
    """
    Sale transaction request.
    """

    app_id: str
    merchant_id: str
    reference_order_id: str
    transaction_request_id: str
    amount: SaleAmount
    description: str
    terminal_sn: str
    payment_method: Optional[PaymentMethodInfo] = None
    attach: Optional[str] = None
    notify_url: Optional[str] = None
    time_expire: Optional[str] = None
    # Receipt print option: NONE, MERCHANT, CUSTOMER, BOTH. Default NONE.
    print_receipt: str = "NONE"
    # Card network type (CREDIT, DEBIT, EBT, EGC, UNKNOWN). Only when payment_method.category=CARD; else auto-detected.
    card_network_type: Optional[str] = None


@dataclass
class AuthRequest:
    """
    Authorization request.
    """

    app_id: str
    merchant_id: str
    reference_order_id: str
    transaction_request_id: str
    amount: AuthAmount
    description: str
    terminal_sn: str
    payment_method: Optional[PaymentMethodInfo] = None
    attach: Optional[str] = None
    notify_url: Optional[str] = None
    time_expire: Optional[str] = None
    # Receipt print option: NONE, MERCHANT, CUSTOMER, BOTH. Default NONE.
    print_receipt: str = "NONE"
    # Card network type (CREDIT, DEBIT, EBT, EGC, UNKNOWN). Only when payment_method.category=CARD; else auto-detected.
    card_network_type: Optional[str] = None


@dataclass
class ForcedAuthRequest:
    """
    Forced authorization request.
    """

    app_id: str
    merchant_id: str
    reference_order_id: str
    transaction_request_id: str
    amount: AuthAmount
    description: str
    terminal_sn: str
    payment_method: Optional[PaymentMethodInfo] = None
    attach: Optional[str] = None
    notify_url: Optional[str] = None
    time_expire: Optional[str] = None
    # Receipt print option: NONE, MERCHANT, CUSTOMER, BOTH. Default NONE.
    print_receipt: str = "NONE"
    # Card network type (CREDIT, DEBIT, EBT, EGC, UNKNOWN). Only when payment_method.category=CARD; else auto-detected.
    card_network_type: Optional[str] = None


@dataclass
class IncrementalAuthRequest:
    """
    Incremental authorization request.
    """

    app_id: str
    merchant_id: str
    original_transaction_id: Optional[str] = None
    original_transaction_request_id: Optional[str] = None
    transaction_request_id: str = ""
    amount: Optional[AuthAmount] = None
    description: Optional[str] = None
    terminal_sn: Optional[str] = None
    attach: Optional[str] = None
    notify_url: Optional[str] = None
    # Receipt print option: NONE, MERCHANT, CUSTOMER, BOTH. Default NONE.
    print_receipt: str = "NONE"
    # Whether to push the transaction to the terminal. Default True.
    push_to_terminal: bool = True


@dataclass
class QueryRequest:
    """
    Query transaction request.
    """

    app_id: str
    merchant_id: str
    transaction_id: Optional[str] = None
    reference_order_id: Optional[str] = None
    transaction_request_id: Optional[str] = None


@dataclass
class PostAuthRequest:
    """
    Post authorization request.
    """

    app_id: str
    merchant_id: str
    original_transaction_id: Optional[str] = None
    original_transaction_request_id: Optional[str] = None
    reference_order_id: Optional[str] = None
    transaction_request_id: str = ""
    amount: Optional[PostAuthAmount] = None
    description: Optional[str] = None
    terminal_sn: Optional[str] = None
    attach: Optional[str] = None
    notify_url: Optional[str] = None
    # Receipt print option: NONE, MERCHANT, CUSTOMER, BOTH. Default NONE.
    print_receipt: str = "NONE"
    # Whether to push the transaction to the terminal. Default True.
    push_to_terminal: bool = True


@dataclass
class RefundRequest:
    """
    Refund request.
    """

    app_id: str
    merchant_id: str
    transaction_request_id: str
    amount: RefundAmount
    original_transaction_id: Optional[str] = None
    original_transaction_request_id: Optional[str] = None
    reference_order_id: Optional[str] = None
    payment_method: Optional[PaymentMethodInfo] = None
    description: Optional[str] = None
    terminal_sn: Optional[str] = None
    attach: Optional[str] = None
    notify_url: Optional[str] = None
    time_expire: Optional[str] = None
    # Receipt print option: NONE, MERCHANT, CUSTOMER, BOTH. Default NONE.
    print_receipt: str = "NONE"
    # Whether to push the transaction to the terminal. Default True.
    push_to_terminal: bool = True
    # Card network type (CREDIT, DEBIT, EBT, EGC, UNKNOWN). Only when payment_method.category=CARD; else auto-detected.
    card_network_type: Optional[str] = None


@dataclass
class BatchCloseRequest:
    """
    Batch close request.
    """

    app_id: str
    merchant_id: str
    transaction_request_id: str
    terminal_sn: str
    channel_code: Optional[str] = None
    description: Optional[str] = None


@dataclass
class BatchQueryRequest:
    """
    Batch query request.
    """

    app_id: str
    merchant_id: str
    terminal_sn: str


@dataclass
class VoidRequest:
    """
    Void request.
    """

    app_id: str
    merchant_id: str
    transaction_request_id: str
    original_transaction_id: Optional[str] = None
    original_transaction_request_id: Optional[str] = None
    description: Optional[str] = None
    terminal_sn: Optional[str] = None
    attach: Optional[str] = None
    notify_url: Optional[str] = None
    # Receipt print option: NONE, MERCHANT, CUSTOMER, BOTH. Default NONE.
    print_receipt: str = "NONE"
    # Whether to push the transaction to the terminal. Default True.
    push_to_terminal: bool = True


@dataclass
class AbortRequest:
    """
    Abort request.
    """

    app_id: str
    merchant_id: str
    original_transaction_id: Optional[str] = None
    original_transaction_request_id: Optional[str] = None
    terminal_sn: Optional[str] = None
    description: Optional[str] = None
    attach: Optional[str] = None


@dataclass
class TipAdjustRequest:
    """
    Tip adjust request.

    tip_amount is in the smallest currency unit (e.g., cents for USD, fen for CNY).
    """

    app_id: str
    merchant_id: str
    terminal_sn: str
    original_transaction_id: Optional[str] = None
    original_transaction_request_id: Optional[str] = None
    tip_amount: int = 0
    attach: Optional[str] = None


@dataclass
class CreateCheckoutSessionRequest:
    """
    POST /v1/checkout/create-session — Hosted Payment Page session.

    Redirect the customer to the returned checkout URL. Session lifetime is
    typically 30 minutes; see response expires_at.
    """

    app_id: str
    merchant_id: str
    transaction_request_id: str
    reference_order_id: str
    amount: CheckoutAmount
    description: str
    product_list: Optional[List[CheckoutProductItem]] = None
    collect_billing_address: bool = False
    collect_shipping_address: bool = False
    merchant_return_url: Optional[str] = None
    notify_url: Optional[str] = None


@dataclass
class CheckoutSaleRequest:
    """
    POST /v1/checkout/sale — Direct online payment (e.g. Google Pay / Apple Pay).

    card_encrypted_data must contain the wallet token JSON when payment_method
    is GOOGLE_PAY or APPLE_PAY.
    """

    app_id: str
    merchant_id: str
    transaction_request_id: str
    reference_order_id: str
    description: str
    amount: CheckoutAmount
    payment_method: str
    product_list: Optional[List[CheckoutProductItem]] = None
    card_encrypted_data: Optional[str] = None
    customer_email: Optional[str] = None
    customer_name: Optional[str] = None
    billing_address: Optional[CheckoutAddress] = None
    shipping_address: Optional[CheckoutAddress] = None
    notify_url: Optional[str] = None
    merchant_return_url: Optional[str] = None


