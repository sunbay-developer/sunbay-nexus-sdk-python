"""
Enum definitions corresponding to Java SDK enums.

These are optional helpers to make code more self-documenting on the caller side.
The underlying API still uses string values on the wire.
"""

from enum import Enum


class TransactionStatus(str, Enum):
    INITIAL = "I"
    PROCESSING = "P"
    SUCCESS = "S"
    FAIL = "F"
    CLOSED = "C"


class TransactionType(str, Enum):
    SALE = "SALE"
    AUTH = "AUTH"
    FORCED_AUTH = "FORCED_AUTH"
    INCREMENTAL = "INCREMENTAL"
    POST_AUTH = "POST_AUTH"
    REFUND = "REFUND"
    VOID = "VOID"


class CardNetworkType(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    EBT = "EBT"
    EGC = "EGC"
    UNKNOWN = "UNKNOWN"


class EntryMode(str, Enum):
    MANUAL = "MANUAL"
    SWIPE = "SWIPE"
    FALLBACK_SWIPE = "FALLBACK_SWIPE"
    CONTACT = "CONTACT"
    CONTACTLESS = "CONTACTLESS"


class PaymentCategory(str, Enum):
    CARD = "CARD"
    CARD_CREDIT = "CARD-CREDIT"
    CARD_DEBIT = "CARD-DEBIT"
    QR_MPM = "QR-MPM"
    QR_CPM = "QR-CPM"


class AuthenticationMethod(str, Enum):
    NOT_AUTHENTICATED = "NOT_AUTHENTICATED"
    PIN = "PIN"
    OFFLINE_PIN = "OFFLINE_PIN"
    BY_PASS = "BY_PASS"
    SIGNATURE = "SIGNATURE"


