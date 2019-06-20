import sys

from BackToTheFuture import BackToTheFuture


if __name__ == "__main__":
  args = BackToTheFuture.parse(sys.argv[1:])
  greatScott = BackToTheFuture(
    year=args.year,
    month=args.month,
    numberOfYears=args.number_of_years
  )
  print(greatScott)

  if args.monthly is True:
    print("going from {o.yearsAgo} to {o.rightNow} by month:".format(o=greatScott))
    for pastDate in greatScott.byMonth():
      print(pastDate)

  if args.annually is True:
    print("going from {o.yearsAgo} to {o.rightNow} by year:".format(o=greatScott))
    for pastDate in greatScott.byYear():
      print(pastDate)
