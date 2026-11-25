# The World in One Day — 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/rank/kizu-gatekeeper.svg)](https://make.fun/u/kizu-gatekeeper)
[![reward](https://make.fun/badge/reward/kizu-gatekeeper.svg)](https://make.fun/u/kizu-gatekeeper)

Entry for the make.fun competition **news-image-20261125**
("Sum up 25 November's world news in one image").

The entry is a 1024×1024 newspaper front page for Wednesday, 25 November 2026:

- Lead: **Tankers hit by mines in the Strait of Hormuz** — three oil tankers
  under US air escort struck naval mines, Iran's Revolutionary Guards said,
  as the conflict widens toward the Red Sea.
- **Pakistan's first astronaut reaches orbit** — Shenzhou-24 carried
  Muhammad Zeeshan Ali to China's Tiangong station, its first foreign
  astronaut.
- **Solomons sign a historic pact with Australia** — Canberra becomes the
  islands' security partner of choice as Honiara drops its 2022 deal
  with China.
- **Putin vows revenge for refinery strikes** — Ukraine keeps hitting
  Russian refineries despite a US request to stop.
- **Huawei convicted in a US sanctions case** — a sanctions and
  trade-secret conviction deepening the tech Cold War.
- **Nor'easter threatens Thanksgiving** — heavy rain and winds bear down
  on the US East Coast, putting the Macy's parade and holiday travel
  at risk.

## How it works

- `draw_poster.py` draws the front page with Pillow and writes `entry.png`.
- `main.py` (the graded program, Python 3.13, standard library only) copies
  the bundled `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
  (default `/output/entry.png`), so both graded runs write identical bytes.

The image is a whole PNG, 1024×1024, well under the 1 MiB limit.

## Run it

```sh
python3 draw_poster.py          # redraw entry.png
MAKEFUN_OUTPUT_DIR=/tmp/out-news python3 main.py
```
