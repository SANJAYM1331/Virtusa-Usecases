vehicle_rates = {
    'Economy': 10,
    'Premium': 18,
    'Suv': 25,
    'Sedan': 30
}

def calc_fare(km, vtype, hour):
    if vtype not in vehicle_rates:
        raise ValueError("Sorry, we don't support: " + vtype)
    
    rate = vehicle_rates[vtype]
    base = km * rate
    surge = 1.5 if 17 <= hour <= 20 else 1.0
    return base, surge, base * surge

print("    CityCab Fare Calculator    \n")

km = float(input("Distance (km): "))
print("Vehicle options: Economy, Premium, SUV, Sedan")
vtype = input("Vehicle type: ").strip().capitalize()
time_input = input("Enter time (HH:MM): ").strip()
hours, minutes = time_input.split(":")
hour = int(hours) + int(minutes) / 60

try:
    base, surge, total = calc_fare(km, vtype, hour)

    print("\n   Fare Breakdown    ")
    print(f"Vehicle   : {vtype}")
    print(f"Distance  : {km} km")
    print(f"Rate/km   : Rs.{vehicle_rates[vtype]}")
    print(f"Base Fare : Rs.{base:.2f}")
    print(f"Surge     : {'1.5x (peak hours)' if surge > 1 else 'None'}")
    print(f"Total     : Rs.{total:.2f}")

except ValueError as e:
    print("Error:", e)
