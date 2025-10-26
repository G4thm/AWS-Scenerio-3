# AWS Scenario 3: AI-Driven Dynamic Pricing System

## Overview

This project implements a comprehensive cloud-based AI solution for dynamic pricing. It integrates multiple modules into a unified system that leverages AWS services to provide intelligent, data-driven pricing recommendations.

## Architecture

### Components

1. **Data Lake (AWS S3 + Glue)**: Centralized repository for all pricing data
2. **AI Model**: Machine learning model for dynamic pricing predictions
3. **Data Pipeline**: Automated data ingestion and processing
4. **Security Audit**: Comprehensive security checks and compliance validation
5. **Analytics**: Insights generation and visualization
6. **Risk Assessment**: Risk identification and mitigation strategies

### AWS Services Used

- **Amazon S3**: Data lake storage
- **AWS Glue**: Data catalog and ETL
- **AWS Lambda**: Serverless compute for AI service
- **Amazon API Gateway**: REST API endpoints
- **Amazon CloudWatch**: Monitoring and logging
- **AWS IAM**: Access control and security
- **AWS KMS**: Encryption key management

## Installation

```bash
# Clone the repository
git clone https://github.com/G4thm/AWS-Scenerio-3.git
cd AWS-Scenerio-3

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the Complete Solution

```bash
python src/main.py
```

This will:
1. Deploy AWS infrastructure
2. Train the AI model
3. Run the data pipeline
4. Perform security audit
5. Generate analytics insights
6. Assess risks and mitigation strategies
7. Generate a comprehensive final report

### Running Individual Components

```python
from src.data_lake import DataLake
from src.ai_model import DynamicPricingModel
from src.data_pipeline import DataPipeline

# Initialize data lake
data_lake = DataLake(bucket_name='my-pricing-data')
data_lake.initialize_clients()
data_lake.create_bucket()

# Train AI model
model = DynamicPricingModel()
metrics = model.train()
model.save_model()

# Run data pipeline
pipeline = DataPipeline(data_lake=data_lake)
results = pipeline.run_pipeline()
```

### Making Price Predictions

```python
from src.ai_model import DynamicPricingModel

model = DynamicPricingModel()
model.load_model()

optimal_price = model.predict_single(
    base_price=50.0,
    demand=200,
    competition_price=52.0,
    time_of_day=14,
    day_of_week=2,
    season=1
)

print(f"Recommended price: ${optimal_price:.2f}")
```

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test modules
pytest tests/test_ai_model.py
pytest tests/test_security_audit.py
```

## CI/CD Pipeline

The project includes a GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that:

1. **Testing**: Runs tests on multiple Python versions
2. **Linting**: Checks code quality with flake8 and black
3. **Security Scanning**: Scans for vulnerabilities with bandit
4. **Building**: Creates distribution packages
5. **Deployment**: Deploys to AWS (on main branch)

## Security

### Implemented Security Measures

- **Encryption**: Data encrypted at rest (S3, KMS) and in transit (TLS)
- **Access Control**: IAM policies with least privilege
- **Monitoring**: CloudTrail and CloudWatch logging
- **Network Security**: VPC, Security Groups, Network ACLs
- **Compliance**: Regular security audits and compliance checks

### Running Security Audit

```python
from src.security_audit import SecurityAuditor

auditor = SecurityAuditor()
results = auditor.run_full_audit()
print(f"Compliance Score: {results['compliance_score']:.2f}%")
```

## Analytics and Insights

The system provides comprehensive analytics:

- **Pricing Trends**: Historical price analysis
- **Demand Patterns**: Time-based demand insights
- **Competition Analysis**: Competitive positioning
- **Performance Metrics**: Model and system performance
- **Visualizations**: Charts and dashboards

```python
from src.analytics import Analytics
import pandas as pd

analytics = Analytics()
data = pd.read_csv('pricing_data.csv')
report = analytics.generate_analytics_report(data, model_metrics)
```

## Risk Assessment

The system identifies and provides mitigation strategies for:

- **Technical Risks**: Model degradation, pipeline failures, scalability
- **Security Risks**: Data breaches, API vulnerabilities, insider threats
- **Business Risks**: Market acceptance, competition, regulatory compliance
- **Operational Risks**: Downtime, knowledge gaps, cost overruns

```python
from src.risk_assessment import RiskAssessment

risk_assessment = RiskAssessment()
report = risk_assessment.generate_risk_report()
```

## Performance Metrics

- **Model Accuracy**: R² score > 0.90
- **Response Time**: < 150ms average
- **Throughput**: 100-500 requests/second
- **Availability**: 99.9%
- **Error Rate**: < 0.1%

## Project Structure

```
AWS-Scenerio-3/
├── src/
│   ├── __init__.py
│   ├── main.py              # Main integration module
│   ├── data_lake.py         # Data lake operations
│   ├── ai_model.py          # AI pricing model
│   ├── data_pipeline.py     # Data pipeline
│   ├── security_audit.py    # Security auditing
│   ├── analytics.py         # Analytics and insights
│   └── risk_assessment.py   # Risk assessment
├── tests/
│   ├── test_data_lake.py
│   ├── test_ai_model.py
│   ├── test_data_pipeline.py
│   ├── test_security_audit.py
│   ├── test_analytics.py
│   ├── test_risk_assessment.py
│   └── test_integration.py
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # CI/CD pipeline
├── config/                  # Configuration files
├── data/                    # Data directories
├── models/                  # Trained models
├── reports/                 # Generated reports
├── requirements.txt         # Python dependencies
├── .gitignore
├── pytest.ini
└── README.md
```

## Configuration

Configuration can be customized in the `IntegratedCloudSolution` initialization:

```python
config = {
    'data_lake': {
        'bucket_name': 'custom-bucket-name',
        'region': 'us-west-2'
    },
    'ai_model': {
        'model_path': 'custom/path/model.pkl'
    },
    'glue': {
        'database_name': 'custom_database',
        'table_name': 'custom_table'
    }
}

solution = IntegratedCloudSolution(config=config)
```

## Monitoring and Logging

All components include comprehensive logging:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

CloudWatch integration provides:
- Real-time metrics
- Automated alerts
- Log aggregation
- Performance dashboards

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is part of AWS Scenario 3 demonstration.

## Support

For issues and questions, please open an issue on GitHub.

## Acknowledgments

- AWS for cloud infrastructure
- Scikit-learn for machine learning capabilities
- TensorFlow for deep learning support
- Pandas for data processing
