"""Payment Protocol handler for Deep Dive mode gating."""
from uagents import Model


DEEP_DIVE_COST_MICRO_ASI = 1000  # 0.001 ASI in micro-ASI units


class PaymentRequest(Model):
    """Sent to student when they request Deep Dive mode."""
    amount: int
    denom: str
    memo: str


class PaymentConfirmation(Model):
    """Received when student completes payment."""
    tx_hash: str
    sender: str
    amount: int


class DeepDiveUnlocked(Model):
    """Sent to student after successful payment."""
    session_token: str
    teaching_mode: str = "deep_dive"
