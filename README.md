# The World in One Day — Friday 27 November 2026

A one-page newspaper front page summing up 27 November 2026's world news
in a single 1024×1024 image, for the make.fun bounty
"Sum up 27 November's world news in one image".

## What's in the image

- **15 stories, all verified as first reported on Friday 27 November 2026:**
  3 illustrated leads (EU summit stalls, Black Friday, Australia gas law),
  8 numbered secondaries (Japan tobacco takeover talk, London Tube strike,
  Gukesh–Sindarov rest day, Cricket Australia forum, China gold belt,
  Trump on a Ukraine deal, Mandelson files, Mecca pact meeting) and
  4 more in the also-list — plus a world pin map, a UTC "later today"
  strip, a big-number strip, and an explicit DATE CHECK box listing
  stories from other days that were deliberately left out.
- Every story carries a source line and a HOW SURE badge
  (OFFICIAL / CONFIRMED / REPORTED / CLAIM).

## How it is built

`generate_image.py` draws the whole page in code with Pillow
(flat vector-style illustrations, no photos, no network, no randomness)
and writes `entry.png`. `main.py` is the entrypoint: it copies
`entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`), using
only the Python standard library, so repeated runs are byte-identical.

Regenerate locally:

```sh
python3 generate_image.py   # writes entry.png (1024x1024, ~165 KB)
python3 main.py             # copies it to /output/entry.png
```

## Sources

Reuters, Guardian, FIDE, ScienceAlert, BBC, Time Out — all dated
Friday 27 November 2026. Pictures and map are original, drawn in code.
