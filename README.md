<h1 align="center">
    Coronavirus Tracker API
</h1>

Provides up-to-date data about Coronavirus outbreak. Includes numbers about confirmed cases, deaths and recovered.
Support multiple data-sources.

![Travis build](https://api.travis-ci.com/ExpDev07/coronavirus-tracker-api.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/ExpDev07/coronavirus-tracker-api/badge.svg?branch=master)](https://coveralls.io/github/ExpDev07/coronavirus-tracker-api?branch=master)
[![License](https://img.shields.io/github/license/ExpDev07/coronavirus-tracker-api)](LICENSE.md)
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
[![GitHub stars](https://img.shields.io/github/stars/ExpDev07/coronavirus-tracker-api)](https://github.com/ExpDev07/coronavirus-tracker-api/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ExpDev07/coronavirus-tracker-api)](https://github.com/ExpDev07/coronavirus-tracker-api/network/members)
[![GitHub last commit](https://img.shields.io/github/last-commit/ExpDev07/coronavirus-tracker-api)](https://github.com/ExpDev07/coronavirus-tracker-api/commits/master)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/ExpDev07/coronavirus-tracker-api)](https://github.com/ExpDev07/coronavirus-tracker-api/pulls)
[![GitHub issues](https://img.shields.io/github/issues/ExpDev07/coronavirus-tracker-api)](https://github.com/ExpDev07/coronavirus-tracker-api/issues)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/ExpDev07/coronavirus-tracker-api.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ExpDev07/coronavirus-tracker-api/alerts/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tweet](https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2FExpDev07%2Fcoronavirus-tracker-api)](https://twitter.com/intent/tweet?text=COVID19%20Live%20Tracking%20API:%20&url=https%3A%2F%2Fgithub.com%2FExpDev07%2Fcoronavirus-tracker-api)

**Live global stats (provided by [fight-covid19/bagdes](https://github.com/fight-covid19/bagdes)) from this API:**

![Covid-19 Confirmed](https://covid19-badges.herokuapp.com/confirmed/latest)
![Covid-19 Recovered](https://covid19-badges.herokuapp.com/recovered/latest)
![Covid-19 Deaths](https://covid19-badges.herokuapp.com/deaths/latest)

## Recovered cases showing 0

**JHU (our main data provider) [no longer provides data for amount of recoveries](https://github.com/CSSEGISandData/COVID-19/issues/1250), and as a result, the API will be showing 0 for this statistic. Apolegies for any inconvenience. Hopefully we'll be able to find an alternative data-source that offers this.**

## Available data-sources:

Currently 2 different data-sources are available to retrieve the data:

* **jhu** - https://github.com/CSSEGISandData/COVID-19 - Worldwide Data repository operated by the Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE).

* **csbs** - https://www.csbs.org/information-covid-19-coronavirus - U.S. County data that comes from the Conference of State Bank Supervisors.

__jhu__ data-source will be used as a default source if you don't specify a *source parameter* in your request.

## API Reference

All endpoints are located at ``coronavirus-tracker-api.herokuapp.com/v2/`` and are accessible via https. For instance: you can get data per location by using this URL:
*[https://coronavirus-tracker-api.herokuapp.com/v2/locations](https://coronavirus-tracker-api.herokuapp.com/v2/locations)*

You can open the URL in your browser to further inspect the response. Or you can make this curl call in your terminal to see the prettified response:

```
curl https://coronavirus-tracker-api.herokuapp.com/v2/locations | json_pp
```

### Swagger/OpenAPI

Consume our API through [our super awesome and interactive SwaggerUI](https://coronavirus-tracker-api.herokuapp.com/) (on mobile, use the [mobile friendly ReDocs](https://coronavirus-tracker-api.herokuapp.com/docs) instead for the best experience).


The [OpenAPI](https://swagger.io/docs/specification/about/) json definition can be downloaded at https://coronavirus-tracker-api.herokuapp.com/openapi.json

## API Endpoints

### Sources Endpoint

Getting the data-sources that are currently available to Coronavirus Tracker API to retrieve the data of the pandemic.

```http
GET /v2/sources
```

__Sample response__
```json
{
    "sources": [
        "jhu",
        "csbs"
    ]
}
```

### Latest Endpoint

Getting latest amount of total confirmed cases, deaths, and recovered.

```http
GET /v2/latest
```

__Query String Parameters__
| __Query string parameter__ | __Description__                                                                  | __Type__ |
| -------------------------- | -------------------------------------------------------------------------------- | -------- |
| source                     | The data-source where data will be retrieved from *(jhu/csbs)*. Default is *jhu* | String   |

__Sample response__
```json
{
  "latest": {
    "confirmed": 197146,
    "deaths": 7905,
    "recovered": 80840
  }
}
```

### Locations Endpoint

Getting latest amount of confirmed cases, deaths, and recovered per location.

#### The Location Object
```http
GET /v2/locations/:id
```

__Path Parameters__
| __Path parameter__ | __Required/Optional__ | __Description__                                                                                                                                                          | __Type__ |
| ------------------ | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- |
| id                 | OPTIONAL              | The unique location id for which you want to call the Locations Endpoint. The list of valid location IDs (:id) can be found in the locations response: ``/v2/locations`` | Integer  |

__Query String Parameters__
| __Query string parameter__ | __Description__                                                                  | __Type__ |
| -------------------------- | -------------------------------------------------------------------------------- | -------- |
| source                     | The data-source where data will be retrieved from *(jhu/csbs)*. Default is *jhu* | String   |

#### Example Request
```http
GET /v2/locations/39
```

__Sample response__
```json
{
  "location": {
    "id": 39,
    "country": "Norway",
    "country_code": "NO",
    "country_population": 5009150,
    "province": "",
    "county": "",
    "last_updated": "2020-03-21T06:59:11.315422Z",
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

#### List of all locations
```http
GET /v2/locations
```

__Query String Parameters__
| __Query string parameter__ | __Description__                                                                                                                                  | __Type__ |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | -------- |
| source                     | The data-source where data will be retrieved from.<br>__Value__ can be: *jhu/csbs*. __Default__ is *jhu*                                         | String   |
| country_code               | The ISO ([alpha-2 country_code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)) to the Country/Province for which you're calling the Endpoint | String   |
| timelines                  | To set the visibility of timelines (*daily tracking*).<br>__Value__ can be: *0/1*. __Default__ is *0* (timelines are not visible)                | Integer  |

__Sample response__
```json
{
  "latest": {
    "confirmed": 272166,
    "deaths": 11299,
    "recovered": 87256
  },
  "locations": [
    {
      "id": 0,
      "country": "Thailand",
      "country_code": "TH",
      "country_population": 67089500,
      "province": "",
      "county": "",
      "last_updated": "2020-03-21T06:59:11.315422Z",
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
      "county": "",
      "last_updated": "2020-03-21T06:59:11.315422Z",
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

__Response definitions__
| __Response Item__                              | __Description__                                                                                                                                  | __Type__ |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | -------- |
| {latest}                                       | The total amount of confirmed cases, deaths and recovered for all the locations                                                                  | Object   |
| {latest}/confirmed                             | The up-to-date total number of confirmed cases for all the locations within the data-source                                                      | Integer  |
| {latest}/deaths                                | The up-to-date total amount of deaths for all the locations within the data-source                                                               | Integer  |
| {latest}/recovered                             | The up-to-date total amount of recovered for all the locations within the data-source                                                            | Integer  |
| {locations}                                    | The collection of locations contained within the  data-source                                                                                    | Object   |
| {location}                                     | Information that identifies a location                                                                                                           | Object   |
| {latest}                                       | The amount of confirmed cases, deaths and recovered related to the specific location                                                             | Object   |
| {locations}/{location}/{latest}/confirmed      | The up-to-date number of confirmed cases related to the specific location                                                                        | Integer  |
| {locations}/{location}/{latest}/deaths         | The up-to-date number of deaths related to the specific location                                                                                 | Integer  |
| {locations}/{location}/{latest}/recovered      | The up-to-date number of recovered related to the specific location                                                                              | Integer  |
| {locations}/{location}/id                      | The location id. This unique id is assigned to the location by the data-source.                                                                  | Integer  |
| {locations}/{location}/country                 | The Country name                                                                                                                                 | String   |
| {locations}/{location}/country_code            | The [ISO alpha-2 country_code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) Country code for the location.                                  | String   |
| {locations}/{location}/province                | The province where the location belongs to. (Used for US locations coming from __csbs data-source__.<br>__Empty__ when *jhu data-source* is used | String   |
| {locations}/{location}/{coordinates}/latitude  | The location latitude                                                                                                                            | Float    |
| {locations}/{location}/{coordinates}/longitude | The location longitude                                                                                                                           | Float    |


### Example Requests with parameters

__Parameter: country_code__

Getting data for the Country specified by the *country_code parameter*, in this case Italy - IT

```http
GET /v2/locations?country_code=IT
```

__Sample Response__
```json
{
  "latest": {
    "confirmed": 59138,
    "deaths": 5476,
    "recovered": 7024
  },
  "locations": [
    {
      "id": 16,
      "country": "Italy",
      "country_code": "IT",
      "country_population": 60340328,
      "province": "",
      "county": "",
      "last_updated": "2020-03-23T13:32:23.913872Z",
      "coordinates": {
          "latitude": "43",
          "longitude": "12"
      },
      "latest": {
          "confirmed": 59138,
          "deaths": 5476,
          "recovered": 7024
      }
    }
  ]
}
```

__Parameter: source__

Getting the data from the data-source specified by the *source parameter*, in this case [csbs](https://www.csbs.org/information-covid-19-coronavirus)


```http
GET /v2/locations?source=csbs
```

__Sample Response__
```json
{
  "latest": {
    "confirmed": 7596,
    "deaths": 43,
    "recovered": 0
  },
  "locations": [
    {
      "id": 0,
      "country": "US",
      "country_code": "US",
      "country_population": 310232863,
      "province": "New York",
      "state": "New York",
      "county": "New York",
      "last_updated": "2020-03-21T14:00:00Z",
      "coordinates": {
        "latitude": 40.71455,
        "longitude": -74.00714
      },
      "latest": {
        "confirmed": 6211,
        "deaths": 43,
        "recovered": 0
      }
    },
    {
      "id": 1,
      "country": "US",
      "country_code": "US",
      "country_population": 310232863,
      "province": "New York",
      "state": "New York",
      "county": "Westchester",
      "last_updated": "2020-03-21T14:00:00Z",
      "coordinates": {
        "latitude": 41.16319759,
        "longitude": -73.7560629
      },
      "latest": {
        "confirmed": 1385,
        "deaths": 0,
        "recovered": 0
      },
    }
  ]
}
```

__Parameter: timelines__

Getting the data for all the locations including the daily tracking of confirmed cases, deaths and recovered per location.

```http
GET /v2/locations?timelines=1
```
Explore the response by opening the URL in your browser [https://coronavirus-tracker-api.herokuapp.com/v2/locations?timelines=1](https://coronavirus-tracker-api.herokuapp.com/v2/locations?timelines=1) or make the following curl call in your terminal:

```
curl https://coronavirus-tracker-api.herokuapp.com/v2/locations?timelines=1 | json_pp
```

__NOTE:__ Timelines tracking starts from day 22nd January 2020 and ends to the last available day in the data-source.



## Wrappers

These are the available API wrappers created by the community. They are not necessarily maintained by any of this project's authors or contributors.

### PHP

* [CovidPHP by @o-ba](https://github.com/o-ba/covid-php).

### Golang

* [Go-corona by @itsksaurabh](https://github.com/itsksaurabh/go-corona).

### C#

* [CovidSharp by @Abdirahiim](https://github.com/Abdirahiim/covidtrackerapiwrapper)
* [Covid19Tracker.NET by @egbakou](https://github.com/egbakou/Covid19Tracker.NET)

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
* [pipenv](https://pypi.org/project/pipenv/)

## Installation

* `git clone https://github.com/ExpDev07/coronavirus-tracker-api.git`
* `cd coronavirus-tracker-api`

1. Make sure you have [`python3.8` installed and on your `PATH`](https://docs.python-guide.org/starting/installation/).
2. [Install the `pipenv` dependency manager](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)
   *  with [pipx](https://pipxproject.github.io/pipx/) `$ pipx install pipenv`
   * with [Homebrew/Linuxbrew](https://pipenv.readthedocs.io/en/latest/install/#homebrew-installation-of-pipenv) `$ brew install pipenv`
   * with [pip/pip3 directly](https://pipenv.readthedocs.io/en/latest/install/#pragmatic-installation-of-pipenv) `$ pip install --user pipenv`
3. Create virtual environment and install all dependencies `$ pipenv sync --dev`
4. Activate/enter the virtual environment `$ pipenv shell`

And don't despair if don't get the python setup working on the first try. No one did. Guido got pretty close... once. But that's another story. Good luck.

## Running / Development

* `pipenv run dev`
* Visit your app at [http://localhost:8000](http://localhost:8000).

### Running Tests
> [pytest](https://docs.pytest.org/en/latest/)

```bash
pipenv run test
```


### Linting
> [pylint](https://www.pylint.org/)

```bash
pipenv run lint
```

### Formatting
> [black](https://black.readthedocs.io/en/stable/)

```bash
pipenv run fmt
```

### Update requirements files

```bash
invoke generate-reqs
```

[Pipfile.lock](./Pipfile.lock) will be automatically updated during `pipenv install`.

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
    <td align="center"><a href="https://github.com/oliver-xapix-io"><img src="https://avatars0.githubusercontent.com/u/13470858?v=4" width="100px;" alt=""/><br /><sub><b>Oliver Thamm</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=oliver-xapix-io" title="Documentation">📖</a></td>
    <td align="center"><a href="https://maurom.dev"><img src="https://avatars1.githubusercontent.com/u/22800592?v=4" width="100px;" alt=""/><br /><sub><b>Mauro M.</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=MM-coder" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/JKSenthil"><img src="https://avatars2.githubusercontent.com/u/12533226?v=4" width="100px;" alt=""/><br /><sub><b>JKSenthil</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=JKSenthil" title="Code">💻</a> <a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=JKSenthil" title="Documentation">📖</a> <a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=JKSenthil" title="Tests">⚠️</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/SeanCena"><img src="https://avatars1.githubusercontent.com/u/17202203?v=4" width="100px;" alt=""/><br /><sub><b>SeanCena</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=SeanCena" title="Code">💻</a> <a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=SeanCena" title="Documentation">📖</a> <a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=SeanCena" title="Tests">⚠️</a></td>
    <td align="center"><a href="https://github.com/Abdirahiim"><img src="https://avatars0.githubusercontent.com/u/13730460?v=4" width="100px;" alt=""/><br /><sub><b>Abdirahiim Yassin </b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=Abdirahiim" title="Documentation">📖</a> <a href="#tool-Abdirahiim" title="Tools">🔧</a> <a href="#platform-Abdirahiim" title="Packaging/porting to new platform">📦</a></td>
    <td align="center"><a href="https://github.com/kant"><img src="https://avatars1.githubusercontent.com/u/32717?v=4" width="100px;" alt=""/><br /><sub><b>Darío Hereñú</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=kant" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/o-ba"><img src="https://avatars1.githubusercontent.com/u/8812114?v=4" width="100px;" alt=""/><br /><sub><b>Oliver</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=o-ba" title="Documentation">📖</a></td>
    <td align="center"><a href="http://www.carmelagreco.dev"><img src="https://avatars0.githubusercontent.com/u/5394906?v=4" width="100px;" alt=""/><br /><sub><b>carmelag</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=carmelag" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/Kilo59"><img src="https://avatars3.githubusercontent.com/u/13108583?v=4" width="100px;" alt=""/><br /><sub><b>Gabriel</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=Kilo59" title="Code">💻</a> <a href="#infra-Kilo59" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=Kilo59" title="Tests">⚠️</a> <a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=Kilo59" title="Documentation">📖</a></td>
    <td align="center"><a href="https://lioncoding.com"><img src="https://avatars0.githubusercontent.com/u/26142591?v=4" width="100px;" alt=""/><br /><sub><b>Kodjo Laurent Egbakou</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=egbakou" title="Documentation">📖</a> <a href="#tool-egbakou" title="Tools">🔧</a> <a href="#platform-egbakou" title="Packaging/porting to new platform">📦</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/Turreted"><img src="https://avatars2.githubusercontent.com/u/41593269?v=4" width="100px;" alt=""/><br /><sub><b>Turreted</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=Turreted" title="Code">💻</a></td>
    <td align="center"><a href="http://ibtida.me"><img src="https://avatars1.githubusercontent.com/u/33792969?v=4" width="100px;" alt=""/><br /><sub><b>Ibtida Bhuiyan</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=ibhuiyan17" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/james-gray"><img src="https://avatars1.githubusercontent.com/u/2904597?v=4" width="100px;" alt=""/><br /><sub><b>James Gray</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=james-gray" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

## License

See [LICENSE.md](LICENSE.md) for the license. Please link to this repo somewhere in your project :).
