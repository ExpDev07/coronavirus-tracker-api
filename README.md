# coronavirus-tracker (API)

> This is a fast (< 200ms) and basic API for tracking development of the new coronavirus (2019-nCoV). It's written in python using 🍼 Flask.

## Endpoints

All requests must be made to the base url: ``https://coronavirus-tracker-api.herokuapp.com`` (e.g: https://coronavirus-tracker-api.herokuapp.com/all). You can try them out in your browser to further inspect responses.

Getting confirmed cases, deaths, and recoveries:
```http
GET /all
```
```json
{ "latest": { ... }, "confirmed": { ... }, "deaths": { ... }, "recovered": { ... } }
```

Getting just confirmed:
```http
GET /confirmed
```
```json
{ "latest": 42767, "locations": [ ... ] }
```

Getting just deaths:
```http
GET /deaths
```

Getting just recoveries:
```http
GET /recovered
```


## Data

The data is retrieved programatically and re-formatted from the [2019 Novel Coronavirus (nCoV) Data Repository, provided by JHU CCSE](https://github.com/CSSEGISandData/2019-nCoV).

## License

The data is available to the public strictly for educational and academic research purposes.

## Prerequisites

You will need the following things properly installed on your computer.

* [Python 3](https://www.python.org/downloads/) (with pip)
* [Flask](https://pypi.org/project/Flask/)
* [pipenv](https://pypi.org/project/pipenv/)

## Installation

* `git clone https://github.com/ExpDev07/coronavirus-tracker-api.git`
* `cd coronavirus-tracker-api`
* `pipenv shell`
* `pipenv install`

## Running / Development

* `flask run`
* Visit your app at [http://localhost:5000](http://localhost:5000).

### Running Tests

### Linting

### Building

### Deploying
