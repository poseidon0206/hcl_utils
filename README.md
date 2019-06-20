# Hans' Utils

These are just some reusable tools that I wrote.

# BackToTheFuture.py
I started with BackToTheFuture.py one night and finished it next morning. I just wanted something to loop with when I do historical queries, like when I had to calculate monthly totals for each month. Then I’ll have to write this query 12 times:
```
SELECT SUM(cost) AS monthly_total FROM job_costs WHERE start LIKE ‘2018-06-%’
SELECT SUM(cost) AS monthly_total FROM job_costs WHERE start LIKE ‘2018-07-%’
SELECT SUM(cost) AS monthly_total FROM job_costs WHERE start LIKE ‘2018-08-%’
```
 
When I wanted to automate this, we will sure lapse into the next / previous year, of course we can solve that with simple if statements, but what if we want to go two years? Five years? Then I thought a more permanent solution would be a mathematical one.

With this class you can go back thousands of years faithfully. The class can support traversing **by month** and **by year** only. The feature to traverse by day is a bit too steep of an order at the moment.

## Sample Code
Consider the following code:
```python
From BackToTheFuture import BackToTheFuture
 
greatScott = BackToTheFuture(year=2019, month=6, numberOfYears=10)
for pastDate in greatScott.byMonth():
  print(pastDate)
``` 

will generate the following output:
```
2009-06-05
2009-07-05
2009-08-05
2009-09-05
2009-10-05
2009-11-05
2009-12-05
2010-01-05
…
…
…
2018-11-05
2018-12-05
2019-01-05
2019-02-05
2019-03-05
2019-04-05
2019-05-05
2019-06-05
``` 

# QRelease 
**QRelease** and **QRelease2** are basically the same thing. It just figures out the current release from the current date or any given date.

QRelease2 looks more graceful, and it supports any release interval as long as 12 is divisible by it: so intervals of 1, 2, 3, 4, 6 will all be supported.
