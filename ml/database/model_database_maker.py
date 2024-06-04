import sqlite3
import json

class ModelDatabaseMaker:
    def __init__(self, db_file="model_database.db"):
        self.TRAINING_DATA_FILE = "training_data/transforms.json"
        self.PARKING_SPOTS_DATA_FILE = "parking_spot_labeller/spots_data.json"
        self.conn = sqlite3.connect(db_file)
        self.__create_images_table()
        self.__create_spots_table()

    def __create_images_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Images (
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

    def __create_spots_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Spots (
                            id INTEGER PRIMARY KEY,
                            x_BL REAL,
                            y_BL REAL,
                            x_UL REAL,
                            y_UL REAL,
                            x_UR REAL,
                            y_UR REAL,
                            x_BR REAL,
                            y_BR REAL
                        )''')
        self.conn.commit()

    def __add_image_entry(self, image_id, in_view_spots, pitch, roll, x, y, yaw, z):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Images VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (image_id, in_view_spots, pitch, roll, x, y, yaw, z))
        self.conn.commit()

    def __add_spot_entry(self, spot_id, x_BL, y_BL, x_UL, y_UL, x_UR, y_UR, x_BR, y_BR):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Spots VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (spot_id, x_BL, y_BL, x_UL, y_UL, x_UR, y_UR, x_BR, y_BR))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def generate_model_db(self):
        with open(self.TRAINING_DATA_FILE, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                print(key)
                self.__add_image_entry(key, value["x"], value["y"], value["z"], value["roll"], value["pitch"], value["yaw"], value["in_view_spots"])

        with open(self.PARKING_SPOTS_DATA_FILE, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                print(key)
                self.__add_spot_entry(int(key), value[0][0], value[0][1], value[1][0], value[1][1], value[2][0], value[2][1], value[3][0], value[3][1])
            
        self.close()