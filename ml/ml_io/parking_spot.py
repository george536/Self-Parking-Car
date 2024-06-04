class ParkingSpot:
    def __init__(self, spot_id, transform):
        self.spot_id = spot_id
        self.transform = transform

    def get_spot_id(self):
        return self.spot_id

    def get_transform(self):
        return self.transform

    def set_transform(self, new_transform):
        self.transform = new_transform