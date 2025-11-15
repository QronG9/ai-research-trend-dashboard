import os
import pkgutil
import importlib

print("=== Checking Project Structure ===")

BASE = r"E:\trend"

# 1. Check essential folders exist
required_paths = [
    "src",
    "src/api",
    "src/data",
    "src/viz",
    "notebooks",
    "tests",
    "README.md",
]

for p in required_paths:
    full = os.path.join(BASE, p)
    print(f"[OK]" if os.path.exists(full) else "[MISSING]", p)

print("\n=== Checking Python Module Imports ===")

modules = [
    "src.api.openalex_client",
    "src.data.fetch",
    "src.data.process",
    "src.viz.charts",
]

for m in modules:
    try:
        importlib.import_module(m.replace("/", "."))
        print("[IMPORT OK]", m)
    except Exception as e:
        print("[FAILED]", m, "—", e)

print("\n=== Checking Files Are Non-Empty ===")

files = [
    "src/api/openalex_client.py",
    "src/data/fetch.py",
    "src/data/process.py",
    "src/viz/charts.py",
]

for f in files:
    full = os.path.join(BASE, f)
    try:
        size = os.path.getsize(full)
        print("[OK]" if size > 20 else "[EMPTY?]", f, f"({size} bytes)")
    except:
        print("[MISSING]", f)

print("\nDone.")
