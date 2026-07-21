"""Docker image builder.

Provides the ImageBuilder class, which builds an image from a
Dockerfile, tags it against every registry base in config.py's
DOCKER_DTR_BASE, and pushes the tagged images.
"""
import argparse
import docker
import os

from datetime import datetime, timezone


class ImageBuilder:
  """
  Builds the Dockerfile in work_dir into an image, tags it as
  <base>/<work-dir name>:<tag> for every base in DOCKER_DTR_BASE
  (tags: "latest", the current date, and datestamped variants of any
  additional tags), and pushes every combination.
  """
  def __init__(self, work_dir=os.getcwd(), dockerfile="Dockerfile", debug=False, additional_tags=None):
    """
    :param work_dir: directory holding the Dockerfile; its basename
      becomes the image name. Defaults to the current directory.
    :param dockerfile: name of the docker file, defaults to
      "Dockerfile".
    :param debug: show verbose build/tag/push output when True.
    :param additional_tags: extra tags to add to the image, each also
      combined with "latest" and the current date.
    :raises FileNotFoundError: when the dockerfile does not exist.
    """
    self.work_dir = work_dir
    self.dir_name = os.path.basename(self.work_dir)
    self.dockerfile = dockerfile
    self.dockerfile_path = os.path.join(self.work_dir, self.dockerfile)
    self.debug = debug
    if additional_tags is None:
      self.additional_tags = []
    else:
      self.additional_tags = additional_tags
    if not os.path.isfile(self.dockerfile_path):
      raise FileNotFoundError("the dockerfile is not found. maybe you need to specify the file name.")
    self.dc = docker.from_env()
    self.repos = self.get_repos()
    self.tags = self.get_tags()

  def __repr__(self):
    """
    :return: multi-line string listing the builder's settings, repos
      and tags.
    """
    return """
ImageBuilder(
  <work_dir = {o.work_dir}>
  <dockerfile = {o.dockerfile}>
  <dockerfile path = {o.dockerfile_path}>
  <repos = {o.repos}>
  <tags = {o.tags}>
)
    """.format(o=self)

  @staticmethod
  def parse_args(system_args):
    """Parse command-line arguments.

    :param system_args: list of argument strings, e.g. sys.argv[1:].
    :return: argparse.Namespace with debug, file, tags and work_dir
      attributes.
    """
    parser = argparse.ArgumentParser(description="Yoonbok + Jeonghyung = best couple.")
    parser.add_argument("-d",
                        "--debug",
                        default=False,
                        action="store_true",
                        help="show verbose info, defaults to false.")
    parser.add_argument("-f",
                        "--file",
                        default="Dockerfile",
                        help="name of the docker file, defaults to Dockerfile.")
    parser.add_argument("-t",
                        "--tags",
                        nargs="*",
                        default=None,
                        help="additional tags to add to the image.")
    parser.add_argument("-w",
                        "--work-dir",
                        default=os.getcwd(),
                        help="the work directory, defaults to current directory.")
    return parser.parse_args(system_args)

  def get_repos(self):
    """Build the repository names for the image.

    :return: set of "<base>/<work-dir name>" strings, one per registry
      base in config.py's DOCKER_DTR_BASE.
    """
    new_repos = set()
    from config import DOCKER_DTR_BASE
    for dtr_base in DOCKER_DTR_BASE:
      new_repos.add(os.path.join(dtr_base, self.dir_name))
    return new_repos

  def get_tags(self):
    """Build the tag set for the image.

    :return: set with "latest" and the current date (YYYYMMDD), plus
      "<tag>-latest" and "<tag>-<date>" for every additional tag.
    """
    tag_date = datetime.strftime(datetime.now(tz=timezone.utc), "%Y%m%d")
    new_tags = set()
    for tag in [""] + self.additional_tags:
      for datestamp in ("latest", tag_date):
        full_tag = datestamp
        if len(tag) > 0:
          full_tag = tag + "-" + datestamp
        new_tags.add(full_tag)
    return new_tags

  def build_image(self):
    """Build the docker image from the dockerfile.

    :return: the built docker Image object.
    """
    new_image = self.dc.images.build(
      path=self.work_dir,
      dockerfile=self.dockerfile_path,
      rm=True,
      quiet=False
    )
    if self.debug is True:
      for log in new_image[1]:
        print(log)
    return new_image[0]

  def tag_image(self, target_image):
    """Tag the image with every repo/tag combination.

    :param target_image: the docker Image object to tag.
    """
    for repo in self.repos:
      for tag in self.tags:
        if self.debug is True:
          print("tagging image to {repo}:{tag}".format(repo=repo, tag=tag))
        target_image.tag(repository=repo, tag=tag)

  def show_built_image(self, target_image):
    """Print the image id and the tags it carries.

    :param target_image: the docker Image object to show.
    """
    print("\nImage {id} was built with the following tags:\n".format(id=target_image.short_id[7:]))
    for tag in target_image.tags:
      print(tag)
    print("")

  def push_image(self):
    """Push every repo/tag combination, reporting failures per push."""
    for repo in self.repos:
      for tag in self.tags:
        try:
          output = self.dc.images.push(repository=repo, tag=tag, stream=False)
          if self.debug is True:
            print(output)
          else:
            print(f"{repo}:{tag} is pushed.")
        except Exception as err:
          print(f"Unable to push {err}")
