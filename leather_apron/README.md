# Leather Apron

## Named after Jack the Ripper

Video-ripping helpers. `enc_vid.py` takes arguments and composes an
ffmpeg command to rip a video; `enc_vid.sh` batch-rips multiple videos
in a directory.

## Deployment

```bash
git clone git@github.com:poseidon0206/hcl_utils.git
cd hcl_utils/leather_apron

# install python using uv
uv python install "$(cat .python-version)"

# create the virtual environment
uv venv

# install the python modules
uv sync
```

Python dependency: [fancy_logger](https://github.com/poseidon0206/fancy_logger)
(installed from git via `pyproject.toml`/`uv.lock`; `requirements.txt`
carries the same dependency for `enc_vid.sh`'s
`uv run --with-requirements` invocation).

System requirements:

- [uv](https://docs.astral.sh/uv/) — the scripts run through it.
- **ffmpeg** at `/opt/homebrew/bin/ffmpeg`, built with `libfdk_aac`
  (audio) and `hevc_videotoolbox` (default video encoder).
- `~/bin/mk_ss.sh` and `~/bin/post_av.sh` — helper scripts called by
  `enc_vid.sh`.

## Config

| Variable | File | Description |
|----------|------|-------------|
| `FFMPEG_BIN` | `enc_vid.py` | Absolute path of the ffmpeg binary; existence is checked before every run. |
| `FFMPEG_BASE` | `enc_vid.py` | Template of the composed ffmpeg command (placeholders are filled from the CLI options). |
| `x265_opts` / `x264_opts` | `enc_vid.py` | Video-codec options: `hevc_videotoolbox` by default, `libx264` with `--x264`. |
| `requires-python` | `pyproject.toml` | Python version used by uv (see `.python-version`, currently 3.14). |

## Running the scripts

### enc_vid.py

Composes and runs an ffmpeg command that rips the input video, encoding
with hevc_videotoolbox (x265) by default or libx264 with `--x264`.

| Argument | Default | Description |
|----------|---------|-------------|
| `-b`, `--bitrate` | `600` | Video bitrate of the output file in KB. |
| `-c`, `--crop` | — | Crop the video output (ffmpeg `-vf` value). |
| `-e`, `--end` | — | End position in the input file. |
| `-f`, `--framerate` | `24` | Framerate of the output file. |
| `--fake` | off | Log the composed command, don't run it. |
| `-i`, `--input` | `dvd-rip.avi` | Input file (must exist). |
| `-o`, `--output` | `temp.mp4` | Output file. |
| `-r`, `--resolution` | `960x540` | Output resolution as `[w]x[h]`. |
| `-s`, `--start` | — | Start position in the input file. |
| `-v`, `--verbose` | off | Activate debug logging. |
| `--x264` | off | Encode with libx264 instead of hevc_videotoolbox. |

```bash
uv run enc_vid.py -i dvd-rip.avi -o movie.mp4 -b 800 -s 00:00:05 -e 00:42:00
```

### enc_vid.sh

Batch wrapper: rips every `dvd-rip*.avi` in the current directory via
`enc_vid.py`. The output name is derived from the cover image — a `.jpg`
named after the directory; multi-part rips (`dvd-rip-001.avi`, …) get the
part number appended. After each rip it calls `~/bin/mk_ss.sh` on the
output and finishes with `~/bin/post_av.sh`. Extra arguments are passed
through to `enc_vid.py`.

```bash
cd /path/to/rip/folder   # contains dvd-rip*.avi and <folder>.jpg
/path/to/enc_vid.sh -b 800
```

Note: `rename_subbed.py` is deprecated — it was a one-off tool to mass
rename existing "subbed" videos, and everything is renamed. It stays in
the repo for record keeping.
