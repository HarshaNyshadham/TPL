from models import Schedule, Appointable

class ScheduleService:
    @staticmethod
    def get_team_schedules(teams, game_type):
        """Get schedules for a list of teams"""
        schedules = Schedule.query.filter(
            ((Schedule.team1.in_(teams)) | (Schedule.team2.in_(teams))) &
            (Schedule.game_type == game_type)
        ).all()
        
        schedule_data = {}
        for team in teams:
            team_schedules = []
            for schedule in schedules:
                if schedule.team1 == team or schedule.team2 == team:
                    # Try to determine division from team records if not set
                    if schedule.division is None:
                        team_record = Appointable.query.filter_by(team=team).first()
                        if team_record:
                            schedule.division = team_record.division
                    
                    team_schedules.append([
                        schedule.team1,
                        schedule.team2,
                        schedule.score or '',
                        schedule.deadline.strftime('%Y-%m-%d')
                    ])
            schedule_data[team] = team_schedules
        
        return schedule_data 