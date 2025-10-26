"""
Unit tests for Risk Assessment module
"""

import pytest
from src.risk_assessment import RiskAssessment


def test_risk_assessment_initialization():
    """Test risk assessment initialization"""
    risk_assessment = RiskAssessment()
    assert isinstance(risk_assessment.risks, list)


def test_identify_technical_risks():
    """Test technical risk identification"""
    risk_assessment = RiskAssessment()
    risks = risk_assessment.identify_technical_risks()
    
    assert isinstance(risks, list)
    assert len(risks) > 0
    assert 'risk_id' in risks[0]


def test_identify_security_risks():
    """Test security risk identification"""
    risk_assessment = RiskAssessment()
    risks = risk_assessment.identify_security_risks()
    
    assert isinstance(risks, list)
    assert len(risks) > 0


def test_identify_business_risks():
    """Test business risk identification"""
    risk_assessment = RiskAssessment()
    risks = risk_assessment.identify_business_risks()
    
    assert isinstance(risks, list)
    assert len(risks) > 0


def test_identify_operational_risks():
    """Test operational risk identification"""
    risk_assessment = RiskAssessment()
    risks = risk_assessment.identify_operational_risks()
    
    assert isinstance(risks, list)
    assert len(risks) > 0


def test_calculate_risk_score():
    """Test risk score calculation"""
    risk_assessment = RiskAssessment()
    test_risk = {
        'likelihood': 'high',
        'impact': 'high'
    }
    
    score = risk_assessment.calculate_risk_score(test_risk)
    
    assert isinstance(score, float)
    assert score > 0


def test_generate_risk_report():
    """Test risk report generation"""
    risk_assessment = RiskAssessment()
    report = risk_assessment.generate_risk_report()
    
    assert isinstance(report, str)
    assert len(report) > 0
