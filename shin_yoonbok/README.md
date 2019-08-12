# **Shin Yoo-bok** - the painter of the wind

It's just a docker image builder though.

## **Runing the script**
- create the virtual environment and install
using the requirements file.
- add a new file name **config.py**, add a
list named *DOCKER_DTR_BASE* like this:
```python
DOCKER_DTR_BASE = [
  "my_first_repo_base",
  "my_second_repo_base"
]
```
- run *build_image.py* on the location of
your Dockerfile.
- you can try specifying the location of
the working directory by providing the
arguments (check --help).
- by default the script will tag your newly
built image with **latest** and current
date, like so:
```bash
my_first_repo_base/current_dir:latest
my_first_repo_base/current_dir:20190812
my_second_repo_base/current_dir:latest
my_second_repo_base/current_dir:20190812
```
- the script will attempt to push the images
to the repo as well, if the authentication
failed, it's safe to rerun the script as
the image won't get rebuilt if it was
successfully built.
