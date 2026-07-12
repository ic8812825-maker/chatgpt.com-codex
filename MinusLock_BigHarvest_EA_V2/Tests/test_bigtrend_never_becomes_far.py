from pathlib import Path
root=Path(__file__).resolve().parents[1]
config=(root/"Include"/"Config.mqh").read_text()
manual=(root/"Docs"/"MANUAL.md").read_text()
assert "BigTrendNeverBecomesFar" in config
assert "BigTrendNeverBecomesFar=true" in manual
assert "only the remaining BigCore can become a new Far" in manual
print("PASS BigTrend never becomes Far rule documented")
