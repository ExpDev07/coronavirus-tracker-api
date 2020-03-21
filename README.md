# coronavirus-tracker (API)

> This is a fast (< 200ms) and basic API for tracking development of the new coronavirus (COVID-19, SARS-CoV-2). It's written in python using 🍼 Flask.

![Travis build](https://api.travis-ci.com/ExpDev07/coronavirus-tracker-api.svg?branch=master)
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
![GitHub stars](https://img.shields.io/github/stars/ExpDev07/coronavirus-tracker-api)
![GitHub forks](https://img.shields.io/github/forks/ExpDev07/coronavirus-tracker-api)
![GitHub last commit](https://img.shields.io/github/last-commit/ExpDev07/coronavirus-tracker-api)
![GitHub pull requests](https://img.shields.io/github/issues-pr/ExpDev07/coronavirus-tracker-api)
![GitHub issues](https://img.shields.io/github/issues/ExpDev07/coronavirus-tracker-api)
[![Tweet](https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2FExpDev07%2Fcoronavirus-tracker-api)](https://twitter.com/intent/tweet?text=COVID19%20Live%20Tracking%20API:%20&url=https%3A%2F%2Fgithub.com%2FExpDev07%2Fcoronavirus-tracker-api)

## Endpoints

All requests must be made to the base url: ``https://coronavirus-tracker-api.herokuapp.com/v2/`` (e.g: https://coronavirus-tracker-api.herokuapp.com/v2/locations). You can try them out in your browser to further inspect responses.

### Getting latest amount of total confirmed cases, deaths, and recoveries.
```http
GET /v2/latest
```
```json
{
  "latest": {
    "confirmed": 197146,
    "deaths": 7905,
    "recovered": 80840
  }
}
```

### Getting all locations.
```http
GET /v2/locations
```
```json
{
  "locations": [
    {
      "id": 0,
      "country": "Thailand",
      "country_code": "TH",
      "province": "",
      "coordinates": {
        "latitude": "15",
        "longitude": "101"
      },
      "latest": {
        "confirmed": 177,
        "deaths": 1,
        "recovered": 41
      }
    },
    {
      "id": 39,
      "country": "Norway",
      "country_code": "NO",
      "province": "",
      "coordinates": {
        "latitude": "60.472",
        "longitude": "8.4689"
      },
      "latest": {
        "confirmed": 1463,
        "deaths": 3,
        "recovered": 1
      }
    }
  ]
}
```

Additionally, you can also filter by country ([alpha-2 country_code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)).
```http
GET /v2/locations?country_code=US
```

Include timelines.
```http
GET /v2/locations?timelines=1
```

### Getting a specific location (includes timelines by default).
```http
GET /v2/locations/:id
```
```json
{
  "location": {
    "id": 39,
    "country": "Norway",
    "country_code": "NO",
    "province": "",
    "coordinates": { },
    "latest": { },
    "timelines": {
      "confirmed": {
        "latest": 1463,
        "timeline": {
          "2020-03-16T00:00:00Z": 1333,
          "2020-03-17T00:00:00Z": 1463
        }
      },
      "deaths": { },
      "recovered": { }
    }
  }
}
```

Exclude timelines.
```http
GET /v2/locations?timelines=0
```

## Data

The data comes from the [2019 Novel Coronavirus (nCoV) Data Repository, provided
by JHU CCSE](https://github.com/CSSEGISandData/2019-nCoV). It is
programmatically retrieved, re-formatted and stored in the cache for one hour.

## Wrappers

These are the available API wrappers created by the community. They are not necessarily maintained by any of this project's authors or contributors.

### C#

* [Coronavirus tracker API Wrapper by @Abdirahiim](https://github.com/Abdirahiim/covidtrackerapiwrapper).

### Python

* [COVID19Py by @Kamaropoulos](https://github.com/Kamaropoulos/COVID19Py).

### Java

* [Coronavirus by @mew](https://github.com/mew/Coronavirus).

### Node.js

* [jhucsse.covid by @Sem1084](https://www.npmjs.com/package/jhucsse.covid).

### Ruby

* [covid19-data-ruby by @jaerodyne](https://github.com/jaerodyne/covid19-data-ruby).

### Lua

* [lua-covid-data by @imolein](https://codeberg.org/imo/lua-covid-data).

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

* `make test`

### Linting

* `make lint`

### Building

### Deploying

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/ExpDev07"><img src="https://avatars3.githubusercontent.com/u/10024730?v=4" width="100px;" alt=""/><br /><sub><b>ExpDev</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=ExpDev07" title="Code">💻</a> <a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=ExpDev07" title="Documentation">📖</a> <a href="#maintenance-ExpDev07" title="Maintenance">🚧</a></td>
    <td align="center"><a href="https://github.com/bjarkimg"><img src="https://avatars2.githubusercontent.com/u/1289419?v=4" width="100px;" alt=""/><br /><sub><b>bjarkimg</b></sub></a><br /><a href="#question-bjarkimg" title="Answering Questions">💬</a></td>
    <td align="center"><a href="https://github.com/Bost"><img src="https://avatars0.githubusercontent.com/u/1174677?v=4" width="100px;" alt=""/><br /><sub><b>Bost</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=Bost" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/gribok"><img src="https://avatars1.githubusercontent.com/u/40306040?v=4" width="100px;" alt=""/><br /><sub><b>GRIBOK</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=gribok" title="Code">💻</a> <a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=gribok" title="Tests">⚠️</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

## License

The data is available to the public strictly for educational and academic research purposes. Please link to this repo somewhere in your project :).
