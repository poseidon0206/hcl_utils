import argparse

from datetime import date, datetime, timedelta


class BackToTheFuture:
  """
  BackToTheFuture
  :param year: (str or int) the destined year, defaults to 1985.
  :param month: (str or int) the destined month, defaults to 11.
  :param number_of_years: (int) the number of years to go back, defaults to 30.
  """
  def __init__(self, year=1985, month=11, number_of_years=30):
    self.year = int(year)
    self.month = int(month)
    self.number_of_years = number_of_years
    self.right_now = datetime.strptime(f"{year}-{month}-05", "%Y-%m-%d")
    delta_days = self.number_of_years * 365 + (self.number_of_years // 4)
    self.years_ago = self.right_now - timedelta(days=delta_days)
    self.loop_range = self.number_of_years * 12 + 1

  def by_year(self):
    for y in range(self.years_ago.year, self.right_now.year + 1):
      yield date(y, self.right_now.month, self.right_now.day)

  def by_month(self):
    for m in range(self.loop_range):
      new_mth = self.years_ago.month + m
      new_year = self.years_ago.year
      new_year += new_mth // 12
      if new_mth % 12 == 0:
        new_mth -= ((new_mth // 12) - 1) * 12
        new_year -= 1
      else:
        new_mth -= (new_mth // 12) * 12
      yield date(new_year, new_mth, self.right_now.day)

  @staticmethod
  def parse(sys_args):
    parser = argparse.ArgumentParser(description="Great Scott! 1.21 gigawatts!?")
    parser.add_argument("-y",
                        "--year",
                        type=int,
                        default=1985,
                        help="the destined year.")
    parser.add_argument("-m",
                        "--month",
                        default=11,
                        help="the destined month.")
    parser.add_argument("-n",
                        "--number-of-years",
                        type=int,
                        default=30,
                        help="the number of years to traverse.")
    parser.add_argument("-l",
                        "--monthly",
                        action="store_true",
                        help="show traversed months.")
    parser.add_argument("-a",
                        "--annually",
                        action="store_true",
                        help="show traversed years.")
    return parser.parse_args(sys_args)

  def __repr__(self):
    return """
BackToTheFuture(
  <year = {o.year}>
  <month = {o.month}>
  <number of years = {o.number_of_years}>
  <right now = {o.right_now}>
  <years ago = {o.years_ago}>
  <loop range = {o.loop_range}>
)
    """.format(o=self)
