import mlbstatsapi

mlb = mlbstatsapi.Mlb()


class Team:
    def __init__(self):
        pass

    def get_teams(self):
        teams = []
        for team in mlb.get_teams():
            team_info = {
                "id": team.id,
                "name": team.name,
                "franchiseName": team.franchisename,
                "clubName": team.clubname,
                "league": team.league.name,
                "division": team.division.name,
                "springLeague": team.springleague.name,
            }
            teams.append(team_info)
        return sorted(teams, key=lambda x: x["clubName"])

    def get_team(self, team_id: int = None, team_name: str = None):
        team = (
            mlb.get_team(team_id)
            if team_id
            else mlb.get_team(mlb.get_team_id(team_name)[0])
        )
        venue = mlb.get_venue(team.venue.id)
        springVenue = mlb.get_venue(team.springvenue.id)
        team_info = {
            "id": team.id,
            "name": team.name,
            "franchiseName": team.franchisename,
            "clubName": team.clubname,
            "shortName": team.shortname,
            "teamAbbr": team.abbreviation,
            "league": team.league.name,
            "division": team.division.name,
            "venue": {
                "name": venue.name,
                "capacity": venue.fieldinfo.capacity,
                "turfType": venue.fieldinfo.turftype,
                "roofType": venue.fieldinfo.rooftype,
                "leftLine": venue.fieldinfo.leftline,
                "left": venue.fieldinfo.left,
                "leftCenter": venue.fieldinfo.leftcenter,
                "center": venue.fieldinfo.center,
                "rightCenter": venue.fieldinfo.rightcenter,
                "right": venue.fieldinfo.right,
                "rightLine": venue.fieldinfo.rightline,
            },
            "springLeague": {
                "name": team.springleague.name,
                "venue": springVenue.name,
            },
            "firstYear": team.firstyearofplay,
        }

        return team_info

    def get_team_venue(self, team_id):
        team = self.get_team(team_id)
        return mlb.get_venue(team["venueId"])

    def get_team_spring_venue(self, team_id):
        team = self.get_team(team_id)
        return mlb.get_venue(team["springVenueId"])

    def get_team_spring_league(self, team_id):
        team = self.get_team(team_id)
        return mlb.get_league(team["springLeagueId"])

    def get_coaches(self, team_id: int = None, team_name: str = None):
        coaches = (
            mlb.get_team_coaches(team_id)
            if team_id
            else mlb.get_team_coaches(mlb.get_team_id(team_name)[0])
        )

        return coaches

    def get_roster(self, team_id: int = None, team_name: str = None):
        roster = (
            mlb.get_team_roster(team_id)
            if team_id
            else mlb.get_team_roster(mlb.get_team_id(team_name)[0])
        )

        return roster


class Venue:
    def __init__(self):
        pass

    def get_venues(self):
        return mlb.get_venues(sportIds=[1])

    def get_venue(self, venue_id: int = None, venue_name: str = None):
        venue = (
            mlb.get_venue(venue_id)
            if venue_id
            else mlb.get_venue(mlb.get_venue_id(venue_name)[0])
        )

        return venue


class Player:
    def __init__(self, player_name):
        self.id = mlb.get_people_id(player_name)[0]
        self.info = mlb.get_person(self.id)
        self.stats = mlb.get_player_stats(
            self.id,
            stats=["season", "career"],
            groups=["hitting", "pitching", "fielding", "catching", "running"],
        )

    def get_bio(self):
        info = self.info
        bio = {
            "id": info.id,
            "position": info.primaryposition.name,
            "positionCode": info.primaryposition.code,
            "positionType": info.primaryposition.type,
            "positionAbbr": info.primaryposition.abbreviation,
            "throwSide": info.pitchhand.description,
            "throwSideAbbr": info.pitchhand.code,
            "batSide": info.batside.description,
            "batSideAbbr": info.batside.code,
            "fullName": info.fullname,
            "firstName": info.firstname,
            "lastName": info.lastname,
            "primaryNumber": info.primarynumber,
            "birthDate": info.birthdate,
            "currentAge": info.currentage,
            "birthCity": info.birthcity,
            "birthState": info.birthstateprovince,
            "birthCountry": info.birthcountry,
            "height": info.height,
            "weight": info.weight,
            "boxscoreName": info.boxscorename,
            "draftYear": info.draftyear,
            "mlbDebutDate": info.mlbdebutdate,
            "strikeZoneTop": info.strikezonetop,
            "strikeZoneBottom": info.strikezonebottom,
        }

        return bio

    def get_hitting_stats(self):
        hitting = self.stats["hitting"]
        season_hitting = hitting["season"]
        career_hitting = hitting["career"]

        print("Season Hitting Stats:")
        for split in season_hitting.splits:
            for k, v in split.stat.__dict__.items():
                print(k, v)

        print("\nCareer Hitting Stats:")
        for split in career_hitting.splits:
            for k, v in split.stat.__dict__.items():
                print(k, v)

    def get_pitching_stats(self):
        pitching = self.stats["pitching"]
        season_pitching = pitching["season"]
        career_pitching = pitching["career"]

        print("Season Pitching Stats:")
        for split in season_pitching.splits:
            for k, v in split.stat.__dict__.items():
                print(k, v)

        print("\nCareer Pitching Stats:")
        for split in career_pitching.splits:
            for k, v in split.stat.__dict__.items():
                print(k, v)

    def get_fielding_stats(self):
        fielding = self.stats["fielding"]
        season_fielding = fielding["season"]
        career_fielding = fielding["career"]

        print("Season Fielding Stats:")
        for split in season_fielding.splits:
            for k, v in split.stat.__dict__.items():
                print(k, v)

        print("\nCareer Fielding Stats:")
        for split in career_fielding.splits:
            for k, v in split.stat.__dict__.items():
                print(k, v)

    def get_catching_stats(self):
        catching = self.stats["catching"]
        season_catching = catching["season"]
        career_catching = catching["career"]

        print("Season Catching Stats:")
        for split in season_catching.splits:
            for k, v in split.stat.__dict__.items():
                print(k, v)

        print("\nCareer Catching Stats:")
        for split in career_catching.splits:
            for k, v in split.stat.__dict__.items():
                print(k, v)

    def get_running_stats(self):
        running = self.stats["running"]
        season_running = running["season"]
        career_running = running["career"]

        print("Season Running Stats:")
        for split in season_running.splits:
            for k, v in split.stat.__dict__.items():
                print(k, v)

        print("\nCareer Running Stats:")
        for split in career_running.splits:
            for k, v in split.stat.__dict__.items():
                print(k, v)
