from flask import Blueprint, jsonify
from models import Appointable, Season

api_bp = Blueprint('api', __name__)

@api_bp.route('/season_stats', methods=['GET'])
def get_season_stats():
    # You need to define how to get 'season', 'singles', 'doubles', 'mixed_doubles', and 'teams'
    # For example, you might fetch the current season and related teams from your database
    season = Season.query.first()  # Example, adjust as needed
    singles = []  # Replace with actual query
    doubles = []  # Replace with actual query
    mixed_doubles = []  # Replace with actual query
    teams = []  # Replace with actual query

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
        'season': season.to_dict() if season else {},
        'singles': singles,
        'doubles': doubles,
        'mixed_doubles': mixed_doubles,
        'stats': stats
    })