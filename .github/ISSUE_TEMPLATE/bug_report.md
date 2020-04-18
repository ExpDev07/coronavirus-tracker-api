---
name: Bug report
about: Create a report to help us improve
title: "[BUG]"
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is. Please include timestamps and HTTP status codes.
If possible include the [httpie](https://httpie.org/) or `curl` request and response.
Please include the verbose flag. `-v` 

**To Reproduce**
`httpie/curl` request to reproduce the behavior:
1. Getting Italy data at `v2/locations/IT` gives a 422.
2. Expected to same data as `/v2/locations?country_code=IT`
2. See httpie request & response below

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots or Requests**
If applicable, add screenshots or `httpie/curl`requests to help explain your problem.
```sh
 http GET https://coronavirus-tracker-api.herokuapp.com/v2/locations/IT -v                                                                                                                                                            
GET /v2/locations/IT HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: coronavirus-tracker-api.herokuapp.com
User-Agent: HTTPie/2.0.0



HTTP/1.1 422 Unprocessable Entity
Connection: keep-alive
Content-Length: 99
Content-Type: application/json
Date: Sat, 18 Apr 2020 12:50:29 GMT
Server: uvicorn
Via: 1.1 vegur

{
    "detail": [
        {
            "loc": [
                "path",
                "id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```


**Additional context**
Add any other context about the problem here.
Does the other instance at https://covid-tracker-us.herokuapp.com/ produce the same result?
