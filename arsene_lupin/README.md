# Arsène Lupin

The gentleman thief.

## Synopsis

Give him a target page, and he'll steal all the pictures that are linked
to the document by the `<a>` tags. The jpgs are stored in the current
working directory; files that are already fully downloaded are skipped.

## Deployment

```bash
git clone git@github.com:poseidon0206/hcl_utils.git
cd hcl_utils/arsene_lupin
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Dependencies (pinned in `requirements.txt`): `requests`,
`beautifulsoup4`, and
[fancy_logger](https://github.com/poseidon0206/fancy_logger)
(installed from git).

## Config

There is no config file — the script is configured entirely through its
command-line options.

## Running the scripts

### grab_pix_from_html.py

Fetches the target page, finds every `<a>` link pointing at a `.jpg`,
and downloads each one into the current working directory. A file whose
size already matches the server's `Content-Length` is not downloaded
again.

| Argument | Default | Description |
|----------|---------|-------------|
| `-t`, `--target` | (required) | Target URL to grab. |
| `-v`, `--verbose` | off | Activate debug logging. |

```bash
cd /folder/to/store/jpgs
./grab_pix_from_html.py -t https://example.com/gallery.html
```

## TODO

- Take and digest multiple targets.
- Option to specify a destination folder.
