from datetime import datetime, timedelta, tzinfo
import json
from pymlb_statsapi import api as mlb
from pytz import timezone as tz
import requests

# def formatShortDate(date: str, includeYear: bool = False) -> str:
#     dateObj = datetime.strptime(date, "%Y-%m-%d")
#     if includeYear:
#         return dateObj.strftime("%a, %#m/%#d/%y")
#     return dateObj.strftime("%a, %#m/%#d")


# def formatLongDate(date: str, includeYear: bool = False, useTZ: bool = False) -> str:
#     dateObj = (
#         datetime.fromisoformat(date.replace("Z", "+00:00"))
#         .astimezone(tz('US/Eastern'))
#     ) if useTZ else datetime.fromisoformat(date.replace("Z", "+00:00"))
#     if includeYear:
#         return dateObj.strftime("%b %#d, %Y, %#I:%M %p")
#     return dateObj.strftime("%b %#d, %#I:%M %p")


# hydrations = [
#     "previousSchedule",
#     "nextSchedule",
#     "venue",
#     "springVenue",
#     "social",
#     "deviceProperties",
#     "game(promotions)",
#     "game(atBatPromotions)",
#     "game(tickets)",
#     "game(atBatTickets)",
#     "game(sponsorships)",
#     "league",
#     "person",
#     "sport",
#     "standings",
#     "division",
#     "xrefId",
#     "location"
# ]
# response = requests.get("https://statsapi.mlb.com/api/v1/teams/144")
# # response = requests.get(f"https://statsapi.mlb.com/api/v1/teams/144?hydrate={','.join(hydrations[0:3])}")
# print(json.dumps(response.json().get("teams", []), indent=2))

# for hydration in hydrations:
#     response = requests.get(f"https://statsapi.mlb.com/api/v1/teams/144?hydrate={hydration},")
#     print(f"Hydration: {hydration}")
#     print(json.dumps(response.json().get("teams", []), indent=2))
#     print("\n\n")

# BASE_URL: str = "https://statsapi.mlb.com/api/v1"


BASE_URL: str = "https://statsapi.mlb.com/api/v1"
ENDPOINTS: dict = {
    "divisions": {
        "url": BASE_URL + "/divisions",
        "pathParams": [],
        "queryParams": [
            {"paramName": "divisionId", "isRequired": False},
            {"paramName": "leagueId", "isRequired": False},
            {"paramName": "season", "isRequired": False},
            {"paramName": "sportId", "isRequired": False},
        ],
    },
    "game": {
        "url": BASE_URL + "/game/{gamePk}/feed/live",
        "pathParams": [
            {"paramName": "gamePk", "isRequired": True},
        ],
        "queryParams": [
            {"paramName": "timecode", "isRequired": False},
            {"paramName": "hydrate", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "gameBoxscore": {
        "url": BASE_URL + "/game/{gamePk}/boxscore",
        "pathParams": [
            {"paramName": "gamePk", "isRequired": True},
        ],
        "queryParams": [
            {"paramName": "timecode", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "gameLinescore": {
        "url": BASE_URL + "/game/{gamePk}/linescore",
        "pathParams": [
            {"paramName": "gamePk", "isRequired": True},
        ],
        "queryParams": [
            {"paramName": "timecode", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "gamePlayByPlay": {
        "url": BASE_URL + "/game/{gamePk}/playByPlay",
        "pathParams": [
            {"paramName": "gamePk", "isRequired": True},
        ],
        "queryParams": [
            {"paramName": "timecode", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "league": {
        "url": BASE_URL + "/league",
        "pathParams": [],
        "queryParams": [
            {"paramName": "leagueIds", "isRequired": True},
            {"paramName": "sportId", "isRequired": True},
            {"paramName": "seasons", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "people": {
        "url": BASE_URL + "/people",
        "pathParams": [],
        "queryParams": [
            {"paramName": "personIds", "isRequired": True},
            {"paramName": "hydrate", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "person": {
        "url": BASE_URL + "/people/{personId}",
        "pathParams": [
            {"paramName": "personId", "isRequired": True},
        ],
        "queryParams": [
            {"paramName": "hydrate", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "personStats": {
        "url": BASE_URL + "/people/{personId}/stats/game/{gamePk}",
        "pathParams": [
            {"paramName": "gamePk", "isRequired": True},
            {"paramName": "personId", "isRequired": True},
        ],
        "queryParams": [
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "jobs": {
        "url": BASE_URL + "/jobs",
        "pathParams": [],
        "queryParams": [
            {"paramName": "jobType", "isRequired": True},
            {"paramName": "date", "isRequired": False},
            {"paramName": "sportId", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "schedule": {
        "url": BASE_URL + "/schedule",
        "pathParams": [],
        "queryParams": [
            {"paramName": "gamePk", "isRequired": True},
            {"paramName": "gamePks", "isRequired": True},
            {"paramName": "sportId", "isRequired": True},
            {"paramName": "date", "isRequired": False},
            {"paramName": "endDate", "isRequired": False},
            {"paramName": "eventTypes", "isRequired": False},
            {"paramName": "gameTypes", "isRequired": False},
            {"paramName": "leagueId", "isRequired": False},
            {"paramName": "opponentId", "isRequired": False},
            {"paramName": "scheduleType", "isRequired": False},
            {"paramName": "season", "isRequired": False},
            {"paramName": "startDate", "isRequired": False},
            {"paramName": "teamId", "isRequired": False},
            {"paramName": "venueIds", "isRequired": False},
            {"paramName": "hydrate", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "seasons": {
        "url": BASE_URL + "/seasons{all}",
        "pathParams": [{"paramName": "all", "isRequired": False}],
        "queryParams": [
            {"paramName": "divisionId", "isRequired": True},
            {"paramName": "leagueId", "isRequired": True},
            {"paramName": "sportId", "isRequired": True},
            {"paramName": "season", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "season": {
        "url": BASE_URL + "/seasons/{seasonId}",
        "pathParams": [{"paramName": "seasonId", "isRequired": True}],
        "queryParams": [
            {"paramName": "sportId", "isRequired": True},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "sports": {
        "url": BASE_URL + "/sports",
        "pathParams": [],
        "queryParams": [
            {"paramName": "sportId", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "sportsPlayers": {
        "url": BASE_URL + "/sports/{sportId}/players",
        "pathParams": [{"paramName": "sportId", "isRequired": True}],
        "queryParams": [
            {"paramName": "season", "isRequired": True},
            {"paramName": "gameType", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "standings": {
        "url": BASE_URL + "/standings",
        "pathParams": [],
        "queryParams": [
            {"paramName": "leagueId", "isRequired": True},
            {"paramName": "date", "isRequired": False},
            {"paramName": "season", "isRequired": False},
            {"paramName": "standingsTypes", "isRequired": False},
            {"paramName": "hydrate", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "stats": {
        "url": BASE_URL + "/stats",
        "pathParams": [],
        "queryParams": [
            {"paramName": "group", "isRequired": True},
            {"paramName": "stats", "isRequired": True},
            {"paramName": "endDate", "isRequired": False},
            {"paramName": "gameType", "isRequired": False},
            {"paramName": "leagueId", "isRequired": False},
            {"paramName": "limit", "isRequired": False},
            {"paramName": "metrics", "isRequired": False},
            {"paramName": "offset", "isRequired": False},
            {"paramName": "order", "isRequired": False},
            {"paramName": "personId", "isRequired": False},
            {"paramName": "playerPool", "isRequired": False},
            {"paramName": "position", "isRequired": False},
            {"paramName": "season", "isRequired": False},
            {"paramName": "sortStat", "isRequired": False},
            {"paramName": "sportIds", "isRequired": False},
            {"paramName": "startDate", "isRequired": False},
            {"paramName": "teamId", "isRequired": False},
            {"paramName": "hydrate", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "statsLeaders": {
        "url": BASE_URL + "/stats/leaders",
        "pathParams": [],
        "queryParams": [
            {"paramName": "leaderCategories", "isRequired": True},
            {"paramName": "leaderGameTypes", "isRequired": False},
            {"paramName": "leagueId", "isRequired": False},
            {"paramName": "limit", "isRequired": False},
            {"paramName": "playerPool", "isRequired": False},
            {"paramName": "season", "isRequired": False},
            {"paramName": "sportId", "isRequired": False},
            {"paramName": "statGroup", "isRequired": False},
            {"paramName": "statType", "isRequired": False},
            {"paramName": "hydrate", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "statsStreaks": {
        "url": BASE_URL + "/stats/streaks",
        "pathParams": [],
        "queryParams": [
            {"paramName": "limit", "isRequired": True},
            {"paramName": "season", "isRequired": True},
            {"paramName": "sportId", "isRequired": True},
            {"paramName": "streakSpan", "isRequired": True},
            {"paramName": "streakType", "isRequired": True},
            {"paramName": "gameType", "isRequired": False},
            {"paramName": "hydrate", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "teams": {
        "url": BASE_URL + "/teams",
        "pathParams": [],
        "queryParams": [
            {"paramName": "activeStatus", "isRequired": False},
            {"paramName": "gameType", "isRequired": False},
            {"paramName": "leagueIds", "isRequired": False},
            {"paramName": "season", "isRequired": False},
            {"paramName": "sportId", "isRequired": False},
            {"paramName": "sportIds", "isRequired": False},
            {"paramName": "hydrate", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "teamsHistory": {
        "url": BASE_URL + "/teams/history",
        "pathParams": [],
        "queryParams": [
            {"paramName": "teamIds", "isRequired": True},
            {"paramName": "endSeason", "isRequired": False},
            {"paramName": "startSeason", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "teamsStats": {
        "url": BASE_URL + "/teams/stats",
        "pathParams": [],
        "queryParams": [
            {"paramName": "group", "isRequired": True},
            {"paramName": "season", "isRequired": True},
            {"paramName": "stats", "isRequired": True},
            {"paramName": "endDate", "isRequired": False},
            {"paramName": "gameType", "isRequired": False},
            {"paramName": "order", "isRequired": False},
            {"paramName": "sortStat", "isRequired": False},
            {"paramName": "sportIds", "isRequired": False},
            {"paramName": "startDate", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "teamsAffiliates": {
        "url": BASE_URL + "/teams/affiliates",
        "pathParams": [],
        "queryParams": [
            {"paramName": "teamIds", "isRequired": True},
            {"paramName": "season", "isRequired": False},
            {"paramName": "sportId", "isRequired": False},
            {"paramName": "hydrate", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "team": {
        "url": BASE_URL + "/teams/{teamId}",
        "pathParams": [{"paramName": "teamId", "isRequired": True}],
        "queryParams": [
            {"paramName": "season", "isRequired": False},
            {"paramName": "sportId", "isRequired": False},
            {"paramName": "hydrate", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "teamAlumni": {
        "url": BASE_URL + "/teams/{teamId}/alumni",
        "pathParams": [{"paramName": "teamId", "isRequired": True}],
        "queryParams": [
            {"paramName": "season", "isRequired": True},
            {"paramName": "group", "isRequired": True},
            {"paramName": "hydrate", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "teamCoaches": {
        "url": BASE_URL + "/teams/{teamId}/coaches",
        "pathParams": [{"paramName": "teamId", "isRequired": True}],
        "queryParams": [
            {"paramName": "date", "isRequired": False},
            {"paramName": "season", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "teamPersonnel": {
        "url": BASE_URL + "/teams/{teamId}/personnel",
        "pathParams": [{"paramName": "teamId", "isRequired": True}],
        "queryParams": [
            {"paramName": "date", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "teamLeaders": {
        "url": BASE_URL + "/teams/{teamId}/leaders",
        "pathParams": [{"paramName": "teamId", "isRequired": True}],
        "queryParams": [
            {"paramName": "leaderCategories", "isRequired": True},
            {"paramName": "season", "isRequired": True},
            {"paramName": "leaderGameTypes", "isRequired": False},
            {"paramName": "limit", "isRequired": False},
            {"paramName": "hydrate", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "teamRoster": {
        "url": BASE_URL + "/teams/{teamId}/roster",
        "pathParams": [{"paramName": "teamId", "isRequired": True}],
        "queryParams": [
            {"paramName": "date", "isRequired": False},
            {"paramName": "rosterType", "isRequired": False},
            {"paramName": "season", "isRequired": False},
            {"paramName": "hydrate", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "teamStats": {
        "url": BASE_URL + "/teams/{teamId}/stats",
        "pathParams": [{"paramName": "teamId", "isRequired": True}],
        "queryParams": [
            {"paramName": "group", "isRequired": True},
            {"paramName": "season", "isRequired": True},
            {"paramName": "gameType", "isRequired": False},
            {"paramName": "sitCodes", "isRequired": False},
            {"paramName": "sportIds", "isRequired": False},
            {"paramName": "stats", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "teamUniforms": {
        "url": BASE_URL + "/uniforms/team",
        "pathParams": [],
        "queryParams": [
            {"paramName": "teamIds", "isRequired": True},
            {"paramName": "season", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "venue": {
        "url": BASE_URL + "/venues",
        "pathParams": [],
        "queryParams": [
            {"paramName": "venueIds", "isRequired": True},
            {"paramName": "season", "isRequired": False},
            {"paramName": "hydrate", "isRequired": False},
            {"paramName": "fields", "isRequired": False},
        ],
    },
    "meta": {
        "url": BASE_URL + "/{type}",
        "pathParams": [
            {"paramName": "type", "isRequired": True},
        ],
        "queryParams": [],
    },
}


def main():
    # pass

    # for k, v in ENDPOINTS.items():
    #     _endpoint = k
    #     _url = v.get("url")
    #     _pathParams = [param.get("paramName") for param in v.get("pathParams", [])]
    #     _queryParams = [param.get("paramName") for param in v.get("queryParams", [])]
    #     _requiredParams = [
    #         param.get("paramName")
    #         for param in v.get("queryParams", [])
    #         if param.get("isRequired") is True
    #     ] + [
    #         param.get("paramName")
    #         for param in v.get("pathParams", [])
    #         if param.get("isRequired") is True
    #     ]
    #     print(f"Endpoint: {_endpoint}")
    #     print(f"URL: {_url}")
    #     print(f"Path Params: {', '.join(_pathParams) if _pathParams else 'None'}")
    #     print(f"Query Params: {', '.join(_queryParams) if _queryParams else 'None'}")
    #     print(f"Required Params: {', '.join(_requiredParams) if _requiredParams else 'None'}")
    #     print(f"\n{'-'*50}\n")
    response = requests.get(f"{ENDPOINTS.get('teamsAffiliates', {}).get('url')}?teamIds=144")
    data = response.json()
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
