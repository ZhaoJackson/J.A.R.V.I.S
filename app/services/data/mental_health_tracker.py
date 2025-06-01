import sqlite3
import pandas as pd
from datetime import datetime
import os

class MentalHealthTracker:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'health_finance.db')
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'output')
        self._init_db()
        self._init_output_dir()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Drop existing tables if they exist
        c.execute('DROP TABLE IF EXISTS mental_health')
        c.execute('DROP TABLE IF EXISTS new_people')
        
        # Create mental health table with timestamp
        c.execute('''
            CREATE TABLE IF NOT EXISTS mental_health (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                mental_status TEXT,
                positive_things TEXT,
                challenging_thing TEXT,
                impact TEXT
            )
        ''')
        
        # Create new people table with timestamp
        c.execute('''
            CREATE TABLE IF NOT EXISTS new_people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                job TEXT,
                sex TEXT,
                graduated TEXT,
                potential_to_meet TEXT,
                interest TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _init_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _export_to_csv(self):
        # Export mental health data
        conn = sqlite3.connect(self.db_path)
        df_mental = pd.read_sql_query("SELECT * FROM mental_health", conn)
        if not df_mental.empty:
            df_mental['date'] = pd.to_datetime(df_mental['date'])
            df_mental = df_mental.sort_values(['date', 'time'])
            df_mental['date'] = df_mental['date'].dt.strftime('%b/%d/%Y')
            output_path = os.path.join(self.output_dir, 'mental_health.csv')
            df_mental.to_csv(output_path, index=False)
        
        # Export new people data
        df_people = pd.read_sql_query("SELECT * FROM new_people", conn)
        if not df_people.empty:
            df_people['date'] = pd.to_datetime(df_people['date'])
            df_people = df_people.sort_values(['date', 'time'])
            df_people['date'] = df_people['date'].dt.strftime('%b/%d/%Y')
            output_path = os.path.join(self.output_dir, 'new_people.csv')
            df_people.to_csv(output_path, index=False)
        
        conn.close()

    def save_daily_data(self, mental_status, positive_things, challenging_thing, impact):
        # Get current timestamp and format dates
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        today = datetime.now().strftime('%b/%d/%Y')  # Format as Mon/Day/Year
        current_time = datetime.now().strftime('%H:%M:%S')
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Always insert a new record
        c.execute('''
            INSERT INTO mental_health 
            (timestamp, date, time, mental_status, positive_things, challenging_thing, impact)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, today, current_time, mental_status, 
              ','.join(positive_things), challenging_thing, impact))
        
        conn.commit()
        conn.close()
        self._export_to_csv()

    def save_new_person(self, job, sex, graduated, potential_to_meet, interest):
        # Get current timestamp and format dates
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        today = datetime.now().strftime('%b/%d/%Y')  # Format as Mon/Day/Year
        current_time = datetime.now().strftime('%H:%M:%S')
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Always insert a new record
        c.execute('''
            INSERT INTO new_people 
            (timestamp, date, time, job, sex, graduated, potential_to_meet, interest)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, today, current_time, job, sex, graduated, potential_to_meet, interest))
        
        conn.commit()
        conn.close()
        self._export_to_csv()

    def get_daily_data(self):
        today = datetime.now().strftime('%b/%d/%Y')  # Format as Mon/Day/Year
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(
            "SELECT * FROM mental_health WHERE date = ? ORDER BY time DESC",
            conn,
            params=(today,)
        )
        conn.close()
        return df

    def get_new_people_history(self):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(
            "SELECT date, time, COUNT(*) as new_people_count FROM new_people GROUP BY date, time ORDER BY date, time",
            conn
        )
        conn.close()
        return df

    def get_mental_status_history(self, days=30):
        """Get mental status history for the last n days"""
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql(
                'SELECT date, mental_status FROM mental_health ORDER BY date DESC LIMIT ?',
                conn,
                params=(days,)
            ) 