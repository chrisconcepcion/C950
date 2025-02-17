class Truck:
    def __init__(self, truck_id, capacity):
        self.id = truck_id
        self.capacity = capacity
        self.packages = []
        self.mileage = 0.0
        self.current_location = "HUB" # Default location.
        self.speed = 18  # In miles per hour... considered naming this class golf cart due to the speed.
        self.departure_time = None