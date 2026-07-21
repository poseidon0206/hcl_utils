#! /usr/bin/env python3
"""Animate image frames into a GIF using ImageMagick commands.

Takes the JPEG frames under a directory and — unless --reanimate is
given — optionally removes odd-numbered frames, then crops, logo-pads
and shrinks them, before animating them into the output file.
ImageMagick must be installed and the LOGO_FILE constant updated.
"""
import argparse
import os
import sys

from datetime import datetime
from humanfriendly import format_size
from subprocess import Popen


LOGO_FILE = "/path/to/your/logo_file.png"


class FrameAnimator:
  """
  Preprocesses the .jpg frames in a directory (optional odd-frame
  removal, crop, logo pad, shrink) and animates them into output_file
  via ImageMagick commands. With fake=True every command is echoed
  instead of executed.
  """
  def __init__(self, output_file, current_working_directory, crop_geometry="640x1080+640+0",
               remove_odd=True, fake=True):
    """
    :param output_file: name of the animation file to produce.
    :param current_working_directory: directory holding the .jpg frames;
      all commands run from here.
    :param crop_geometry: ImageMagick crop geometry applied to every
      frame, defaults to "640x1080+640+0".
    :param remove_odd: remove the odd-numbered frames when True.
    :param fake: echo the commands instead of executing them when True.
    """
    self.output_file = output_file
    self.cwd = current_working_directory
    self.crop_geometry = crop_geometry
    self.remove_odd = remove_odd
    self.fake = fake

    self.frame_list, self.remove_list = self.create_lists()
    if len(self.frame_list) <= 0:
      raise FileNotFoundError("No frames found in {o.cwd}.".format(o=self))

  def __repr__(self):
    """
    :return: multi-line string listing the animator's settings and
      frame lists.
    """
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
    """Split the directory's .jpg files into frames to keep and to remove.

    A frame counts as odd-numbered when the digit at the 8th character
    of its filename is odd; those go on the removal list when
    remove_odd is enabled.

    :return: tuple of (sorted frame list, sorted removal list).
    """
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
    """Delete the frames on the removal list when remove_odd is enabled."""
    if self.remove_odd is True and len(self.remove_list) > 0:
      rm_cmd = "rm " + " ".join(self.remove_list)
      self.do_cmd(rm_cmd)
      print("odd-numbered frames removed.")

  def crop_frames(self):
    """Crop every frame to crop_geometry using mogrify."""
    crop_cmd = "mogrify -crop {o.crop_geometry} {frames}".format(
      o=self,
      frames=" ".join(self.frame_list)
    )
    self.do_cmd(crop_cmd)
    print("frames cropped.")

  def pad_and_shrink(self):
    """Pad the logo onto every frame, then shrink each one."""
    for frame in self.frame_list:
      self.pad_logo(frame_file=frame)
      self.shrink_frame(frame_file=frame)
    print("logo padded and shrunk")

  def pad_logo(self, frame_file):
    """Composite LOGO_FILE onto the south-east corner of a frame.

    :param frame_file: filename of the frame to pad.
    """
    pad_cmd = "composite -geometry 80x80+12+12 -gravity southeast {logo} {frame} {frame}".format(
      logo=LOGO_FILE,
      frame=frame_file
    )
    self.do_cmd(pad_cmd)

  def shrink_frame(self, frame_file):
    """Resize a frame to 400 pixels tall, keeping the aspect ratio.

    :param frame_file: filename of the frame to shrink.
    """
    shrink_cmd = "mogrify -resize x400 {frame}".format(frame=frame_file)
    self.do_cmd(shrink_cmd)

  def animate_frames(self):
    """Animate the frames into output_file with magick (looped, optimised)."""
    animate_cmd = "magick {list_of_frames} " \
                  "-delay 1x10 " \
                  "-loop 0 " \
                  "-layers optimize-plus " \
                  "-colors 256 " \
                  "-dither floydsteinberg " \
                  "{o.output_file}".format(list_of_frames=" ".join(self.frame_list), o=self)
    self.do_cmd(animate_cmd)
    print("frames animated.")

  def output_size(self):
    """
    :return: human-friendly string describing the output file's size.
    """
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
  """Parse command-line arguments.

  :param system_args: list of argument strings, e.g. sys.argv[1:].
  :return: argparse.Namespace with crop, fake, location, output,
    remove and reanimate attributes.
  """
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
