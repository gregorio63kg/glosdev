import sqlite3
import os

# Esta función es la que arma el tarantín de la base de datos
def init_db(db_path='data/glosdev.db'):
    # Si la carpeta no existe, la creamos de una vez para que no chille
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Nos conectamos al coroto de SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Aquí montamos la tabla con toda su parentela de campos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS functions (
        uid INTEGER PRIMARY KEY AUTOINCREMENT, -- El ID único de cada bicho
        name TEXT NOT NULL,                    -- El nombre de la función
        language TEXT NOT NULL,                -- ¿En qué lenguaje está el beta?
        syntax_example TEXT,                   -- El código de ejemplo bien fino
        library_module TEXT,                   -- ¿A qué librería pertenece?
        description TEXT,                      -- ¿Qué hace esta vaina?
        usage_history TEXT,                    -- ¿Dónde lo hemos usado antes?
        project_tags TEXT,                     -- Etiquetas para no perderse
        is_variant_of INTEGER,                 -- Por si es primo de otra función
        is_reserved BOOLEAN DEFAULT 0,         -- Si es palabra fija del lenguaje
        FOREIGN KEY (is_variant_of) REFERENCES functions (uid)
    )
    ''')
    
    # Guardamos los cambios y cerramos el boliche
    conn.commit()
    conn.close()

# Si ejecutas este archivo solo, inicializa todo el mandado
if __name__ == "__main__":
    init_db()
