# Quarter Release

Release-calendar helpers. `QRelease` works out the current, previous,
two-back and next releases (quarterly by default, optionally monthly) and
prints them as a table. `QRelease2` does the same thing, just fancier: it
supports any release interval that divides 12 (1, 2, 3, 4 or 6 months) and
any number of previous/next releases.

## Deployment

```bash
git clone git@github.com:poseidon0206/hcl_utils.git
cd hcl_utils/qrelease
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Dependencies (pinned in `requirements.txt`): `python-dateutil`, `six`,
`tabulate`.

## Config

There is no config file. The public API of the two project-internal
libraries is what a caller configures:

### qrelease.py

| Name | Kind | Description |
|------|------|-------------|
| `QRelease(start=datetime.now(), args=None, monthly=False)` | class | Computes the current, previous, two-back and next releases from `start`. `args` may instead carry a `"YYYY.MM"` string to anchor the calculation; `monthly=True` uses a 1-month period instead of 3. |
| `curRel` / `prvRel` / `ppRel` / `nRel` | attributes | Release strings in `YYYY.MM` format (current / previous / two back / next); each also has `*Short` (`YYMM`), `*Year` and `*Mth` variants. |
| `repr(QRelease())` | repr | psql-style table of all four releases. |

### QRelease2.py

| Name | Kind | Description |
|------|------|-------------|
| `QRelease2(query_date=<today>, every=3, num_rels=2)` | class | Computes releases around `query_date` (`YYYY-MM-DD` string) with a release every `every` months, obtaining `num_rels` previous and next releases. |
| `current` / `prev_releases` / `next_releases` | attributes | The current release as a `Quarter`, and lists of `Quarter` objects for the previous/next releases. |
| `ghosts_of_christmas` | attribute | Sorted list of all release strings — past, present and future. |
| `Quarter(start_of_quarter)` | class | Strings for one release: `release` (`YYYY.MM`), `abbreviation` (`YYMM`), `folder_str` (`YYYY_MM`), plus `year` and `month`. |

## Running the scripts

### get_rels.py

Sample script demonstrating both classes. It takes no CLI arguments and
prints three demos: the `QRelease` table for the current date, a
`QRelease2` anchored at 2009-08-12 with a two-month release interval, and a
`QRelease2` with a six-month interval obtaining eight previous and next
releases.

```bash
$ python3 get_rels.py
+-------------+-----------+--------+--------+---------+
| Item        |   Release |   Abbr |   Year |   Month |
|-------------+-----------+--------+--------+---------|
| Current     |   2026.06 |   2606 |   2026 |      06 |
| Previous    |   2026.03 |   2603 |   2026 |      03 |
| 2 rels back |   2025.12 |   2512 |   2025 |      12 |
| Next        |   2026.09 |   2609 |   2026 |      09 |
+-------------+-----------+--------+--------+---------+

QRelease(
  <current =
  Quarter(
    <year = 2009>
    <month = 08>
    ...
```
