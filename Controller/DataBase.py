import sqlite3

class DataBase:
    def __init__(self, database_name='database.db'):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS programas (
                                id INTEGER PRIMARY KEY,
                                nome_programa TEXT,
                                setpoint_quente REAL,
                                setpoint_fria REAL,
                                tempo_quente INTEGER,
                                tempo_fria INTEGER,
                                qtd_ciclos INTEGER,
                                potencia_ventilador INTEGER,
                                controle_proporcional REAL,
                                inicio_ciclo TEXT,
                                estabilizar_temperatura TEXT)''')
        self.conn.commit()

    def create_record(self, data):
        self.cursor.execute('''INSERT INTO programas 
                               (nome_programa, setpoint_quente, setpoint_fria, 
                               tempo_quente, tempo_fria, qtd_ciclos, potencia_ventilador, 
                               controle_proporcional, inicio_ciclo, estabilizar_temperatura) 
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
        self.conn.commit()

    def update_record(self, record_id, data):
        query = '''UPDATE programas SET 
                   nome_programa=?, setpoint_quente=?, setpoint_fria=?, 
                   tempo_quente=?, tempo_fria=?, qtd_ciclos=?, potencia_ventilador=?, 
                   controle_proporcional=?, inicio_ciclo=?, estabilizar_temperatura=?
                   WHERE id=?'''
        self.cursor.execute(query, data + [record_id])
        self.conn.commit()

    def delete_record(self, record_id):
        query = 'DELETE FROM programas WHERE id=?'
        self.cursor.execute(query, (record_id,))
        self.conn.commit()

    def search_record(self, record_id):
        query = 'SELECT * FROM programas WHERE id=?'
        self.cursor.execute(query, (record_id,))
        return self.cursor.fetchone()
    
    def search_record_by_name(self, name):
        query = 'SELECT * FROM programas WHERE nome_programa=?'
        self.cursor.execute(query, (name,))
        return self.cursor.fetchone()

    def get_all_records(self):
        query = 'SELECT * FROM programas'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()
