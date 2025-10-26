"""
AI-Driven Dynamic Pricing Model
Implements machine learning model for dynamic pricing optimization
"""

import numpy as np
import pandas as pd
import logging
from typing import Dict, List, Any, Tuple
from datetime import datetime
import pickle
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DynamicPricingModel:
    """AI model for dynamic pricing optimization"""
    
    def __init__(self, model_path: str = 'models/pricing_model.pkl'):
        """
        Initialize Dynamic Pricing Model
        
        Args:
            model_path: Path to save/load the model
        """
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.is_trained = False
        
    def generate_training_data(self, n_samples: int = 10000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate synthetic training data for dynamic pricing
        
        Args:
            n_samples: Number of samples to generate
            
        Returns:
            Tuple of (features, targets)
        """
        np.random.seed(42)
        
        # Features: base_price, demand, competition_price, time_of_day, day_of_week, season
        base_prices = np.random.uniform(10, 100, n_samples)
        demand = np.random.randint(0, 1000, n_samples)
        competition_prices = base_prices * np.random.uniform(0.8, 1.2, n_samples)
        time_of_day = np.random.randint(0, 24, n_samples)
        day_of_week = np.random.randint(0, 7, n_samples)
        season = np.random.randint(0, 4, n_samples)
        
        features = np.column_stack([
            base_prices, demand, competition_prices,
            time_of_day, day_of_week, season
        ])
        
        # Target: optimal_price (simplified formula with some noise)
        optimal_price = (
            base_prices * 0.7 +
            (demand / 1000) * base_prices * 0.3 +
            competition_prices * 0.2 -
            (time_of_day > 20) * base_prices * 0.05 +
            np.random.normal(0, 2, n_samples)
        )
        
        return features, optimal_price
        
    def train(self, features: np.ndarray = None, targets: np.ndarray = None) -> Dict[str, float]:
        """
        Train the dynamic pricing model
        
        Args:
            features: Training features (if None, generates synthetic data)
            targets: Training targets (if None, generates synthetic data)
            
        Returns:
            Dictionary containing training metrics
        """
        try:
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.model_selection import train_test_split
            from sklearn.preprocessing import StandardScaler
            from sklearn.metrics import mean_squared_error, r2_score
            
            # Generate data if not provided
            if features is None or targets is None:
                features, targets = self.generate_training_data()
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                features, targets, test_size=0.2, random_state=42
            )
            
            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate
            y_pred = self.model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)
            
            self.is_trained = True
            
            metrics = {
                'mse': float(mse),
                'rmse': float(rmse),
                'r2_score': float(r2),
                'trained_at': datetime.now().isoformat()
            }
            
            logger.info(f"Model trained successfully. RMSE: {rmse:.2f}, R²: {r2:.4f}")
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to train model: {e}")
            return {'error': str(e)}
            
    def predict(self, features: np.ndarray) -> np.ndarray:
        """
        Predict optimal prices
        
        Args:
            features: Input features
            
        Returns:
            Predicted prices
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
            
        try:
            features_scaled = self.scaler.transform(features)
            predictions = self.model.predict(features_scaled)
            return predictions
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise
            
    def predict_single(self, base_price: float, demand: int, competition_price: float,
                      time_of_day: int, day_of_week: int, season: int) -> float:
        """
        Predict optimal price for a single product
        
        Args:
            base_price: Base price of the product
            demand: Current demand level
            competition_price: Competitor's price
            time_of_day: Hour of the day (0-23)
            day_of_week: Day of the week (0-6)
            season: Season (0-3)
            
        Returns:
            Predicted optimal price
        """
        features = np.array([[
            base_price, demand, competition_price,
            time_of_day, day_of_week, season
        ]])
        
        prediction = self.predict(features)
        return float(prediction[0])
        
    def save_model(self):
        """Save trained model to disk"""
        if not self.is_trained:
            logger.warning("Model not trained, nothing to save")
            return False
            
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            with open(self.model_path, 'wb') as f:
                pickle.dump({
                    'model': self.model,
                    'scaler': self.scaler
                }, f)
            logger.info(f"Model saved to {self.model_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
            return False
            
    def load_model(self):
        """Load trained model from disk"""
        try:
            with open(self.model_path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.scaler = data['scaler']
                self.is_trained = True
            logger.info(f"Model loaded from {self.model_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
            
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance from the trained model
        
        Returns:
            Dictionary of feature names and their importance
        """
        if not self.is_trained:
            return {}
            
        feature_names = [
            'base_price', 'demand', 'competition_price',
            'time_of_day', 'day_of_week', 'season'
        ]
        
        importances = self.model.feature_importances_
        return dict(zip(feature_names, [float(imp) for imp in importances]))
