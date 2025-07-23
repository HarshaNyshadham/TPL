def calculate_points(team1_sets, team2_sets, score):
    """
    Returns:
        (t1_points, t2_points, t1_bonus, t2_bonus, t1_win, t2_win, t1_loss, t2_loss)
    """
    if 'forfeit' in score.lower():
        return 0, 0, 0, 0, 0, 0, 0, 0
    if team1_sets > team2_sets:
        t1_points = 40
        t2_points = 10 + (team2_sets * 10)
        t1_bonus = 0
        t2_bonus = team2_sets * 10
        t1_win = 1
        t2_win = 0
        t1_loss = 0
        t2_loss = 1
    elif team2_sets > team1_sets:
        t1_points = 10 + (team1_sets * 10)
        t2_points = 40
        t1_bonus = team1_sets * 10
        t2_bonus = 0
        t1_win = 0
        t2_win = 1
        t1_loss = 1
        t2_loss = 0
    else:
        t1_points = 10 + (team1_sets * 10)
        t2_points = 10 + (team2_sets * 10)
        t1_bonus = team1_sets * 10
        t2_bonus = team2_sets * 10
        t1_win = 0
        t2_win = 0
        t1_loss = 1
        t2_loss = 1
    return t1_points, t2_points, t1_bonus, t2_bonus, t1_win, t2_win, t1_loss, t2_loss
