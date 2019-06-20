from BackToTheFuture import BackToTheFuture

greatScott = BackToTheFuture(year=2015, month=11, numberOfYears=30)
print(greatScott)

# go by month
print("going by month")
for pastDate in greatScott.byMonth():
  print(pastDate)

# go by year
print("going by year")
for pastDate in greatScott.byYear():
  print(pastDate)