# Back To The Future

A small date-travel utility. The `BackToTheFuture` class takes a destined
year/month and a number of years to go back, computes the date that far in
the past, and can enumerate every stop on the way back to the destined time
either by month or by year.

Great Scott! 1.21 gigawatts!?

## Deployment

```bash
git clone git@github.com:poseidon0206/hcl_utils.git
cd hcl_utils/back_to_the_future
python3 -m venv .venv
source .venv/bin/activate
```

There are no third-party dependencies — only the Python standard library
(`argparse`, `datetime`) is used, so no `pip install` step is needed.
Python 3.6+ is required (f-strings).

## Config

There is no config file. The public API of the project-internal library
`BackToTheFuture.py` is what a caller configures:

| Name | Kind | Description |
|------|------|-------------|
| `BackToTheFuture(year=1985, month=11, number_of_years=30)` | class | Computes `right_now` (the destined date, always pinned to day 05 of the month) and `years_ago` (`number_of_years` earlier, including leap-day adjustment). |
| `by_year()` | generator method | Yields one `datetime.date` per year from the past date back to the destined date. |
| `by_month()` | generator method | Yields one `datetime.date` per month from the past date back to the destined date. |
| `parse(sys_args)` | static method | Parses CLI arguments (see below) and returns an `argparse.Namespace`. |

## Running the scripts

### great_scott.py

Sample script demonstrating the `BackToTheFuture` class. By default it
prints the constructed instance (destined date 1985-11-05 and the date 30
years earlier). With `--monthly` and/or `--annually` it also prints every
traversed date on the way back to the destined time.

| Argument | Default | Description |
|----------|---------|-------------|
| `-y`, `--year` | `1985` | The destined year. |
| `-m`, `--month` | `11` | The destined month. |
| `-n`, `--number-of-years` | `30` | The number of years to traverse. |
| `-l`, `--monthly` | off | Show the traversed months. |
| `-a`, `--annually` | off | Show the traversed years. |

Example:

```bash
$ python3 great_scott.py -y 1985 -m 11 -n 30 -a

BackToTheFuture(
  <year = 1985>
  <month = 11>
  <number of years = 30>
  <right now = 1985-11-05 00:00:00>
  <years ago = 1955-11-06 00:00:00>
  <loop range = 361>
)

going from 1955-11-06 00:00:00 to 1985-11-05 00:00:00 by year:
1955-11-05
1956-11-05
...
1985-11-05
```

Note: `test_round.py` is a legacy byte-identical copy of `great_scott.py`
and is not maintained.

## TO DO

- a method to come back by days.
