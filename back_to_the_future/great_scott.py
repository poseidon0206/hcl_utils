import sys

from BackToTheFuture import BackToTheFuture


if __name__ == "__main__":
  args = BackToTheFuture.parse(sys.argv[1:])
  great_scott = BackToTheFuture(
    year=args.year,
    month=args.month,
    number_of_years=args.number_of_years
  )
  print(great_scott)

  if args.monthly is True:
    print("going from {o.years_ago} to {o.right_now} by month:".format(o=great_scott))
    for past_date in great_scott.by_month():
      print(past_date)

  if args.annually is True:
    print("going from {o.years_ago} to {o.right_now} by year:".format(o=great_scott))
    for past_date in great_scott.by_year():
      print(past_date)
