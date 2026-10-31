
import csv
import hashlib
import logging
import re
import time
from pathlib import Path
from urllib.parse import quote_plus

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=OUTPUTS / "engine.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

PLATFORMS = ["Instagram", "LinkedIn", "YouTube Shorts"]

TEMPLATES = [
    ("Instagram", "Short video",
     "A practical idea creators can use today",
     "Explain the problem, share two useful steps, show an example and finish with one action."),
    ("LinkedIn", "Text post",
     "A repeatable workflow is more useful than a one-off tactic",
     "Explain the idea, why it matters, give a practical example and invite the audience to try it."),
    ("YouTube Shorts", "Short video",
     "One idea. One clear takeaway.",
     "Open with the audience problem, explain the key point, give an example and close with a next step."),
    ("Instagram", "Carousel",
     "Break the idea into a simple checklist",
     "Slide 1: Problem. Slide 2: First step. Slide 3: Second step. Slide 4: Example. Slide 5: Action."),
    ("LinkedIn", "Graphic",
     "A simple framework to remember",
     "Create a clean visual with the main idea, three short steps and one takeaway.")
]

PILLARS = [
    "Creator workflow",
    "Repurposing",
    "Audience growth",
    "Content strategy",
    "Production efficiency"
]

FIELDS = [
    "asset_id", "platform", "format", "content_pillar",
    "hook", "caption", "cta", "utm_link", "source_input",
    "tools_used", "rights_checked", "ai_label_needed",
    "status", "notes"
]


def quality_check(item):
    issues = []

    for key in [
        "asset_id", "platform", "format", "content_pillar",
        "hook", "caption", "cta", "utm_link"
    ]:
        if not str(item.get(key, "")).strip():
            issues.append("missing_" + key)

    if len(item.get("hook", "")) < 12:
        issues.append("weak_hook")

    if len(item.get("caption", "")) < 40:
        issues.append("caption_short")

    if item.get("platform") not in PLATFORMS:
        issues.append("unsupported_platform")

    if item.get("format") not in [
        "Short video", "Carousel", "Graphic", "Text post"
    ]:
        issues.append("unsupported_format")

    return issues


def generate(text, count=10):
    start = time.perf_counter()

    text = re.sub(r"\s+", " ", text or "").strip()

    if len(text) < 80:
        raise ValueError("Input must contain at least 80 characters.")

    if not isinstance(count, int) or not 1 <= count <= 30:
        raise ValueError("Choose between 1 and 30 drafts.")

    first = re.split(r"(?<=[.!?])\s+", text)[0][:130]

    rows = []
    rejected = []
    seen = set()

    for i in range(count):
        platform, fmt, base_hook, body = TEMPLATES[i % len(TEMPLATES)]

        angle = i + 1
        asset_id = "GEN-" + hashlib.sha1(
            f"{text}|{i}".encode("utf-8")
        ).hexdigest()[:8].upper()

        hook = f"{base_hook} | Perspective {angle}"

        caption = (
            f"{body} "
            f"Source insight: {first} "
            f"Content angle: {angle}. "
            "Adapt this idea to your audience and brand voice."
        )

        slug = quote_plus(platform.lower().replace(" ", "_"))

        item = {
            "asset_id": asset_id,
            "platform": platform,
            "format": fmt,
            "content_pillar": PILLARS[i % len(PILLARS)],
            "hook": hook,
            "caption": caption,
            "cta": "Try this with your next piece of content.",
            "utm_link": (
                f"https://incubrix.com/?utm_source={slug}"
                f"&utm_medium=organic_social"
                f"&utm_campaign=content_engine"
                f"&utm_content={asset_id}"
            ),
            "source_input": "user-provided input",
            "tools_used": "offline template generator",
            "rights_checked": "Pending human review",
            "ai_label_needed": "Assess before publishing",
            "status": "Draft",
            "notes": "Draft only; human review required."
        }

        # Check the actual generated content for duplicates.
        fingerprint = hashlib.sha256(
            (
                item["platform"] + "|" +
                item["format"] + "|" +
                item["hook"] + "|" +
                item["caption"]
            ).lower().encode("utf-8")
        ).hexdigest()

        if fingerprint in seen:
            rejected.append({
                "asset_id": asset_id,
                "issues": ["duplicate"]
            })
            continue

        seen.add(fingerprint)

        issues = quality_check(item)

        if issues:
            rejected.append({
                "asset_id": asset_id,
                "issues": issues
            })
        else:
            rows.append(item)

    elapsed = (time.perf_counter() - start) / 60

    logging.info(
        "produced=%s rejected=%s runtime_min=%s",
        len(rows), len(rejected), elapsed
    )

    return {
        "items": rows,
        "rejected": rejected,
        "runtime_minutes": round(elapsed, 5),
        "mode": "offline-template"
    }


def export_csv(rows, path):
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = {}

    if output_path.exists():
        with output_path.open(
            encoding="utf-8-sig", newline=""
        ) as file:
            for row in csv.DictReader(file):
                if row.get("asset_id"):
                    data[row["asset_id"]] = row

    for row in rows:
        data[row["asset_id"]] = row

    with output_path.open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows([
            {key: row.get(key, "") for key in FIELDS}
            for row in data.values()
        ])
