class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes):
        self.id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = "At hub" # Default status. 
        self.delivery_time = None
        self.truck = None