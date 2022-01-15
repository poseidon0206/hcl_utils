#! /usr/bin/env python3

import argparse
import os
import sys

from datetime import datetime
from fancy_logger import FancyLogger
from subprocess import Popen

FFMPEG_BASE = "ffmpeg -nostdin -y " \
              "__START_POS__ " \
              "__END_POS__ " \
              "-i __INPUT_FILE__ " \
              "__VF_CROP__ " \
              "-r __FRAME_RATE__ " \
              "-s __RESOLUTION__ " \
              "__VID_OPTS__ " \
              "-acodec libfdk_aac -vbr 5 -ar 48000 " \
              "-ac 2 " \
              "__OUTPUT_FILE__"
FFMPEG_BIN = "/usr/local/bin/ffmpeg"
x264_opts = "-c:v libx264 -b:v __VID_BITRATE__ -strict -2 -movflags faststart"
x265_opts = "-c:v libx265 -preset fast -x265-params crf=23"
fancy_logger = FancyLogger(caller=__name__).get_logger()


class VideoEncoder:
  def __init__(self, input_file, output_file, **kwargs):
    self.check_binary()
    self._verbose = kwargs.get("verbose", False)
    if self._verbose is True:
      fancy_logger.setLevel(10)
      fancy_logger.debug(f"activating verbose mode.")
    self.input_file = input_file
    if not os.path.isfile(self.input_file):
      raise FileNotFoundError(f"Input file <{self.input_file}> does not exist.")
    self.output_file = output_file
    self.frame_rate = str(kwargs.get("frame_rate", 24))
    self.resolution = kwargs.get("resolution", "960x540")
    self.bitrate = kwargs.get("bitrate", "0.8M")
    self.start_pos = kwargs.get("start_pos", None)
    self.end_pos = kwargs.get("end_pos", None)
    self.crop = kwargs.get("crop_opt", None)
    self._x264 = kwargs.get("x264", False)
    self.ffmpeg_cmd = self._compose_command()
    self._fake = kwargs.get("fake", False)
    fancy_logger.debug(f"Are we faking it? <{self._fake}>")

    fancy_logger.debug(self)

  def __repr__(self):
    return """
Encoding '{o.input_file}' to '{o.output_file}'
at '{o.frame_rate}fps' and '{o.bitrate}' per frame, resizing to '{o.resolution}'.

{o.ffmpeg_cmd} 
    """.format(o=self)

  @staticmethod
  def check_binary():
    if not os.path.isfile(FFMPEG_BIN):
      raise FileNotFoundError(f"<ffmpeg> binary not found, unable to continue...")

  def _compose_command(self):
    start_opt = self.get_opt(opt_dict={"name": "ss", "value": self.start_pos})
    end_opt = self.get_opt(opt_dict={"name": "to", "value": self.end_pos})
    crop_opt = self.get_opt(opt_dict={"name": "vf", "value": self.crop})
    _cmd_base = FFMPEG_BASE.replace(
      "__START_POS__",
      start_opt
    ).replace(
      "__END_POS__",
      end_opt
    ).replace(
      "__INPUT_FILE__",
      self.input_file
    ).replace(
      "__FRAME_RATE__",
      self.frame_rate
    ).replace(
      "__VF_CROP__",
      crop_opt
    ).replace(
      "__RESOLUTION__",
      self.resolution
    ).replace(
      "__OUTPUT_FILE__",
      self.output_file
    )
    _vid_opts = x265_opts
    if self._x264 is True:
      _vid_opts = x264_opts.replace(
        "__VID_BITRATE__",
        self.bitrate
      )
    return _cmd_base.replace(
      "__VID_OPTS__",
      _vid_opts
    )

  @staticmethod
  def get_opt(opt_dict):
    if opt_dict["value"] is not None:
      return "-{d[name]} {d[value]}".format(d=opt_dict)
    return ""

  def encode_video(self):
    _enc_start = datetime.now()
    if self.do_command(command=self.ffmpeg_cmd):
      fancy_logger.info("ripping complete.")
    _enc_end = datetime.now()
    _enc_delta = _enc_end - _enc_start
    fancy_logger.info(f"start = {_enc_start}, end = {_enc_end}, delta = {_enc_delta}")

  def do_command(self, command, do_we_need_shell=False):
    """
    a wrapper for Popen
    """
    fancy_logger.debug(command)
    if self._fake is True:
      return
    if do_we_need_shell is True:
      cmd = command
    else:
      cmd = [w for w in command.split()]
    try:
      proc = Popen(cmd, shell=do_we_need_shell)
      proc.communicate()
      if proc.returncode != 0:
        raise ValueError(f"Command did not return ZERO status : {proc.returncode}")
      return True
    except OSError as err:
      fancy_logger.error(f"Command <{command}> was unsuccessful.")
      fancy_logger.debug(err)
      raise err
    except Exception as e:
      fancy_logger.error(f"Command <{command}> encountered unknown error.")
      fancy_logger.debug(e)
      raise e

  @staticmethod
  def parse_args(sys_args):
    parser = argparse.ArgumentParser(description="Video Encoder")
    parser.add_argument("-b",
                        "--bitrate",
                        help="video bitrate of ourput file in MB, defaults to 0.8",
                        type=float,
                        default=[0.8],
                        nargs=1)
    parser.add_argument("-c",
                        "--crop",
                        help="crop the video output",
                        type=str,
                        nargs=1)
    parser.add_argument("-e",
                        "--end",
                        help="end position of the input file",
                        type=str,
                        nargs=1)
    parser.add_argument("-f",
                        "--framerate",
                        help="framerate of output file, defaults to 24",
                        type=int,
                        default=[24],
                        nargs=1)
    parser.add_argument("--fake",
                        help="fake it, don't do it.",
                        action="store_true")
    parser.add_argument("-i",
                        "--input",
                        help="input file, default = dvd-ript.avi",
                        type=str,
                        default=["dvd-rip.avi"],
                        nargs=1)
    parser.add_argument("-o",
                        "--output",
                        help="output file, default = temp.mp4",
                        type=str,
                        default=["temp.mp4"],
                        nargs=1)
    parser.add_argument("-r",
                        "--resolution",
                        help="resolution of output file, defaults to 960x540",
                        type=str,
                        default=["960x540"],
                        nargs=1)
    parser.add_argument("-s",
                        "--start",
                        help="start position of input file",
                        type=str,
                        nargs=1)
    parser.add_argument("-v",
                        "--verbose",
                        help="activate verbose mode.",
                        action="store_true")
    parser.add_argument("--x264",
                        help="use x264 instead of x265",
                        action="store_true")
    parsed_args = parser.parse_args(sys_args)
    if "x" not in vars(parsed_args)["resolution"][0]:
      return parser.error(
        "The resolution format = [w]x[h], such as 720x480. {}".format(
          vars(parsed_args)["resolution"][0]
        )
      )
    if not os.path.isfile(vars(parsed_args)["input"][0]):
      return parser.error(f"Input file <{vars(parsed_args)['input'][0]}> does not exist.")
    return parsed_args


if __name__ == "__main__":
  VideoEncoder.check_binary()
  args = VideoEncoder.parse_args(sys_args=sys.argv[1:])
  bit_rate = str(args.bitrate[0]) + "M"
  start = args.start[0] if args.start else args.start
  end = args.end[0] if args.end else args.end
  crop = args.crop[0] if args.crop else args.crop
  ve = VideoEncoder(
    input_file=args.input[0],
    output_file=args.output[0],
    frame_rate=args.framerate[0],
    resolution=args.resolution[0],
    bitrate=bit_rate,
    start_pos=start,
    end_pos=end,
    crop_opt=crop,
    verbose=args.verbose,
    x264=args.x264,
    fake=args.fake
  )
  ve.encode_video()
