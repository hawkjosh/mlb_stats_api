data = [
    {
        "springLeague": {
            "id": 114,
            "name": "Cactus League",
            "link": "/api/v1/league/114",
            "abbreviation": "CL",
        },
        "allStarStatus": "N",
        "id": 133,
        "name": "Athletics",
        "link": "/api/v1/teams/133",
        "season": 2026,
        "venue": {
            "id": 2529,
            "name": "Sutter Health Park",
            "link": "/api/v1/venues/2529",
        },
        "springVenue": {"id": 2507, "link": "/api/v1/venues/2507"},
        "teamCode": "ath",
        "fileCode": "ath",
        "abbreviation": "ATH",
        "teamName": "Athletics",
        "locationName": "Sacramento",
        "firstYearOfPlay": "1901",
        "league": {"id": 103, "name": "American League", "link": "/api/v1/league/103"},
        "division": {
            "id": 200,
            "name": "American League West",
            "link": "/api/v1/divisions/200",
        },
        "sport": {"id": 1, "link": "/api/v1/sports/1", "name": "Major League Baseball"},
        "shortName": "Athletics",
        "franchiseName": "Athletics",
        "clubName": "Athletics",
        "active": True,
    },
    {
        "springLeague": {
            "id": 115,
            "name": "Grapefruit League",
            "link": "/api/v1/league/115",
            "abbreviation": "GL",
        },
        "allStarStatus": "N",
        "id": 134,
        "name": "Pittsburgh Pirates",
        "link": "/api/v1/teams/134",
        "season": 2026,
        "venue": {"id": 31, "name": "PNC Park", "link": "/api/v1/venues/31"},
        "springVenue": {"id": 2526, "link": "/api/v1/venues/2526"},
        "teamCode": "pit",
        "fileCode": "pit",
        "abbreviation": "PIT",
        "teamName": "Pirates",
        "locationName": "Pittsburgh",
        "firstYearOfPlay": "1882",
        "league": {"id": 104, "name": "National League", "link": "/api/v1/league/104"},
        "division": {
            "id": 205,
            "name": "National League Central",
            "link": "/api/v1/divisions/205",
        },
        "sport": {"id": 1, "link": "/api/v1/sports/1", "name": "Major League Baseball"},
        "shortName": "Pittsburgh",
        "franchiseName": "Pittsburgh",
        "clubName": "Pirates",
        "active": True,
    },
    {
        "springLeague": {
            "id": 114,
            "name": "Cactus League",
            "link": "/api/v1/league/114",
            "abbreviation": "CL",
        },
        "allStarStatus": "N",
        "id": 135,
        "name": "San Diego Padres",
        "link": "/api/v1/teams/135",
        "season": 2026,
        "venue": {"id": 2680, "name": "Petco Park", "link": "/api/v1/venues/2680"},
        "springVenue": {"id": 2530, "link": "/api/v1/venues/2530"},
        "teamCode": "sdn",
        "fileCode": "sd",
        "abbreviation": "SD",
        "teamName": "Padres",
        "locationName": "San Diego",
        "firstYearOfPlay": "1968",
        "league": {"id": 104, "name": "National League", "link": "/api/v1/league/104"},
        "division": {
            "id": 203,
            "name": "National League West",
            "link": "/api/v1/divisions/203",
        },
        "sport": {"id": 1, "link": "/api/v1/sports/1", "name": "Major League Baseball"},
        "shortName": "San Diego",
        "franchiseName": "San Diego",
        "clubName": "Padres",
        "active": True,
    },
    {
        "springLeague": {
            "id": 114,
            "name": "Cactus League",
            "link": "/api/v1/league/114",
            "abbreviation": "CL",
        },
        "allStarStatus": "N",
        "id": 136,
        "name": "Seattle Mariners",
        "link": "/api/v1/teams/136",
        "season": 2026,
        "venue": {"id": 680, "name": "T-Mobile Park", "link": "/api/v1/venues/680"},
        "springVenue": {"id": 2530, "link": "/api/v1/venues/2530"},
        "teamCode": "sea",
        "fileCode": "sea",
        "abbreviation": "SEA",
        "teamName": "Mariners",
        "locationName": "Seattle",
        "firstYearOfPlay": "1977",
        "league": {"id": 103, "name": "American League", "link": "/api/v1/league/103"},
        "division": {
            "id": 200,
            "name": "American League West",
            "link": "/api/v1/divisions/200",
        },
        "sport": {"id": 1, "link": "/api/v1/sports/1", "name": "Major League Baseball"},
        "shortName": "Seattle",
        "franchiseName": "Seattle",
        "clubName": "Mariners",
        "active": True,
    },
]

from pprint import pprint as pp

# team = data[0]


teams = []

for team in data:
    springLeague = team.get('springLeague', {})
    springLeague_id = springLeague.get('id')
    springLeague_name = springLeague.get('name')
    springLeague_link = springLeague.get('link')
    springLeague_abbreviation = springLeague.get('abbreviation')

    allStarStatus = team.get('allStarStatus')
    teamId = team.get('id')
    name = team.get('name')
    teamLink = team.get('link')
    season = team.get('season')

    venue = team.get('venue', {})
    venue_id = venue.get('id')
    venue_name = venue.get('name')
    venue_link = venue.get('link')

    springVenue = team.get('springVenue', {})
    springVenue_id = springVenue.get('id')
    springVenue_link = springVenue.get('link')

    teamCode = team.get('teamCode')
    fileCode = team.get('fileCode')
    teamAbbreviation = team.get('abbreviation')
    teamName = team.get('teamName')
    locationName = team.get('locationName')
    firstYearOfPlay = team.get('firstYearOfPlay')

    league = team.get('league', {})
    league_id = league.get('id')
    league_name = league.get('name')
    league_link = league.get('link')

    division = team.get('division', {})
    division_id = division.get('id')
    division_name = division.get('name')
    division_link = division.get('link')

    sport = team.get('sport', {})
    sport_id = sport.get('id')
    sport_name = sport.get('name')
    sport_link = sport.get('link')

    shortName = team.get('shortName')
    franchiseName = team.get('franchiseName')
    clubName = team.get('clubName')
    activeStatus = team.get('active')

    teamInfo = {}
    # teamInfo['springLeague'] = springLeague
    teamInfo['springLeague_id'] = springLeague_id
    teamInfo['springLeague_name'] = springLeague_name
    teamInfo['springLeague_link'] = springLeague_link
    teamInfo['springLeague_abbreviation'] = springLeague_abbreviation
    teamInfo['allStarStatus'] = allStarStatus
    teamInfo['teamId'] = teamId
    teamInfo['name'] = name
    teamInfo['teamLink'] = teamLink
    teamInfo['season'] = season
    # teamInfo['venue'] = venue
    teamInfo['venue_id'] = venue_id
    teamInfo['venue_name'] = venue_name
    teamInfo['venue_link'] = venue_link
    # teamInfo['springVenue'] = springVenue
    teamInfo['springVenue_id'] = springVenue_id
    teamInfo['springVenue_link'] = springVenue_link
    teamInfo['teamCode'] = teamCode
    teamInfo['fileCode'] = fileCode
    teamInfo['teamAbbreviation'] = teamAbbreviation
    teamInfo['teamName'] = teamName
    teamInfo['locationName'] = locationName
    teamInfo['firstYearOfPlay'] = firstYearOfPlay
    # teamInfo['league'] = league
    teamInfo['league_id'] = league_id
    teamInfo['league_name'] = league_name
    teamInfo['league_link'] = league_link
    # teamInfo['division'] = division
    teamInfo['division_id'] = division_id
    teamInfo['division_name'] = division_name
    teamInfo['division_link'] = division_link
    # teamInfo['sport'] = sport
    teamInfo['sport_id'] = sport_id
    teamInfo['sport_name'] = sport_name
    teamInfo['sport_link'] = sport_link
    teamInfo['shortName'] = shortName
    teamInfo['franchiseName'] = franchiseName
    teamInfo['clubName'] = clubName
    teamInfo['activeStatus'] = activeStatus

    teams.append(teamInfo)



pp(teams)