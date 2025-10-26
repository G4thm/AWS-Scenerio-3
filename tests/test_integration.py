"""
Integration tests for the complete system
"""

import pytest
from src.main import IntegratedCloudSolution


def test_integrated_solution_initialization():
    """Test integrated solution initialization"""
    solution = IntegratedCloudSolution()
    
    assert solution.data_lake is not None
    assert solution.ai_model is not None
    assert solution.data_pipeline is not None


def test_deploy_infrastructure():
    """Test infrastructure deployment"""
    solution = IntegratedCloudSolution()
    result = solution.deploy_infrastructure()
    
    assert 'status' in result
    assert 'components' in result


def test_train_ai_model():
    """Test AI model training"""
    solution = IntegratedCloudSolution()
    result = solution.train_ai_model()
    
    assert 'status' in result
    assert 'metrics' in result


def test_run_data_pipeline():
    """Test data pipeline execution"""
    solution = IntegratedCloudSolution()
    result = solution.run_data_pipeline()
    
    assert 'status' in result


def test_perform_security_audit():
    """Test security audit"""
    solution = IntegratedCloudSolution()
    result = solution.perform_security_audit()
    
    assert 'compliance_score' in result


def test_generate_analytics():
    """Test analytics generation"""
    solution = IntegratedCloudSolution()
    result = solution.generate_analytics()
    
    assert result is not None


def test_assess_risks():
    """Test risk assessment"""
    solution = IntegratedCloudSolution()
    result = solution.assess_risks()
    
    assert 'summary' in result
