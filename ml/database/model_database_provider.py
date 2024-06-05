import sqlite3

class ModelDatabaseProvider:
    def __init__(self, db_file="model_database.db"):
        self.conn = sqlite3.connect(db_file)

    def get_all_image_ids(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM Images")
        return cursor.fetchone()

    def get_parking_spot_corners(self, spot_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT x_BL, y_BL, x_UL, y_UL, x_UR, y_UR, x_BR, y_BR FROM Spots WHERE id = ?", (spot_id,))
        return cursor.fetchone()

    def get_all_in_view_spots(self, image_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT in_view_spots FROM Images WHERE id = ?", (image_id,))
        result = cursor.fetchone()
        if result:
            return result[0].split(",")
        return []

    def get_car_transform(self, image_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT x, y, z, roll, pitch, yaw FROM Images WHERE id = ?", (image_id,))
        return cursor.fetchone()
    
    def close(self):
        self.conn.close()