vehicle_rates = {
    'Economy': 10,
    'Premium': 18,
    'SUV': 25,
    'Sedan': 30
}

def calculate_fare(km, vehicle_type, hour):
    
    if vehicle_type not in vehicle_rates:
        raise ValueError("Service Not Available for vehicle type: " + vehicle_type)
    
    rate = vehicle_rates[vehicle_type]
    base_fare = km * rate
    
    surge_multiplier = 1.0
    if hour >= 17 and hour <= 20:
        surge_multiplier = 1.5
    
    final_fare = base_fare * surge_multiplier
    return base_fare, surge_multiplier, final_fare

print("       Welcome to CityCab FareCalc      ")

km = float(input("Enter distance in KM        : "))

print("Available vehicle types: Economy, Premium, SUV, Sedan")
vehicle_type = input("Enter vehicle type          : ").strip().capitalize()

hour = int(input("Enter hour of day (0-23)    : "))
try:
    base_fare, surge_multiplier, final_fare = calculate_fare(km, vehicle_type, hour)
    print("           Price Receipt             ")
    print(f" Vehicle Type     : {vehicle_type}")
    print(f" Distance         : {km} km")
    print(f" Rate per KM      : ₹{vehicle_rates[vehicle_type]}")
    print(f" Base Fare        : ₹{base_fare:.2f}")
    
    if surge_multiplier > 1.0:
        print(f" Surge Pricing  : {surge_multiplier}x (Peak Hours!)")
    else:
        print(f" Surge Pricing    : No Surge")
    print(f" Total Fare       : ₹{final_fare:.2f}")
    
except ValueError as e:
    print("\nError:", e)
    print("Please choose from: Economy, Premium, SUV, Sedan")