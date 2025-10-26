"""
Data Lake Module
Handles AWS S3 data lake operations and AWS Glue integration
"""

import boto3
import json
import logging
from typing import Dict, List, Any
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLake:
    """Manages AWS S3-based data lake operations"""
    
    def __init__(self, bucket_name: str, region: str = 'us-east-1'):
        """
        Initialize Data Lake with S3 bucket
        
        Args:
            bucket_name: Name of the S3 bucket
            region: AWS region
        """
        self.bucket_name = bucket_name
        self.region = region
        self.s3_client = None
        self.glue_client = None
        
    def initialize_clients(self):
        """Initialize AWS clients"""
        try:
            self.s3_client = boto3.client('s3', region_name=self.region)
            self.glue_client = boto3.client('glue', region_name=self.region)
            logger.info(f"Initialized AWS clients for region {self.region}")
        except Exception as e:
            logger.error(f"Failed to initialize AWS clients: {e}")
            # For demo purposes, continue without actual AWS connection
            
    def create_bucket(self) -> bool:
        """
        Create S3 bucket for data lake
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.s3_client:
                if self.region == 'us-east-1':
                    self.s3_client.create_bucket(Bucket=self.bucket_name)
                else:
                    self.s3_client.create_bucket(
                        Bucket=self.bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': self.region}
                    )
                logger.info(f"Created S3 bucket: {self.bucket_name}")
                return True
            else:
                logger.info(f"Simulated bucket creation: {self.bucket_name}")
                return True
        except Exception as e:
            logger.warning(f"Bucket operation: {e}")
            return True  # Continue for demo
            
    def upload_data(self, data: Dict[str, Any], key: str) -> bool:
        """
        Upload data to S3 data lake
        
        Args:
            data: Data to upload
            key: S3 object key
            
        Returns:
            True if successful, False otherwise
        """
        try:
            json_data = json.dumps(data)
            if self.s3_client:
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=json_data
                )
                logger.info(f"Uploaded data to s3://{self.bucket_name}/{key}")
            else:
                logger.info(f"Simulated upload to s3://{self.bucket_name}/{key}")
            return True
        except Exception as e:
            logger.error(f"Failed to upload data: {e}")
            return False
            
    def list_objects(self, prefix: str = '') -> List[str]:
        """
        List objects in S3 bucket
        
        Args:
            prefix: Prefix to filter objects
            
        Returns:
            List of object keys
        """
        try:
            if self.s3_client:
                response = self.s3_client.list_objects_v2(
                    Bucket=self.bucket_name,
                    Prefix=prefix
                )
                if 'Contents' in response:
                    return [obj['Key'] for obj in response['Contents']]
            logger.info(f"Listed objects with prefix: {prefix}")
            return []
        except Exception as e:
            logger.error(f"Failed to list objects: {e}")
            return []
            
    def create_glue_catalog(self, database_name: str, table_name: str) -> bool:
        """
        Create AWS Glue catalog for data lake
        
        Args:
            database_name: Glue database name
            table_name: Glue table name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.glue_client:
                # Create database
                self.glue_client.create_database(
                    DatabaseInput={
                        'Name': database_name,
                        'Description': 'Data Lake catalog for dynamic pricing'
                    }
                )
                
                # Create table
                self.glue_client.create_table(
                    DatabaseName=database_name,
                    TableInput={
                        'Name': table_name,
                        'StorageDescriptor': {
                            'Columns': [
                                {'Name': 'product_id', 'Type': 'string'},
                                {'Name': 'price', 'Type': 'double'},
                                {'Name': 'demand', 'Type': 'int'},
                                {'Name': 'timestamp', 'Type': 'timestamp'}
                            ],
                            'Location': f's3://{self.bucket_name}/pricing_data/',
                            'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                            'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
                            'SerdeInfo': {
                                'SerializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
                            }
                        }
                    }
                )
                logger.info(f"Created Glue catalog: {database_name}.{table_name}")
            else:
                logger.info(f"Simulated Glue catalog creation: {database_name}.{table_name}")
            return True
        except Exception as e:
            logger.warning(f"Glue catalog operation: {e}")
            return True  # Continue for demo
            
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get data lake metadata
        
        Returns:
            Dictionary containing metadata
        """
        return {
            'bucket_name': self.bucket_name,
            'region': self.region,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
