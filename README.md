# data visualization of COVID 19 pandemic in Ukraine

Scripts that visualize data from [analytic panels](https://covid19.gov.ua/analitichni-paneli-dashbordy) provided by Ukraine government


## requirements

- python `3.8`+


## how to use

- install pipenv
```
py -m pip install pipenv
```
- install dependencies
```
py -m pipenv install --dev
```
- run script
```
py -m pipenv run ./src/app.py --data PATH_TO_DATA_DIR
```


## data

Original files downloaded from [analytic panels provided by ukraine government](https://covid19.gov.ua/analitichni-paneli-dashbordy)

Table view of data placed here - https://cloud.phc.org.ua/index.php/s/Rz5Z37jBNLdFrJm

### raw data

Raw data stored in `.\data\raw` directory in CSV format, splitted by `;` with `win-1251` encoding

Format of data in files changed from time to time (todo: describe formats). Format used in latest files described here - `.\data\raw\headers.md`

### fixed data

- deleted headers
- changed encoding to `utf-8`
- deleted new lines in rows
- deleted empty rows
- deleted row with total calculations in data for `27.10.2020`
- aligned columns to latest format
- fixed `0-` values for `PCR Samples leftovers (all)` column


## notes

- [Understanding Antibody Testing for COVID-19](https://doi.org/10.1016/j.arth.2020.04.055)