from datetime import datetime, timedelta
import json
from pytz import timezone as tz
import requests
from functools import lru_cache

import statsapi

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
    players = (
        requests.get("https://statsapi.mlb.com/api/v1/sports/1/players")
        .json()
        .get("people", [])
    )
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


def printSample(endpoint: str, **kwargs) -> None:
    sampleTitle = kwargs.get(
        "sampleTitle", f"MLB {endpoint.capitalize()} Response Sample"
    )
    sampleSize = kwargs.get("size", None)
    print(f"\n{'='*len(sampleTitle)}\n{sampleTitle}\n{'='*len(sampleTitle)}\n")
    response = getData(endpoint, **kwargs).get(endpoint, [])
    sampleSize = kwargs.get(
        "sampleSize", len(response) if not sampleSize else sampleSize
    )
    data = response[0] if len(response) == 1 else response[0:sampleSize]
    print(json.dumps(data, indent=2))


def getLogoUrl(teamId: int | None = None, teamName: str | None = None, **kwargs) -> str:
    teamId = teamId if teamId else getTeamId(teamName) if teamName else None
    logoType = kwargs.get("logoType", "cap")
    logoShade = kwargs.get("logoShade", "light")
    return f"https://www.mlbstatic.com/team-logos/team-{logoType}-on-{logoShade}/{teamId}.svg"


def getHeadshotUrl(playerId: int | None = None, playerName: str | None = None) -> str:
    playerId = playerId if playerId else getPlayerId(playerName) if playerName else None
    return f"https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{playerId}/headshot/67/current"


def printTeamTotalSeasonWins(teamName: str, season: int = None) -> None:
    teamId = getTeamId(teamName)
    year = season or CURR_SEASON
    isCurrSeason = year == CURR_SEASON

    gameDates = getData(
        "schedule", teamId=teamId, startDate=f"{year}-01-01", endDate=f"{year}-12-31"
    ).get("dates", [])

    totalWins = 0
    for games in gameDates:
        for game in games.get("games", []):
            teams = game.get("teams", {})
            homeTeamResult = {
                "id": teams.get("home", {}).get("team", {}).get("id"),
                "isWinner": teams.get("home", {}).get("isWinner", False),
            }
            awayTeamResult = {
                "id": teams.get("away", {}).get("team", {}).get("id"),
                "isWinner": teams.get("away", {}).get("isWinner", False),
            }
            winningTeamId = (
                homeTeamResult["id"]
                if homeTeamResult["isWinner"]
                else awayTeamResult["id"] if awayTeamResult["isWinner"] else None
            )

            if winningTeamId == teamId:
                totalWins += 1

    print(
        f"The {teamName}{' have won ' if isCurrSeason else ' won '}{totalWins} games {'this season' if isCurrSeason else f'in {year}'}."
    )








# # Example: Print the linescores of all games won by the Atlanta Braves in July 2025
# for x in [
#     y
#     for y in statsapi.schedule(team=144, start_date="07/01/2025", end_date="07/31/2025")
#     if y.get("winning_team", "") == "Atlanta Braves"
# ]:
#     print(
#         "%s\nWinner: %s, Loser: %s\n%s\n\n"
#         % (
#             x["game_date"],
#             x["winning_team"],
#             x["losing_team"],
#             statsapi.linescore(x["game_id"]),
#         )
#     )

# # Example: Print the Braves 40-man Roster on opening day of the 2025 season
# print(
#     "Braves 40-man roster on opening day of the 2025 season:\n%s"
#     % statsapi.roster(
#         144,
#         "40Man",
#         date=statsapi.get("season", {"seasonId": 2025, "sportId": 1})["seasons"][0][
#             "regularSeasonStartDate"
#         ],
#     )
# )

# # Example: Print boxscore and linescore from Braves most recent game (which may be in progress or may not have started yet based on MLB response to 'last game' request)
# most_recent_game_id = statsapi.last_game(144)
# print(
#     statsapi.boxscore(most_recent_game_id),
#     statsapi.linescore(most_recent_game_id),
#     sep="\n\n",
# )

# # Other Examples:
# # - find team with longest name
# longest_team_name = max(
#     [
#         x["name"]
#         for x in statsapi.get(
#             "teams", {"sportIds": 1, "activeStatus": "Yes", "fields": "teams,name"}
#         )["teams"]
#     ],
#     key=len,
# )
# print(
#     "The team with the longest name is %s, at %s characters."
#     % (longest_team_name, len(longest_team_name))
# )

# # - print standings from July 4, 2025
# print(statsapi.standings(date="07/04/2025"))

# #  - print top 5 team leaders in walks for 2025 Braves
# print(statsapi.team_leaders(144, "walks", limit=5, season=2025))

# # - print top 10 all time career leaders in doubles
# print(
#     statsapi.league_leaders("doubles", statGroup="hitting", statType="career", limit=10)
# )

# # - print Ronald Acuña Jr.'s career hitting stats
# print(
#     statsapi.player_stats(
#         statsapi.lookup_player("Ronald Acuña Jr.")[0]["id"],
#         "hitting",
#         "career",
#     )
# )

# # - print list of scoring plays from 6/23/2024 Braves @ Yankees
# print(statsapi.game_scoring_plays(745727))

def main() -> None:
    def jprint(data: dict | list) -> None:
        print(json.dumps(data, indent=2))


    title = "Running Development Testing"
    border = "~ " * (len(title) // 2 + 10)
    print(
        f"\n{border}",
        f"{title:^{int((len(border)))}}",
        f"{border}\n\n",
        sep="\n",
    )


    # Example: Print the linescores of all games won by the Atlanta Braves in July 2025
    # for x in [
    #     y
    #     for y in statsapi.schedule(team=144, start_date="07/01/2025", end_date="07/31/2025")
    #     if y.get("winning_team", "") == "Atlanta Braves"
    # ]:
    #     print(
    #         "%s\nWinner: %s, Loser: %s\n%s\n\n"
    #         % (
    #             x["game_date"],
    #             x["winning_team"],
    #             x["losing_team"],
    #             statsapi.linescore(x["game_id"]),
    #         )
    #     )
    # for x in [
    #     y
    #     for y in getData("schedule", teamId=144, start_date="07/01/2025", end_date="07/31/2025").get("dates", [])
    #     # if y.get("winning_team", "") == "Atlanta Braves"
    # ]:
    #     print(
    #         "%s\nWinner: %s, Loser: %s\n%s\n\n"
    #         % (
    #             x["game_date"],
    #             x["winning_team"],
    #             x["losing_team"],
    #             statsapi.linescore(x["game_id"]),
    #         )
    #     )
    # jprint(statsapi.schedule(team=144, date="7/2/2025"))
    jprint(statsapi.schedule(team=144, start_date="7/1/2025", end_date="7/5/2025"))
    # jprint(getData("schedule", teamId=144, date="7/2/2025"))
    # dates = getData("schedule", teamId=144, startDate="7/1/2025", endDate="7/5/2025", hydrate="linescore").get("dates", [])
    dates = getData("schedule", teamId=144, startDate="7/1/2025", endDate="7/5/2025", hydrate="linescore").get("dates", [])
    games = []
    linescores = []
    for date in dates:
        for game in date.get("games", []):
            gameDetails = {
                "game_id": game.get("gamePk", ""),
                "game_datetime": game.get("gameDate", ""),
                "game_date": game.get("gameDate", "")[:10],
                "game_type": game.get("gameType", ""),
                "status": game.get("status", {}).get("detailedState", ""),
                "away_name": game.get("teams", {}).get("away", {}).get("team", {}).get("name", ""),
                "home_name": game.get("teams", {}).get("home", {}).get("team", {}).get("name", ""),
                "away_id": game.get("teams", {}).get("away", {}).get("team", {}).get("id", ""),
                "home_id": game.get("teams", {}).get("home", {}).get("team", {}).get("id", ""),
                "doubleheader": game.get("doubleHeader", "N"),
                "game_num": game.get("gameNumber", 1),
                "home_probable_pitcher": game.get("teams", {}).get("home", {}).get("probablePitcher", {}).get("fullName", ""),
                "away_probable_pitcher": game.get("teams", {}).get("away", {}).get("probablePitcher", {}).get("fullName", ""),
                "home_pitcher_note": game.get("teams", {}).get("home", {}).get("pitcherNote", ""),
                "away_pitcher_note": game.get("teams", {}).get("away", {}).get("pitcherNote", ""),
                "away_score": game.get("teams", {}).get("away", {}).get("score", 0),
                "home_score": game.get("teams", {}).get("home", {}).get("score", 0),
                "current_inning": game.get("linescore", {}).get("currentInning", 0),
                "inning_state": game.get("linescore", {}).get("inningState", ""),
                "venue_id": game.get("venue", {}).get("id", ""),
                "venue_name": game.get("venue", {}).get("name", ""),
                "national_broadcasts": game.get("broadcasts", []),
                "series_status": game.get("seriesStatus", ""),
                "winning_team": game.get("seriesStatus", {}).get("winningTeam", ""),
                "losing_team": game.get("seriesStatus", {}).get("losingTeam", ""),
                "winning_pitcher": game.get("seriesStatus", {}).get("winningPitcher", ""),
                "losing_pitcher": game.get("seriesStatus", {}).get("losingPitcher", ""),
                "save_pitcher": game.get("seriesStatus", {}).get("savePitcher", ""),
                "summary": f"{game.get('gameDate', '')[:10]} - {game.get('teams', {}).get('away', {}).get('team', {}).get('name', '')} ({game.get('teams', {}).get('away', {}).get('score', 0)}) @ {game.get('teams', {}).get('home', {}).get('team', {}).get('name', '')} ({game.get('teams', {}).get('home', {}).get('score', 0)}) ({game.get('status', {}).get('detailedState', '')})"
            }
            games.append(gameDetails)
    # for date in dates:
    #     for game in date.get("games", []):
    #         winningTeam = game.get("seriesStatus", {}).get("winningTeam", "")
    print("\n\n","="*40,"\n\n")
    jprint(games)
    # gameDates = []
    # for game in [games for games in dates]:
    #     gameData = {
    #         "gameId": game.get("gamePk", ""),
    #         "gameLink": game.get("link", ""),
    #         "gameDate": game.get("gameDate", ""),
    #         "gameStatus": game.get("status", {}).get("detailedState", "")
    #     }
    #     gameDates.append(gameData)
    
    # jprint(dates)
    # jprint(gameDates)


        # "game_datetime": "2025-07-02T23:15:00Z",
        # "game_date": "2025-07-02",
        # "game_type": "R",
        # "status": "Final",
        # "away_name": "Los Angeles Angels",
        # "home_name": "Atlanta Braves",
        # "away_id": 108,
        # "home_id": 144,
        # "doubleheader": "N",
        # "game_num": 1,
        # "home_probable_pitcher": "Didier Fuentes",
        # "away_probable_pitcher": "Yusei Kikuchi",
        # "home_pitcher_note": "",
        # "away_pitcher_note": "",
        # "away_score": 3,
        # "home_score": 8,
        # "current_inning": 9,
        # "inning_state": "Top",
        # "venue_id": 4705,
        # "venue_name": "Truist Park",
        # "national_broadcasts": [],
        # "series_status": "Series tied 1-1",
        # "winning_team": "Atlanta Braves",
        # "losing_team": "Los Angeles Angels",
        # "winning_pitcher": "Aaron Bummer",
        # "losing_pitcher": "Ryan Zeferjahn",
        # "save_pitcher": null,
        # "summary": "2025-07-02 - Los Angeles Angels (3) @ Atlanta Braves (8) (Final)"
        
    
    # gameData = {
    #     "game_id": data.get(""),
    #     "game_datetime": "2025-07-02T23:15:00Z",
    #     "game_date": "2025-07-02",
    #     "game_type": "R",
    #     "status": "Final",
    #     "away_name": "Los Angeles Angels",
    #     "home_name": "Atlanta Braves",
    #     "away_id": 108,
    #     "home_id": 144,
    #     "doubleheader": "N",
    #     "game_num": 1,
    #     "home_probable_pitcher": "Didier Fuentes",
    #     "away_probable_pitcher": "Yusei Kikuchi",
    #     "home_pitcher_note": "",
    #     "away_pitcher_note": "",
    #     "away_score": 3,
    #     "home_score": 8,
    #     "current_inning": 9,
    #     "inning_state": "Top",
    #     "venue_id": 4705,
    #     "venue_name": "Truist Park",
    #     "national_broadcasts": [],
    #     "series_status": "Series tied 1-1",
    #     "winning_team": "Atlanta Braves",
    #     "losing_team": "Los Angeles Angels",
    #     "winning_pitcher": "Aaron Bummer",
    #     "losing_pitcher": "Ryan Zeferjahn",
    #     "save_pitcher": null,
    #     "summary": "2025-07-02 - Los Angeles Angels (3) @ Atlanta Braves (8) (Final)"
    # }
    
    # for hydration in hydrations:
    #     print("\n\n###",
    #           f"GET https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId=144&date=2025-03-27&hydrate={hydration}",
    #           sep="\n"
    #     )




if __name__ == "__main__":
    main()