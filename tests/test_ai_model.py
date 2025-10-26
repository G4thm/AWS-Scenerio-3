"""
Unit tests for AI Model module
"""

import pytest
import numpy as np
from src.ai_model import DynamicPricingModel


def test_model_initialization():
    """Test model initialization"""
    model = DynamicPricingModel(model_path='test_model.pkl')
    assert model.model_path == 'test_model.pkl'
    assert model.is_trained is False


def test_generate_training_data():
    """Test training data generation"""
    model = DynamicPricingModel()
    features, targets = model.generate_training_data(n_samples=100)
    
    assert features.shape[0] == 100
    assert features.shape[1] == 6  # 6 features
    assert len(targets) == 100


def test_model_training():
    """Test model training"""
    model = DynamicPricingModel()
    metrics = model.train()
    
    assert 'rmse' in metrics
    assert 'r2_score' in metrics
    assert 'trained_at' in metrics
    assert model.is_trained is True


def test_model_prediction():
    """Test model prediction"""
    model = DynamicPricingModel()
    model.train()
    
    prediction = model.predict_single(
        base_price=50.0,
        demand=200,
        competition_price=52.0,
        time_of_day=14,
        day_of_week=2,
        season=1
    )
    
    assert isinstance(prediction, float)
    assert prediction > 0


def test_feature_importance():
    """Test feature importance extraction"""
    model = DynamicPricingModel()
    model.train()
    
    importance = model.get_feature_importance()
    
    assert isinstance(importance, dict)
    assert len(importance) == 6
    assert 'base_price' in importance
    assert 'demand' in importance
