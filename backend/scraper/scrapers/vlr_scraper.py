import datetime
import time
from typing import List
from bs4 import BeautifulSoup
import pytz
import requests


BASE_URL = "https://www.vlr.gg"


class VLRClient:
    """Class to get URLs from VLR"""

    def __init__(self, sleep=1.0, max_retries=3, timeout=20.0):
        """Initializes a new VLRScraper Object

        Args:
            sleep (float, optional): Time to wait (in seconds) between requests. Defaults to 1.0.
            max_retries (int, optional): Max times to try fetching a url if it fails. Defaults to 3.
            timeout (float, optional): Max time to wait (in seconds) for a url before giving up. Defaults to 20.0.
        """
        self.session = requests.Session()
        self.sleep = sleep
        self.max_retries = max_retries
        self.timeout = timeout

    def get(self, url: str) -> BeautifulSoup:
        """Fetches a URL with custom constraints

        Args:
            url (str): URL to get

        Returns:
            BeautifulSoup: BeautifulSoup object with request content
        """
        for _ in range(self.max_retries):
            try:
                r = self.session.get(url, timeout=self.timeout)
                if r.status_code == 200:
                    time.sleep(self.sleep)
                    return BeautifulSoup(r.content, "html.parser")
            except Exception as e:
                print(f"Error fetching {url}: {e}")
            time.sleep(self.sleep)
        raise RuntimeError(f"Failed to fetch {url}")


def get_homepage_soup() -> BeautifulSoup:
    """Gets the soup for the VLR home page

    Returns:
        BeautifulSoup: BeautifulSoup object with the homepage content
    """
    client = VLRClient()
    return client.get(BASE_URL)


def extract_upcoming_match_urls(soup: BeautifulSoup) -> List[str]:
    """Gets the match URLs from the upcoming matches section.

    Returns:
        List[str]: a list of the URLs for the upcoming matches
    """
    anchors = soup.select(
        ".js-home-matches-upcoming .wf-module.wf-card.mod-home-matches a"
    )

    return [BASE_URL + "/" + a.get("href") for a in anchors]


def parse_event_page(soup: BeautifulSoup) -> dict:
    """Parses a VLR event page and returns structured event data.

    Args:
        soup (BeautifulSoup): BeautifulSoup object containing content for the event

    Returns:
        dict: returns a structured dict:
        {
            "name": str,                # the name of the event
            "stages": List[str]         # names of the stages in the event
            "stages_url": List[str]     # URL of the stages in the event
        }
    """
    event_name = soup.select_one(".event-desc-inner .wf-title").get_text(strip=True)
    event_stages = soup.select(".wf-subnav-item-title")
    event_stages_urls = soup.select(".wf-subnav.mod-dark a")
    for i in range(len(event_stages)):
        event_stages[i] = event_stages[i].get_text(strip=True)
        event_stages_urls[i] = BASE_URL + event_stages_urls[i].get("href")

    return {"name": event_name, "stages": event_stages, "stages_url": event_stages_urls}


def extract_match_urls_from_event(soup: BeautifulSoup) -> List[str]:
    """Gets all the matches (finished and upcoming) shown in an event

    Args:
        soup (BeautifulSoup): BeautifulSoup object containing content for the matches in an event

    Returns:
        List[str]: a list of the URLs for the matches in the event
    """
    anchors = soup.select(
        ".wf-card .wf-module-item.match-item.mod-color.mod-bg-after-blue.mod-first"
    )
    return [BASE_URL + a.get("href") for a in anchors]


def parse_match_page(soup: BeautifulSoup) -> dict:
    """Parses a VLR match page and returns structured match data.

    Args:
        soup (BeautifulSoup): BeautifulSoup object containing content for a match

    Returns:
        dict: Structured dict containing either one of two dicts if the match isn't finished:
        {
            "event": str,               # URL of the event
            "date": datetime,           # Match start time in UTC
            "team_1": str,              # URL of the first team
            "team_2": str,              # URL of the second team
            "finished": bool,           # whether the match is finished
        }
        
        or this dict if the match is finished:
        {
            "event": str,               # URL of the event
            "date": datetime,           # Match start time in UTC
            "team_1": str,              # URL of the first team
            "team_2": str,              # URL of the second team
            "finished": bool,           # whether the match is finished
            "team_1_match_score": int,  # maps won by the first team
            "team_2_match_score": int,  # maps won by the second team
            "maps_played": int,         # number of maps played
            "maps": List[dict]          # stats for each map
        }
        
        
        Each maps dict includes:
        {
            "team_1_score": int,        # rounds won in this map by the first team
            "team_2_score": int,        # rounds won in this map by the second team
            "map_played": str,          # which map was played
            "team_1_stats": List[dict]  # the stats for the first team (5 players)
            "team_2_stats": List[dict]  # the stats for the      the second team (5 players)
        }
        
        Each of the team_x_stats dict includes:
        {
            "player": str,              # URL of the player
            "kills": int,               # number of kills the player got
            "deaths": int,              # number of times the player died
            "assists": int,             # number of assists the player got
            "agent_played": str,        # the agent the player played
            "acs": int,                 # player's acs for this map
        }
    """
    event_url = soup.select_one(".match-header-super a").get("href")

    match_date = soup.select_one(".moment-tz-convert")
    eastern = pytz.timezone("America/New_York")
    match_date = datetime.datetime.strptime(
        match_date.get("data-utc-ts"), "%Y-%m-%d %H:%M:%S"
    )
    match_date = eastern.localize(match_date).astimezone(pytz.utc)

    team_urls = soup.select(".match-header-vs a")
    team_urls = [BASE_URL + a.get("href") for a in team_urls]

    is_finished = (
        soup.select_one(".match-header-vs-note").get_text(strip=True).lower() == "final"
    )

    if not is_finished:
        return {
            "event": event_url,
            "date": match_date,
            "team_1": team_urls[0],
            "team_2": team_urls[1],
            "finished": is_finished,
        }

    match_scores = soup.select(".match-header-vs-score .js-spoiler span")
    match_scores = [
        match_scores[0].get_text(strip=True),
        match_scores[2].get_text(strip=True),
    ]
    match_scores = [int(score) for score in match_scores]

    maps = soup.select(".vm-stats-container .vm-stats-game")
    for i in range(len(maps)):
        if maps[i].get("data-game-id") == "all":
            maps.pop(i)
            break
    maps_played = len(maps)

    map_data = []
    for map in maps:
        scores = map.select(".vm-stats-game-header .team .score")
        scores = [score.get_text(strip=True) for score in scores]
        map_played = (
            map.select_one(".vm-stats-game-header .map span")
            .get_text(strip=True)
            .replace("PICK", "")
        )

        stats = map.select("tbody")
        teams_stats = []
        for team in stats:
            players_stats = team.select("tr")
            team_stats = []
            for stat in players_stats:
                player = BASE_URL + stat.select_one(".mod-player a").get("href")
                agent = stat.select_one(".mod-agents img").get("title")
                acs = (
                    stat.select(".mod-stat")[1]
                    .select_one(".side.mod-side.mod-both")
                    .get_text(strip=True)
                )
                kills = stat.select_one(
                    ".mod-stat.mod-vlr-kills .side.mod-side.mod-both"
                ).get_text(strip=True)
                deaths = stat.select_one(
                    ".mod-stat.mod-vlr-deaths .side.mod-both"
                ).get_text(strip=True)
                assists = stat.select_one(
                    ".mod-stat.mod-vlr-assists .side.mod-both"
                ).get_text(strip=True)

                team_stats.append(
                    {
                        "player": player,
                        "kills": kills,
                        "deaths": deaths,
                        "assists": assists,
                        "agent_played": agent,
                        "acs": acs,
                    }
                )

            teams_stats.append(team_stats)

        map_data.append(
            {
                "team_1_score": scores[0],
                "team_2_score": scores[1],
                "map_played": map_played,
                "team_1_stats": teams_stats[0],
                "team_2_stats": teams_stats[1],
            }
        )

    return {
        "event": event_url,
        "date": match_date,
        "team_1": team_urls[0],
        "team_2": team_urls[1],
        "finished": is_finished,
        "team_1_match_score": match_scores[0],
        "team_2_match_score": match_scores[1],
        "maps_played": maps_played,
        "maps": map_data,
    }


client = VLRClient()

url = (
    BASE_URL
    + "/508828/gen-g-vs-global-esports-vct-2025-pacific-stage-2-w2/?game=all&tab=overview"
)
soup = client.get(url)

print(parse_match_page(soup))
