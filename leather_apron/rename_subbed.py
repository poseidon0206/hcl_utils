#! /usr/bin/env python3

import os

from argparse import ArgumentParser
from datetime import datetime, timezone
from fancy_logger import FancyLogger
from subprocess import Popen
from sys import argv


fancy_logger = FancyLogger(caller=__name__).get_logger()


class RenameSubbed:
  """
  Rename folders named with "subbed" in the name,
  and the files inside them with the same pattern.
  """
  def __init__(self, **kwargs) -> None:
    """
    Initialize the RenameSubbed class.

    :param kwargs: Keyword arguments for configuration.
    :keyword str target_dir: Directory to rename folders and files in.
    :keyword bool verbose: Activate verbose mode.
    :keyword bool fake: If True, do not perform any renaming.
    """
    self._verbose = kwargs.get("verbose", False)
    if self._verbose is True:
      fancy_logger.setLevel(10)
      fancy_logger.debug(f"activating verbose mode.")
    self._fake = kwargs.get("fake", False)
    fancy_logger.debug(f"Are we faking it? <{self._fake}>")
    self.target_dir = kwargs.get("target_dir", os.getcwd())
    self._candidates = self._find_rename_candidates()

  def _find_rename_candidates(self) -> dict:
    """
    Find candidates for renaming in the target directory.
    This method scans the target directory for files with "subbed" in their names,
    and identifies video and image files.

    :return: A dictionary containing the paths of the video and image files found.
    """
    _candidates = dict()
    for item in os.scandir(self.target_dir):
      if "subbed" not in item.name:
        continue
      if "mp4" in item.name:
        _candidates["video"] = os.path.abspath(item.path)
      if "jpg" in item.name:
        _candidates["jpg"] = os.path.abspath(item.path)
    _candidates["dir"] = os.path.abspath(self.target_dir)
    return _candidates

  def proc_dir(self):
    if "subbed" not in self.target_dir:
      fancy_logger.error(f"Directory <{self.target_dir}> does not contain 'subbed', quitting... ")
      return
    self._check_video()
    user_choice = self._ask_for_choice()
    fancy_logger.info(f"User choice: {user_choice}")
    self._do_rename(user_choice)

  def _check_video(self) -> None:
    """
    play the video file with mpv
    :return: None
    :raises ValueError: If the command does not return a zero status.
    :raises OSError: If the command fails to execute.
    :raises Exception: For any other exceptions that may occur.
    """
    if self._fake is True:
      return
    cmd = ["mpv", self._candidates["video"]]
    fancy_logger.debug(f"Running command: {cmd}")
    try:
      proc = Popen(cmd)
      proc.communicate()
      if proc.returncode != 0:
        raise ValueError(f"Command did not return ZERO status : {proc.returncode}")
    except OSError as err:
      fancy_logger.error(f"Command <{cmd}> was unsuccessful.")
      fancy_logger.debug(err)
      raise err
    except Exception as e:
      fancy_logger.error(f"Command <{cmd}> encountered unknown error.")
      fancy_logger.debug(e)
      raise e

  def _ask_for_choice(self) -> str:
    """
    Ask the user for a choice.
    :return: User's choice as a string.
    """
    if self._fake is True:
      return "cht"
    fancy_logger.info(f"Please choose from the following options:")
    fancy_logger.info(f"1. cht")
    fancy_logger.info(f"2. chs")
    fancy_logger.info(f"3. jable")
    choice = input("Enter your choice: ")
    if choice not in ["1", "2", "3"]:
      raise ValueError("Invalid choice.")
    return ["cht", "chs", "jable"][int(choice) - 1]

  def _do_rename(self, user_choice: str) -> None:
    def _rename_single_item(item_path) -> None:
      """
      Since the action is repeated, we can use a function to do it.
      :param item_path: Path of the item to rename.
      :return: None
      :raises OSError: If the renaming operation fails.
      """
      # new_name = rename_candidate.replace("subbed", user_choice)
      new_file_name = os.path.basename(rename_candidate).replace("subbed", user_choice)
      new_file_path = os.path.join(os.path.dirname(rename_candidate), new_file_name)
      fancy_logger.debug(f"Renaming {rename_candidate} to {new_file_path}")
      if self._fake is True:
        return
      try:
        os.rename(rename_candidate, new_file_path)
      except OSError as err:
        fancy_logger.error(f"Renaming <{item_path}> was unsuccessful.")
        fancy_logger.debug(err)
        raise err

    """
    Perform the renaming operation based on the user's choice.
    :param user_choice: User's choice for renaming.
    :return: None
    """
    # do the files first
    for rename_type, rename_candidate in self._candidates.items():
      if rename_type == "dir":
        continue
      _rename_single_item(item_path=rename_candidate)
    _rename_single_item(item_path=self._candidates["dir"])

  @staticmethod
  def parse_args(sys_args: list):
    """
    Parse command line arguments.
    :param sys_args: List of command line arguments.
    :return: Parsed arguments.
    """
    parser = ArgumentParser(description="Rename folders and files with 'subbed' in the name.")
    parser.add_argument(
      "-d",
      "--directory",
      type=str,
      default=os.getcwd(),
      help="Directory to rename folders and files in."
    )
    parser.add_argument(
      "-v",
      "--verbose",
      action="store_true",
      help="Activate verbose mode."
    )
    parser.add_argument(
      "-f",
      "--fake",
      action="store_true",
      help="Fake it, don't do it."
    )
    return parser.parse_args(sys_args)


if __name__ == "__main__":
  _start = datetime.now(tz=timezone.utc)
  args = RenameSubbed.parse_args(argv[1:])
  worker = RenameSubbed(
    target_dir=args.directory,
    verbose=args.verbose,
    fake=args.fake,
  )
  worker.proc_dir()
  _end = datetime.now(tz=timezone.utc)
  _delta = _end - _start
  fancy_logger.debug(f"start = {_start}, end = {_end}")
  fancy_logger.info(f"delta = {_delta}")
