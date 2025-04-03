from models import db, Appointable, Schedule

class ScoreService:
    @staticmethod
    def update_match_score(team1, team2, score):
        """Update match score and recalculate team statistics"""
        try:
            # Find the match
            match = Schedule.query.filter(
                ((Schedule.team1 == team1) & (Schedule.team2 == team2)) |
                ((Schedule.team1 == team2) & (Schedule.team2 == team1))
            ).first()
            
            if not match:
                raise ValueError('Match not found')

            # Reverse previous score's impact if exists
            if match.score:
                ScoreService._reverse_previous_score(match, team1, team2)
            
            # Update score
            match.score = score
            
            # Calculate and update new statistics
            ScoreService._update_team_statistics(match, team1, team2, score)
            
            # Commit changes
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def _reverse_previous_score(match, team1, team2):
        """Reverse the impact of previous score on team statistics"""
        old_sets = match.score.split(', ')
        old_team1_sets = 0
        old_team2_sets = 0
        old_team1_games = 0
        old_team2_games = 0
        
        for set_score in old_sets:
            if not set_score:
                continue
            games = set_score.split('-')
            if len(games) != 2:
                continue
            
            g1 = int(games[0])
            g2 = int(games[1])
            old_team1_games += g1
            old_team2_games += g2
            
            if g1 > g2:
                old_team1_sets += 1
            else:
                old_team2_sets += 1
        
        # Get team records
        team1_record = Appointable.query.filter_by(team=team1).first()
        team2_record = Appointable.query.filter_by(team=team2).first()
        
        if team1_record and team2_record:
            # Reverse matches played
            team1_record.matches -= 1
            team2_record.matches -= 1
            
            # Reverse wins/losses and points
            if old_team1_sets > old_team2_sets:
                team1_record.won -= 1
                team2_record.loss -= 1
                team1_record.points -= 40
                if old_team1_sets == 2 and old_team2_sets == 0:
                    team1_record.bonus -= 1
                    team1_record.points -= 10
            else:
                team2_record.won -= 1
                team1_record.loss -= 1
                team2_record.points -= 40
                if old_team2_sets == 2 and old_team1_sets == 0:
                    team2_record.bonus -= 1
                    team2_record.points -= 10
            
            # Reverse games statistics
            team1_record.games_total -= (old_team1_games + old_team2_games)
            team2_record.games_total -= (old_team1_games + old_team2_games)
            team1_record.games_won -= old_team1_games
            team2_record.games_won -= old_team2_games

    @staticmethod
    def _update_team_statistics(match, team1, team2, score):
        """Calculate and update team statistics based on new score"""
        sets = score.split(', ')
        team1_sets = 0
        team2_sets = 0
        team1_games = 0
        team2_games = 0
        
        for set_score in sets:
            if not set_score:
                continue
            games = set_score.split('-')
            if len(games) != 2:
                continue
            
            g1 = int(games[0])
            g2 = int(games[1])
            team1_games += g1
            team2_games += g2
            
            if g1 > g2:
                team1_sets += 1
            else:
                team2_sets += 1
        
        # Update team statistics
        team1_record = Appointable.query.filter_by(team=team1).first()
        team2_record = Appointable.query.filter_by(team=team2).first()
        
        if team1_record and team2_record:
            # Update matches played
            team1_record.matches += 1
            team2_record.matches += 1
            
            # Update wins/losses and calculate points
            base_points = 40  # Base points for winning
            bonus_points = 10  # Bonus points for clean win (2-0)
            
            if team1_sets > team2_sets:
                team1_record.won += 1
                team2_record.loss += 1
                # Add base points for winning
                team1_record.points += base_points
                # Add bonus points for clean win (2-0)
                if team1_sets == 2 and team2_sets == 0:
                    team1_record.bonus += 1
                    team1_record.points += bonus_points
            else:
                team2_record.won += 1
                team1_record.loss += 1
                # Add base points for winning
                team2_record.points += base_points
                # Add bonus points for clean win (2-0)
                if team2_sets == 2 and team1_sets == 0:
                    team2_record.bonus += 1
                    team2_record.points += bonus_points
            
            # Update games statistics
            team1_record.games_total += (team1_games + team2_games)
            team2_record.games_total += (team1_games + team2_games)
            team1_record.games_won += team1_games
            team2_record.games_won += team2_games
            
            # Update games percentage
            if team1_record.games_total > 0:
                team1_record.games_percentage = (team1_record.games_won / team1_record.games_total) * 100
            if team2_record.games_total > 0:
                team2_record.games_percentage = (team2_record.games_won / team2_record.games_total) * 100 