from engine.content_engine import generate,quality_check,export_csv
def sample():
 return "Creators can plan useful content by collecting audience questions, selecting one topic, adapting it for different platforms, checking the draft and measuring the response."
def test_generates_ten():
 r=generate(sample(),10); assert len(r["items"])==10; assert r["runtime_minutes"]<30
def test_quality_check():
 x={"asset_id":"x","platform":"Instagram","format":"Text post","content_pillar":"Creator education","caption":"This caption is long enough for a simple test.","cta":"Try it","utm_link":"https://incubrix.com/?x=1"}
 assert "missing_hook" in quality_check(x)
def test_csv_upsert(tmp_path):
 rows=generate(sample(),10)["items"]; p=tmp_path/"x.csv"; export_csv(rows,p); export_csv(rows,p)
 import csv
 with p.open(encoding="utf-8-sig") as f: assert len(list(csv.DictReader(f)))==10
