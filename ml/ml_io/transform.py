class Transform:
    def __init__(self, x, y, z, roll, pitch, yaw):
        self.x = x
        self.y = y
        self.z = z
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
        
    def calculate_distance(self, other_transform):
        distance = ((self.x - other_transform.x) ** 2 +
                    (self.y - other_transform.y) ** 2 +
                    (self.z - other_transform.z) ** 2) ** 0.5
        return distance