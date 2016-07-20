#pokestop

Find nearby Pokéstops

##Installation

This utility depends on the Python `requests` library. To install:

```
sudo pip install requests
```

##Usage

```
usage: python pokestop.py [-h] [--latitude LATITUDE] [--longitude LONGITUDE]
                          [--guid GUID] [--min MINIMUM] [--max MAXIMUM]
                          [--order {ASC,DESC}] [--limit LIMIT]
                          [--offset OFFSET] [--SACSID SACSID]
                          [--csrftoken CSRFTOKEN] [--save]

Find nearby Pokéstops

optional arguments:
  -h, --help             show this help message and exit
  --latitude LATITUDE    Coordinate latitude
  --longitude LONGITUDE  Coordinate longitude
  --guid GUID            Pokéstop ID
  --min MINIMUM          Minimum distance (meters)
  --max MAXIMUM          Maximum distance (meters)
  --order {ASC,DESC}     Results order
  --limit LIMIT          Results limit
  --offset OFFSET        Results offset
  --SACSID SACSID        SACSID cookie
  --csrftoken CSRFTOKEN  csrftoken cookie
  --save                 Save cookies to ~/.pokestop
```

##Schema

Results are returned in JSON. Here is the format for a single Pokéstop entity:

```
{
    "distance": <distance (meters)>,
    "name": "<name of Pokéstop>",
    "bearing": <bearing from origin to Pokéstop (degrees)>,
    "latitude": <latitude coordinate>,
    "image": "<image of Pokéstop>",
    "guid": "<unique identifier of Pokéstop>",
    "compass": "<compass direction to Pokéstop>",
    "longitude": <longitude coordinate>
}
```

When several entities are returned, they come back in an array of entities.

##Example

To find the Pokéstops within 20 meters of the center of Times Square in New York City:

```
python pokestop.py --latitude 40.758903 --longitude -73.985131 --max 20
```

Ouput:

```json
[
    {
        "distance": 17, 
        "name": "George M. Cohan Statue at Times Square", 
        "bearing": 182, 
        "latitude": 40.758746, 
        "image": "http://www.panoramio.com/photos/small/24779431.jpg", 
        "guid": "f51cc4736b2042549a8a9cf086e50d44.12", 
        "compass": "S", 
        "longitude": -73.985138
    }, 
    {
        "distance": 20, 
        "name": "Francis Patrick Duffy (1871 - 1932)", 
        "bearing": 43, 
        "latitude": 40.759055, 
        "image": "http://www.panoramio.com/photos/small/80872997.jpg", 
        "guid": "9851cb13578d42f6bfa15c5e6f31919a.12", 
        "compass": "NE", 
        "longitude": -73.984988
    }
]
```

##Setup

If not set up correctly, you may get the following alert:

```
Log into https://www.ingress.com/intel and copy the following cookies:
  SACSID
  csrftoken

For more information, visit https://github.com/kevinselwyn/pokestop
```

You need to collect some cookies from [https://www.ingress.com/intel](https://www.ingress.com/intel) to proceed. Follow these steps:

1. Navigate to [https://www.ingress.com/intel](https://www.ingress.com/intel)
2. Log in with your Google account
3. Gather the `SACSID` and `csrftoken` cookies

To gather cookies, you will have the greatest success with a cookie viewer plugin for your browser.

After you gather the cookies, you have several options:

1. Include each on the commandline using the `--SACSID` and `--csrftoken` flags (these will have to be included on every run)
2. Place them in a JSON-formatted file named `~/.pokestop` (ex: `{"SACSID":"<SACSID cookie>","csrftoken":"<csrftoken cookie>"}`)
3. Place them in the `pokestop.py` file itself in the `COOKIES` constant

Note: If you choose Option 1 (command-line arguments), you can add the `--save` flag to save them to a `~/.pokestop` file

##API

To start locally:

```
python api.py --port 8000
```

You may also deploy to Heroku to set up your own REST API for easy web access to all Pokéstops.

Follow the steps on Heroku's website [here](https://devcenter.heroku.com/articles/git) to deploy.

API info:

| Endpoint  | Notes                                               |
|-----------|-----------------------------------------------------|
| /nearby   | Find nearby Pokéstops given a lat/lng               |
| /pokestop | Get information on a specific Pokéstop given a guid |

All call require `SACSID` and `csrftoken` (can be gathered by following the instructions in the Setup section above).

`/nearby` requires `latitude` and `longitude`

`/pokestop` requires `guid`

Here are all the fields that can be used (same functions/explanations as the Usage section above):

| Field     |
|-----------|
| SACSID    |
| csrftoken |
| guid      |
| latitude  |
| longitude |
| minimum   |
| maximum   |
| order     |
| limit     |

Example API call:

```
curl -X POST -H "Content-Type: application/json" -d '{
    "latitude": "40.758903",
    "longitude": "-73.985131",
    "max": "20",
    "SACSID": "<SACSID cookie>",
    "csrftoken": "<csrftoken cookie>"
}' "http://app-name-123.herokuapp.com/nearby"
```

This will yield the same output as in the Example section above.

##Disclaimer

These may or may not violate some Terms of Service for Niantic Lab's Ingress and Pokémon GO. Use at your own risk.

* [Ingress Terms of Service](https://www.nianticlabs.com/terms)
* [Pokémon GO Terms of Service](https://www.nianticlabs.com/terms/pokemongo/en) (page down as of writing)