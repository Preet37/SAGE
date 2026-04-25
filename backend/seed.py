"""Idempotent seed script for SAGE.

Creates:
  - tables (idempotent)
  - demo user (`demo@sage.ai` / `demo1234`)
  - two seeded "courses" (modeled as Lesson rows owned by demo)

Re-running is safe: every insert is gated on a uniqueness check.
"""

from __future__ import annotations

from app.db import SessionLocal, init_db
from app.models import Lesson, User
from app.security import hash_password


DEMO_EMAIL = "demo@sage.ai"
DEMO_PASSWORD = "demo1234"
DEMO_NAME = "Demo Student"

SEED_LESSONS: list[dict[str, str]] = [
    {
        "title": "Photosynthesis",
        "subject": "Biology",
        "objective": (
            "Photosynthesis is the process by which green plants and some other organisms "
            "use sunlight to synthesize foods from carbon dioxide and water. "
            "Photosynthesis in plants generally involves the green pigment chlorophyll and generates oxygen as a byproduct.\n\n"
            "The light-dependent reactions take place in the thylakoid membranes of the chloroplasts. "
            "Chlorophyll absorbs photons and excites electrons, which power ATP and NADPH synthesis.\n\n"
            "The Calvin cycle (light-independent) uses ATP and NADPH to fix carbon dioxide into glucose."
        ),
    },
    {
        "title": "Neural Network Basics",
        "subject": "Machine Learning",
        "objective": (
            "A neural network is a series of layers that transform an input vector into an output vector. "
            "Each layer applies a learned linear transformation followed by a nonlinear activation.\n\n"
            "Training is performed with backpropagation: the loss is computed at the output, then gradients "
            "flow backward through the network using the chain rule, and weights are updated by gradient descent.\n\n"
            "Common activations include ReLU, sigmoid, and tanh. Common losses include cross-entropy for "
            "classification and mean-squared-error for regression."
        ),
    },
    {
        "title": "Attention and Transformers",
        "subject": "Machine Learning",
        "objective": (
            "Attention computes a weighted sum of value vectors, where weights come from the compatibility "
            "between a query and keys. Self-attention lets each token in a sequence attend to every other token.\n\n"
            "A transformer block stacks multi-head self-attention with a feed-forward MLP, residual "
            "connections, and layer normalization.\n\n"
            "Positional encoding (sinusoidal or learned) injects token order into the otherwise permutation-"
            "invariant attention operation."
        ),
    },
]


def seed() -> None:
    init_db()
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == DEMO_EMAIL).first()
        if not user:
            user = User(
                email=DEMO_EMAIL,
                name=DEMO_NAME,
                hashed_password=hash_password(DEMO_PASSWORD),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"[seed] created demo user id={user.id}")
        else:
            print(f"[seed] demo user already exists id={user.id}")

        for entry in SEED_LESSONS:
            existing = (
                db.query(Lesson)
                .filter(Lesson.owner_id == user.id, Lesson.title == entry["title"])
                .first()
            )
            if existing:
                continue
            db.add(Lesson(owner_id=user.id, **entry))
        db.commit()
        count = db.query(Lesson).filter(Lesson.owner_id == user.id).count()
        print(f"[seed] demo lessons total={count}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
