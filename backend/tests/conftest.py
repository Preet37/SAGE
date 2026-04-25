import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Tests share the FastAPI client across modules; rate limits would compound and
# falsely fail later tests. Production env never sets this flag.
os.environ.setdefault("RATE_LIMIT_DISABLED", "1")
