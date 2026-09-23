"""Release and package invariants; no network access."""
import importlib.util
from pathlib import Path
r = Path(__file__).resolve().parents[1]
v = (r / "VERSION").read_text().strip()
for p in ("scripts/score_earnings.py", "scripts/legacy_earnings.py", "references/parsing-checklist.md", "references/scoring-engine.md"):
    assert (r / p).is_file(), p
text = (r / "SKILL.md").read_text()
assert f'version: "{v}"' in text, "Skill version mismatch"
spec = importlib.util.spec_from_file_location("scorer", r / "scripts/score_earnings.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
assert m.VERSION == v, "Script version mismatch"
assert "\n    - earnings-analysis" not in text, "Metadata values must be strings"
print("Package paths and versions verified")
