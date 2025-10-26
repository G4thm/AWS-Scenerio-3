"""
Unit tests for Data Pipeline module
"""

import pytest
import pandas as pd
from src.data_pipeline import DataPipeline


def test_pipeline_initialization():
    """Test pipeline initialization"""
    pipeline = DataPipeline()
    assert pipeline.processed_records == 0


def test_generate_sample_data():
    """Test sample data generation"""
    pipeline = DataPipeline()
    data = pipeline.generate_sample_data(n_products=10, days=5)
    
    assert isinstance(data, pd.DataFrame)
    assert len(data) == 50  # 10 products * 5 days
    assert 'product_id' in data.columns
    assert 'current_price' in data.columns


def test_data_validation():
    """Test data validation"""
    pipeline = DataPipeline()
    data = pipeline.generate_sample_data(n_products=5, days=2)
    
    validation = pipeline.validate_data(data)
    
    assert 'total_records' in validation
    assert 'missing_values' in validation
    assert validation['total_records'] == 10


def test_data_transformation():
    """Test data transformation"""
    pipeline = DataPipeline()
    data = pipeline.generate_sample_data(n_products=5, days=2)
    
    transformed = pipeline.transform_data(data)
    
    assert isinstance(transformed, pd.DataFrame)
    assert len(transformed) > 0


def test_aggregate_metrics():
    """Test metrics aggregation"""
    pipeline = DataPipeline()
    data = pipeline.generate_sample_data(n_products=5, days=2)
    
    metrics = pipeline.aggregate_metrics(data)
    
    assert 'total_products' in metrics
    assert 'avg_price' in metrics
    assert metrics['total_products'] > 0


def test_run_pipeline():
    """Test complete pipeline execution"""
    pipeline = DataPipeline()
    results = pipeline.run_pipeline()
    
    assert 'status' in results
    assert 'records_processed' in results
    assert 'validation' in results
