# L1 vs. L2 Regularization

An animated explanation of how L1 and L2 regularization affect neural-network weights, including the gradients and update rules behind their different behavior.

## Watch

[![Watch the video](https://img.youtube.com/vi/ErA7QN2pys4/hqdefault.jpg)](https://youtu.be/ErA7QN2pys4)

Also on [YouTube](https://youtu.be/ErA7QN2pys4) · [TikTok](https://www.tiktok.com/@mezo_magdy)

## What it covers

- L1 and L2 penalty terms for a neural network.
- Why L1 can drive some weights to zero.
- Why L2 progressively shrinks weights.
- The L2 update rule and its weight-decay form.
- The L1 sign gradient and its constant-magnitude pull.

## Project files

- src/l1_l2_video.py — main Manim animation.
- src/intro.py — animated channel intro.
- scripts/voiceover_en.md — English narration with visual cues.

## Render

From this folder, install shared dependencies with python -m pip install -r ../../requirements.txt, then render with manim -pql src/l1_l2_video.py L1L2Video or manim -pql src/intro.py ChannelIntro. Manim math text needs LaTeX with dvisvgm; video rendering needs FFmpeg.

## Music credit

If the Zeta recording by Vincent Rubinetti is used in a public release, include the credit requested by the composer in that release description:

> Music by Vincent Rubinetti
> Download the music on Bandcamp: https://vincerubinetti.bandcamp.com
> Stream the music on Spotify: https://open.spotify.com/artist/2SRhEEt2tlDQWxzwfUo9Dl
