Open access for all. If you like this code, consider donating.

# What is this:
This script produces basic financial modelling insights on E2's profitability.

# Why is this useful:
Forming insights about company health.

# Development Environment
1) Python 3.11.0
2) Windows 11

# Setup & Run Instructions
1) Install Python 3.11.0
2) [optional] Grab new Windows Terminal (https://apps.microsoft.com/detail/9n0dx20hk701?hl=en-gb&gl=GB)
3) Clone github repo
4) Setup Environment & Install Requirements
```
python -m venv venv
source
pip install -r requirements.txt
```
5) Run either via `python main.py` or `wt_run.py` if you have new Windows Terminal


# Tech Notes
**https://r.earth2.io/territory_releases?released=true&sort_by=votes_value&sort_dir=desc&page=1&perPage=12**
```json
{
    "data": [
        {
            "id": "EE-67",
            "type": "territoryRelease",
            "attributes": {
                "territoryCode": "EE-67",
                "territoryName": "Pärnu",
                "country": "EE",
                "countryName": "Estonia",
                "votesValue": 14549708,
                "votesT1": 64029,
                "votesT2": 126690,
                "votesEsnc": 13275968,
                "releaseAt": "2023-11-20T15:00:00.000Z",
                "center": [
                    24.5081751,
                    58.3835136
                ],
                "flag": null,
                "backgroundImage": null,
                "myVotesValue": null,
                "myVotesT1": null,
                "myVotesT2": null,
                "myVotesEsnc": null
            }
        },
        
        ...

        {
            "id": "US-NY",
            "type": "territoryRelease",
            "attributes": {
                "territoryCode": "US-NY",
                "territoryName": "New York",
                "country": "US",
                "countryName": "United States of America",
                "votesValue": 2893366,
                "votesT1": 30865,
                "votesT2": 134216,
                "votesEsnc": 1913636,
                "releaseAt": "2023-12-05T13:00:00.000Z",
                "center": [
                    -75.46524714683039,
                    42.751210955038
                ],
                "flag": null,
                "backgroundImage": null,
                "myVotesValue": null,
                "myVotesT1": null,
                "myVotesT2": null,
                "myVotesEsnc": null
            }
        }
    ],
    "meta": {
        "count": 121,
        "pages": 11,
        "nextLockTime": "2024-08-16T00:00:00.000Z",
        "myVotes": {
            "value": null,
            "t1": null,
            "t2": null,
            "esnc": null
        },
        "totalVotes": {
            "value": 24004342,
            "t1": 1012489,
            "t2": 2575501,
            "esnc": 1001947
        },
        "winningTerritoryCode": "HN-CR"
    }
}
```


**https://app.earth2.io/api/v2/**
```json
[
    {
        "countryCode": "BL",
        "countryFlag": "https://app-static.earth2.io/assets/flags/bl.png",
        "countryName": "Saint Barth\u00e9lemy",
        "percentIncrease": 480.0,
        "final": 0.58,
        "current": 0.58,
        "value": 0.58,
        "totalTilesSold": 176230,
        "promised_essence_balance": "Temporarily N/A",
        "landfield_tier": 1
    },
    
    ...

    {
        "countryCode": "FI",
        "countryFlag": "https://app-static.earth2.io/assets/flags/fi.png",
        "countryName": "Finland",
        "percentIncrease": 311.0,
        "final": 0.411,
        "current": 0.411,
        "value": 0.411,
        "totalTilesSold": 212259,
        "promised_essence_balance": "Temporarily N/A",
        "landfield_tier": 2
    }
]
```
