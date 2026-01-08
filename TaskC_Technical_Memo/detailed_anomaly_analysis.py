"""
Detailed Anomaly Analysis - Finding operational inefficiencies
"""

import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('../data/mindx test dataset.csv')

# Calculate fuel efficiency and CO2 per km
df['fuel_efficiency'] = df['fuel_consumption'] / df['distance']
df['co2_per_km'] = df['CO2_emissions'] / df['distance']

print("="*70)
print("DETAILED ANOMALY ANALYSIS")
print("="*70)

# Find vessels with highest fuel consumption relative to distance
print("\nTop 10 Vessels with Highest Fuel Efficiency (L/km):")
print("="*70)

top_fuel = df.nlargest(10, 'fuel_efficiency')[
    ['ship_id', 'ship_type', 'route_id', 'month', 'distance', 
     'fuel_consumption', 'fuel_efficiency', 'CO2_emissions', 'co2_per_km',
     'weather_conditions', 'engine_efficiency', 'fuel_type']
]

for idx, row in top_fuel.iterrows():
    print(f"\nVessel: {row['ship_id']} ({row['ship_type']})")
    print(f"Route: {row['route_id']}, Month: {row['month']}")
    print(f"Distance: {row['distance']:.2f} km | Fuel: {row['fuel_consumption']:.2f} L | Efficiency: {row['fuel_efficiency']:.3f} L/km")
    print(f"CO2: {row['CO2_emissions']:.2f} kg | CO2/km: {row['co2_per_km']:.2f} kg/km")
    print(f"Weather: {row['weather_conditions']} | Engine Eff: {row['engine_efficiency']:.2f}% | Fuel Type: {row['fuel_type']}")
    
    # Calculate deviation
    ship_type_avg = df[df['ship_type'] == row['ship_type']]['fuel_efficiency'].mean()
    deviation = ((row['fuel_efficiency'] - ship_type_avg) / ship_type_avg) * 100
    print(f"Deviation from {row['ship_type']} average: {deviation:+.1f}%")
    print("-"*70)

# Analyze by weather conditions
print("\n" + "="*70)
print("FUEL EFFICIENCY BY WEATHER CONDITIONS")
print("="*70)
weather_analysis = df.groupby(['ship_type', 'weather_conditions'])['fuel_efficiency'].agg(['mean', 'count'])
print(weather_analysis)

# Find specific anomalous patterns
print("\n" + "="*70)
print("ANOMALOUS PATTERNS ANALYSIS")
print("="*70)

# Pattern 1: High fuel consumption in calm weather
calm_high_fuel = df[(df['weather_conditions'] == 'Calm') & 
                    (df['fuel_efficiency'] > df.groupby('ship_type')['fuel_efficiency'].transform('mean') * 1.3)]

print(f"\nVessels with unusually high fuel consumption in CALM weather: {len(calm_high_fuel)}")
if len(calm_high_fuel) > 0:
    print("\nTop 5 Examples:")
    for idx, row in calm_high_fuel.nlargest(5, 'fuel_efficiency').iterrows():
        print(f"  {row['ship_id']} ({row['ship_type']}) - {row['fuel_efficiency']:.2f} L/km in {row['month']}")
        print(f"    Route: {row['route_id']}, Engine Eff: {row['engine_efficiency']:.1f}%")

# Pattern 2: Low engine efficiency with high fuel consumption
low_engine_high_fuel = df[(df['engine_efficiency'] < 75) & 
                          (df['fuel_efficiency'] > df.groupby('ship_type')['fuel_efficiency'].transform('mean'))]

print(f"\n\nVessels with low engine efficiency (<75%) AND high fuel consumption: {len(low_engine_high_fuel)}")
if len(low_engine_high_fuel) > 0:
    print("\nTop 5 Examples:")
    for idx, row in low_engine_high_fuel.nlargest(5, 'fuel_efficiency').iterrows():
        print(f"  {row['ship_id']} ({row['ship_type']}) - Fuel: {row['fuel_efficiency']:.2f} L/km, Engine: {row['engine_efficiency']:.1f}%")
        print(f"    {row['month']}, Weather: {row['weather_conditions']}, Route: {row['route_id']}")

# Select the most anomalous case for memo
print("\n" + "="*70)
print("SELECTED ANOMALY FOR TECHNICAL MEMO")
print("="*70)

# Find Tanker Ship with highest fuel efficiency (they should be most efficient per ton-mile)
tanker_anomaly = df[df['ship_type'] == 'Tanker Ship'].nlargest(1, 'fuel_efficiency').iloc[0]

print(f"\nVessel ID: {tanker_anomaly['ship_id']}")
print(f"Ship Type: {tanker_anomaly['ship_type']}")
print(f"Route: {tanker_anomaly['route_id']}")
print(f"Month: {tanker_anomaly['month']}")
print(f"\nAnomalous Metrics:")
print(f"  Fuel Efficiency: {tanker_anomaly['fuel_efficiency']:.3f} L/km")
print(f"  Tanker Fleet Average: {df[df['ship_type'] == 'Tanker Ship']['fuel_efficiency'].mean():.3f} L/km")
print(f"  Deviation: {((tanker_anomaly['fuel_efficiency'] - df[df['ship_type'] == 'Tanker Ship']['fuel_efficiency'].mean()) / df[df['ship_type'] == 'Tanker Ship']['fuel_efficiency'].mean() * 100):+.1f}%")
print(f"  Distance: {tanker_anomaly['distance']:.2f} km")
print(f"  Fuel Consumed: {tanker_anomaly['fuel_consumption']:.2f} L")
print(f"  CO2 Emissions: {tanker_anomaly['CO2_emissions']:.2f} kg")
print(f"  GHG Intensity: {tanker_anomaly['co2_per_km']:.2f} kg/km")
print(f"  Engine Efficiency: {tanker_anomaly['engine_efficiency']:.2f}%")
print(f"  Weather: {tanker_anomaly['weather_conditions']}")
print(f"  Fuel Type: {tanker_anomaly['fuel_type']}")

print("\n" + "="*70)

