from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user
from models import Appointable, Schedule, db, Player, Season
from models.seed_data import seed_database
from services.point_calculation import calculate_points
from datetime import datetime, timedelta
import csv
import io
import itertools
import pandas as pd

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')





def admin_required(f):
    """Decorator to check if user is an admin"""
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.newindex'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function




@admin_bp.route('/')
@admin_required
def admin():
    seasons = Season.query.all()
    for season in seasons:
        # Player does not have season_id, so just get all players (or filter by game_type/division/group if needed)
        season.players = Player.query.all()
    return render_template('admin.html', seasons=seasons)

#get all players
@admin_bp.route('/players')
@admin_required
def players():
    players = Player.query.all()
    #plaers list to json
    players_list = [player.to_dict() for player in players]
    return jsonify(players_list)

#delete all players clear database
@admin_bp.route('/delete_players')
@admin_required
def delete_players():
    Player.query.delete()
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Players deleted successfully'})


@admin_bp.route('/upload_players', methods=['POST'])
@admin_required
def upload_players():
    if 'playerFile' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file uploaded.'}), 400
    file = request.files['playerFile']
    if file.filename == '' or not (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
        return jsonify({'status': 'error', 'message': 'Invalid file format. Please upload an Excel file (.xlsx, .xls).'}), 400
    try:
        df = pd.read_excel(file, engine="openpyxl")
        # Validate required columns (case-insensitive)
        required_columns = ['name', 'division', 'game type', 'group']
        # Create a mapping from lower-case column names to actual column names
        col_map = {c.lower(): c for c in df.columns}
        missing_columns = [col for col in required_columns if col not in col_map]
        if missing_columns:
            # Return the required columns in original case for clarity
            return jsonify({'status': 'error', 'message': f"Missing required columns: {', '.join([col.title() for col in missing_columns])}"}), 400

        # Rename columns to standard names for internal use
        df = df.rename(columns={col_map['name']: 'name',
                                col_map['division']: 'division',
                                col_map['game type']: 'game type',
                                col_map['group']: 'group'})
        # Only keep required columns in the returned player data
        filtered_columns = ['name', 'division', 'game type', 'group']
        player_data = [
            {col: row.get(col, None) for col in filtered_columns}
            for row in df.to_dict(orient='records')
        ]
        return jsonify({'status': 'success', 'players': player_data, 'message': f'Loaded {len(player_data)} players. Please review and publish.'})
    except Exception as e:
        import traceback
        db.session.rollback()
        tb = traceback.format_exc()
        return jsonify({'status': 'error', 'message': f'Upload failed: {str(e)}', 'traceback': tb}), 400
@admin_bp.route('/publish_players', methods=['POST'])
def publish_players():
    try:
        data = request.json
        players = data.get('players', [])
        if not players:
            return jsonify({'status': 'error', 'message': 'No player data provided.'}), 400
        # Check for duplicate names in the submitted list (case-insensitive)
        names = [str(row['name']).strip().lower() for row in players]
        from collections import Counter
        name_counts = Counter(names)
        duplicates = [name for name, count in name_counts.items() if count > 1]
        if duplicates:
            # Find all rows that are duplicates
            duplicate_rows = [row for row in players if str(row['name']).strip().lower() in duplicates]
            # User-friendly message
            message = 'Duplicate player names found. Please ensure each player name is unique.'
            return jsonify({'status': 'error', 'message': message, 'duplicates': duplicate_rows}), 400
        # Get active season
        active_season = Season.query.filter_by(is_active=True).first()
        if not active_season:
            return jsonify({'status': 'error', 'message': 'No active season found. Please create a season first.'}), 400
        count = 0
        for row in players:
            try:
                player = Player(
                    name=str(row['name']),
                    game_type=str(row['game type']),
                    division=float(row['division']),
                    group=str(row['group'])
                )
                db.session.add(player)
                count += 1
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'message': f'Row error: {str(e)}'}), 400
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # User-friendly SQL error
            if 'NOT NULL constraint failed' in str(e) or 'IntegrityError' in str(e):
                return jsonify({'status': 'error', 'message': 'A required field is missing for one or more players. Please ensure all players have all required fields and are associated with a season.'}), 400
            return jsonify({'status': 'error', 'message': f'Publish failed: {str(e)}'}), 400
        return jsonify({'status': 'success', 'message': f'Published {count} players successfully.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Publish failed: {str(e)}'}), 400

@admin_bp.route('/assign_players', methods=['POST'])
@admin_required
def assign_players():
    player_ids = request.form.get('player_ids', '').split(',')
    division = float(request.form.get('division'))
    group = request.form.get('group')
    
    if not player_ids or not division or not group:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    
    try:
        for player_id in player_ids:
            player = Player.query.get(int(player_id))
            if player:
                player.division = division
                player.group = group
        
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Players assigned successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@admin_bp.route('/remove_assignment/<int:player_id>', methods=['POST'])
@admin_required
def remove_assignment(player_id):
    player = Player.query.get_or_404(player_id)
    player.division = None
    player.group = None
    db.session.commit()
    
    flash('Player assignment removed successfully.', 'success')
    return redirect(url_for('admin.admin'))

@admin_bp.route('/assign_player', methods=['POST'])
@admin_required
def assign_player():
    player_id = request.form.get('player_id')
    division = request.form.get('division')
    group = request.form.get('group')
    
    if not all([player_id, division, group]):
        flash('Missing required fields.', 'danger')
        return redirect(url_for('admin.admin'))
    
    player = Player.query.get_or_404(player_id)
    player.division = float(division)
    player.group = group
    db.session.commit()
    
    flash('Player assigned successfully.', 'success')
    return redirect(url_for('admin.admin'))

@admin_bp.route('/create_season', methods=['POST'])
@admin_required
def create_season():
    name = request.form.get('name')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    game_type = request.form.get('game_type')
    
    if not all([name, start_date, end_date, game_type]):
        flash('Missing required fields.', 'danger')
        return redirect(url_for('admin.admin'))
    
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start_date >= end_date:
            flash('End date must be after start date.', 'danger')
            return redirect(url_for('admin.admin'))
        
        # Deactivate current active season if exists
        Season.query.filter_by(is_active=True).update({'is_active': False})
        
        # Create new season
        season = Season(
            name=name,
            start_date=start_date,
            end_date=end_date,
            game_type=game_type,
            is_active=True
        )
        db.session.add(season)
        db.session.commit()
        
        # Get all players for this game type
        players = Player.query.filter_by(game_type=game_type).all()
        
        # Group players by division and group
        player_groups = {}
        for player in players:
            key = (player.division, player.group)
            if key not in player_groups:
                player_groups[key] = []
            player_groups[key].append(player)
        
        # Create teams and schedules for each group
        for (division, group), group_players in player_groups.items():
            # Create teams
            teams = []
            for player in group_players:
                team = Appointable(
                    team=player.name,
                    division=division,
                    group=group,
                    game_type=game_type,
                    season_id=season.id,
                    matches=0,
                    won=0,
                    loss=0,
                    bonus=0,
                    points=0,
                    games_total=0,
                    games_won=0,
                    games_percentage=0
                )
                teams.append(team)
                db.session.add(team)
            
            # Create schedules for this group
            if len(teams) >= 2:
                n = len(teams)
                for i in range(n):
                    for j in range(i + 1, n):
                        schedule = Schedule(
                            team1=teams[i].team,
                            team2=teams[j].team,
                            division=division,
                            group=group,
                            game_type=game_type,
                            season_id=season.id,
                            deadline=start_date + timedelta(days=7 * (i + j))
                        )
                        db.session.add(schedule)
        
        db.session.commit()
        flash('Season created successfully with schedules.', 'success')
        
    except ValueError:
        flash('Invalid date format.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('admin.admin'))

@admin_bp.route('/publish_season/<int:season_id>', methods=['POST'])
@admin_required
def publish_season(season_id):
    try:
        # Get the season
        season = Season.query.get_or_404(season_id)
        if season.is_active:
            flash('Season is already active.', 'warning')
            return redirect(url_for('admin.admin'))
        
        # Deactivate any currently active season
        Season.query.filter_by(is_active=True).update({'is_active': False})
        
        # Activate the selected season
        season.is_active = True
        
        # Generate schedules for each division and group
        teams = Appointable.query.filter_by(season_id=season.id).all()
        divisions = {team.division for team in teams}
        
        for division in divisions:
            groups = {team.group for team in teams if team.division == division}
            for group in groups:
                group_teams = [team for team in teams if team.division == division and team.group == group]
                create_schedule(group_teams, season)
        
        db.session.commit()
        flash('Season published successfully with schedules.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('admin.admin'))

def create_schedule(teams, season):
    """Create a round-robin schedule for the given teams"""
    if len(teams) < 2:
        return
    
    n = len(teams)
    if n % 2:
        teams.append(None)  # Add a bye if odd number of teams
        n += 1
    
    # Generate rounds using circle method
    for i in range(n - 1):
        for j in range(n // 2):
            team1 = teams[j]
            team2 = teams[n - 1 - j]
            
            if team1 and team2:  # Skip if either team is a bye
                schedule = Schedule(
                    team1=team1.team,
                    team2=team2.team,
                    division=team1.division,
                    group=team1.group,
                    game_type=season.game_type,
                    season_id=season.id,
                    deadline=season.start_date + timedelta(days=7 * i)
                )
                db.session.add(schedule)
        
        # Rotate teams for next round (keep first team fixed)
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]

@admin_bp.route('/add_team', methods=['POST'])
@admin_required
def add_team():
    data = request.json
    player1 = data.get('player1')
    player2 = data.get('player2')
    division = data.get('division')
    
    if not all([player1, player2, division]):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    
    # Create team name
    team_name = f"{player1}/{player2}"
    
    # Check if team already exists
    existing_team = Appointable.query.filter_by(team=team_name).first()
    if existing_team:
        return jsonify({'status': 'error', 'message': 'Team already exists'}), 400
    
    # Create new team
    new_team = Appointable(
        team=team_name,
        division=division,
        matches=0,
        won=0,
        loss=0,
        points=0,
        bonus=0,
        games_total=0,
        games_won=0,
        games_percentage=0
    )
    
    db.session.add(new_team)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Team added successfully'})

@admin_bp.route('/delete_team', methods=['POST'])
@admin_required
def delete_team():
    data = request.json
    team = data.get('team')
    
    if not team:
        return jsonify({'status': 'error', 'message': 'Team name is required'}), 400
    
    # Find and delete team
    team_record = Appointable.query.filter_by(team=team).first()
    if not team_record:
        return jsonify({'status': 'error', 'message': 'Team not found'}), 404
    
    # Delete related schedules
    Schedule.query.filter(
        (Schedule.team1 == team) | (Schedule.team2 == team)
    ).delete()
    
    db.session.delete(team_record)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Team deleted successfully'})

@admin_bp.route('/get_teams')
@admin_required
def get_teams():
    teams = Appointable.query.all()
    teams_list = [team.team for team in teams]
    divisions = {team.team: team.division for team in teams}
    
    return jsonify({
        'status': 'success',
        'teams': teams_list,
        'divisions': divisions
    })

@admin_bp.route('/get_scores')
@admin_required
def get_scores():
    scores = Schedule.query.filter(Schedule.score.isnot(None)).all()
    scores_list = [{
        'id': score.id,
        'team1': score.team1,
        'team2': score.team2,
        'score': score.score,
        'date': score.updated_at.strftime('%Y-%m-%d')
    } for score in scores]
    
    return jsonify({
        'status': 'success',
        'scores': scores_list
    })

@admin_bp.route('/delete_score', methods=['POST'])
@admin_required
def delete_score():
    data = request.json
    score_id = data.get('score_id')
    
    if not score_id:
        return jsonify({'status': 'error', 'message': 'Score ID is required'}), 400
    
    # Find and delete score
    score = Schedule.query.get(score_id)
    if not score:
        return jsonify({'status': 'error', 'message': 'Score not found'}), 404
    
    # ScoreService removed, so no team statistics update
    
    # Clear the score
    score.score = None
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Score deleted successfully'})

@admin_bp.route('/new_season', methods=['POST'])
@admin_required
def new_season():
    data = request.json
    season_name = data.get('name')
    start_date = data.get('start_date')
    
    if not all([season_name, start_date]):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    
    # Clear existing data
    db.session.query(Schedule).delete()
    db.session.query(Appointable).delete()
    db.session.commit()
    
    # Seed new data
    seed_database()
    
    return jsonify({'status': 'success', 'message': 'New season created successfully'})

@admin_bp.route('/create_schedule', methods=['POST'])
@admin_required
def create_schedule():
    division = request.form.get('division')
    group = request.form.get('group')
    game_type = request.form.get('game_type')
    
    if not all([division, group, game_type]):
        flash('Missing required fields.', 'danger')
        return redirect(url_for('admin.admin'))
    
    try:
        # Get active season
        active_season = Season.query.filter_by(is_active=True).first()
        if not active_season:
            flash('No active season found.', 'danger')
            return redirect(url_for('admin.admin'))
        
        # Get players in the specified division and group
        players = Player.query.filter_by(
            division=float(division),
            group=group,
            game_type=game_type
        ).all()
        
        if len(players) < 2:
            flash('Need at least 2 players to create a schedule.', 'danger')
            return redirect(url_for('admin.admin'))
        
        # Create teams for each player/pair
        teams = []
        for player in players:
            team_name = f"{player.name}{' & ' + player.partner_name if player.partner_name else ''}"
            team = Appointable(
                team=team_name,
                division=float(division),
                group=group,
                game_type=game_type,
                season_id=active_season.id,
                matches=0,
                won=0,
                loss=0,
                bonus=0,
                points=0,
                games_total=0,
                games_won=0,
                games_percentage=0
            )
            teams.append(team)
            db.session.add(team)
        
        db.session.commit()
        
        # Create schedule for each pair of teams
        total_teams = len(teams)
        matches_per_team = total_teams - 1
        days_between_matches = (active_season.end_date - active_season.start_date).days // matches_per_team
        
        for i, j in itertools.combinations(range(total_teams), 2):
            match_date = active_season.start_date + timedelta(days=days_between_matches * min(i, j))
            schedule = Schedule(
                team1=teams[i].team,
                team2=teams[j].team,
                division=float(division),
                group=group,
                game_type=game_type,
                season_id=active_season.id,
                deadline=match_date
            )
            db.session.add(schedule)
        
        db.session.commit()
        flash('Schedule created successfully.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating schedule: {str(e)}', 'danger')
    
    return redirect(url_for('admin.admin'))

@admin_bp.route('/update_score', methods=['POST'])
@admin_required
def update_score():
    schedule_id = request.form.get('schedule_id')
    score = request.form.get('score')
    
    if not all([schedule_id, score]):
        flash('Missing required fields.', 'danger')
        return redirect(url_for('admin.admin'))
    
    try:
        schedule = Schedule.query.get_or_404(schedule_id)
        
        # Parse score (format: "6-4,6-3" or similar)
        sets = score.split(',')
        team1_sets = 0
        team2_sets = 0
        team1_games = 0
        team2_games = 0
        
        for set_score in sets:
            t1_score, t2_score = map(int, set_score.split('-'))
            team1_games += t1_score
            team2_games += t2_score
            if t1_score > t2_score:
                team1_sets += 1
            else:
                team2_sets += 1
        
        # Update schedule
        schedule.score = score
        
        # Update team statistics
        team1 = Appointable.query.filter_by(team=schedule.team1).first()
        team2 = Appointable.query.filter_by(team=schedule.team2).first()
        
        # Update matches played
        team1.matches += 1
        team2.matches += 1
        
        # Update wins/losses
        if team1_sets > team2_sets:
            team1.won += 1
            team2.loss += 1
            team1.points += 2  # 2 points for a win
        else:
            team2.won += 1
            team1.loss += 1
            team2.points += 2
        
        # Update games statistics
        team1.games_total += team1_games + team2_games
        team2.games_total += team1_games + team2_games
        team1.games_won += team1_games
        team2.games_won += team2_games
        
        # Update games percentage
        team1.games_percentage = (team1.games_won / team1.games_total * 100) if team1.games_total > 0 else 0
        team2.games_percentage = (team2.games_won / team2.games_total * 100) if team2.games_total > 0 else 0
        
        db.session.commit()
        flash('Score updated successfully.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating score: {str(e)}', 'danger')
    
    return redirect(url_for('admin.admin'))

@admin_bp.route('/player/<int:player_id>/update', methods=['POST'])
@admin_required
def update_player(player_id):
    player = Player.query.get_or_404(player_id)
    player.division = float(request.form.get('division'))
    player.group = request.form.get('group')
    
    try:
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)})

@admin_bp.route('/player/<int:player_id>/remove', methods=['POST'])
@admin_required
def remove_player(player_id):
    player = Player.query.get_or_404(player_id)
    
    try:
        db.session.delete(player)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)})

def create_schedules(season_id):
    """Create schedules for all divisions and groups in a season"""
    season = Season.query.get(season_id)
    teams = Appointable.query.filter_by(season_id=season_id).all()
    
    # Group teams by division and group
    team_groups = {}
    for team in teams:
        key = (team.division, team.group)
        if key not in team_groups:
            team_groups[key] = []
        team_groups[key].append(team)
    
    # Create schedules for each group
    for (division, group), group_teams in team_groups.items():
        if len(group_teams) < 2:
            continue
            
        # Create round-robin schedule
        n = len(group_teams)
        if n % 2:
            group_teams.append(None)  # Add bye if odd number of teams
            n += 1
        
        # Generate rounds
        for i in range(n - 1):
            for j in range(n // 2):
                team1 = group_teams[j]
                team2 = group_teams[n - 1 - j]
                
                if team1 and team2:  # Skip if either team is a bye
                    schedule = Schedule(
                        team1=team1.team,
                        team2=team2.team,
                        division=division,
                        group=group,
                        game_type=season.game_type,
                        season_id=season_id,
                        deadline=season.start_date + timedelta(days=7 * i)
                    )
                    db.session.add(schedule)
            
            # Rotate teams for next round (keep first team fixed)
            group_teams = [group_teams[0]] + [group_teams[-1]] + group_teams[1:-1]
    
    db.session.commit()

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.newindex'))

@admin_bp.route('/schedule/<int:sched_id>/update', methods=['POST'])
def update_schedule(sched_id):
    data = request.json
    sched = Schedule.query.get(sched_id)
    if not sched:
        return jsonify({'status': 'error', 'message': 'Schedule not found'}), 404
    sched.score = data.get('score', sched.score)
    sched.updated_at = db.func.now()
    db.session.commit()
    return jsonify({'status': 'success'})

@admin_bp.route('/pointtable/<int:team_id>/update', methods=['POST'])
def update_pointtable(team_id):
    data = request.json
    appoint = Appointable.query.get(team_id)
    if not appoint:
        return jsonify({'status': 'error', 'message': 'Team not found'}), 404
    appoint.matches = int(data.get('matches', appoint.matches))
    appoint.won = int(data.get('won', appoint.won))
    appoint.loss = int(data.get('loss', appoint.loss))
    appoint.points = int(data.get('points', appoint.points))
    appoint.updated_at = db.func.now()
    db.session.commit()
    return jsonify({'status': 'success'})

@admin_bp.route('/recalculate_scores', methods=['POST'])
def recalculate_scores():
    try:
        active_season = Season.query.filter_by(is_active=True).first()
        if not active_season:
            return jsonify({'status': 'error', 'message': 'No active season'}), 400
        # Reset all appointables
        appoints = Appointable.query.filter_by(season_id=active_season.id).all()
        for appoint in appoints:
            appoint.matches = 0
            appoint.won = 0
            appoint.loss = 0
            appoint.points = 0
            appoint.bonus = 0
            appoint.games_total = 0
            appoint.games_won = 0
            appoint.games_percentage = 0.0
        # Recalculate from all schedules
        schedules = Schedule.query.filter_by(season_id=active_season.id).all()
        for sched in schedules:
            if not sched.score:
                continue
            sets = [s.strip() for s in sched.score.split(',') if '-' in s]
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
            t1_points, t2_points, t1_bonus, t2_bonus, t1_win, t2_win, t1_loss, t2_loss = calculate_points(team1_sets, team2_sets, sched.score)
            for team, points, bonus, win, loss, games, sets in [
                (sched.team1, t1_points, t1_bonus, t1_win, t1_loss, team1_games, team1_sets),
                (sched.team2, t2_points, t2_bonus, t2_win, t2_loss, team2_games, team2_sets)
            ]:
                appoint = Appointable.query.filter_by(team=team, game_type=sched.game_type, season_id=active_season.id).first()
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
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500