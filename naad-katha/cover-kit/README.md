# Naad Katha cover kit

Everything needed to make a Naad Katha Short/Reel cover in the final style (option B, owner 15 Nov 2026), from any project.

- `make-cover.js`: `node make-cover.js <art.jpg> "<series>" "भाग N" "<big word>" "<question>" <out.jpg> [style]` (Playwright, real Yatra One font). Style: 1-navy-gold (default), 2-violet, 3-gold-band, 4-diya-saffron, 5-white-green. Series lock: every part uses its भाग 1 style.
- `series.json`: one list of every Short/Reel by series and part, with its YouTube id, Instagram id (or scheduled time), cover and public cover link. **Covers are numbered from this list, never from one platform's grid.** Add each new post before its cover is made.
- `check_series.py`: compares the list with what is live and scheduled on YouTube and Instagram and flags any post missing on one side, any post not in the list, gaps in भाग numbers, and scheduled posts without a template cover.
- `clean-backgrounds/`: text-free art used for the covers so far.

The working copy lives in the Naad Katha project at `/mnt/project-files/naad-katha-covers/` (copy this folder there; keep `series.json` up to date there).
