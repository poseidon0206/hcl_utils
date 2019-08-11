from datetime import date, datetime


class QRelease2:
  def __init__(self, query_date=datetime.now().strftime("%Y-%m-%d"), every=3):
    """
    QRelease2: does the same thing as QRelease, just fancier.
    :param query_date: (str) the date in YYYY-MM-DD format, defaults to current time.
    :param every: (int) the release period, defaults to 3.
    """
    self.query_datetime = datetime.strptime(query_date, "%Y-%m-%d")
    self.rel_period = every

    self.current = Quarter(self.get_start_of_quarter(self.query_datetime.year, self.query_datetime.month))

    prv_mth = self.query_datetime.month - (1 * self.rel_period)
    self.previous = Quarter(self.get_start_of_quarter(self.query_datetime.year, prv_mth))

    bfr_mth = self.query_datetime.month - (2 * self.rel_period)
    self.before = Quarter(self.get_start_of_quarter(self.query_datetime.year, bfr_mth))

    nxt_mth = self.query_datetime.month + (1 * self.rel_period)
    self.next = Quarter(self.get_start_of_quarter(self.query_datetime.year, nxt_mth))

  def get_start_of_quarter(self, year, month):
    int_year = int(year)
    int_mth = int(month)
    # this will give me the current release from current date
    int_mth = int_mth - (int_mth % self.rel_period)
    # if we get zero, then we're on the last release of last year.
    if int_mth <= 0:
      int_mth += 12
      int_year -= 1
    # if we get more than 12, then we're on the first release of next year.
    if int_mth > 12:
      int_mth -= 12
      int_year += 1
    return date(int_year, int_mth, 1)

  def __repr__(self):
    return """
QRelease(
  <current = {o.current}>
  <previous = {o.previous}>
  <before = {o.before}>
  <next = {o.next}>
)
    """.format(o=self)


class Quarter:
  def __init__(self, start_of_quarter):
    """
    Qurater: a class to store quarter data.
    :param start_of_quarter: (date) the date which the quarter starts.
    """
    self.year = start_of_quarter.year
    self.month = "{m:02d}".format(m=start_of_quarter.month)
    self.release = "{o.year}.{o.month}".format(o=self)
    self.abbreviation = "{y}{m}".format(y=str(self.year)[2:], m=self.month)

  def __repr__(self):
    return """
  Quarter(
    <year = {o.year}>
    <month = {o.month}>
    <release = {o.release}>
    <abbreviation = {o.abbreviation}>
  )
    """.format(o=self)
