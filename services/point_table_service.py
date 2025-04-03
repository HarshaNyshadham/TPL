from models import Appointable

class PointTableService:
    @staticmethod
    def get_division_standings(division):
        """Get standings for a specific division, sorted by points and games percentage"""
        teams = Appointable.query.filter_by(division=division)\
            .order_by(Appointable.points.desc(), Appointable.games_percentage.desc())\
            .all()
        return teams

    @staticmethod
    def format_standings_data(teams):
        """Format team data for display in point table"""
        formatted_data = []
        for team in teams:
            formatted_data.append([
                team.team,
                team.matches,
                team.won,
                team.loss,
                team.bonus,
                team.points,
                team.group,
                team.games_total,
                team.games_won,
                round(team.games_percentage, 2) if team.games_percentage else 0
            ])
        return formatted_data

    @staticmethod
    def get_all_divisions_standings():
        """Get standings for all divisions"""
        divisions = [5.0, 4.5, 4.0]
        standings = {}
        
        for division in divisions:
            teams = PointTableService.get_division_standings(division)
            standings[division] = PointTableService.format_standings_data(teams)
        
        return standings 