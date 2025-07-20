from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from services.point_table_service import PointTableService
from services.schedule_service import ScheduleService
from services.score_service import ScoreService
from models import Season, Appointable, db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    return redirect(url_for('main.newindex'))

@main_bp.route('/newindex')
def newindex():
    try:
        # Get game type from query parameter, default to singles
        game_type = request.args.get('game_type', 'singles')
        
        # Get active season
        active_season = Season.query.filter_by(is_active=True).first()
        if not active_season:
            return render_template('newindex.html',
                                game_type=game_type,
                                pt_data_50=[],
                                pt_data_45=[],
                                pt_data_40=[],
                                schedule_data={})

        # Get data for each division
        divisions = [5.0, 4.5, 4.0]
        standings = {}
        
        for division in divisions:
            # Get teams for this division and game type
            teams = Appointable.query.filter_by(
                division=division,
                game_type=game_type,
                season_id=active_season.id
            ).all()
            
            # Convert to list of tuples for template
            standings[division] = [
                (
                    team.team,           # [0] Team name
                    team.matches,        # [1] Matches played
                    team.won,           # [2] Matches won
                    team.loss,          # [3] Matches lost
                    team.points,        # [4] Total points
                    team.games_percentage, # [5] Games percentage
                    team.group          # [6] Group (A or B)
                )
                for team in teams
            ]
        
        # Get schedule data for all teams
        all_teams = []
        for division_teams in standings.values():
            all_teams.extend(team[0] for team in division_teams)
        
        schedule_data = {}
        if all_teams:
            schedules = ScheduleService.get_team_schedules(all_teams, game_type)
            schedule_data = {team: schedules.get(team, []) for team in all_teams}
        
        return render_template('newindex.html',
                             game_type=game_type,
                             pt_data_50=standings[5.0],
                             pt_data_45=standings[4.5],
                             pt_data_40=standings[4.0],
                             schedule_data=schedule_data)
                             
    except Exception as e:
        print(f"Error in newindex route: {e}")
        return render_template('newindex.html',
                             game_type=game_type,
                             pt_data_50=[],
                             pt_data_45=[],
                             pt_data_40=[],
                             schedule_data={})

@main_bp.route('/update_score', methods=['POST'])
def update_score():
    try:
        data = request.json
        team1 = data.get('team1')
        team2 = data.get('team2')
        score = data.get('score')
        game_type = data.get('game_type', 'singles')
        
        if not all([team1, team2, score]):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        # Update the score
        ScoreService.update_match_score(team1, team2, score, game_type=game_type)
        
        # Get updated standings for all divisions
        standings = {}
        active_season = Season.query.filter_by(is_active=True).first()
        
        for division in [5.0, 4.5, 4.0]:
            teams = Appointable.query.filter_by(
                division=division,
                game_type=game_type,
                season_id=active_season.id
            ).all()
            
            standings[division] = [
                (
                    team.team,
                    team.matches,
                    team.won,
                    team.loss,
                    team.points,
                    team.games_percentage,
                    team.group
                )
                for team in teams
            ]
        
        return jsonify({
            'status': 'success',
            'standings': standings
        })
        
    except Exception as e:
        print(f"Error updating score: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main_bp.route('/history')
def history():
    seasons = Season.query.order_by(Season.start_date.desc()).all()
    return render_template('history.html', seasons=seasons) 