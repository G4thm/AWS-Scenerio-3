"""
Unit tests for Data Lake module
"""

import pytest
from src.data_lake import DataLake


def test_data_lake_initialization():
    """Test DataLake initialization"""
    data_lake = DataLake(bucket_name='test-bucket', region='us-east-1')
    assert data_lake.bucket_name == 'test-bucket'
    assert data_lake.region == 'us-east-1'


def test_data_lake_metadata():
    """Test DataLake metadata generation"""
    data_lake = DataLake(bucket_name='test-bucket')
    metadata = data_lake.get_metadata()
    
    assert 'bucket_name' in metadata
    assert 'region' in metadata
    assert 'created_at' in metadata
    assert 'status' in metadata
    assert metadata['bucket_name'] == 'test-bucket'


def test_create_bucket():
    """Test bucket creation"""
    data_lake = DataLake(bucket_name='test-bucket')
    result = data_lake.create_bucket()
    assert result is True


def test_upload_data():
    """Test data upload"""
    data_lake = DataLake(bucket_name='test-bucket')
    test_data = {'test': 'data', 'value': 123}
    result = data_lake.upload_data(test_data, 'test/key.json')
    assert result is True


def test_list_objects():
    """Test object listing"""
    data_lake = DataLake(bucket_name='test-bucket')
    objects = data_lake.list_objects(prefix='test/')
    assert isinstance(objects, list)
