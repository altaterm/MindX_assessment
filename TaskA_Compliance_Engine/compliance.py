"""
Task A: Compliance Calculation Logic

This module implements:
- GHG Intensity calculation
- Regulatory benchmark computation
- Compliance balance classification
- Surplus/Deficit status assignment

Author: MindX Strategic Navigator Challenge
"""

import pandas as pd
import numpy as np


class ComplianceEngine:
    """
    Engine for calculating maritime vessel GHG compliance metrics.
    
    Implements the regulatory compliance framework:
    1. Calculate GHG Intensity per vessel
    2. Compute fleet-wide regulatory benchmark (2026 target)
    3. Calculate compliance balance for each vessel
    4. Classify vessels as Surplus or Deficit
    """
    
    def __init__(self, target_year=2026, reduction_factor=0.95):
        """
        Initialize the compliance engine.
        
        Args:
            target_year (int): Target compliance year (default: 2026)
            reduction_factor (float): Regulatory reduction target as fraction (default: 0.95 = 5% reduction)
        """
        self.target_year = target_year
        self.reduction_factor = reduction_factor
        self.target_intensity = None
        self.fleet_average_intensity = None
        
    def calculate_ghg_intensity(self, co2_emission, distance):
        """
        Calculate GHG Intensity for a vessel operation.
        
        Formula: GHG Intensity = CO2 Emission (Kg) / Distance (km)
        
        Args:
            co2_emission (float or array): CO2 emissions in kilograms
            distance (float or array): Distance traveled in kilometers
            
        Returns:
            float or array: GHG intensity in kg CO2 per km
        """
        # Handle division by zero
        if isinstance(distance, (int, float)):
            if distance == 0:
                return np.nan
            return co2_emission / distance
        else:
            # Array-like input
            result = np.divide(co2_emission, distance, 
                             out=np.full_like(co2_emission, np.nan, dtype=float),
                             where=distance != 0)
            return result
    
    def calculate_fleet_average_intensity(self, ghg_intensities):
        """
        Calculate fleet-wide average GHG intensity.
        
        Args:
            ghg_intensities (array-like): Array of GHG intensities
            
        Returns:
            float: Fleet average GHG intensity
        """
        # Remove NaN values before averaging
        valid_intensities = [i for i in ghg_intensities if not np.isnan(i)]
        
        if len(valid_intensities) == 0:
            raise ValueError("No valid GHG intensities to calculate fleet average")
        
        self.fleet_average_intensity = np.mean(valid_intensities)
        return self.fleet_average_intensity
    
    def calculate_target_intensity(self, fleet_average_intensity=None):
        """
        Calculate the regulatory target intensity for the target year.
        
        Formula: Target Intensity = Fleet Average Intensity × Reduction Factor
        
        Args:
            fleet_average_intensity (float, optional): Fleet average intensity.
                                                       If None, uses previously calculated value.
        
        Returns:
            float: Target GHG intensity for compliance
        """
        if fleet_average_intensity is not None:
            self.fleet_average_intensity = fleet_average_intensity
        
        if self.fleet_average_intensity is None:
            raise ValueError("Fleet average intensity must be calculated first")
        
        self.target_intensity = self.fleet_average_intensity * self.reduction_factor
        return self.target_intensity
    
    def calculate_compliance_balance(self, vessel_intensity, target_intensity=None):
        """
        Calculate compliance balance for a vessel.
        
        Formula: Compliance Balance = Target Intensity - Vessel Intensity
        
        Positive balance → Surplus (vessel is compliant)
        Negative balance → Deficit (vessel needs offsetting)
        
        Args:
            vessel_intensity (float or array): Vessel's GHG intensity
            target_intensity (float, optional): Target intensity. If None, uses calculated target.
            
        Returns:
            float or array: Compliance balance
        """
        if target_intensity is None:
            if self.target_intensity is None:
                raise ValueError("Target intensity must be calculated first")
            target_intensity = self.target_intensity
        
        return target_intensity - vessel_intensity
    
    def classify_compliance_status(self, compliance_balance):
        """
        Classify vessel compliance status based on balance.
        
        Args:
            compliance_balance (float or array): Compliance balance value(s)
            
        Returns:
            str or array: 'Surplus' if CB > 0, 'Deficit' if CB < 0, 'Compliant' if CB == 0
        """
        if isinstance(compliance_balance, (int, float)):
            if np.isnan(compliance_balance):
                return 'Unknown'
            elif compliance_balance > 0:
                return 'Surplus'
            elif compliance_balance < 0:
                return 'Deficit'
            else:
                return 'Compliant'
        else:
            # Array-like input
            status = np.where(np.isnan(compliance_balance), 'Unknown',
                            np.where(compliance_balance > 0, 'Surplus',
                                   np.where(compliance_balance < 0, 'Deficit', 'Compliant')))
            return status
    
    def process_fleet(self, df, co2_column='CO2_emissions', distance_column='distance'):
        """
        Process entire fleet and calculate compliance metrics for all vessels.
        
        Args:
            df (pd.DataFrame): Fleet dataframe with CO2 emissions and distance
            co2_column (str): Name of CO2 emissions column
            distance_column (str): Name of distance column
            
        Returns:
            pd.DataFrame: DataFrame with added compliance metrics
        """
        print("="*60)
        print("FLEET COMPLIANCE ANALYSIS")
        print("="*60)
        
        # Make a copy to avoid modifying original
        result_df = df.copy()
        
        # Step 1: Calculate GHG Intensity for each vessel
        print("\n[1/5] Calculating GHG Intensity...")
        result_df['ghg_intensity'] = self.calculate_ghg_intensity(
            result_df[co2_column].values,
            result_df[distance_column].values
        )
        
        valid_count = result_df['ghg_intensity'].notna().sum()
        print(f"  ✓ Calculated GHG intensity for {valid_count} records")
        print(f"  ✓ Mean GHG Intensity: {result_df['ghg_intensity'].mean():.4f} kg/km")
        print(f"  ✓ Range: {result_df['ghg_intensity'].min():.4f} to {result_df['ghg_intensity'].max():.4f} kg/km")
        
        # Step 2: Calculate Fleet Average Intensity
        print("\n[2/5] Computing Fleet Average Intensity...")
        fleet_avg = self.calculate_fleet_average_intensity(result_df['ghg_intensity'].values)
        print(f"  ✓ Fleet Average GHG Intensity: {fleet_avg:.4f} kg/km")
        
        # Step 3: Calculate Target Intensity (2026 benchmark)
        print(f"\n[3/5] Computing {self.target_year} Regulatory Target...")
        target = self.calculate_target_intensity()
        print(f"  ✓ Target Intensity: {target:.4f} kg/km")
        print(f"  ✓ Reduction Required: {(1 - self.reduction_factor) * 100:.1f}%")
        
        # Add target intensity column
        result_df['target_intensity'] = target
        
        # Step 4: Calculate Compliance Balance
        print("\n[4/5] Calculating Compliance Balance...")
        result_df['compliance_balance'] = self.calculate_compliance_balance(
            result_df['ghg_intensity'].values
        )
        print(f"  ✓ Compliance balance calculated for all vessels")
        
        # Step 5: Classify Compliance Status
        print("\n[5/5] Classifying Compliance Status...")
        result_df['status'] = self.classify_compliance_status(
            result_df['compliance_balance'].values
        )
        
        # Generate summary statistics
        status_counts = result_df['status'].value_counts()
        print("\n" + "-"*60)
        print("FLEET COMPLIANCE SUMMARY:")
        print("-"*60)
        print(f"  Total Vessels: {len(result_df)}")
        
        for status in ['Surplus', 'Deficit', 'Compliant', 'Unknown']:
            count = status_counts.get(status, 0)
            percentage = (count / len(result_df)) * 100
            print(f"  {status}: {count} ({percentage:.1f}%)")
        
        if 'Surplus' in status_counts:
            surplus_total = result_df[result_df['status'] == 'Surplus']['compliance_balance'].sum()
            print(f"\n  Total Surplus Available: {surplus_total:.2f} kg/km")
        
        if 'Deficit' in status_counts:
            deficit_total = result_df[result_df['status'] == 'Deficit']['compliance_balance'].sum()
            print(f"  Total Deficit: {deficit_total:.2f} kg/km")
        
        print("-"*60)
        print("\n" + "="*60)
        print("COMPLIANCE ANALYSIS COMPLETE ✓")
        print("="*60 + "\n")
        
        return result_df
    
    def get_compliance_summary(self, df):
        """
        Generate a summary dictionary of compliance metrics.
        
        Args:
            df (pd.DataFrame): Processed fleet dataframe
            
        Returns:
            dict: Summary statistics
        """
        status_counts = df['status'].value_counts().to_dict()
        
        summary = {
            'total_vessels': len(df),
            'surplus_count': status_counts.get('Surplus', 0),
            'deficit_count': status_counts.get('Deficit', 0),
            'compliant_count': status_counts.get('Compliant', 0),
            'fleet_average_intensity': self.fleet_average_intensity,
            'target_intensity': self.target_intensity,
            'target_year': self.target_year,
            'reduction_percentage': (1 - self.reduction_factor) * 100
        }
        
        if 'Surplus' in status_counts:
            summary['total_surplus'] = df[df['status'] == 'Surplus']['compliance_balance'].sum()
        
        if 'Deficit' in status_counts:
            summary['total_deficit'] = df[df['status'] == 'Deficit']['compliance_balance'].sum()
        
        return summary


def calculate_compliance(dataset_path='../data/mindx test dataset.csv', 
                        co2_column='CO2_emissions',
                        distance_column='distance'):
    """
    Convenience function to calculate compliance for a dataset.
    
    Args:
        dataset_path (str): Path to the dataset
        co2_column (str): Name of CO2 emissions column
        distance_column (str): Name of distance column
        
    Returns:
        tuple: (processed_dataframe, compliance_summary)
    """
    # Load data
    print(f"Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    print(f"✓ Loaded {len(df)} records\n")
    
    # Initialize compliance engine
    engine = ComplianceEngine(target_year=2026, reduction_factor=0.95)
    
    # Process fleet
    result_df = engine.process_fleet(df, co2_column=co2_column, distance_column=distance_column)
    
    # Get summary
    summary = engine.get_compliance_summary(result_df)
    
    return result_df, summary


if __name__ == "__main__":
    """
    Test the compliance calculation pipeline.
    """
    # Calculate compliance
    df_compliance, summary = calculate_compliance()
    
    # Display sample results
    print("\n" + "="*60)
    print("SAMPLE COMPLIANCE RESULTS")
    print("="*60)
    
    print("\nFirst 5 Surplus Vessels:")
    surplus = df_compliance[df_compliance['status'] == 'Surplus'].head()
    if len(surplus) > 0:
        print(surplus[['ship_id', 'ship_type', 'distance', 'CO2_emissions', 
                      'ghg_intensity', 'compliance_balance', 'status']].to_string(index=False))
    
    print("\n\nFirst 5 Deficit Vessels:")
    deficit = df_compliance[df_compliance['status'] == 'Deficit'].head()
    if len(deficit) > 0:
        print(deficit[['ship_id', 'ship_type', 'distance', 'CO2_emissions', 
                      'ghg_intensity', 'compliance_balance', 'status']].to_string(index=False))
    
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")
    print("="*60)

