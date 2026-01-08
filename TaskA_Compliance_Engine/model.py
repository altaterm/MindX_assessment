"""
Task A: ML Model for CO2 Emission Prediction

This module implements the machine learning pipeline:
- Feature preprocessing (encoding, scaling)
- Linear Regression model
- Training and prediction
- Model evaluation

Author: MindX Strategic Navigator Challenge
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os


class CO2EmissionPredictor:
    """
    Machine Learning model for predicting CO2 emissions from maritime vessels.
    
    Uses Linear Regression with OneHotEncoding for categorical ship types.
    """
    
    def __init__(self):
        """Initialize the predictor with model and encoder."""
        self.model = LinearRegression()
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.feature_names = ['ship_type', 'distance', 'fuel_consumption']
        self.target_name = 'CO2_emissions'
        self.is_trained = False
        self.metrics = {}
        
    def prepare_features(self, df, fit_encoder=False):
        """
        Prepare features for model training/prediction.
        
        Args:
            df (pd.DataFrame): Input dataframe with raw features
            fit_encoder (bool): Whether to fit the encoder (True for training, False for prediction)
            
        Returns:
            np.ndarray: Prepared feature matrix
        """
        # Extract ship_type for encoding
        ship_type = df[['ship_type']].values
        
        # Encode ship_type
        if fit_encoder:
            ship_type_encoded = self.encoder.fit_transform(ship_type)
        else:
            ship_type_encoded = self.encoder.transform(ship_type)
        
        # Extract numerical features
        numerical_features = df[['distance', 'fuel_consumption']].values
        
        # Combine encoded categorical and numerical features
        X = np.hstack([ship_type_encoded, numerical_features])
        
        return X
    
    def train(self, df, test_size=0.2, random_state=42):
        """
        Train the Linear Regression model.
        
        Args:
            df (pd.DataFrame): Training dataframe with features and target
            test_size (float): Proportion of data for testing (default: 0.2)
            random_state (int): Random seed for reproducibility (default: 42)
            
        Returns:
            dict: Training metrics (RMSE, MAE, R²)
        """
        print("="*60)
        print("TRAINING CO2 EMISSION PREDICTION MODEL")
        print("="*60)
        
        # Verify required columns exist
        required_cols = self.feature_names + [self.target_name]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Prepare features
        print("\n[1/5] Preparing features...")
        X = self.prepare_features(df, fit_encoder=True)
        y = df[self.target_name].values
        
        print(f"  ✓ Feature matrix shape: {X.shape}")
        print(f"  ✓ Target vector shape: {y.shape}")
        print(f"  ✓ Ship types encoded: {self.encoder.categories_[0].tolist()}")
        
        # Train-test split
        print(f"\n[2/5] Splitting data (test_size={test_size})...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        print(f"  ✓ Training samples: {len(X_train)}")
        print(f"  ✓ Testing samples: {len(X_test)}")
        
        # Train model
        print("\n[3/5] Training Linear Regression model...")
        self.model.fit(X_train, y_train)
        print("  ✓ Model trained successfully!")
        
        # Make predictions
        print("\n[4/5] Evaluating model performance...")
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        
        # Calculate metrics
        train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
        test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
        
        train_mae = mean_absolute_error(y_train, y_train_pred)
        test_mae = mean_absolute_error(y_test, y_test_pred)
        
        train_r2 = r2_score(y_train, y_train_pred)
        test_r2 = r2_score(y_test, y_test_pred)
        
        # Store metrics
        self.metrics = {
            'train_rmse': train_rmse,
            'test_rmse': test_rmse,
            'train_mae': train_mae,
            'test_mae': test_mae,
            'train_r2': train_r2,
            'test_r2': test_r2,
            'train_samples': len(X_train),
            'test_samples': len(X_test)
        }
        
        self.is_trained = True
        
        # Display results
        print("\n[5/5] Training Results:")
        print("-" * 60)
        print(f"  RMSE (Train): {train_rmse:.2f} Kg")
        print(f"  RMSE (Test):  {test_rmse:.2f} Kg")
        print(f"  MAE (Train):  {train_mae:.2f} Kg")
        print(f"  MAE (Test):   {test_mae:.2f} Kg")
        print(f"  R² (Train):   {train_r2:.4f}")
        print(f"  R² (Test):    {test_r2:.4f}")
        print("-" * 60)
        
        # Model interpretation
        print("\n[Model Coefficients]")
        feature_names_full = list(self.encoder.get_feature_names_out(['ship_type'])) + ['distance', 'fuel_consumption']
        coefficients = self.model.coef_
        
        print(f"  Intercept: {self.model.intercept_:.2f}")
        print(f"\n  Top 5 Most Important Features:")
        coef_importance = sorted(zip(feature_names_full, coefficients), 
                                key=lambda x: abs(x[1]), reverse=True)[:5]
        for feat, coef in coef_importance:
            print(f"    {feat}: {coef:.2f}")
        
        print("\n" + "="*60)
        print("MODEL TRAINING COMPLETE ✓")
        print("="*60 + "\n")
        
        return self.metrics
    
    def predict(self, df):
        """
        Predict CO2 emissions for new data.
        
        Args:
            df (pd.DataFrame): Dataframe with features (ship_type, distance, fuel_consumption)
            
        Returns:
            np.ndarray: Predicted CO2 emissions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions. Call train() first.")
        
        # Prepare features
        X = self.prepare_features(df, fit_encoder=False)
        
        # Make predictions
        predictions = self.model.predict(X)
        
        return predictions
    
    def save_model(self, filepath='model_artifacts.pkl'):
        """
        Save trained model and encoder to disk.
        
        Args:
            filepath (str): Path to save the model
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained model. Call train() first.")
        
        artifacts = {
            'model': self.model,
            'encoder': self.encoder,
            'feature_names': self.feature_names,
            'target_name': self.target_name,
            'metrics': self.metrics
        }
        
        joblib.dump(artifacts, filepath)
        print(f"✓ Model saved to: {filepath}")
    
    def load_model(self, filepath='model_artifacts.pkl'):
        """
        Load trained model and encoder from disk.
        
        Args:
            filepath (str): Path to load the model from
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        artifacts = joblib.load(filepath)
        
        self.model = artifacts['model']
        self.encoder = artifacts['encoder']
        self.feature_names = artifacts['feature_names']
        self.target_name = artifacts['target_name']
        self.metrics = artifacts['metrics']
        self.is_trained = True
        
        print(f"✓ Model loaded from: {filepath}")
        print(f"  Test RMSE: {self.metrics['test_rmse']:.2f} Kg")
        print(f"  Test R²: {self.metrics['test_r2']:.4f}")


def train_model(dataset_path='../data/mindx test dataset.csv', save_path='model_artifacts.pkl'):
    """
    Convenience function to train and save the model.
    
    Args:
        dataset_path (str): Path to the training dataset
        save_path (str): Path to save the trained model
        
    Returns:
        CO2EmissionPredictor: Trained model instance
    """
    # Load data
    print(f"Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    print(f"✓ Loaded {len(df)} records\n")
    
    # Initialize and train model
    predictor = CO2EmissionPredictor()
    metrics = predictor.train(df)
    
    # Save model
    predictor.save_model(save_path)
    
    return predictor


if __name__ == "__main__":
    """
    Test the model training pipeline.
    """
    # Train model
    predictor = train_model()
    
    # Test prediction on a sample
    print("\n" + "="*60)
    print("TESTING PREDICTION")
    print("="*60)
    
    sample_data = pd.DataFrame({
        'ship_type': ['Oil Service Boat'],
        'distance': [132.26],
        'fuel_consumption': [3779.77]
    })
    
    prediction = predictor.predict(sample_data)
    print(f"\nSample Input:")
    print(f"  Ship Type: {sample_data['ship_type'].values[0]}")
    print(f"  Distance: {sample_data['distance'].values[0]} km")
    print(f"  Fuel Consumption: {sample_data['fuel_consumption'].values[0]} L")
    print(f"\nPredicted CO2 Emission: {prediction[0]:.2f} Kg")
    print("="*60)

