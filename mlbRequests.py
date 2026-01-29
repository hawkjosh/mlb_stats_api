from datetime import datetime, timedelta
import json
from pytz import timezone as tz
import requests
import time
from functools import lru_cache

BASE_URL: str = "https://statsapi.mlb.com/api/v1"
CURR_SEASON: str = str(datetime.now().year)


def getData(endpoint: str, **kwargs) -> dict:
    queryParams: str = (
        f"&{'&'.join(f'{k}={v}' for k, v in kwargs.items())}" if kwargs else ""
    )
    url = f"{BASE_URL}/{endpoint}?sportId=1&season={CURR_SEASON}{queryParams}"
    return requests.get(url).json()


@lru_cache(maxsize=1)
def _teamsIndex() -> dict:
    index = {}
    for team in getData("teams").get("teams", []):
        aliases = {
            team.get("name"),
            team.get("teamName"),
            team.get("abbreviation"),
            team.get("shortName"),
            team.get("locationName"),
        }
        teamId = team.get("id")
        for alias in aliases:
            if alias:
                index[alias.lower()] = teamId
    return index

def getTeamId(teamName: str) -> int | None:
    return _teamsIndex().get(teamName.lower())


@lru_cache(maxsize=1)
def _playersIndex() -> dict:
    players = requests.get("https://statsapi.mlb.com/api/v1/sports/1/players").json().get("people", [])
    index = {}
    for player in players:
        aliases = {
            player.get("firstLastName"),
            player.get("lastFirstName"),
        }
        playerId = player.get("id")
        for alias in aliases:
            if alias:
                index[alias.lower()] = playerId
    return index

def getPlayerId(playerName: str) -> int | None:
    return _playersIndex().get(playerName.lower())


def getLogoUrl(teamId: int | None = None, teamName: str | None = None, **kwargs) -> str:
    teamId = teamId if teamId else getTeamId(teamName) if teamName else None
    logoType = kwargs.get("logoType", "cap")
    logoShade = kwargs.get("logoShade", "light")
    return f"https://www.mlbstatic.com/team-logos/team-{logoType}-on-{logoShade}/{teamId}.svg"


def getHeadshotUrl(playerId: int | None = None, playerName: str | None = None) -> str:
    playerId = playerId if playerId else getPlayerId(playerName) if playerName else None
    return f"https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{playerId}/headshot/67/current"


def main():
    # pass
    # print(getRequestUrl("teams", teamId=144))
    # print(makeAPICall("teams"))
    print(getTeamId("Braves"))


if __name__ == "__main__":
    main()
