# Fandom Gifs

A frame animator. Takes the JPEG frames under a directory and animates
them into a looping GIF using ImageMagick commands, cropping the frames,
padding your logo onto them and shrinking them along the way.

## Deployment

```bash
git clone git@github.com:poseidon0206/hcl_utils.git
cd hcl_utils/fandom_gifs
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Python dependency (pinned in `requirements.txt`): `humanfriendly`.

System requirement: **ImageMagick 7** — the script shells out to `magick`,
`mogrify` and `composite`.

## Config

| Variable | File | Description |
|----------|------|-------------|
| `LOGO_FILE` | `animate_frames.py` | Absolute path to the logo image composited onto the south-east corner of every frame. Update this before the first run. |

## Running the scripts

### animate_frames.py

Preprocesses the `.jpg` frames in a directory and animates them into the
output file. By default it crops each frame, pads the logo onto it and
shrinks it to 400 px tall before animating; with `--reanimate` the
preprocessing is skipped and the existing frames are animated as-is.
A frame counts as odd-numbered (for `--remove`) when the digit at the
8th character of its filename is odd.

| Argument | Default | Description |
|----------|---------|-------------|
| `-c`, `--crop` | `640x1080+640+0` | ImageMagick crop geometry applied to every frame. |
| `-f`, `--fake` | off | Don't execute the commands, just print them. |
| `-l`, `--location` | current directory | Directory holding the frames. |
| `-o`, `--output` | (required) | Name of the output file. |
| `-r`, `--remove` | off | Remove odd-numbered frames first. |
| `--reanimate` | off | Skip preprocessing, just animate the frames. |

Example:

```bash
# dry run: show the ImageMagick commands without executing them
./animate_frames.py --fake -r -l ~/frames -o fandom.gif

# real run
./animate_frames.py -r -l ~/frames -o fandom.gif
```
