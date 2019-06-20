from datetime import date, datetime


class QRelease2:
  def __init__(self, queryDate=datetime.now().strftime("%Y-%m-%d"), every=3):
    """
    QRelease2: does the same thing as QRelease, just fancier.
    :param queryDate: (str) the date in YYYY-MM-DD format, defaults to current time.
    :param every: (int) the release period, defaults to 3.
    """
    self.queryDatetime = datetime.strptime(queryDate, "%Y-%m-%d")
    self.relPeriod = every

    self.current = Quarter(self.getStartOfQuarter(self.queryDatetime.year, self.queryDatetime.month))

    prvMth = self.queryDatetime.month - (1 * self.relPeriod)
    self.previous = Quarter(self.getStartOfQuarter(self.queryDatetime.year, prvMth))

    bfrMth = self.queryDatetime.month - (2 * self.relPeriod)
    self.before = Quarter(self.getStartOfQuarter(self.queryDatetime.year, bfrMth))

    nxtMth = self.queryDatetime.month + (1 * self.relPeriod)
    self.next = Quarter(self.getStartOfQuarter(self.queryDatetime.year, nxtMth))

  def getStartOfQuarter(self, year, month):
    iYear = int(year)
    iMth = int(month)
    # this will give me the current release from current date
    iMth = iMth - (iMth % self.relPeriod)
    # if we get zero, then we're on the last release of last year.
    if iMth <= 0:
      iMth += 12
      iYear -= 1
    # if we get more than 12, then we're on the first release of next year.
    if iMth > 12:
      iMth -= 12
      iYear += 1
    return date(iYear, iMth, 1)

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
  def __init__(self, startOfQuarter):
    """
    Qurater: a class to store quarter data.
    :param startOfQuarter: (date) the date which the quarter starts.
    """
    self.year = startOfQuarter.year
    self.month = "{m:02d}".format(m=startOfQuarter.month)
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
