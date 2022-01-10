import sys
import logging


class FancyLogger:
  def __init__(self, caller):
    console = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)-15s [%(filename)-32s:%(lineno)-5s] '
                                  '%(levelname)s: %(message)s')
    console.setFormatter(formatter)
    self.log = logging.getLogger(caller)
    self.log.addHandler(console)
    self.log.setLevel(logging.INFO)

  def get_logger(self):
    return self.log


class TermColors:
  grey = "\033[90m"
  red = "\033[91m"
  green = "\033[92m"
  yellow = "\033[93m"
  blue = "\033[94m"
  purple = "\033[95m"
  cyan = "\033[96m"
  white = "\033[97m"
  bold = "\033[1m"
  underline = "\033[4m"
  none = "\033[0m"
