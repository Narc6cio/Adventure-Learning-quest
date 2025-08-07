import sqlite3
import os
import json

class DatabaseManager:
    def __init__(self, db_path="data/game.db"):
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create players table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                points INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0,
                subjects TEXT,
                last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create history table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                question TEXT,
                user_answer TEXT,
                correct_answer TEXT,
                is_correct BOOLEAN,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players (id)
            )
            ''')
            
            conn.commit()

    def save_player(self, player_data):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Convert subjects dict to JSON string
            subjects_json = json.dumps(player_data["subjects"])
            
            # Update or insert player data
            cursor.execute('''
            INSERT OR REPLACE INTO players 
            (name, level, points, current_streak, subjects)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                player_data["name"],
                player_data["level"],
                player_data["points"],
                player_data["current_streak"],
                subjects_json
            ))
            
            player_id = cursor.lastrowid
            
            # Save new history entries
            for entry in player_data["history"]:
                cursor.execute('''
                INSERT INTO history 
                (player_id, question, user_answer, correct_answer, is_correct)
                VALUES (?, ?, ?, ?, ?)
                ''', (
                    player_id,
                    entry["question"],
                    entry["user_answer"],
                    entry["correct_answer"],
                    entry["is_correct"]
                ))
            
            conn.commit()

    def load_player(self, name="Aventurier"):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get player data
            cursor.execute('SELECT * FROM players WHERE name = ?', (name,))
            player = cursor.fetchone()
            
            if not player:
                return None
                
            # Get player history
            cursor.execute('SELECT * FROM history WHERE player_id = ?', (player[0],))
            history = cursor.fetchall()
            
            # Convert to dictionary
            player_data = {
                "name": player[1],
                "level": player[2],
                "points": player[3],
                "current_streak": player[4],
                "subjects": json.loads(player[5]),
                "history": [{
                    "question": h[2],
                    "user_answer": h[3],
                    "correct_answer": h[4],
                    "is_correct": h[5]
                } for h in history]
            }
            
            return player_data