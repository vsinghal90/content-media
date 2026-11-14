"""Compare the series list with what is live and scheduled on YouTube and Instagram.
Usage: python3 -I check_series.py series.json yt.json ig.json [scheduled.json]
  yt.json  = items from Composio YOUTUBE_LIST_CHANNEL_VIDEOS (snippet.resourceId.videoId, snippet.title, snippet.publishedAt)
  ig.json  = data from INSTAGRAM_GET_IG_USER_MEDIA (id, permalink, timestamp, caption)
  scheduled.json (optional) = [{"platform": "instagram"|"youtube", "when": "...", "title": "...", "cover_url": "..."}]
Prints every problem; exit code 1 if any. Fix the list or the posts before making a cover."""
import json, sys
s = json.load(open(sys.argv[1])); yt = json.load(open(sys.argv[2])); ig = json.load(open(sys.argv[3]))
sched = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else []
cut = s.get("ignore_youtube_before", "2026-01-01")
yt_live = {v["snippet"]["resourceId"]["videoId"]: v["snippet"]["title"] for v in yt
           if v["snippet"]["publishedAt"] >= cut}
ig_live = {m["id"]: (m.get("caption") or "")[:60] for m in ig}
cover_urls = set(); listed_yt = set(); listed_ig = set(); problems = []
for ser in s["series"]:
    nums = sorted(p["bhag"] for p in ser["parts"])
    if nums != list(range(1, len(nums) + 1)):
        problems.append(f"{ser['name']}: parts are {nums}, expected 1..{len(nums)} with no gap")
    for p in ser["parts"]:
        tag = f"{ser['name']} भाग {p['bhag']} ({p['title']})"
        if p.get("cover_url"): cover_urls.add(p["cover_url"])
        else: problems.append(f"{tag}: cover has no public link (cover_url) yet")
        for plat, live, listed in (("youtube", yt_live, listed_yt), ("instagram", ig_live, listed_ig)):
            v = p.get(plat)
            if isinstance(v, str):
                listed.add(v)
                if v not in live: problems.append(f"{tag}: {plat} id {v} is not live")
            elif isinstance(v, dict) and v.get("scheduled"):
                print(f"note  {tag}: {plat} scheduled {v['scheduled']} by {v.get('by','?')}")
            else:
                problems.append(f"{tag}: MISSING on {plat} (not posted, not scheduled)")
for i, t in yt_live.items():
    if i not in listed_yt: problems.append(f"YouTube post not in the series list: {i} {t}")
for i, t in ig_live.items():
    if i not in listed_ig: problems.append(f"Instagram post not in the series list: {i} {t}")
for x in sched:
    if x.get("cover_url") not in cover_urls:
        problems.append(f"Scheduled {x['platform']} post '{x.get('title','?')}' ({x.get('when','?')}) does not use a template cover: {x.get('cover_url','none')}")
for p in problems: print("FLAG ", p)
print("OK: series list matches both platforms" if not problems else f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
