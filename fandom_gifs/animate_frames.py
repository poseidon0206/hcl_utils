#! /Users/poseidon206/venvs/bin_py37/bin/python -u

import argparse
import os
import sys

from datetime import datetime
from humanfriendly import format_size
from subprocess import Popen


LOGO_FILE = "/path/to/your/logo_file.png"


class FrameAnimator:
  def __init__(self, output_file, current_working_directory, crop_geometry="640x1080+640+0",
               remove_odd=True, fake=True):
    self.output_file = output_file
    self.cwd = current_working_directory
    self.crop_geometry = crop_geometry
    self.remove_odd = remove_odd
    self.fake = fake

    self.frame_list, self.remove_list = self.create_lists()
    if len(self.frame_list) <= 0:
      raise FileNotFoundError("No frames found in {o.cwd}.".format(o=self))

  def __repr__(self):
    return """
Frame Animator(
  <output file = {o.output_file}>,
  <crop geometry = {o.crop_geometry}>,
  <working dir = {o.cwd}>,
  <remove odd = {o.remove_odd}>,
  <frames = {o.frame_list}>,
  <removing = {o.remove_list}>,
  <we're faking = {o.fake}>
)
    """.format(o=self)

  def create_lists(self):
    frame_list = list()
    remove_list = list()
    for file in os.listdir(self.cwd):
      if ".jpg" in file:
        if self.remove_odd is True and int(file[7]) % 2 == 1:
          remove_list.append(file)
        else:
          frame_list.append(file)
    return sorted(frame_list), sorted(remove_list)

  def remove_odd_frames(self):
    if self.remove_odd is True and len(self.remove_list) > 0:
      rm_cmd = "rm " + " ".join(self.remove_list)
      self.do_cmd(rm_cmd)
      print("odd-numbered frames removed.")

  def crop_frames(self):
    crop_cmd = "mogrify -crop {o.crop_geometry} {frames}".format(
      o=self,
      frames=" ".join(self.frame_list)
    )
    self.do_cmd(crop_cmd)
    print("frames cropped.")

  def pad_and_shrink(self):
    for frame in self.frame_list:
      self.pad_logo(frame_file=frame)
      self.shrink_frame(frame_file=frame)
    print("logo padded and shrunk")

  def pad_logo(self, frame_file):
    pad_cmd = "composite -geometry 80x80+12+12 -gravity southeast {logo} {frame} {frame}".format(
      logo=LOGO_FILE,
      frame=frame_file
    )
    self.do_cmd(pad_cmd)

  def shrink_frame(self, frame_file):
    shrink_cmd = "mogrify -resize x400 {frame}".format(frame=frame_file)
    self.do_cmd(shrink_cmd)

  def animate_frames(self):
    animate_cmd = "convert -delay 1x10 -loop 0 -layers optimize-plus -colors 256 -dither floydsteinberg " \
                  "{list} {o.output_file}".format(list=" ".join(self.frame_list), o=self)
    self.do_cmd(animate_cmd)
    print("frames animated.")

  def output_size(self):
    file_size = os.stat(os.path.join(self.cwd, self.output_file)).st_size
    return "{o.output_file} is {disp_size} in size.".format(
      o=self,
      disp_size=format_size(file_size)
    )

  def do_cmd(self, cmd):
    """
    doCmd: do the system command
    :param cmd: (str) the command in string.
    :return: None
    """
    if self.fake is True:
      cmd = f"echo \"{cmd}\""
    try:
      proc = Popen(cmd, shell=True, cwd=self.cwd)
      proc.communicate()
      if proc.returncode != 0:
        raise ValueError("Command did not return ZERO status : {status}".format(status=proc.returncode))
    except OSError as err:
      print("Command was unsuccessful : {err}".format(err=err))
      raise


def parse_args(system_args):
  parser = argparse.ArgumentParser(description="animate frames hehe.")
  parser.add_argument("-c",
                      "--crop",
                      type=str,
                      default="640x1080+640+0",
                      help="the crop geometry of the frames used by imagemagick, such as '640x1080+640+0'.")
  parser.add_argument("-f",
                      "--fake",
                      action="store_true",
                      help="Don't actually execute the command, just print the command.")
  parser.add_argument("-l",
                      "--location",
                      type=str,
                      default=os.getcwd(),
                      help="location of the frames. defaults to current directory")
  parser.add_argument("-o",
                      "--output",
                      type=str,
                      required=True,
                      help="name of the output file.")
  parser.add_argument("-r",
                      "--remove",
                      action="store_true",
                      default=False,
                      help="remove odd-numbered frames.")
  parser.add_argument("--reanimate",
                      action="store_true",
                      default=False,
                      help="don't do preprocess, just animate the cropped frames.")
  return parser.parse_args(system_args)


if __name__ == "__main__":
  start = datetime.now()
  args = parse_args(system_args=sys.argv[1:])
  animator = FrameAnimator(
    output_file=args.output,
    crop_geometry=args.crop,
    current_working_directory=args.location,
    remove_odd=args.remove,
    fake=args.fake
  )
  if not args.reanimate:
    animator.remove_odd_frames()
    animator.crop_frames()
    animator.pad_and_shrink()
  animator.animate_frames()
  print(animator.output_size())

  end = datetime.now()
  delta = end - start
  print(F"start = {start}, end = {end}, delta = {delta}")
