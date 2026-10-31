# L1 vs. L2 Regularization

An educational video project explaining how **L1** and **L2 regularization** affect neural-network weights. The animations are written in Python with [Manim Community Edition](https://www.manim.community/), then assembled and edited in Adobe Premiere Pro.

## Watch the video

- [Full video with channel intro (MP4)](Editing/L1L2%20Video%20%2B%20Intro.mp4)
- [Main video without the intro (MP4)](Editing/L1L2%20Video.mp4)

The MP4 files are included in the `Editing` folder. Click a link above to open the video from the repository.

## What it covers

- A fully connected neural network with a **3–3–1** layout.
- The L1 penalty: the sum of the absolute values of the weights.
- The L2 penalty: the sum of the squared weights.
- Why L1 can drive some weights to exactly zero.
- Why L2 usually shrinks weights progressively toward zero.
- The cost functions, gradients, update rules, and the rearranging step behind L2 weight decay.

## Project structure

| Path | Description |
| --- | --- |
| `Code/l1_l2_video.py` | Main Manim animation for the regularization explainer. |
| `Code/Intro video.py` | Separate Manim scene for the channel intro. |
| `Code/voiceover_script_en.md` | English narration script with scene cues. |
| `Editing/L1L2 Video + Intro.mp4` | Final video with the channel intro. |
| `Editing/L1L2 Video.mp4` | Final video without the channel intro. |

Manim render caches, Premiere autosaves, and preview files are local working files and are excluded from Git.

## Render the animations

### Requirements

- Python supported by your installed Manim release
- Manim Community Edition
- NumPy
- A LaTeX distribution with `dvisvgm` for Manim's `MathTex`
- FFmpeg

Install Manim and NumPy in the Python environment you will use:

```powershell
python -m pip install manim numpy
```

Render the main animation from the `Code` directory:

```powershell
cd Code
manim -pql l1_l2_video.py L1L2Video
```

Render the channel intro:

```powershell
manim -pql "Intro video.py" ChannelIntro
```

`-pql` creates a quick, low-quality preview and opens it when rendering finishes. Change it to `-pqh` for a higher-quality render.

## Music credit

If the published video uses **“Zeta”** by Vincent Rubinetti, include the credit requested by the composer in the video's description:

> Music by Vincent Rubinetti  
> Download the music on Bandcamp: https://vincerubinetti.bandcamp.com  
> Stream the music on Spotify: https://open.spotify.com/artist/2SRhEEt2tlDQWxzwfUo9Dl

## License

No license has been added. Unless the project owner chooses and adds one, the source code remains under the owner's default copyright.
