import statsapi

# ENDPOINTS: attendance, awards, conferences, divisions, draft, game, game_diff, game_timestamps, game_changes, game_contextMetrics, game_winProbability, game_boxscore, game_content, game_color, game_color_diff, game_color_timestamps, game_linescore, game_playByPlay, gamePace, highLow, homeRunDerby, league, league_allStarBallot, league_allStarWriteIns, league_allStarFinalVote, people, people_changes, people_freeAgents, person, person_stats, jobs, jobs_umpires, jobs_umpire_games, jobs_datacasters, jobs_officialScorers, schedule, schedule_tied, schedule_postseason, schedule_postseason_series, schedule_postseason_tuneIn, seasons, season, sports, sports_players, standings, stats, stats_leaders, stats_streaks, teams, teams_history, teams_stats, teams_affiliates, team, team_alumni, team_coaches, team_personnel, team_leaders, team_roster, team_stats, transactions, venue, meta


def get_notes(endpoint):
    print(statsapi.notes(endpoint))


class Team:
    def __init__(self):
        pass

    def get_teams(self):
        teams = []
        for team in statsapi.get("teams", {"sportId": 1, "hydrate": "division"})[
            "teams"
        ]:
            team_info = {
                "id": team["id"],
                "franchiseName": team["franchiseName"],
                "clubName": team["clubName"],
                "teamName": f"{team['franchiseName']} {team['clubName']}",
                "league": team["league"]["name"],
                "division": team["division"]["nameShort"],
                "divisionSort": team["division"]["sortOrder"],
            }
            teams.append(team_info)
            teams = sorted(teams, key=lambda x: x["clubName"])
            teams = sorted(teams, key=lambda x: x["divisionSort"])
        return teams

    def get_team(self, team_query):
        team_id = statsapi.lookup_team(team_query)[0]["id"]
        team = statsapi.get("team", {"teamId": team_id})["teams"][0]
        venue = statsapi.get(
            "venue", {"venueIds": team["venue"]["id"], "hydrate": "location,fieldInfo"}
        )["venues"][0]
        team_info = {
            "id": team["id"],
            "franchiseName": team["franchiseName"],
            "clubName": team["clubName"],
            "teamName": f"{team['franchiseName']} {team['clubName']}",
            "abbrName": team["abbreviation"],
            "firstYear": team["firstYearOfPlay"],
            "league": team["league"]["name"],
            "division": team["division"]["name"],
            "venue": {
                "name": venue["name"] or "N/A",
                "capacity": venue["fieldInfo"]["capacity"] or "N/A",
                "turfType": venue["fieldInfo"]["turfType"] or "N/A",
                "roofType": venue["fieldInfo"]["roofType"] or "N/A",
                "dimensions": {
                    "left": venue["fieldInfo"]["leftLine"] or "N/A",
                    "center": venue["fieldInfo"]["center"] or "N/A",
                    "right": venue["fieldInfo"]["rightLine"] or "N/A",
                },
            },
        }

        return team_info
