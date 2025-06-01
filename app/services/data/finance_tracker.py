import sqlite3
import pandas as pd
from datetime import datetime
import os

class FinanceTracker:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'health_finance.db')
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'output')
        self._init_db()
        self._init_output_dir()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Drop existing table if it exists
        c.execute('DROP TABLE IF EXISTS personal_finance')
        
        # Create new table with timestamp
        c.execute('''
            CREATE TABLE IF NOT EXISTS personal_finance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                amount REAL,
                transaction_type TEXT,
                category TEXT,
                card_owner TEXT,
                card_type TEXT,
                debit_total REAL,
                credit_total REAL
            )
        ''')
        conn.commit()
        conn.close()

    def _init_output_dir(self):
        """Initialize output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _export_to_csv(self):
        """Export finance data to CSV"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM personal_finance", conn)
        conn.close()
        
        if not df.empty:
            # Convert date to datetime for sorting
            df['date'] = pd.to_datetime(df['date'])
            # Sort by date and time
            df = df.sort_values(['date', 'time'])
            # Format date as Mon/Day/Year
            df['date'] = df['date'].dt.strftime('%b/%d/%Y')
            output_path = os.path.join(self.output_dir, 'personal_finance.csv')
            df.to_csv(output_path, index=False)

    def save_daily_data(self, amount, transaction_type, category, card_owner, debit_total, credit_total):
        """Save daily finance data"""
        # Get current timestamp and format dates
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        today = datetime.now().strftime('%b/%d/%Y')  # Format as Mon/Day/Year
        current_time = datetime.now().strftime('%H:%M:%S')
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Always insert a new record
        c.execute('''
            INSERT INTO personal_finance 
            (timestamp, date, time, amount, transaction_type, category, card_owner, card_type, 
             debit_total, credit_total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, today, current_time, amount, transaction_type, category, card_owner,
              'Credit' if card_owner == 'Family' else 'Debit',
              debit_total, credit_total))
        
        conn.commit()
        conn.close()
        self._export_to_csv()

    def get_daily_data(self):
        """Get finance data for a specific date"""
        today = datetime.now().strftime('%b/%d/%Y')  # Format as Mon/Day/Year
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(
            "SELECT * FROM personal_finance WHERE date = ? ORDER BY time DESC",
            conn,
            params=(today,)
        )
        conn.close()
        return df

    def get_transaction_history(self):
        """Get transaction history for the last n days"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(
            "SELECT date, time, COUNT(*) as transaction_count FROM personal_finance GROUP BY date, time ORDER BY date, time",
            conn
        )
        conn.close()
        return df

    def get_balance_history(self):
        """Get balance history for the last n days"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(
            "SELECT date, time, debit_total, credit_total FROM personal_finance ORDER BY date, time",
            conn
        )
        conn.close()
        return df

    def get_daily_transaction_count(self, date=None):
        """Get transaction count for a specific date"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT transaction_count FROM personal_finance WHERE date = ?', (date,))
            result = cursor.fetchone()
            return result[0] if result else 0 