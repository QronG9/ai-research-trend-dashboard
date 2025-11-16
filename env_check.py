import os
import sys
import importlib
import subprocess
from pathlib import Path

BASE = Path(r"E:\trend")

print("========== PROJECT HEALTH CHECK ==========\n")

# 1. Check Python interpreter path
print("1) Python Interpreter Check")
print("   Current interpreter:", sys.executable)
if "trend-env" in sys.executable.replace("\\", "/"):
    print("   ✓ Using correct virtual environment (trend-env)\n")
else:
    print("   ✗ NOT using trend-env — please activate it.\n")

# 2. Check essential folders
print("2) Project Structure Check")
required_dirs = [
    "src",
    "src/api",
    "src/data",
    "src/viz",
    "notebooks",
    "tests"
]
for d in required_dirs:
    p = BASE / d
    print(f"   {'✓' if p.exists() else '✗'}  {d}")

print("\n")

# 3. Check important files
print("3) Required Files Check")
required_files = [
    "README.md",
    "requirements.txt",
    "env_check.py"
]
for f in required_files:
    p = BASE / f
    print(f"   {'✓' if p.exists() else '✗'}  {f}")

print("\n")

# 4. Check Python module imports
print("4) Python Module Import Check")
modules = [
    "src.api.openalex_client",
    "src.data.fetch",
    "src.data.process",
    "src.viz.charts",
]
for m in modules:
    try:
        importlib.import_module(m.replace("/", "."))
        print(f"   ✓ Import OK: {m}")
    except Exception as e:
        print(f"   ✗ Import FAILED: {m} — {e}")

print("\n")

# 5. Check installed packages
print("5) Dependency Check (pandas/matplotlib/seaborn)")
deps = ["pandas", "matplotlib", "seaborn", "requests", "jupyter"]

for pkg in deps:
    try:
        importlib.import_module(pkg)
        print(f"   ✓ Installed: {pkg}")
    except ImportError:
        print(f"   ✗ Missing: {pkg}")

print("\n")

# 6. Syntax check for all .py files
print("6) Syntax Check for All Python Files")

py_files = list(BASE.rglob("*.py"))
errors = 0

for f in py_files:
    try:
        subprocess.check_output([sys.executable, "-m", "py_compile", str(f)])
        print(f"   ✓ {f.name} syntax OK")
    except subprocess.CalledProcessError as e:
        print(f"   ✗ Syntax ERROR in {f.name}: {e}")
        errors += 1

print("\n")

# 7. Summary
print("========== SUMMARY ==========")

if errors == 0:
    print("All Python files compiled successfully.")
else:
    print(f"{errors} file(s) have syntax errors.")

print("\nCompleted.")
