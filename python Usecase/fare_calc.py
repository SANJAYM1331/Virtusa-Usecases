import re

#  Custom Exception (Exception Handling) 

class InvalidVehicleError(Exception):
    def __init__(self, vtype):
        super().__init__(f"Service Not Available for '{vtype}'.")


#  Base Class (Encapsulation + Abstraction) 

class Vehicle:

    def __init__(self, vtype, rate):
        self.__vtype = vtype       
        self.__rate  = rate        

    def get_type(self):
        return self.__vtype

    def get_rate(self):
        return self.__rate

    def describe(self):
        return f"{self.__vtype} at Rs.{self.__rate}/km"


#  Child Classes (Inheritance + Polymorphism) 

class EconomyVehicle(Vehicle):
    def __init__(self):
        super().__init__("Economy", 10)

    def describe(self):                          # overriding parent method
        return "Economy - Budget friendly at Rs.10/km"


class PremiumVehicle(Vehicle):
    def __init__(self):
        super().__init__("Premium", 18)

    def describe(self):
        return "Premium - Comfortable ride at Rs.18/km"


class SuvVehicle(Vehicle):
    def __init__(self):
        super().__init__("SUV", 25)

    def describe(self):
        return "SUV - Spacious ride at Rs.25/km"


#  Vehicle lookup dictionary 

vehicle_map = {
    "Economy" : EconomyVehicle,
    "Premium" : PremiumVehicle,
    "Suv"     : SuvVehicle
}


#  Trip Class (Instance data + methods) 

class Trip:

    def __init__(self, vehicle, km, hour):
        self.__vehicle   = vehicle
        self.__km        = km
        self.__hour      = hour
        self.__base_fare = 0.0
        self.__surge     = 1.0
        self.__total     = 0.0

    def __is_peak_hour(self):                   
        return 17 <= self.__hour <= 20

    def calculate(self):
        self.__base_fare = self.__km * self.__vehicle.get_rate()
        self.__surge     = 1.5 if self.__is_peak_hour() else 1.0
        self.__total     = self.__base_fare * self.__surge

    def print_receipt(self):
        print("     CityCab Price Receipt")

        print(f"Vehicle    : {self.__vehicle.get_type()}")
        print(f"Description: {self.__vehicle.describe()}")
        print(f"Distance   : {self.__km} km")
        print(f"Base Fare  : Rs.{self.__base_fare:.2f}")
        if self.__surge > 1.0:
            print(f"Surge      : 1.5x  (Peak Hours 5PM - 8PM)")
        else:
            print(f"Surge      : None")
        print(f"Total Fare : Rs.{self.__total:.2f}")


#  InputHandler Class (Regex validation)

class InputHandler:

    def __init__(self):
        self.__km_pattern      = re.compile(r"^\d+(\.\d+)?$")  # 10 or 5.5
        self.__vehicle_pattern = re.compile(r"^[A-Za-z]+$")    # letters only
        self.__hour_pattern    = re.compile(r"^\d{1,2}:[0-5]\d$")       

    def get_km(self):
        while True:
            raw = input("Enter distance in km     : ").strip()
            if not self.__km_pattern.match(raw):
                print("Invalid input. Enter a number like 10 or 5.5")
                continue
            km = float(raw)
            if km <= 0:
                print("Distance must be greater than 0.")
            else:
                return km

    def get_vehicle_type(self):
        print("Available vehicles       :", list(vehicle_map.keys()))
        while True:
            raw = input("Enter vehicle type       : ").strip()
            if not self.__vehicle_pattern.match(raw):
                print("Vehicle type must contain letters only.")
                continue
            vtype = raw.capitalize()
            if vtype in vehicle_map:
                return vtype
            else:
                raise InvalidVehicleError(vtype)

    def get_hour(self):
        while True:
            raw = input("Enter time (HH:MM) : ").strip()

            if not self.__hour_pattern.match(raw):
                print("Invalid input. Enter time like 09:30 or 17:45")
                continue

            hour, minute = map(int, raw.split(":"))

            if 0 <= hour <= 23:
                return hour
            else:
                print("Hour must be between 0 and 23.")


#  Main Program 

print("=" * 30)
print("   CityCab Fare Calculator")
print("=" * 30)

handler = InputHandler()

km    = handler.get_km()

try:
    vtype = handler.get_vehicle_type()
except InvalidVehicleError as e:
    print("Error:", e)
    exit()

hour = handler.get_hour()

vehicle = vehicle_map[vtype]()
trip    = Trip(vehicle, km, hour)
trip.calculate()
trip.print_receipt()
