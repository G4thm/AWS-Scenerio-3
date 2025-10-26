"""
Unit tests for Analytics module
"""

import pytest
import pandas as pd
from src.analytics import Analytics


def test_analytics_initialization():
    """Test analytics initialization"""
    analytics = Analytics()
    assert isinstance(analytics.insights, list)


def test_analyze_pricing_trends():
    """Test pricing trend analysis"""
    analytics = Analytics()
    data = pd.DataFrame({
        'current_price': [10.0, 20.0, 30.0, 40.0, 50.0]
    })
    
    result = analytics.analyze_pricing_trends(data)
    
    assert 'price_statistics' in result
    assert 'mean' in result['price_statistics']


def test_analyze_demand_patterns():
    """Test demand pattern analysis"""
    analytics = Analytics()
    data = pd.DataFrame({
        'demand': [100, 200, 300, 400, 500],
        'day_of_week': [0, 1, 2, 3, 4]
    })
    
    result = analytics.analyze_demand_patterns(data)
    
    assert 'demand_statistics' in result


def test_calculate_performance_metrics():
    """Test performance metrics calculation"""
    analytics = Analytics()
    model_metrics = {'r2_score': 0.92, 'rmse': 3.45}
    
    result = analytics.calculate_performance_metrics(model_metrics)
    
    assert 'model_performance' in result
    assert 'system_metrics' in result


def test_generate_insights():
    """Test insights generation"""
    analytics = Analytics()
    data = pd.DataFrame({
        'current_price': [10.0, 20.0, 30.0],
        'demand': [100, 200, 300],
        'competition_price': [12.0, 22.0, 32.0],
        'day_of_week': [0, 1, 2]
    })
    model_metrics = {'r2_score': 0.92, 'rmse': 3.45}
    
    insights = analytics.generate_insights(data, model_metrics)
    
    assert isinstance(insights, list)
    assert len(insights) > 0


def test_create_visualization_config():
    """Test visualization configuration"""
    analytics = Analytics()
    config = analytics.create_visualization_config()
    
    assert isinstance(config, dict)
    assert 'price_trend_chart' in config
