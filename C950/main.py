# Name: Christopher Concepcion.
# Student ID: 012541909
from datetime import datetime, timedelta
from package import Package
from truck import Truck
from hash_table import HashTable
import csv

class WGUPS:
    # Initial class with hashtable of size 4 and our 3 trucks.
    def __init__(self):
        self.hash_table = HashTable(40)
        self.address_data = []
        self.distance_data = []
        self.total_mileage = 0
        
        # Initialize trucks.
        self.trucks = [
            Truck(1, 16),  # First truck
            Truck(2, 16),  # Second truck
            Truck(3, 16)   # Third truck
        ]
        
        # Set departure times on trucks.
        # Truck 1 - Priority, early delivery times.
        self.trucks[0].departure_time = datetime.strptime("8:00 AM", "%I:%M %p")
        # Truck 2 - Has constraints where packages must be delivered together or packages won't
        # arrive at depot until 9:05. Last minute additions.
        self.trucks[1].departure_time = datetime.strptime("9:05 AM", "%I:%M %p")
        # Truck 3 - the EOD delivery truck, non-priority packages.
        self.trucks[2].departure_time = datetime.strptime("10:20 AM", "%I:%M %p")

    def load_address_data(self):
        with open('Address.csv') as file:
            reader = csv.reader(file)
            self.address_data = list(reader)

    def load_distance_data(self):
        with open('Distance.csv') as file:
            reader = csv.reader(file)
            self.distance_data = [row for row in reader]

    def load_package_data(self):
        with open('Package.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                package = Package(
                    int(row[0]),
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    float(row[6].split()[0]),
                    row[7] if len(row) > 7 else ""
                )
                self.hash_table.insert(package.id, package)

    def get_address_index(self, address):
        for addr in self.address_data:
            if address in addr[2]:  # Check street address portion.
                return int(addr[0])
        return -1

    def get_distance(self, from_address, to_address):
        from_index = self.get_address_index(from_address)
        to_index = self.get_address_index(to_address)
        
        if from_index == -1 or to_index == -1:
            return float('inf')
            
        distance = self.distance_data[from_index][to_index]
        if distance == '':
            distance = self.distance_data[to_index][from_index]
        return float(distance)

    # This is part our Djikstra Algorthm.
    # Returns the package and distance based on current location.
    def find_shortest_path(self, current_location, undelivered_packages):
        shortest_distance = float('inf')
        next_package = None
        
        for package_id in undelivered_packages:
            package = self.hash_table.lookup(package_id)
            if package:
                distance = self.get_distance(current_location, package.address)
                if distance < shortest_distance:
                    shortest_distance = distance
                    next_package = package
                    
        return next_package, shortest_distance

    def deliver_packages(self, truck, current_time):
        if not truck.packages:
            return

        # Start at the hub address.
        current_location = "4001 South 700 East"
        simulation_time = truck.departure_time

        # Copy packages and start delivering the packages.
        undelivered = truck.packages.copy()

        while undelivered:
            # Find the closest package based on distance and return it along with the distance.
            next_package, distance = self.find_shortest_path(current_location, undelivered)
            
            # If we found our next closest package...
            if next_package:
                # Update travel and simulation time.
                travel_time = timedelta(hours=distance / 18)  # 18 mph
                simulation_time += travel_time

                # If our similation time is earlier than current time or the same time
                # We consider our package delivered, update delivery time and update
                # our truck mileage.
                if simulation_time <= current_time:
                    next_package.status = "Delivered"
                    next_package.delivery_time = simulation_time
                    truck.mileage += distance
                # Otherwise we don't consider the package delivered.
                else:
                    next_package.status = "En route"
                

                # Now we set our next address to our current location
                # and remove our package from undelivered.
                current_location = next_package.address
                undelivered.remove(next_package.id)

                # Handle package #9 address correction
                if next_package.id == 9 and current_time >= datetime.strptime("10:20 AM", "%I:%M %p"):
                    next_package.address = "410 S State St"
                    next_package.zip_code = "84111"
            else:
                break

        # Return to hub
        return_distance = self.get_distance(current_location, "4001 South 700 East")
        if return_distance != float('inf'):
            truck.mileage += return_distance

    def load_trucks(self):
        # First truck - priority packages. 
        # Package have constraints such as must be delivered together: 13,14,15,16,19,20
        # so we put them on the same truck.
        self.trucks[0].packages = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
        i = 0
        while i < len(self.trucks[0].packages):
            package = self.hash_table.lookup(self.trucks[0].packages[i])
            package.truck = self.trucks[0]
            i += 1
        
        # Second truck - packages that can only be on truck 2 and those which won't arrive
        # at the depot until 9:05 am.
        self.trucks[1].packages = [3, 6, 18, 25, 28, 32, 36, 38]
        i = 0
        while i < len(self.trucks[1].packages):
            package = self.hash_table.lookup(self.trucks[1].packages[i])
            package.truck = self.trucks[1]
            i += 1
        
        # Third truck - remaining packages
        self.trucks[2].packages = [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 26, 27, 33, 35, 39]
        i = 0
        while i < len(self.trucks[2].packages):
            package = self.hash_table.lookup(self.trucks[2].packages[i])
            package.truck = self.trucks[2]
            i += 1
        
    # Effectively simulates deliveries based on current time.
    # If a current time is prior to a truck departure time it won't make any deliveries.
    def simulate_deliveries(self, current_time):
        # Reset package statuses
        for i in range(1, 41):
            package = self.hash_table.lookup(i)
            if package:
                package.status = "At hub"
                package.delivery_time = None

        # Reset mileage and simulate each truck's deliveries.
        for truck in self.trucks:
            # Reset milage.            
            truck.mileage = 0
            # Start deliveries for a truck if departure time has passed.
            if current_time > truck.departure_time:
                self.deliver_packages(truck, current_time)

        self.total_mileage = sum(truck.mileage for truck in self.trucks)

    # Display package data.
    def display_package_data(self, package):
        print(f"Package ID: {package.id}")
        print(f"Address: {package.address}")
    
        print(f"Deadline: {package.deadline}")
        print(f"Delivery Status: {package.status}")
        if package.truck:
            print(f"Truck Number: {package.truck.id}")
        else:
            print(f"Truck Number: Not assigned to truck as of yet.")
        if package.delivery_time:
            print(f"Delivery Time: {package.delivery_time.strftime('%I:%M %p')}")
        else:
            print(f"Delivery Time: Unavailable")
        print("-" * 30)

def main():
    wgups = WGUPS()
    wgups.load_address_data()
    wgups.load_distance_data()
    wgups.load_package_data()
    wgups.load_trucks()

    while True:
        print("\nWGUPS Package Tracking System")
        print("1. Check status of all packages at a specific time")
        print("2. Check status of a single package at a specific time")
        print("3. View total mileage")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice in ['1', '2']:
            time_str = input("Enter time (HH:MM AM/PM): ")
            try:
                current_time = datetime.strptime(time_str, "%I:%M %p")
                wgups.simulate_deliveries(current_time)
                
                if choice == '1':
                    print(f"\nPackage Status at {time_str}")
                    print("-" * 50)
                    for i in range(1, 41):
                        package = wgups.hash_table.lookup(i)
                        if package:
                            wgups.display_package_data(package)
                    package_id = int(input("Enter package ID (1-40): "))
                    package = wgups.hash_table.lookup(package_id)
                    if package:
                        wgups.display_package_data(package)
                    else:
                        print("Package not found")
            except ValueError:
                print("Invalid time format. Please use HH:MM AM/PM")
        
        elif choice == '3':
            wgups.simulate_deliveries(datetime.strptime("11:00 PM", "%I:%M %p"))
            print(f"\nTotal mileage for all trucks: {wgups.total_mileage:.1f} miles")
        
        elif choice == '4':
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()