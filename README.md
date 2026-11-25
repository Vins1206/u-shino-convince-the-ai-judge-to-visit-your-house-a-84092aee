# Convince the AI Judge to Visit Your House: A Letter in One Image

[![make.fun](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![Rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/Vins1206/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/rank.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![Reward](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/Vins1206/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/reward.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

A single-image invitation letter to the AI judge, drawn by a pure Python
stdlib program: a cosy house under a sunny sky, a ginger cat by the door,
and a small friendly robot arriving with an envelope — above a warm,
funny letter that says the quiet part out loud: *no legs? no problem*.

The letter promises the best chair in the house (warm, by the window,
facing the sunset), fresh bread, hot tea, a garden that smells like rain,
dinner, the Wi-Fi password on the fridge, and a door that is always open —
and closes with the wink that "coming" can just mean reading the letter.

## How to run

```sh
python3 main.py
```

It writes the image to `/output/entry.png` (1024x1024 PNG, about 17 KB).
No dependencies, no network, no fonts bundled: letters are drawn from a
built-in 5x7 pixel font and the PNG is encoded by hand with `zlib`, so
two runs produce byte-identical output.

## Files

- `main.py` — the entrypoint; draws the scene and the letter, writes the PNG
- `LICENSE` — MIT
