import os
import sys
import importlib
import subprocess
from pathlib import Path

BASE = Path(r"E:\trend")

print("\n========== PROJECT HEALTH CHECK ==========\n")

##############################################################
# 1. Python Interpreter Check
##############################################################
print("1) Python Interpreter Check")
print("   Current interpreter:", sys.executable)

if "trend-env" in sys.executable.replace("\\", "/"):
    print("   OK Using correct virtual environment (trend-env)\n")
else:
    print("   FAIL Not using trend-env - please activate before running.\n")

##############################################################
# 2. Project Structure Check (only inside project folders)
##############################################################
print("2) Project Structure Check")
required_dirs = [
    "src",
    "src/api",
    "src/data",
    "src/viz",
    "notebooks",
    "tests",
]
for d in required_dirs:
    p = BASE / d
    print(f"   {'OK' if p.exists() else 'FAIL'}  {d}")

print()

##############################################################
# 3. Required File Check
##############################################################
print("3) Required Files Check")
required_files = ["README.md", "requirements.txt", "env_check.py"]
for f in required_files:
    p = BASE / f
    print(f"   {'OK' if p.exists() else 'FAIL'}  {f}")

print()

##############################################################
# 4. Import Check (only your modules)
##############################################################
print("4) Python Module Import Check")
modules = [
    "src.api.openalex_client",
    "src.data.fetch",
    "src.data.process",
    "src.viz.charts",
    "src.frontend_api.server",
]


for m in modules:
    try:
        importlib.import_module(m)
        print(f"   OK Import: {m}")
    except Exception as e:
        print(f"   FAIL Import: {m} - {e}")

print()

##############################################################
# 5. Dependency Check
##############################################################
print("5) Dependency Check (core libraries)")
deps = ["pandas", "matplotlib", "seaborn", "requests"]

for pkg in deps:
    try:
        importlib.import_module(pkg)
        print(f"   OK Installed: {pkg}")
    except ImportError:
        print(f"   MISSING: {pkg}")

print()

##############################################################
# 6. Syntax check ONLY project .py files (not entire environment)
##############################################################
print("6) Syntax Check (only project code)")
py_files = [f for f in BASE.rglob("*.py") if "trend-env" not in str(f)]

if not py_files:
    print("   FAIL No Python files found!")
else:
    for f in py_files:
        try:
            subprocess.check_output([sys.executable, "-m", "py_compile", str(f)])
            print(f"   OK Syntax: {f.name}")
        except subprocess.CalledProcessError:
            print(f"   FAIL Syntax in: {f.name}")

##############################################################
# 7. Quick OpenAlex smoke test (group_by 2020-2020)
##############################################################
try:
    from src.api.openalex_client import OpenAlexClient
    print("7) OpenAlex group_by test (2020-2020)")
    client = OpenAlexClient()
    counts = client.fetch_nlp_counts(2020, 2020, mode="group_by")
    print(f"   NLP works in 2020 (group_by): {counts.get(2020, 0)}")
    # Test multi-direction utility on 2 sample directions (short run)
    from src.config.directions import DIRECTIONS
    from src.data.aggregate import aggregate_all_directions
    df = aggregate_all_directions(DIRECTIONS[:2], 2020, 2021)
    print(f"   Aggregated rows (2 dirs, 2 years): {len(df)}")
    print("   OK OpenAlex request\n")
except Exception as e:
    print(f"   FAIL OpenAlex request: {e}\n")



print("\n========== DONE ==========\n")

