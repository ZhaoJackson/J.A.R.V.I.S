import sqlite3
import pandas as pd
from datetime import datetime
import os

class PhysicalHealthTracker:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'health_finance.db')
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'output')
        self._init_db()
        self._init_output_dir()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Drop existing table if it exists
        c.execute('DROP TABLE IF EXISTS physical_health')
        
        # Create new table with timestamp
        c.execute('''
            CREATE TABLE IF NOT EXISTS physical_health (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                kilometers_run REAL,
                meals TEXT,
                weight REAL,
                fitness TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _init_output_dir(self):
        """Initialize output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _export_to_csv(self):
        """Export physical health data to CSV"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM physical_health", conn)
        conn.close()
        
        if not df.empty:
            # Convert date to datetime for sorting
            df['date'] = pd.to_datetime(df['date'])
            # Sort by date and time
            df = df.sort_values(['date', 'time'])
            # Format date as Mon/Day/Year
            df['date'] = df['date'].dt.strftime('%b/%d/%Y')
            output_path = os.path.join(self.output_dir, 'physical_health.csv')
            df.to_csv(output_path, index=False)

    def save_daily_data(self, kilometers_run, meals, weight, fitness):
        """Save daily physical health data"""
        # Get current timestamp and format dates
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        today = datetime.now().strftime('%b/%d/%Y')  # Format as Mon/Day/Year
        current_time = datetime.now().strftime('%H:%M:%S')
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Always insert a new record
        c.execute('''
            INSERT INTO physical_health 
            (timestamp, date, time, kilometers_run, meals, weight, fitness)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, today, current_time, kilometers_run, meals, weight, fitness))
        
        conn.commit()
        conn.close()
        self._export_to_csv()

    def get_daily_data(self):
        """Get physical health data for a specific date"""
        today = datetime.now().strftime('%b/%d/%Y')  # Format as Mon/Day/Year
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(
            "SELECT * FROM physical_health WHERE date = ? ORDER BY time DESC",
            conn,
            params=(today,)
        )
        conn.close()
        return df

    def get_weight_history(self):
        """Get weight history for the last n days"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(
            "SELECT date, time, weight FROM physical_health ORDER BY date, time",
            conn
        )
        conn.close()
        return df

    def get_running_history(self):
        """Get running history for the last n days"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(
            "SELECT date, time, kilometers_run FROM physical_health ORDER BY date, time",
            conn
        )
        conn.close()
        return df 