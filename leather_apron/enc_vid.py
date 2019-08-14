#! /usr/bin/env python3

import argparse
import os
import sys

from subprocess import Popen

FFMPEG_BASE = "/usr/local/bin/ffmpeg -nostdin -y __START_POS__ __END_POS__ -i __INPUT_FILE__ \
__VF_CROP__ -r __FRAME_RATE__ -s __RESOLUTION__ -c:v libx264 -b:v __VID_BITRATE__ \
-strict -2 -movflags faststart -acodec libfdk_aac -vbr 5 -ar 48000 -ac 2 \
__OUTPUT_FILE__"


class VideoEncoder:
  def __init__(self, input_file, output_file,
               frame_rate=24, resolution="960x540", bitrate="0.8M",
               start_pos=None, end_pos=None, crop_opt=None):
    self.input_file = input_file
    if not os.path.isfile(self.input_file):
      raise FileNotFoundError("Input file '{o.input_file}' does not exist.".format(o=self))
    self.output_file = output_file
    self.frame_rate = str(frame_rate)
    self.resolution = resolution
    self.bitrate = bitrate
    self.start_pos = start_pos
    self.end_pos = end_pos
    self.crop = crop_opt
    self.ffmpeg_cmd = self.compose_command()

    print(self)

  def __repr__(self):
    return """
Encoding '{o.input_file}' to '{o.output_file}'
at '{o.frame_rate}fps' and '{o.bitrate}' per frame, resizing to '{o.resolution}'.

{o.ffmpeg_cmd} 
    """.format(o=self)

  def compose_command(self):
    start_opt = self.get_opt(opt_dict={"name": "ss", "value": self.start_pos})
    end_opt = self.get_opt(opt_dict={"name": "to", "value": self.end_pos})
    crop_opt = self.get_opt(opt_dict={"name": "vf", "value": self.crop})
    return FFMPEG_BASE.replace(
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
      "__VID_BITRATE__",
      self.bitrate
    ).replace(
      "__OUTPUT_FILE__",
      self.output_file
    )

  def get_opt(self, opt_dict):
    if opt_dict["value"] is not None:
      return "-{d[name]} {d[value]}".format(d=opt_dict)
    return ""

  def encode_video(self):
    if self.do_command(command=self.ffmpeg_cmd):
      print("ripping complete.")

  def do_command(self, command, do_we_need_shell=False):
    """
    a wrapper for Popen
    """
    print(command)
    if do_we_need_shell is True:
      cmd = command
    else:
      cmd = [w for w in command.split()]
    try:
      Popen(cmd, shell=do_we_need_shell).wait()
      return True
    except OSError as err:
      print("Command '{}' was unsuccessful : {}".format(command, err))
      raise OSError
    except Exception as e:
      print("Unknown error: {}".format(e))
      raise Exception


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
  parser.add_argument("-i",
                      "--input",
                      help="input file",
                      required=True,
                      type=str,
                      nargs=1)
  parser.add_argument("-o",
                      "--output",
                      help="output file",
                      required=True,
                      type=str,
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
  parsed_args = parser.parse_args(sys_args)
  if "x" not in vars(parsed_args)["resolution"][0]:
    return parser.error(
      "The resolution format = [w]x[h], such as 720x480. {}".format(
        vars(parsed_args)["resolution"][0]
      )
    )
  if not os.path.isfile(vars(parsed_args)["input"][0]):
    return parser.error("Input file does not exist.")
  return parsed_args


if __name__ == "__main__":
  args = parse_args(sys_args=sys.argv[1:])
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
    crop_opt=crop
  )
  ve.encode_video()
