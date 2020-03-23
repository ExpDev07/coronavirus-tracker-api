## Coronavirus Tracker API
Provides up-to-date data about Coronavirus outbreak. Includes numbers about confirmed cases, deaths and recovered.
Support multiple data-sources.

![Travis build](https://api.travis-ci.com/ExpDev07/coronavirus-tracker-api.svg?branch=master)
[![License](https://img.shields.io/github/license/ExpDev07/coronavirus-tracker-api)](LICENSE.md)
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
[![GitHub stars](https://img.shields.io/github/stars/ExpDev07/coronavirus-tracker-api)](https://github.com/ExpDev07/coronavirus-tracker-api/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ExpDev07/coronavirus-tracker-api)](https://github.com/ExpDev07/coronavirus-tracker-api/network/members)
[![GitHub last commit](https://img.shields.io/github/last-commit/ExpDev07/coronavirus-tracker-api)](https://github.com/ExpDev07/coronavirus-tracker-api/commits/master)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/ExpDev07/coronavirus-tracker-api)](https://github.com/ExpDev07/coronavirus-tracker-api/pulls)
[![GitHub issues](https://img.shields.io/github/issues/ExpDev07/coronavirus-tracker-api)](https://github.com/ExpDev07/coronavirus-tracker-api/issues)
[![Tweet](https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2FExpDev07%2Fcoronavirus-tracker-api)](https://twitter.com/intent/tweet?text=COVID19%20Live%20Tracking%20API:%20&url=https%3A%2F%2Fgithub.com%2FExpDev07%2Fcoronavirus-tracker-api)

**Live global stats (provided by [fight-covid19/bagdes](https://github.com/fight-covid19/bagdes)) from this API:**

![Covid-19 Confirmed](https://covid19-badges.herokuapp.com/confirmed/latest)
![Covid-19 Recovered](https://covid19-badges.herokuapp.com/recovered/latest)
![Covid-19 Deaths](https://covid19-badges.herokuapp.com/deaths/latest)


## API Endpoints

All endpoints are located at ``coronavirus-tracker-api.herokuapp.com/v2/`` and are accessible via https. For instance: you can get data per location by using this URL: 
``https://coronavirus-tracker-api.herokuapp.com/v2/locations``

You can try to open the URL in your browser to further inspect the response.


#### Available data-sources:

Currently 2 different data-sources are available to retrieve the data:

* **jhu** - https://github.com/CSSEGISandData/COVID-19 - Worldwide Data repository operated by the Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE). 

* **csbs** - https://www.csbs.org/information-covid-19-coronavirus - U.S. County data that comes from the Conference of State Bank Supervisors.

__JHU__ data-source will be used as a default source if you don't specify a source parameter in your request.

### Latest Endpoint

Getting latest amount of total confirmed cases, deaths, and recoveries.

```http
GET /v2/latest
```

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

__Query String Parameters__
| Query string parameter | Description                                                                      | Type   |
| ---------------------- | -------------------------------------------------------------------------------- | ------ |
| source                 | The data-source where data will be retrieved from *(jhu/csbs)*. Default is *jhu* | String |

### Locations Endpoint

Getting latest amount of total confirmed cases, deaths, and recoveries per location. 

```http
GET /v2/locations/{locationId}
```

__Path Parameters__
| Path parameter | Required/Optional | Description                                                        | Type    |
| -------------- | ----------------- | ------------------------------------------------------------------ | ------- |
| locationId     | OPTIONAL          | The location id for which you want to call the locations Endpoint. | Integer |


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
    "province": "",
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

```http
GET /v2/locations
```

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
      "province": "",
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

__Query String Parameters__
| Query string parameter | Description                                                                                                                                      | Type    |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------- |
| source                 | The data-source where data will be retrieved from. __Value__ can be: __jhu/csbs__. __Default__ is __jhu__                                        | String  |
| country_code           | The ISO ([alpha-2 country_code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)) to the Country/Province for which you're calling the Endpoint | String  |
| timelines              | To set the visibility of timelines (*daily tracking*).__Value__ can be: __0/1__. __Default__ is __0__                                            | Integer |


__Response definitions__
| Response Item                                  | Description                                                                                                                          | Type    |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------- |
| {latest}                                       | The total amount of confirmed cases, deaths and recoveries for all the locations                                                     | Object  |
| {latest}/confirmed                             | The up-to-date total number of confirmed cases for all the locations within the data-source                                          | Integer |
| {latest}/deaths                                | The up-to-date total amount of deaths for all the locations within the data-source                                                   | Integer |
| {latest}/recovered                             | The up-to-date total amount of recovered for all the locations within the data-source                                                | Integer |
| {locations}                                    | The collection of locations contained within the  data-source                                                                        | Object  |
| {location}                                     | Information that identifies a location                                                                                               | Object  |
| {latest}                                       | The amount of confirmed cases, deaths and recovered related to the specific location                                                 | Object  |
| {locations}/{location}/{latest}/confirmed      | The up-to-date number of confirmed cases related to the specific location                                                            | Integer |
| {locations}/{location}/{latest}/deaths         | The up-to-date number of deaths related to the specific location                                                                     | Integer |
| {locations}/{location}/{latest}/deaths         | The up-to-date number of recovered related to the specific location                                                                  | Integer |
| {locations}/{location}/id                      | The location id. This id number is assigned to the location by the data-source.                                                      | Integer |
| {locations}/{location}/country                 | The Country name                                                                                                                     | String  |
| {locations}/{location}/country_code            | The ISO ([alpha-2 country_code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)) Country code for the location.                    | String  |
| {locations}/{location}/province                | The province where the location belongs to. (Used only for __csbs data-source__ of US locations. __Empty__ with __jhu data-source__. | String  |
| {locations}/{location}/{coordinates}/latitude  | The location latitude                                                                                                                | Float   |
| {locations}/{location}/{coordinates}/longitude | The location longitude                                                                                                               | Float   |


```http
GET /v2/locations?country_code=US
```

```http
GET /v2/locations?timelines=1
```

### Getting a specific location (includes timelines by default).


Exclude timelines.
```http
GET /v2/locations?timelines=0
```

### Getting US per county information.
```http
GET /v2/locations?source=csbs
```
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

## Wrappers

These are the available API wrappers created by the community. They are not necessarily maintained by any of this project's authors or contributors.

### PHP

* [CovidPHP by @o-ba](https://github.com/o-ba/covid-php).

### Golang

* [Go-corona by @itsksaurabh](https://github.com/itsksaurabh/go-corona).

### C#

* [CovidSharp by @Abdirahiim](https://github.com/Abdirahiim/covidtrackerapiwrapper).

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
    <td align="center"><a href="https://github.com/oliver-xapix-io"><img src="https://avatars0.githubusercontent.com/u/13470858?v=4" width="100px;" alt=""/><br /><sub><b>Oliver Thamm</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=oliver-xapix-io" title="Documentation">📖</a></td>
    <td align="center"><a href="https://maurom.dev"><img src="https://avatars1.githubusercontent.com/u/22800592?v=4" width="100px;" alt=""/><br /><sub><b>Mauro M.</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=MM-coder" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/JKSenthil"><img src="https://avatars2.githubusercontent.com/u/12533226?v=4" width="100px;" alt=""/><br /><sub><b>JKSenthil</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=JKSenthil" title="Code">💻</a> <a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=JKSenthil" title="Documentation">📖</a> <a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=JKSenthil" title="Tests">⚠️</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/SeanCena"><img src="https://avatars1.githubusercontent.com/u/17202203?v=4" width="100px;" alt=""/><br /><sub><b>SeanCena</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=SeanCena" title="Code">💻</a> <a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=SeanCena" title="Documentation">📖</a> <a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=SeanCena" title="Tests">⚠️</a></td>
    <td align="center"><a href="https://github.com/Abdirahiim"><img src="https://avatars0.githubusercontent.com/u/13730460?v=4" width="100px;" alt=""/><br /><sub><b>Abdirahiim Yassin </b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=Abdirahiim" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/kant"><img src="https://avatars1.githubusercontent.com/u/32717?v=4" width="100px;" alt=""/><br /><sub><b>Darío Hereñú</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=kant" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/o-ba"><img src="https://avatars1.githubusercontent.com/u/8812114?v=4" width="100px;" alt=""/><br /><sub><b>Oliver</b></sub></a><br /><a href="https://github.com/ExpDev07/coronavirus-tracker-api/commits?author=o-ba" title="Documentation">📖</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

## License

See [LICENSE.md](LICENSE.md) for the license. Please link to this repo somewhere in your project :).
