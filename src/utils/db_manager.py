import sqlite3
import os
from models.player import Player

class DatabaseManager:
    def __init__(self, db_path="data/game.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path

        first_run = not os.path.exists(db_path)
        self.init_db()
        if first_run:
            print(f"\u2705 Base de données créée: {db_path}")

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                level INTEGER NOT NULL DEFAULT 1,
                points INTEGER NOT NULL DEFAULT 0,
                current_streak INTEGER NOT NULL DEFAULT 0
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                player_id INTEGER,
                subject TEXT,
                points INTEGER,
                FOREIGN KEY (player_id) REFERENCES players(id),
                PRIMARY KEY (player_id, subject)
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                question TEXT,
                user_answer TEXT,
                correct_answer TEXT,
                is_correct BOOLEAN,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
            ''')
            conn.commit()

    def save_player(self, player):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            if player.id is not None:
                # Mise à jour
                cursor.execute('''
                    UPDATE players SET name = ?, level = ?, points = ?, current_streak = ?
                    WHERE id = ?
                ''', (player.name, player.level, player.points, player.current_streak, player.id))
            else:
                # Nouvelle insertion
                cursor.execute('''
                    INSERT INTO players (name, level, points, current_streak)
                    VALUES (?, ?, ?, ?)
                ''', (player.name, player.level, player.points, player.current_streak))
                player.id = cursor.lastrowid

            # Sauvegarde des matières
            for subject, points in player.subjects.items():
                cursor.execute('''
                    INSERT OR REPLACE INTO subjects (player_id, subject, points)
                    VALUES (?, ?, ?)
                ''', (player.id, subject, points))

            # Sauvegarde historique
            if player.history:
                new_entries = []
                for entry in player.history:
                    if 'id' not in entry:  # Nouvelle entrée sans ID
                        cursor.execute('''
                            INSERT INTO history (player_id, question, user_answer, correct_answer, is_correct)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (
                            player.id,
                            entry['question'],
                            entry['user_answer'],
                            entry['correct_answer'],
                            1 if entry['is_correct'] else 0
                        ))
                        new_entries.append({
                            'id': cursor.lastrowid,
                            'question': entry['question'],
                            'user_answer': entry['user_answer'],
                            'correct_answer': entry['correct_answer'],
                            'is_correct': entry['is_correct']
                        })
                
                # Mettre à jour l'historique du joueur avec les nouveaux IDs
                player.history = [e for e in player.history if 'id' in e] + new_entries
            
            conn.commit()
            return player.id

    def load_player(self, player_id=None, name="Aventurier"):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if player_id is not None:
                cursor.execute('''
                    SELECT id, name, level, points, current_streak
                    FROM players WHERE id = ?
                ''', (player_id,))
            else:
                cursor.execute('''
                    SELECT id, name, level, points, current_streak
                    FROM players WHERE name = ? LIMIT 1
                ''', (name,))
            
            player_data = cursor.fetchone()
            if not player_data:
                return None

            player_id, name, level, points, current_streak = player_data

            # Matières
            subjects = {}
            cursor.execute('SELECT subject, points FROM subjects WHERE player_id = ?', (player_id,))
            for row in cursor.fetchall():
                subjects[row[0]] = row[1]

            # Historique
            history = []
            cursor.execute('''
                SELECT id, question, user_answer, correct_answer, is_correct
                FROM history WHERE player_id = ? ORDER BY timestamp DESC
            ''', (player_id,))
            for row in cursor.fetchall():
                history.append({
                    'id': row[0],
                    'question': row[1],
                    'user_answer': row[2],
                    'correct_answer': row[3],
                    'is_correct': bool(row[4])
                })

            player = Player(
                id=player_id,
                name=name,
                level=level,
                points=points,
                current_streak=current_streak,
                subjects=subjects,
                history=history
            )
            return player
