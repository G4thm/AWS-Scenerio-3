"""
Data Pipeline Module
Handles data ingestion, processing, and transformation
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPipeline:
    """Manages data ingestion and processing pipeline"""
    
    def __init__(self, data_lake=None):
        """
        Initialize Data Pipeline
        
        Args:
            data_lake: DataLake instance for storage
        """
        self.data_lake = data_lake
        self.processed_records = 0
        
    def generate_sample_data(self, n_products: int = 100, days: int = 30) -> pd.DataFrame:
        """
        Generate sample pricing data for simulation
        
        Args:
            n_products: Number of products
            days: Number of days of data
            
        Returns:
            DataFrame with sample data
        """
        np.random.seed(42)
        
        data = []
        start_date = datetime.now() - timedelta(days=days)
        
        for product_id in range(1, n_products + 1):
            base_price = np.random.uniform(10, 200)
            
            for day in range(days):
                timestamp = start_date + timedelta(days=day)
                
                # Simulate daily variations
                demand = np.random.randint(50, 500)
                competition_price = base_price * np.random.uniform(0.85, 1.15)
                current_price = base_price * np.random.uniform(0.9, 1.1)
                
                data.append({
                    'product_id': f'PROD-{product_id:04d}',
                    'timestamp': timestamp,
                    'base_price': round(base_price, 2),
                    'current_price': round(current_price, 2),
                    'demand': demand,
                    'competition_price': round(competition_price, 2),
                    'time_of_day': timestamp.hour,
                    'day_of_week': timestamp.weekday(),
                    'season': (timestamp.month - 1) // 3
                })
        
        df = pd.DataFrame(data)
        logger.info(f"Generated {len(df)} sample records")
        return df
        
    def ingest_data(self, data: pd.DataFrame) -> bool:
        """
        Ingest data into the pipeline
        
        Args:
            data: DataFrame to ingest
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Ingesting {len(data)} records")
            self.processed_records += len(data)
            
            # Upload to data lake if available
            if self.data_lake:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                key = f"raw_data/pricing_data_{timestamp}.json"
                # Convert DataFrame to dict with proper type handling
                data_copy = data.copy()
                if 'timestamp' in data_copy.columns:
                    data_copy['timestamp'] = data_copy['timestamp'].astype(str)
                data_dict = data_copy.to_dict(orient='records')
                self.data_lake.upload_data({'data': data_dict}, key)
            
            return True
        except Exception as e:
            logger.error(f"Failed to ingest data: {e}")
            return False
            
    def validate_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate data quality
        
        Args:
            data: DataFrame to validate
            
        Returns:
            Dictionary with validation results
        """
        validation_results = {
            'total_records': len(data),
            'missing_values': data.isnull().sum().to_dict(),
            'duplicate_records': data.duplicated().sum(),
            'data_types': {col: str(dtype) for col, dtype in data.dtypes.items()},
            'validated_at': datetime.now().isoformat()
        }
        
        # Check for negative prices
        if 'current_price' in data.columns:
            negative_prices = (data['current_price'] < 0).sum()
            validation_results['negative_prices'] = int(negative_prices)
        
        # Check for outliers
        if 'demand' in data.columns:
            q1 = data['demand'].quantile(0.25)
            q3 = data['demand'].quantile(0.75)
            iqr = q3 - q1
            outliers = ((data['demand'] < (q1 - 1.5 * iqr)) | 
                       (data['demand'] > (q3 + 1.5 * iqr))).sum()
            validation_results['demand_outliers'] = int(outliers)
        
        logger.info("Data validation completed")
        return validation_results
        
    def transform_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform and clean data
        
        Args:
            data: DataFrame to transform
            
        Returns:
            Transformed DataFrame
        """
        try:
            df = data.copy()
            
            # Remove duplicates
            df = df.drop_duplicates()
            
            # Handle missing values
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
            
            # Remove negative prices
            if 'current_price' in df.columns:
                df = df[df['current_price'] > 0]
            
            # Add derived features
            if 'current_price' in df.columns and 'base_price' in df.columns:
                df['price_ratio'] = df['current_price'] / df['base_price']
            
            if 'demand' in df.columns:
                df['demand_level'] = pd.cut(
                    df['demand'],
                    bins=[0, 100, 300, 500, np.inf],
                    labels=['low', 'medium', 'high', 'very_high']
                )
            
            logger.info(f"Transformed data: {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Failed to transform data: {e}")
            return data
            
    def aggregate_metrics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Aggregate key metrics from the data
        
        Args:
            data: DataFrame to aggregate
            
        Returns:
            Dictionary with aggregated metrics
        """
        try:
            metrics = {
                'total_products': data['product_id'].nunique() if 'product_id' in data.columns else 0,
                'avg_price': float(data['current_price'].mean()) if 'current_price' in data.columns else 0,
                'avg_demand': float(data['demand'].mean()) if 'demand' in data.columns else 0,
                'total_records': len(data),
                'date_range': {
                    'start': str(data['timestamp'].min()) if 'timestamp' in data.columns else None,
                    'end': str(data['timestamp'].max()) if 'timestamp' in data.columns else None
                },
                'aggregated_at': datetime.now().isoformat()
            }
            
            # Price statistics
            if 'current_price' in data.columns:
                metrics['price_stats'] = {
                    'min': float(data['current_price'].min()),
                    'max': float(data['current_price'].max()),
                    'median': float(data['current_price'].median()),
                    'std': float(data['current_price'].std())
                }
            
            logger.info("Metrics aggregated successfully")
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to aggregate metrics: {e}")
            return {}
            
    def run_pipeline(self) -> Dict[str, Any]:
        """
        Run the complete data pipeline
        
        Returns:
            Dictionary with pipeline results
        """
        try:
            logger.info("Starting data pipeline execution")
            
            # Generate sample data
            data = self.generate_sample_data()
            
            # Ingest data
            ingest_success = self.ingest_data(data)
            
            # Validate data
            validation_results = self.validate_data(data)
            
            # Transform data
            transformed_data = self.transform_data(data)
            
            # Aggregate metrics
            metrics = self.aggregate_metrics(transformed_data)
            
            results = {
                'status': 'success' if ingest_success else 'partial',
                'records_processed': self.processed_records,
                'validation': validation_results,
                'metrics': metrics,
                'completed_at': datetime.now().isoformat()
            }
            
            logger.info("Data pipeline execution completed")
            return results
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'completed_at': datetime.now().isoformat()
            }
