from datetime import date, datetime, timedelta


class BackToTheFuture:
  """
  BackToTheFuture
  :param year: (str or int) the destined year, defaults to 1985.
  :param month: (str or int) the destined month, defaults to 11.
  :param numberOfYears: (int) the number of years to go back, defaults to 30.
  """
  def __init__(self, year=1985, month=11, numberOfYears=30):
    self.year = int(year)
    self.month = int(month)
    self.numberOfYears = numberOfYears
    self.rightNow = datetime.strptime(f"{year}-{month}-05", "%Y-%m-%d")
    self.yearsAgo = self.rightNow - timedelta(days=self.numberOfYears * 365)
    self.loopRange = self.numberOfYears * 12 + 1

  def byYear(self):
    for y in range(self.yearsAgo.year, self.rightNow.year + 1):
      yield date(y, self.rightNow.month, self.rightNow.day)

  def byMonth(self):
    for m in range(self.loopRange):
      newMth = self.yearsAgo.month + m
      newYear = self.yearsAgo.year
      newYear += newMth // 12
      if newMth % 12 == 0:
        newMth -= ((newMth // 12) - 1) * 12
        newYear -= 1
      else:
        newMth -= (newMth // 12) * 12
      yield date(newYear, newMth, self.rightNow.day)

  def __repr__(self):
    return """
BackToTheFuture(
  <year = {o.year}>
  <month = {o.month}>
  <number of years = {o.numberOfYears}>
  <right now = {o.rightNow}>
  <years ago = {o.yearsAgo}>
  <loop range = {o.loopRange}>
)
    """.format(o=self)
