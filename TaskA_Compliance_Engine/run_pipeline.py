"""
Task A: End-to-End Pipeline Orchestration

This script orchestrates the complete compliance engine workflow:
1. Load dataset
2. Train ML model
3. Predict CO2 emissions
4. Calculate compliance metrics
5. Generate output JSON

Usage:
    python run_pipeline.py

Author: MindX Strategic Navigator Challenge
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from model import CO2EmissionPredictor
from compliance import ComplianceEngine


def run_full_pipeline(
    dataset_path='../data/mindx test dataset.csv',
    output_dir='output',
    output_filename='compliance_results.json',
    train_new_model=True,
    model_path='model_artifacts.pkl'
):
    """
    Execute the complete compliance engine pipeline.
    
    Args:
        dataset_path (str): Path to input dataset
        output_dir (str): Directory for output files
        output_filename (str): Name of output JSON file
        train_new_model (bool): Whether to train a new model or load existing
        model_path (str): Path to save/load model artifacts
        
    Returns:
        dict: Pipeline execution summary
    """
    print("\n" + "="*70)
    print(" "*15 + "MINDX COMPLIANCE ENGINE PIPELINE")
    print("="*70)
    print(f"\nExecution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Dataset: {dataset_path}")
    print(f"Output: {os.path.join(output_dir, output_filename)}")
    print("="*70 + "\n")
    
    # ========== STEP 1: Load Dataset ==========
    print("STEP 1/5: LOADING DATASET")
    print("-"*70)
    try:
        df = pd.read_csv(dataset_path)
        print(f"✓ Successfully loaded dataset")
        print(f"  Records: {len(df)}")
        print(f"  Columns: {list(df.columns)}")
        print(f"  Date range: {df['month'].unique().tolist()}")
        print(f"  Ship types: {df['ship_type'].nunique()}")
    except Exception as e:
        print(f"✗ Error loading dataset: {e}")
        return None
    
    # ========== STEP 2: Train/Load ML Model ==========
    print("\n" + "="*70)
    print("STEP 2/5: ML MODEL FOR CO2 PREDICTION")
    print("-"*70)
    
    predictor = CO2EmissionPredictor()
    
    if train_new_model:
        print("Training new model...")
        try:
            metrics = predictor.train(df)
            predictor.save_model(model_path)
            print(f"\n✓ Model training complete")
            print(f"  Test RMSE: {metrics['test_rmse']:.2f} Kg")
            print(f"  Test R²: {metrics['test_r2']:.4f}")
        except Exception as e:
            print(f"✗ Error training model: {e}")
            return None
    else:
        print(f"Loading existing model from {model_path}...")
        try:
            predictor.load_model(model_path)
            print("✓ Model loaded successfully")
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            print("  Attempting to train new model...")
            try:
                metrics = predictor.train(df)
                predictor.save_model(model_path)
                print("✓ New model trained successfully")
            except Exception as e2:
                print(f"✗ Error training new model: {e2}")
                return None
    
    # ========== STEP 3: Predict CO2 Emissions ==========
    print("\n" + "="*70)
    print("STEP 3/5: PREDICTING CO2 EMISSIONS")
    print("-"*70)
    
    try:
        # Note: We'll use actual CO2 values from dataset for compliance calculation
        # But we'll also generate predictions to show model capability
        df['CO2_predicted'] = predictor.predict(df)
        
        # Calculate prediction accuracy
        mae = np.mean(np.abs(df['CO2_emissions'] - df['CO2_predicted']))
        rmse = np.sqrt(np.mean((df['CO2_emissions'] - df['CO2_predicted'])**2))
        
        print(f"✓ Predictions generated for all {len(df)} records")
        print(f"  Prediction MAE: {mae:.2f} Kg")
        print(f"  Prediction RMSE: {rmse:.2f} Kg")
        print(f"  Mean Actual CO2: {df['CO2_emissions'].mean():.2f} Kg")
        print(f"  Mean Predicted CO2: {df['CO2_predicted'].mean():.2f} Kg")
    except Exception as e:
        print(f"✗ Error making predictions: {e}")
        return None
    
    # ========== STEP 4: Calculate Compliance Metrics ==========
    print("\n" + "="*70)
    print("STEP 4/5: CALCULATING COMPLIANCE METRICS")
    print("-"*70)
    
    try:
        # Initialize compliance engine
        compliance_engine = ComplianceEngine(target_year=2026, reduction_factor=0.95)
        
        # Process fleet (using actual CO2 emissions)
        df_compliance = compliance_engine.process_fleet(
            df, 
            co2_column='CO2_emissions',
            distance_column='distance'
        )
        
        # Get summary
        summary = compliance_engine.get_compliance_summary(df_compliance)
        
        print("✓ Compliance metrics calculated")
        
    except Exception as e:
        print(f"✗ Error calculating compliance: {e}")
        return None
    
    # ========== STEP 5: Generate Output JSON ==========
    print("\n" + "="*70)
    print("STEP 5/5: GENERATING OUTPUT JSON")
    print("-"*70)
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Prepare output data
        output_records = []
        
        for idx, row in df_compliance.iterrows():
            record = {
                "vessel_id": str(row['ship_id']),
                "ship_type": str(row['ship_type']),
                "route_id": str(row['route_id']),
                "month": str(row['month']),
                "distance": float(row['distance']),
                "fuel_type": str(row['fuel_type']),
                "fuel_consumption": float(row['fuel_consumption']),
                "co2_emission": float(row['CO2_emissions']),
                "co2_predicted": float(row['CO2_predicted']),
                "ghg_intensity": float(row['ghg_intensity']),
                "target_intensity": float(row['target_intensity']),
                "compliance_balance": float(row['compliance_balance']),
                "status": str(row['status']),
                "weather_conditions": str(row['weather_conditions']),
                "engine_efficiency": float(row['engine_efficiency'])
            }
            output_records.append(record)
        
        # Create output structure
        output_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "dataset_path": dataset_path,
                "total_records": len(output_records),
                "model_performance": {
                    "test_rmse": float(predictor.metrics.get('test_rmse', 0)),
                    "test_mae": float(predictor.metrics.get('test_mae', 0)),
                    "test_r2": float(predictor.metrics.get('test_r2', 0))
                },
                "compliance_summary": {
                    "target_year": summary['target_year'],
                    "fleet_average_intensity": float(summary['fleet_average_intensity']),
                    "target_intensity": float(summary['target_intensity']),
                    "reduction_percentage": float(summary['reduction_percentage']),
                    "total_vessels": summary['total_vessels'],
                    "surplus_count": summary['surplus_count'],
                    "deficit_count": summary['deficit_count'],
                    "total_surplus": float(summary.get('total_surplus', 0)),
                    "total_deficit": float(summary.get('total_deficit', 0))
                }
            },
            "vessels": output_records
        }
        
        # Write to JSON file
        output_path = os.path.join(output_dir, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Output JSON generated successfully")
        print(f"  File: {output_path}")
        print(f"  Size: {os.path.getsize(output_path) / 1024:.2f} KB")
        print(f"  Records: {len(output_records)}")
        
    except Exception as e:
        print(f"✗ Error generating output: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    # ========== Pipeline Summary ==========
    print("\n" + "="*70)
    print("PIPELINE EXECUTION SUMMARY")
    print("="*70)
    print(f"✓ Dataset loaded: {len(df)} records")
    print(f"✓ Model performance: R² = {predictor.metrics.get('test_r2', 0):.4f}")
    print(f"✓ Fleet compliance calculated")
    print(f"  - Surplus vessels: {summary['surplus_count']} ({summary['surplus_count']/summary['total_vessels']*100:.1f}%)")
    print(f"  - Deficit vessels: {summary['deficit_count']} ({summary['deficit_count']/summary['total_vessels']*100:.1f}%)")
    print(f"✓ Output JSON: {output_path}")
    print("="*70)
    print("\n✓✓✓ PIPELINE COMPLETED SUCCESSFULLY ✓✓✓\n")
    
    return {
        'success': True,
        'records_processed': len(df),
        'output_file': output_path,
        'summary': summary,
        'model_metrics': predictor.metrics
    }


def generate_summary_report(output_dir='output'):
    """
    Generate a human-readable summary report from the compliance results.
    
    Args:
        output_dir (str): Directory containing compliance_results.json
    """
    json_path = os.path.join(output_dir, 'compliance_results.json')
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Run the pipeline first.")
        return
    
    # Load results
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    metadata = data['metadata']
    vessels = data['vessels']
    
    # Generate report
    report = []
    report.append("\n" + "="*70)
    report.append("COMPLIANCE ENGINE - EXECUTIVE SUMMARY")
    report.append("="*70)
    report.append(f"\nGenerated: {metadata['generated_at']}")
    report.append(f"Total Vessels Analyzed: {metadata['total_records']}")
    
    report.append("\n" + "-"*70)
    report.append("MODEL PERFORMANCE")
    report.append("-"*70)
    model_perf = metadata['model_performance']
    report.append(f"  R² Score: {model_perf['test_r2']:.4f}")
    report.append(f"  RMSE: {model_perf['test_rmse']:.2f} Kg")
    report.append(f"  MAE: {model_perf['test_mae']:.2f} Kg")
    
    report.append("\n" + "-"*70)
    report.append("COMPLIANCE ANALYSIS")
    report.append("-"*70)
    comp = metadata['compliance_summary']
    report.append(f"  Target Year: {comp['target_year']}")
    report.append(f"  Fleet Average Intensity: {comp['fleet_average_intensity']:.4f} kg/km")
    report.append(f"  Target Intensity: {comp['target_intensity']:.4f} kg/km")
    report.append(f"  Required Reduction: {comp['reduction_percentage']:.1f}%")
    report.append(f"\n  Surplus Vessels: {comp['surplus_count']} ({comp['surplus_count']/comp['total_vessels']*100:.1f}%)")
    report.append(f"  Deficit Vessels: {comp['deficit_count']} ({comp['deficit_count']/comp['total_vessels']*100:.1f}%)")
    report.append(f"\n  Total Surplus Available: {comp['total_surplus']:.2f} kg/km")
    report.append(f"  Total Deficit: {comp['total_deficit']:.2f} kg/km")
    report.append(f"  Net Position: {comp['total_surplus'] + comp['total_deficit']:.2f} kg/km")
    
    report.append("\n" + "="*70 + "\n")
    
    # Print report
    report_text = "\n".join(report)
    print(report_text)
    
    # Save report
    report_path = os.path.join(output_dir, 'compliance_summary.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"✓ Summary report saved to: {report_path}\n")


if __name__ == "__main__":
    """
    Run the complete pipeline.
    """
    # Execute pipeline
    result = run_full_pipeline(
        dataset_path='../data/mindx test dataset.csv',
        output_dir='output',
        output_filename='compliance_results.json',
        train_new_model=True,
        model_path='model_artifacts.pkl'
    )
    
    if result and result['success']:
        # Generate summary report
        generate_summary_report('output')
        
        print("\n" + "="*70)
        print("NEXT STEPS")
        print("="*70)
        print("1. Review compliance_results.json in the output/ directory")
        print("2. Check compliance_summary.txt for executive summary")
        print("3. Use the JSON file as input for Task B (Fleet Dashboard)")
        print("="*70 + "\n")
    else:
        print("\n✗ Pipeline execution failed. Check errors above.\n")

