"""Dumps the live FastAPI OpenAPI schema to a file for the frontend contract check to read."""
import json
import sys
from pathlib import Path

# Run from anywhere — put the backend package root on sys.path regardless of cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app  # noqa: E402

out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("openapi.json")
out_path.write_text(json.dumps(app.openapi(), indent=2))
print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)")
