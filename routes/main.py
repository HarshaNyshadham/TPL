from flask import Blueprint, render_template, redirect, url_for, jsonify, request
# Removed unused service imports
from models import Season, Appointable, db, Schedule
from services.point_calculation import calculate_points

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    return redirect(url_for('main.newindex'))

@main_bp.route('/newindex')
def newindex():
    try:
        # Get game type from query parameter, default to 'singles' (lowercase)
        game_type = request.args.get('game_type', 'singles')
        print(f"DEBUG: Game type for newindex: {game_type}")
        # Get active season
        active_season = Season.query.filter_by(is_active=True).first()
        print(f"DEBUG: Active season for newindex: {active_season}")
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
        print(f"DEBUG: Standings for {game_type}: {standings}")
        # Get schedule data for all teams
        all_teams = []
        for division_teams in standings.values():
            all_teams.extend(team[0] for team in division_teams)
        schedule_data = {}
        schedules = Schedule.query.filter_by(season_id=active_season.id, game_type=game_type).all()
        for team in all_teams:
            team_matches = []
            for sched in schedules:
                if sched.team1 == team or sched.team2 == team:
                    team_matches.append([
                        sched.team1,
                        sched.team2,
                        sched.score,
                        sched.deadline.strftime('%Y-%m-%d') if sched.deadline else ''
                    ])
            schedule_data[team] = team_matches
        print(f"DEBUG: Schedule data for {game_type}: {schedule_data}")
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
        active_season = Season.query.filter_by(is_active=True).first()
        if not all([team1, team2, score, active_season]):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

        # Find the schedule entry
        sched = Schedule.query.filter_by(
            team1=team1, team2=team2, game_type=game_type, season_id=active_season.id
        ).first()
        if not sched:
            sched = Schedule.query.filter_by(
                team1=team2, team2=team1, game_type=game_type, season_id=active_season.id
            ).first()
        if not sched:
            return jsonify({'status': 'error', 'message': 'Match not found'}), 404

        # Update the score in the schedule table
        sched.score = score
        sched.updated_at = db.func.now()

        # Parse the score string (e.g., '6-4,6-3')
        sets = [s.strip() for s in score.split(',') if '-' in s]
        team1_sets = 0
        team2_sets = 0
        team1_games = 0
        team2_games = 0
        for s in sets:
            try:
                g1, g2 = map(int, s.split('-'))
                if g1 > g2:
                    team1_sets += 1
                elif g2 > g1:
                    team2_sets += 1
                team1_games += g1
                team2_games += g2
            except Exception:
                continue

        # Use modular point calculation
        t1_points, t2_points, t1_bonus, t2_bonus, t1_win, t2_win, t1_loss, t2_loss = calculate_points(team1_sets, team2_sets, score)

        # Update Appointable (point table) for both teams
        for team, points, bonus, win, loss, games, sets in [
            (team1, t1_points, t1_bonus, t1_win, t1_loss, team1_games, team1_sets),
            (team2, t2_points, t2_bonus, t2_win, t2_loss, team2_games, team2_sets)
        ]:
            appoint = Appointable.query.filter_by(
                team=team, game_type=game_type, season_id=active_season.id
            ).first()
            if appoint:
                appoint.matches = (appoint.matches or 0) + 1
                appoint.points = (appoint.points or 0) + points + bonus
                appoint.bonus = (appoint.bonus or 0) + bonus
                appoint.games_total = (appoint.games_total or 0) + games
                appoint.games_won = (appoint.games_won or 0) + sets
                appoint.won = (appoint.won or 0) + win
                appoint.loss = (appoint.loss or 0) + loss
                appoint.calculate_games_percentage()
                appoint.updated_at = db.func.now()
        db.session.commit()

        # Get updated standings for all divisions
        standings = {}
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