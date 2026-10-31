import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent
VSA = WORK / "omni_turbo_vsa_36case_4tier_eval_20260917" / "outputs" / "omni_turbo_vsa_retake_36case"
TEASER = WORK / "teaser_portrait_20261031"
EXCLUDED_CASES = {0, 10, 14, 21, 23, 25, 27, 29, 31, 35}
PORTRAIT_ORDER = ["07_contemporary_dance", "04_taichi_garden", "08_drummer_performance", "02_basketball_court", "03_skateboard_promenade"]


def poster(path: str) -> str:
    rel = Path(path)
    name = rel.name.replace(".mp4", ".jpg")
    if rel.parts[1] == "vsa":
        name = "vsa-" + name
    elif rel.parts[1] == "teaser":
        name = "teaser-" + name
    elif rel.parts[1] == "wandb":
        name = "wandb-" + name
    return "posters/" + name


def vsa_data():
    manifest = json.loads((VSA / "prompts_36.json").read_text(encoding="utf-8"))["cases"]
    tiers = [
        ("dense_s0.0", "Dense / reference", "s = 0.0"),
        ("quality_s0.3", "Sparse / quality", "s = 0.3"),
        ("balanced_s0.5", "Sparse / balanced", "s = 0.5"),
        ("fastest_s0.7", "Sparse / fastest", "s = 0.7"),
    ]
    out = []
    for item in manifest:
        n = int(item["case_id"])
        if n in EXCLUDED_CASES:
            continue
        stem = f"{n:03d}"
        videos = []
        for folder, label, sparsity in tiers:
            src = f"media/vsa/{stem}-{folder}.mp4"
            videos.append({"src": src, "poster": poster(src), "label": f"{label} · {sparsity}"})
        out.append(
            {
                "id": f"vsa-{stem}",
                "title": item["expected_subject"].capitalize() + " · " + item["expected_action"],
                "prompt": item["prompt"],
                "promptLabel": "Original prompt",
                "category": item["category"],
                "badge": item["category"].replace("_", " "),
                "meta": f"Case {stem} · seed {item['seed']} · four attention settings",
                "videos": videos,
            }
        )
    return out


def teaser_data():
    prompts = {}
    with (TEASER / "prompts.csv").open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            prompts[row["sample_id"]] = row
    out = []
    for path in sorted((TEASER / "videos").glob("*.mp4")):
        key = path.stem
        if key not in prompts:
            continue
        row = prompts[key]
        src = f"media/teaser/{path.name}"
        out.append(
            {
                "id": key,
                "title": row["title_en"],
                "prompt": row["prompt"],
                "promptLabel": "Original prompt",
                "meta": "teaser_portrait_20261031 · audio included",
                "src": src,
                "poster": poster(src),
                "label": row["title_en"],
            }
        )
    for path in sorted((TEASER / "batch2" / "videos").glob("*.mp4")):
        key = path.stem
        if key not in prompts:
            with (TEASER / "batch2" / "prompts.csv").open(encoding="utf-8", newline="") as f:
                for row in csv.DictReader(f):
                    prompts[row["sample_id"]] = row
        row = prompts[key]
        src = f"media/teaser/{path.name}"
        out.append(
            {
                "id": key,
                "title": row["title_en"],
                "prompt": row["prompt"],
                "promptLabel": "Original prompt",
                "meta": "teaser_portrait_20261031 / batch2 · audio included",
                "src": src,
                "poster": poster(src),
                "label": row["title_en"],
            }
        )
    return sorted((c for c in out if c["id"] in PORTRAIT_ORDER), key=lambda c: PORTRAIT_ORDER.index(c["id"]))


def samples_data():
    titles = ["Blacksmith at work", "Lakeside kayaking", "Wildlife on the savanna", "Vinyl record player", "Performer at a mirror", "Wok cooking", "Café conversation", "Wedding celebration"]
    out = []
    for path in sorted((WORK / "wandb" / "我们的").glob("*.mp4")):
        src = f"media/wandb/{path.name}"
        out.append(
            {
                "id": f"wandb-{path.stem}",
                "title": titles[int(path.stem.removeprefix('sample'))],
                "prompt": "Prompt metadata was not included in the supplied wandb folder.",
                "promptLabel": "Prompt unavailable",
                "meta": "wandb · audio included",
                "src": src,
                "poster": poster(src),
                "label": titles[int(path.stem.removeprefix('sample'))],
            }
        )
    return out


payload = {
    "generation": vsa_data(),
    "portraits": teaser_data(),
    "samples": samples_data(),
    "contact": [],
}
(ROOT / "data.js").write_text("window.DEMO_DATA = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
print(f"generated {len(payload['generation'])} VSA cases, {len(payload['portraits'])} teaser clips, {len(payload['samples'])} W&B samples")
