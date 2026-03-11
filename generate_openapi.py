import json
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from backend.main import app

openapi_schema = app.openapi()
os.makedirs("docs", exist_ok=True)
with open("docs/openapi.json", "w") as f:
    json.dump(openapi_schema, f, indent=2)

print("OpenAPI spec generated at docs/openapi.json")
