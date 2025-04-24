import requests
from tqdm import tqdm
import json
from dataclasses import dataclass
from datetime import datetime

from crawl.get_cached import get_cached


@dataclass
class ReliefArticle:
    title: str
    body: str
    original_date: str


def get_reliefweb_data(country_id: int, year: int, month: int) -> list[ReliefArticle]:
    """
    Returns all reports for a given country and month from the ReliefWeb API.

    @param country_id: The ID of the country to get reports for. (i.e. 226 for Syria)
    """
    request = requests.post(
        "https://api.reliefweb.int/v1/reports?appname=rwint-user-0",
        data=json.dumps(
            {
                "offset": 0,
                "limit": 1000,  # limit of API: 1000
                "filter": {
                    "conditions": [
                        {
                            "field": "date.original",
                            "value": {
                                "from": f"{datetime(year=year, month=month, day=1).strftime('%Y-%m-%d')}T00:00:00+00:00",
                                "to": f"{datetime(year=year + ((month + 1) // 12), month=(month + 1) % 12, day=1).strftime('%Y-%m-%d')}T23:59:59+00:00",
                            },
                        },
                        {"field": "primary_country.id", "value": str(country_id)},
                    ],
                    "operator": "AND",
                },
                "preset": "latest",
                "profile": "list",
            }
        ),
    )
    if request.status_code != 200:
        raise Exception(f"Error: {request.status_code}")
    list_data = request.json()

    result = []
    for item in tqdm(list_data["data"], desc="Downloading reports"):
        article_data = json.loads(get_cached(item["href"]))
        try:
            result.append(
                ReliefArticle(
                    title=article_data["data"][0]["fields"]["title"],
                    body=article_data["data"][0]["fields"]["body"],
                    original_date=article_data["data"][0]["fields"]["date"]["original"],
                )
            )
        except KeyError:
            print(f"WARNING: Cannot parse article: {item['href']}")
    return result
