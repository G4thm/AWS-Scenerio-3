"""
Unit tests for Security Audit module
"""

import pytest
from src.security_audit import SecurityAuditor


def test_security_auditor_initialization():
    """Test security auditor initialization"""
    auditor = SecurityAuditor()
    assert auditor.compliance_score == 0


def test_check_data_encryption():
    """Test data encryption checks"""
    auditor = SecurityAuditor()
    result = auditor.check_data_encryption()
    
    assert 'check_name' in result
    assert 'checks' in result
    assert 'overall_status' in result


def test_check_access_control():
    """Test access control checks"""
    auditor = SecurityAuditor()
    result = auditor.check_access_control()
    
    assert 'check_name' in result
    assert result['check_name'] == 'access_control'


def test_check_network_security():
    """Test network security checks"""
    auditor = SecurityAuditor()
    result = auditor.check_network_security()
    
    assert 'check_name' in result
    assert result['check_name'] == 'network_security'


def test_full_audit():
    """Test full security audit"""
    auditor = SecurityAuditor()
    results = auditor.run_full_audit()
    
    assert 'audit_id' in results
    assert 'compliance_score' in results
    assert 'audit_details' in results
    assert results['compliance_score'] > 0


def test_generate_compliance_report():
    """Test compliance report generation"""
    auditor = SecurityAuditor()
    report = auditor.generate_compliance_report()
    
    assert isinstance(report, str)
    assert len(report) > 0
