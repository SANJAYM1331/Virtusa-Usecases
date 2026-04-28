import re
import datetime

# Custom Exception Classes
# (Inheritance - extends Exception)

class InvalidVehicleError(Exception):
    def __init__(self, vtype):
        self.vtype = vtype
        super().__init__(f"Sorry, we don't support vehicle type: {vtype}")


class InvalidTimeError(Exception):
    def __init__(self):
        super().__init__("Invalid time. Use HH:MM or a number between 0 and 23.")


class InvalidDistanceError(Exception):
    def __init__(self):
        super().__init__("Distance must be greater than 0.")


# Base Class - Vehicle
# (Abstraction + Encapsulation)

class Vehicle:

    def __init__(self, vtype, rate_per_km):
        self.__vtype       = vtype
        self.__rate_per_km = rate_per_km

    def get_type(self):
        return self.__vtype

    def get_rate(self):
        return self.__rate_per_km

    def describe(self):
        return f"{self.__vtype} at Rs.{self.__rate_per_km}/km"


# Child Classes
# (Inheritance + Polymorphism)

class EconomyVehicle(Vehicle):
    def __init__(self):
        super().__init__("Economy", 10)

    def describe(self):
        return "Economy - Budget friendly ride at Rs.10/km"


class PremiumVehicle(Vehicle):
    def __init__(self):
        super().__init__("Premium", 18)

    def describe(self):
        return "Premium - Comfortable ride at Rs.18/km"


class SuvVehicle(Vehicle):
    def __init__(self):
        super().__init__("Suv", 25)

    def describe(self):
        return "SUV - Spacious ride at Rs.25/km"


class SedanVehicle(Vehicle):
    def __init__(self):
        super().__init__("Sedan", 30)

    def describe(self):
        return "Sedan - Stylish ride at Rs.30/km"


# Trip Class
# (Instance data, encapsulation)

class Trip:

    def __init__(self, vehicle, km, hour):
        self.__vehicle = vehicle
        self.__km      = km
        self.__hour    = hour
        self.__base    = 0.0
        self.__surge   = 1.0
        self.__total   = 0.0

    def __is_peak_hour(self):
        if self.__hour >= 17 and self.__hour <= 20:
            return True
        elif self.__hour >= 8 and self.__hour <= 10:
            return True
        else:
            return False

    def calculate(self):
        self.__base  = self.__km * self.__vehicle.get_rate()
        self.__surge = 1.5 if self.__is_peak_hour() else 1.0
        self.__total = self.__base * self.__surge

    def get_base(self):
        return self.__base

    def get_surge(self):
        return self.__surge

    def get_total(self):
        return self.__total

    def get_vehicle(self):
        return self.__vehicle

    def get_km(self):
        return self.__km

    def get_summary(self):
        return {
            "vehicle" : self.__vehicle.get_type(),
            "km"      : self.__km,
            "total"   : self.__total
        }


# Receipt Class
# (File I/O - open, write, read, close, finally)

class Receipt:

    def __init__(self, trip):
        self.__trip     = trip
        self.__filename = "receipt.txt"

    def print_receipt(self):
        trip = self.__trip
        print("\n" + "-" * 35)
        print("      CityCab Fare Receipt")
        print("-" * 35)
        print(f"Vehicle    : {trip.get_vehicle().get_type()}")
        print(f"Description: {trip.get_vehicle().describe()}")
        print(f"Distance   : {trip.get_km()} km")
        print(f"Base Fare  : Rs.{trip.get_base():.2f}")
        if trip.get_surge() > 1.0:
            print(f"Surge      : 1.5x (Peak Hours)")
        else:
            print(f"Surge      : None")
        print("-" * 35)
        print(f"Total      : Rs.{trip.get_total():.2f}")
        print("-" * 35)

    def save_to_file(self):
        trip = self.__trip
        try:
            file = open(self.__filename, "w")
            file.write("CityCab Fare Receipt\n")
            file.write("-" * 30 + "\n")
            file.write(f"Date       : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            file.write(f"Vehicle    : {trip.get_vehicle().get_type()}\n")
            file.write(f"Distance   : {trip.get_km()} km\n")
            file.write(f"Base Fare  : Rs.{trip.get_base():.2f}\n")
            file.write(f"Surge      : {'1.5x Peak Hours' if trip.get_surge() > 1 else 'None'}\n")
            file.write(f"Total      : Rs.{trip.get_total():.2f}\n")
            file.write("-" * 30 + "\n")
            file.close()
            print(f"Receipt saved to {self.__filename}")
        except IOError as e:
            print("Could not save receipt:", e)
        finally:
            print("Receipt process complete.")

    def read_from_file(self):
        try:
            file    = open(self.__filename, "r")
            content = file.read()
            file.close()
            print("\n    Saved Receipt    ")
            print(content)
        except FileNotFoundError:
            print("No saved receipt found.")



# VehicleFactory Class
# (Class methods and class data)

class VehicleFactory:

    __vehicle_map = {
        'Economy' : EconomyVehicle,
        'Premium' : PremiumVehicle,
        'Suv'     : SuvVehicle,
        'Sedan'   : SedanVehicle
    }

    @classmethod
    def get_vehicle(cls, vtype):
        if vtype not in cls.__vehicle_map:
            raise InvalidVehicleError(vtype)
        return cls.__vehicle_map[vtype]()

    @classmethod
    def get_available_types(cls):
        return list(cls.__vehicle_map.keys())

    @classmethod
    def remove_vehicle(cls, vtype):
        if vtype in cls.__vehicle_map:
            del cls.__vehicle_map[vtype]
            print(f"{vtype} removed from service.")
        else:
            print(f"{vtype} not found.")


# InputHandler Class
# (Regex validation, while loops,
#  exception handling, string operations)

class InputHandler:

    def __init__(self):
        self.__time_pattern = re.compile(r"^\d{1,2}:[0-5]\d$")
        self.__km_pattern      = re.compile(r"^\d+(\.\d+)?$")
        self.__vehicle_pattern = re.compile(r"^[A-Za-z]+$")

    def __is_valid_time_format(self, time_input):
        return bool(self.__time_pattern.match(time_input))

    def __is_valid_km_format(self, raw_input):
        return bool(self.__km_pattern.match(raw_input))

    def __is_valid_vehicle_format(self, raw_input):
        return bool(self.__vehicle_pattern.match(raw_input))

    def parse_time(self, time_input):
        if ":" in time_input:
            parts   = time_input.split(":")
            hours   = int(parts[0])
            minutes = int(parts[1])
            # Validate minutes range
            if minutes > 59:
                raise InvalidTimeError()
            return hours + minutes / 60
        else:
            return float(time_input)

    def get_km(self):
        while True:
            try:
                raw = input("Enter distance in km  : ").strip()
                if not self.__is_valid_km_format(raw):
                    print("Invalid input. Enter a number like 10 or 5.5")
                    continue
                km = float(raw)
                if km <= 0:
                    raise InvalidDistanceError()
                return km
            except InvalidDistanceError as e:
                print("Error:", e)

    def get_vehicle_type(self):
        available = VehicleFactory.get_available_types()
        print("Available vehicles    :", available)
        while True:
            try:
                vtype = input("Enter vehicle type    : ").strip().capitalize()
                if not self.__is_valid_vehicle_format(vtype):
                    print("Vehicle type must contain letters only.")
                    continue
                VehicleFactory.get_vehicle(vtype)
                return vtype
            except InvalidVehicleError as e:
                print("Error:", e)

    def get_time(self):
        while True:
            try:
                time_input = input("Enter time (HH:MM or 0-23): ").strip()
                if ":" in time_input:
                    if not self.__is_valid_time_format(time_input):
                        print("Invalid format. Use HH:MM in the range of 0-23:0-59")
                        continue
                hour = self.parse_time(time_input)
                if 0 <= hour <= 23.99:
                    return hour
                else:
                    raise InvalidTimeError()
            except InvalidTimeError as e:
                print("Error:", e)
            except ValueError:
                print("Invalid format. Try again.")


# TripHistory Class
# (Lists, list methods, for loop, range())

class TripHistory:

    def __init__(self):
        self.__history = []

    def add(self, trip):
        self.__history.append(trip.get_summary())

    def show(self):
        if len(self.__history) == 0:
            print("No trips taken yet.")
            return
        print("\n--- Trip History ---")
        for i in range(len(self.__history)):
            trip = self.__history[i]
            print(f"{i+1}. {trip['vehicle']} | {trip['km']}km | Rs.{trip['total']:.2f}")
        print("--------------------")
        print(f"Total trips : {len(self.__history)}")

        total_spent = 0
        for trip in self.__history:
            total_spent += trip['total']
        print(f"Total spent : Rs.{total_spent:.2f}")


# CityCabApp - Main Controller Class
# (Ties everything together)

class CityCabApp:

    def __init__(self):
        self.__input_handler = InputHandler()
        self.__history       = TripHistory()
        self.__app_name      = r"CityCab Fare Calculator"

    def __del__(self):
        print("\nCityCab session ended. Have a safe journey!")

    def __run_trip(self):
        km    = self.__input_handler.get_km()
        vtype = self.__input_handler.get_vehicle_type()
        hour  = self.__input_handler.get_time()

        try:
            vehicle = VehicleFactory.get_vehicle(vtype)
            trip    = Trip(vehicle, km, hour)
            trip.calculate()

            receipt = Receipt(trip)
            receipt.print_receipt()

            self.__history.add(trip)

            save = input("\nSave receipt to file? (yes/no): ").strip().lower()
            if save == "yes":
                receipt.save_to_file()

            read = input("Read saved receipt?   (yes/no): ").strip().lower()
            if read == "yes":
                receipt.read_from_file()

        except InvalidVehicleError as e:
            print("Error:", e)
        except Exception as e:
            print("Unexpected error:", e)

    def run(self):
        print("=" * 35)
        print(f"     {self.__app_name}")
        print("=" * 35)

        while True:
            print("\n1. Calculate Fare")
            print("2. View Trip History")
            print("3. Exit")

            choice = input("\nEnter choice (1/2/3): ").strip()

            if choice == "1":
                self.__run_trip()
            elif choice == "2":
                self.__history.show()
            elif choice == "3":
                print("\nThank you for using CityCab. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2 or 3.")


# Entry point
# (Module concept)

if __name__ == "__main__":
    app = CityCabApp()
    app.run()
