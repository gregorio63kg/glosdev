import sqlite3
import os

def init_db(db_path='data/glosdev.db'):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS functions (
        uid INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        language TEXT NOT NULL,
        syntax_example TEXT,
        library_module TEXT,
        description TEXT,
        usage_history TEXT,
        project_tags TEXT,
        is_variant_of INTEGER,
        is_reserved BOOLEAN DEFAULT 0,
        FOREIGN KEY (is_variant_of) REFERENCES functions (uid)
    )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
