#! /usr/bin/env python3

import argparse
import os.path
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from nds_logger import NDSLogger
from sys import argv


nds_logger = NDSLogger(caller=__name__).get_logger()


def _connect_url(target_url, streaming=False):
  """
    Load the html data into memory
    :param target_url: (str) the URL of the html document
    :param streaming: (bool) whether we're streaming or not:
                      True for downloading files; False for fetching pages.
    :return: requests object
    """
  try:
    r = requests.get(
      target_url,
      stream=streaming
    )
    if r.status_code != 200:
      nds_logger.error(f"target URL did not return 200 status!")
      raise ValueError(f"bailing out for now.")
    return r
  except Exception as e:
    nds_logger.error(f"unable to retrieve data from target url <{target_url}>!")
    nds_logger.debug(e)


def _pull_html(target_url):
  """
  Load the html data into memory
  :param target_url: (str) the URL of the html document
  :return: beautiful soup object
  """
  r = _connect_url(target_url=target_url)
  return BeautifulSoup(r.text, "html.parser")


def main(target_url, **kwargs):
  if kwargs.get("verbose", False) is True:
    nds_logger.setLevel(10)
    nds_logger.debug("verbose mode activated.")
  soup = _pull_html(target_url=target_url)
  ctr = 0
  for link in soup.find_all("a"):
    link_url = link.get("href")
    if ".jpg" not in link_url:
      continue
    ctr += 1
    nds_logger.info(f"{ctr:02d}. {link_url}")
    download_target(target_url=link_url)


def download_target(target_url):
  """
  download the given url
  :param target_url: (str) the URL to download
  :return: None
  """
  r = _connect_url(target_url=target_url, streaming=True)
  total_size = int(r.headers.get("Content-Length", 0))
  chunk_size = 1024
  file_name = os.path.basename(target_url)
  if os.path.isfile(file_name) and os.path.getsize(file_name) == total_size:
    nds_logger.debug(f"<{file_name}> downloaded.")
  else:
    nds_logger.debug(f"downloading <{file_name}> ({total_size}).")
    with open(file_name, "wb") as target_fh:
      r.raw.decode_content = True
      for chunk in r.iter_content(chunk_size=chunk_size):
        if chunk:
          target_fh.write(chunk)


def parse_args(sys_args):
  parser = argparse.ArgumentParser(description="grab links for jpgs")
  parser.add_argument("-v",
                      "--verbose",
                      action="store_true",
                      help="activate verbose mode.")
  parser.add_argument("-t",
                      "--target",
                      type=str,
                      help="target url to grab.",
                      required=True)
  return parser.parse_args(sys_args)


if __name__ == "__main__":
  _start = datetime.utcnow()
  args = parse_args(sys_args=argv[1:])
  main(
    target_url=args.target,
    verbose=args.verbose
  )
  _end = datetime.utcnow()
  _delta = _end - _start
  nds_logger.info(f"start = <{_start}>, end = <{_end}>, delta = <{_delta}>")
