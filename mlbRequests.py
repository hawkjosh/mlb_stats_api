from datetime import datetime, timedelta
import json
from pytz import timezone as tz
import requests


BASE_URL: str = "https://statsapi.mlb.com/api/v1"
CURR_SEASON: int = datetime.now().year


def getRequestURL(endpoint: str, **kwargs) -> str:
    queryParams: str = (
        f"&{'&'.join(f'{k}={v}' for k, v in kwargs.items())}" if kwargs else ""
    )
    return f"{BASE_URL}/{endpoint}?sportId=1{queryParams}"



def makeAPICall(endpoint: str, **kwargs) -> dict:
    url = getRequestURL(endpoint, **kwargs)
    return requests.get(url).json()


def getTeamId(teamName: str, season: int = None) -> int:
    seasonYear = season or CURR_SEASON
    response = api.Team.teams(sportId=1, season=seasonYear)
    teamsData = response.json().get("teams", [])
    teamLookup = []
    for team in teamsData:
        namesList = [
            team.get("name").lower(),
            team.get("teamName").lower(),
            team.get("abbreviation").lower(),
            team.get("shortName").lower(),
            team.get("locationName").lower(),
        ]
        teamLookup.append(
            {
                "id": team.get("id"),
                "name": team.get("name"),
                "namesList": namesList,
            }
        )
    for team in teamLookup:
        if teamName.lower() in team.get("namesList", []):
            return team.get("id")
    return None


# print(getTeamId("Braves"))


def getRequestUrl(endpoint: str = "", pathParams: dict = None, **kwargs) -> str:
    baseUrl: str = "https://statsapi.mlb.com/api/v1"
    endpoints: list | None = (
        list(map(str.strip, endpoint.split(","))) if endpoint else None
    )
    mainEndpoint: str = f"/{endpoints[0]}" if endpoints else ""
    endpointBranches: str = (
        f"/{'/'.join(endpoints[1:])}" if endpoints and len(endpoints) > 1 else ""
    )
    pathParam1: str = (
        f"/{pathParams.get(list(pathParams.keys())[0])}" if pathParams else ""
    )
    pathParam2: str = (
        f"/{pathParams.get(list(pathParams.keys())[1])}"
        if pathParams and len(list(pathParams.keys())) > 1
        else ""
    )
    queryParams: str = (
        f"?{'&'.join(f'{k}={v}' for k, v in kwargs.items())}" if kwargs else ""
    )

    return f"{baseUrl}{mainEndpoint}{pathParam1}{endpointBranches}{pathParam2}{queryParams}"


def callStatsAPI(endpoint: str = "", pathParams: dict = None, **kwargs) -> dict:
    url: str = getRequestUrl(endpoint, pathParams, **kwargs)
    response: requests.Response = requests.get(url)
    data: dict = json.dumps(response.json(), indent=2)
    return data


def getLogoUrl(teamId: int, type: str = "cap", shade: str = "light") -> str:
    baseUrl = "https://www.mlbstatic.com/team-logos"
    return f"{baseUrl}/team-{type}-on-{shade}/{teamId}.svg"


def getHeadshotUrl(playerId: int) -> str:
    baseUrl = "https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people"
    return f"{baseUrl}/{playerId}/headshot/67/current"

# print(getLogoUrl(144))
# print(getHeadshotUrl(660670))


def main():
    pass



if __name__ == "__main__":
    # main()
    # team = makeAPICall("teams", teamIds=144)
    # print(json.dumps(team, indent=2))
    print(getRequestUrl("teams", teamId=144))