BASE_URL: str = "https://statsapi.mlb.com/api/v1"
ENDPOINTS: list = [
	{
		"endpoint": "seasons",
		"url": BASE_URL + "/seasons/?sportId=1",
	},
	{
		"endpoint": "leagues",
		"url": BASE_URL + "/leagues?sportId=1",
		"pathParamUrl": BASE_URL + "/leagues?sportId=1&leagueIds={leagueIds}",
	},
	{
		"endpoint": "divisions",
		"url": BASE_URL + "/divisions?sportId=1",
		"pathParamUrl": BASE_URL + "/divisions/{divisionId}",
	},
	{
		"endpoint": "teams",
		"url": BASE_URL + "/teams?sportId=1",
		"pathParamUrl": BASE_URL + "/teams/{teamId}",
	},
	{
		"endpoint": "players",
		"url": BASE_URL + "/sports/1/players",
		"pathParamUrl": BASE_URL + "/people/{playerId}",
	},
	{
		"endpoint": "schedule",
		"url": BASE_URL + "/schedule?sportId=1",
	},
	{
		"endpoint": "game",
		"url": BASE_URL + "/schedule?sportId=1&gamePk={gameId}",
	}
]
