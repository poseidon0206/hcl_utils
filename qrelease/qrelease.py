from re import search
from tabulate import tabulate
from datetime import datetime


class QRelease:
  """
  QRelease: the MTC release class
  Args:
      args(list): the command line arguments.
      start(obj): a datetime object.
  Attributes:
      curRel(str): current release in YYYY.MM format.
      curShort(str): current release in YYMM format.
      curYear(str): current release year.
      curMth(str): current release month.
      prvRel(str): previous release in YYYY.MM format.
      prvShort(str): previous release in YYMM format.
      prvYear(str): previous release year.
      prvMth(str): previous release month.
      ppRel(str): two releases before in YYYY.MM format.
      ppShort(str): two releases before in YYMM format.
      ppYear(str): two releases before year.
      ppMth(str): two releases before month.
      nRel(str): next release in YYYY.MM format.
      nShort(str): next release in YYMM format.
      nYear(str): next release year.
      nMth(str): next release month.
  """

  def __init__(self, start=datetime.now(), args=None, monthly=False):
    """
    __init___: instantiate the class and generate the attributes on the fly.
    Args:
        args(list): the command line arguments.
        start(obj): a datetime object.
    Returns:
        None
    """
    if args and search("\d{4}.\d{2}", args):
      self.curYear, self.curMth = args.split(".")
    else:
      self.curYear = start.year
      self.curMth = start.month
    if monthly == True:
      self.relPeriod = 1
    else:
      self.relPeriod = 3
    self.curYear, self.curMth = self.getYearMonth(self.curYear, self.curMth)
    self.curRel, self.curShort = self.getTuple(self.curYear, self.curMth)

    # figure out the previous release
    pYear = int(self.curYear)
    # subtract the month by 3
    pMth = "%02d" % (int(self.curMth) - (1 * self.relPeriod))
    self.prvYear, self.prvMth = self.getYearMonth(pYear, pMth)
    self.prvRel, self.prvShort = self.getTuple(self.prvYear, self.prvMth)

    # two releases before
    ppYear = int(self.curYear)
    ppMth = "%02d" % (int(self.curMth) - (2 * self.relPeriod))
    self.ppYear, self.ppMth = self.getYearMonth(ppYear, ppMth)
    self.ppRel, self.ppShort = self.getTuple(self.ppYear, self.ppMth)

    # next release
    nYear = int(self.curYear)
    nMth = "%02d" % (int(self.curMth) + (1 * self.relPeriod))
    self.nYear, self.nMth = self.getYearMonth(nYear, nMth)
    self.nRel, self.nShort = self.getTuple(self.nYear, self.nMth)

  def getYearMonth(self, year, month):
    """
    getYearMonth: takes the given year and month and returns the current release year and month.
    Args:
        year(str): the year of the requested release.
        month(str): the month of the requested release.
    Returns:
        iYear(str): four-digit year.
        iMnth(str): two-digit month.
    """
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
    relMth = "%02d" % (iMth)
    return (iYear, relMth)

  def getTuple(self, year, month):
    """
    getTuple: takes the year and month and generate the YYYY.MM as well as the YYMM format for the release.
    Args:
        year(str): the year of the release.
        month(str): the month of the release.
    Returns:
        rel(str): the release number in YYYY.MM format.
        short(str): the release number in YYMM format.
    """
    rel = "%s.%s" % (year, month)
    short = "%s%s" % (str(year)[-2:], month)
    return (rel, short)

  def __repr__(self):
    headers = ["Item", "Release", "Abbr", "Year", "Month"]
    dispTable = []
    dispTable.append(["Current", self.curRel, self.curShort, self.curYear, self.curMth])
    dispTable.append(["Previous", self.prvRel, self.prvShort, self.prvYear, self.prvMth])
    dispTable.append(["2 rels back", self.ppRel, self.ppShort, self.ppYear, self.ppMth])
    dispTable.append(["Next", self.nRel, self.nShort, self.nYear, self.nMth])
    return tabulate(dispTable, headers=headers, tablefmt="psql")
