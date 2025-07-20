-- Create season table
CREATE TABLE IF NOT EXISTS season (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create player table
CREATE TABLE IF NOT EXISTS player (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    partner_name VARCHAR(100),
    game_type VARCHAR(20) NOT NULL,
    division FLOAT,
    "group" VARCHAR(1),
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Add game_type and season_id to appointable table
ALTER TABLE appointable ADD COLUMN game_type VARCHAR(20);
ALTER TABLE appointable ADD COLUMN season_id INTEGER REFERENCES season(id);

-- Add game_type and season_id to schedule table
ALTER TABLE schedule ADD COLUMN game_type VARCHAR(20);
ALTER TABLE schedule ADD COLUMN season_id INTEGER REFERENCES season(id); 