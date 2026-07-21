# **Shin Yoon-bok** - the painter of the wind

It's just a docker image builder though.

This was my attempt to simplify docker image building. It's pretty
outdated now that the build and run commands get figured out for you
(e.g. by AI assistants), so the project is all but deprecated.

## Namesake

**Shin Yoon-bok** is known by his pen name *Hyewon*, who was one of the
most influential painters in Korean art history. I was thinking of a
cool name for an image builder, and although he painted his images, it's
close enough.

There was a Korean drama named *Painter of the Wind*, which is where I
learned of the artist.

## Deployment

```bash
git clone git@github.com:poseidon0206/hcl_utils.git
cd hcl_utils/shin_yoonbok
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Dependencies (pinned in `requirements.txt`): `docker` and its
transitive packages. A running docker daemon is required, and you must
be authenticated against the target registries for the push step.

## Config

| Variable | File | Description |
|----------|------|-------------|
| `DOCKER_DTR_BASE` | `config.py` | List of registry/repository bases the image is tagged and pushed to. The file is git-ignored — create it next to the scripts before the first run. |

```python
# config.py
DOCKER_DTR_BASE = [
  "my_first_repo_base",
  "my_second_repo_base"
]
```

## Running the scripts

### build_image.py

Builds the Dockerfile in the work directory into an image named after
the directory, tags it against every base in `DOCKER_DTR_BASE` with
`latest` and the current date — plus datestamped variants of any
additional tags — and pushes every combination. If authentication
failed, it's safe to rerun the script: the image won't get rebuilt if it
was successfully built.

| Argument | Default | Description |
|----------|---------|-------------|
| `-d`, `--debug` | off | Show verbose build/tag/push output. |
| `-f`, `--file` | `Dockerfile` | Name of the docker file. |
| `-t`, `--tags` | — | Additional tags to add to the image. |
| `-w`, `--work-dir` | current directory | The work directory holding the Dockerfile. |

```bash
cd /path/to/my_service   # contains a Dockerfile
python3 /path/to/build_image.py -t stable
```

Resulting tags for `DOCKER_DTR_BASE = ["my_first_repo_base"]`:

```
my_first_repo_base/my_service:latest
my_first_repo_base/my_service:20190812
my_first_repo_base/my_service:stable-latest
my_first_repo_base/my_service:stable-20190812
```
