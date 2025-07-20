from flask import Blueprint, jsonify
from models import Appointable, Season

api_bp = Blueprint('api', __name__)

@api_bp.route('/season/<int:season_id>')
def get_season_data(season_id):
    # Get season data
    season = Season.query.get_or_404(season_id)
    
    # Get all teams for this season
    teams = Appointable.query.filter_by(season_id=season_id).all()
    
    # Organize teams by game type
    singles = [t.to_dict() for t in teams if t.game_type == 'singles']
    doubles = [t.to_dict() for t in teams if t.game_type == 'doubles']
    mixed_doubles = [t.to_dict() for t in teams if t.game_type == 'mixed_doubles']
    
    # Calculate statistics
    stats = {
        'singles_count': len(singles),
        'doubles_count': len(doubles),
        'mixed_doubles_count': len(mixed_doubles),
        'div_50_count': len([t for t in teams if t.division == 5.0]),
        'div_45_count': len([t for t in teams if t.division == 4.5]),
        'div_40_count': len([t for t in teams if t.division == 4.0]),
    }
    
    # Calculate win rates by division
    def calc_win_rate(teams):
        if not teams:
            return 0
        total_win_rate = sum(t.won / t.matches * 100 if t.matches > 0 else 0 for t in teams)
        return total_win_rate / len(teams)
    
    div_50_teams = [t for t in teams if t.division == 5.0]
    div_45_teams = [t for t in teams if t.division == 4.5]
    div_40_teams = [t for t in teams if t.division == 4.0]
    
    stats.update({
        'div_50_win_rate': calc_win_rate(div_50_teams),
        'div_45_win_rate': calc_win_rate(div_45_teams),
        'div_40_win_rate': calc_win_rate(div_40_teams)
    })
    
    return jsonify({
        'season': season.to_dict(),
        'singles': singles,
        'doubles': doubles,
        'mixed_doubles': mixed_doubles,
        'stats': stats
    }) 