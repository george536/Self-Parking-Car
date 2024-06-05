import sqlite3
import json

class ModelDatabaseMaker:
    def __init__(self, db_file="model_database.db"):
        self.TRAINING_DATA_FILE = "training_data/transforms.json"
        self.conn = sqlite3.connect(db_file)
        self.__create_table()

    def __create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                            id INTEGER PRIMARY KEY,
                            x REAL,
                            y REAL,
                            z REAL,
                            roll REAL,
                            pitch REAL,
                            yaw REAL,
                            in_view_spots TEXT
                        )''')
        self.conn.commit()

    def __add_entry(self, data_id, in_view_spots, pitch, roll, x, y, yaw, z):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO data VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (data_id, in_view_spots, pitch, roll, x, y, yaw, z))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def generate_model_db(self):
        with open(self.TRAINING_DATA_FILE, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                print(key)
                self.__add_entry(key, value["x"], value["y"], value["z"], value["roll"], value["pitch"], value["yaw"], value["in_view_spots"])

        self.close()