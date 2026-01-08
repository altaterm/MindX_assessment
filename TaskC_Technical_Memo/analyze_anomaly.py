"""
Anomaly Detection Analysis for Technical Memo
Analyzes the dataset to identify the most significant operational anomaly
"""

import pandas as pd
import numpy as np
from scipy import stats

# Load dataset
df = pd.read_csv('../data/mindx test dataset.csv')

# Calculate fuel efficiency
df['fuel_efficiency'] = df['fuel_consumption'] / df['distance']

# Calculate Z-scores
df['z_score'] = np.abs(stats.zscore(df['fuel_efficiency']))

# Find outliers (Z-score > 3)
outliers = df[df['z_score'] > 3].copy()

print("="*70)
print("ANOMALY DETECTION ANALYSIS")
print("="*70)

print(f"\nTotal records: {len(df)}")
print(f"Outliers found (Z-score > 3): {len(outliers)}")

if len(outliers) > 0:
    print("\nTop 10 Most Anomalous Records:")
    print("="*70)
    
    top_outliers = outliers.nlargest(10, 'fuel_efficiency')[
        ['ship_id', 'ship_type', 'route_id', 'month', 'distance', 
         'fuel_consumption', 'fuel_efficiency', 'CO2_emissions', 
         'weather_conditions', 'engine_efficiency', 'z_score']
    ]
    
    for idx, row in top_outliers.iterrows():
        print(f"\nVessel: {row['ship_id']} ({row['ship_type']})")
        print(f"Route: {row['route_id']}, Month: {row['month']}")
        print(f"Distance: {row['distance']:.2f} km")
        print(f"Fuel Consumption: {row['fuel_consumption']:.2f} L")
        print(f"Fuel Efficiency: {row['fuel_efficiency']:.3f} L/km (Z-score: {row['z_score']:.2f})")
        print(f"CO2 Emissions: {row['CO2_emissions']:.2f} kg")
        print(f"Weather: {row['weather_conditions']}, Engine Efficiency: {row['engine_efficiency']:.2f}%")
        print("-"*70)

# Statistics by ship type
print("\n" + "="*70)
print("FUEL EFFICIENCY BY SHIP TYPE")
print("="*70)
print(df.groupby('ship_type')['fuel_efficiency'].agg(['count', 'mean', 'std', 'min', 'max']))

# Select the most anomalous record for detailed analysis
if len(outliers) > 0:
    most_anomalous = outliers.nlargest(1, 'fuel_efficiency').iloc[0]
    
    print("\n" + "="*70)
    print("MOST ANOMALOUS VESSEL - DETAILED ANALYSIS")
    print("="*70)
    
    print(f"\nVessel ID: {most_anomalous['ship_id']}")
    print(f"Ship Type: {most_anomalous['ship_type']}")
    print(f"Route: {most_anomalous['route_id']}")
    print(f"Month: {most_anomalous['month']}")
    
    print(f"\nOperational Metrics:")
    print(f"  Distance Traveled: {most_anomalous['distance']:.2f} km")
    print(f"  Fuel Consumed: {most_anomalous['fuel_consumption']:.2f} L")
    print(f"  Fuel Efficiency: {most_anomalous['fuel_efficiency']:.3f} L/km")
    print(f"  CO2 Emissions: {most_anomalous['CO2_emissions']:.2f} kg")
    print(f"  Engine Efficiency: {most_anomalous['engine_efficiency']:.2f}%")
    print(f"  Weather Conditions: {most_anomalous['weather_conditions']}")
    
    # Compare to fleet average
    fleet_avg = df['fuel_efficiency'].mean()
    ship_type_avg = df[df['ship_type'] == most_anomalous['ship_type']]['fuel_efficiency'].mean()
    
    print(f"\nComparative Analysis:")
    print(f"  Fleet Average Fuel Efficiency: {fleet_avg:.3f} L/km")
    print(f"  {most_anomalous['ship_type']} Average: {ship_type_avg:.3f} L/km")
    print(f"  This Vessel's Efficiency: {most_anomalous['fuel_efficiency']:.3f} L/km")
    print(f"  Deviation from Fleet Average: {((most_anomalous['fuel_efficiency'] - fleet_avg) / fleet_avg * 100):.1f}%")
    print(f"  Deviation from Ship Type Average: {((most_anomalous['fuel_efficiency'] - ship_type_avg) / ship_type_avg * 100):.1f}%")
    print(f"  Z-Score: {most_anomalous['z_score']:.2f}")
    
    # GHG Intensity impact
    ghg_intensity = most_anomalous['CO2_emissions'] / most_anomalous['distance']
    print(f"\nCompliance Impact:")
    print(f"  GHG Intensity: {ghg_intensity:.2f} kg CO2/km")
    print(f"  Fleet Average GHG Intensity: {(df['CO2_emissions'] / df['distance']).mean():.2f} kg CO2/km")
    
    print("\n" + "="*70)

