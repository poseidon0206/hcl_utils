from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class QRelease2:
  def __init__(self, query_date=datetime.now().strftime("%Y-%m-%d"), every=3, num_rels=2):
    """
    QRelease2: does the same thing as QRelease, just fancier.
    :param query_date: (str) the date in YYYY-MM-DD format, defaults to current time.
    :param every: (int) the release period, defaults to 3.
    :param num_rels: (int) number of previous and next releases to obtain, defaults to 2.
    """
    self.query_datetime = datetime.strptime(query_date, "%Y-%m-%d")
    self.rel_period = every
    self.number_of_rels = num_rels

    self.current = Quarter(self._get_start_of_quarter(self.query_datetime.year, self.query_datetime.month))

    self.next_releases = list()
    self.prev_releases = list()
    for n in range(1, num_rels+1):
      prev_rel = Quarter(
        self._get_start_of_quarter(self.query_datetime.year, self.query_datetime.month, multiplier=-n)
      )
      self.prev_releases.append(prev_rel)
      next_rel = Quarter(
        self._get_start_of_quarter(self.query_datetime.year, self.query_datetime.month, multiplier=n)
      )
      self.next_releases.append(next_rel)

  def _get_start_of_quarter(self, year, month, multiplier=0):
    """
    _get_start_of_quarter: the method will pad the number of release periods,
    and adjust the date to be the start of a release period.
    :param year: (str) the year in question
    :param month: (str) the month in question
    :param multiplier: (int) how many release periods to add / subtract
    :return: date object of the computed release period
    """
    int_mth = int(month)
    int_year = int(year)
    # in order to get to the start of the release period, we use modulus
    reducer = int_mth % self.rel_period
    # work out how many months to add / remove
    padded_months = multiplier * self.rel_period
    # using relativedelta, we can work out any number of releases we need
    return date(int_year, int_mth, 1) - relativedelta(months=reducer) + relativedelta(months=padded_months)

  def __repr__(self):
    return """
QRelease(
  <current = {o.current}>,
  <prev = {o.prev_releases}>,
  <next = {o.next_releases}>,
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
    self.folder_str = "{o.year}_{o.month}".format(o=self)

  def __repr__(self):
    return """
  Quarter(
    <year = {o.year}>
    <month = {o.month}>
    <release = {o.release}>
    <abbreviation = {o.abbreviation}>
    <folder = {o.folder_str}>
  )
    """.format(o=self)
