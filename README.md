# Simple ETL Pipeline Library

A lightweight, intuitive library for building data pipelines with minimal setup and maximum flexibility.

## Core Concept

The library allows users to build data pipelines using a simple, declarative syntax while handling complex ETL operations under the hood. It uses decorator patterns and operator overloading to create readable pipeline definitions.

### Basic Example

```py
@source("kafka")
def read_users(topic):
    return {"topic": topic, "bootstrap_servers": "localhost:9092"}

@transform
def clean_user_data(data):
    return {
        "name": data["name"].strip(),
        "email": data["email"].lower()
    }

@sink("bigquery")
def store_users(dataset, table):
    return {"dataset": dataset, "table": table}

pipeline = (
    read_users("raw_users")
    >> clean_user_data()
    >> store_users("analytics", "processed_users")
)
```

### Features

#### 1\. Cloud Provider Support

- GCP (Google Cloud Platform)
  - PubSub Topics
  - Dataflow Jobs
  - BigQuery Tables
- \[Planned\] AWS
  - Kinesis
  - Lambda
  - Redshift
- \[Planned\] Azure
  - Event Hubs
  - Data Factory
  - Synapse

#### 2\. Infrastructure as Code Generation

- Terraform configurations
- Cloud-specific templates
- Deployment scripts

### Usage Example

```py
# Define pipeline components
@source("pubsub")
def read_messages(topic_name: str):
    return {
        "topic_name": topic_name,
        "subscription_name": f"{topic_name}-sub"
    }

@transform
def process_messages(data):
    return {
        "name": data["name"],
        "email": data["email"].lower()
    }

@sink("bigquery")
def write_to_bq(dataset: str, table: str):
    return {
        "dataset": dataset,
        "table": table
    }

# Create pipeline
pipeline = (
    read_messages("user-events")
    >> process_messages()
    >> write_to_bq("analytics", "processed_users")
)

# Generate infrastructure
generator = InfrastructureGenerator(provider="gcp")
generator.generate(pipeline)
```

### Generated Assets

#### 1\. Terraform Configuration

```
provider "google" {
    project = var.project_id
    region  = var.region
}

# PubSub Topic
resource "google_pubsub_topic" "topic" {
    name = "user-events"
    project = var.project_id
}

# BigQuery Resources
resource "google_bigquery_dataset" "dataset" {
    dataset_id = "analytics"
    project    = var.project_id
}

resource "google_bigquery_table" "table" {
    dataset_id = google_bigquery_dataset.dataset.dataset_id
    table_id   = "processed_users"
}
```

#### 2\. Dataflow Template

```
{
    "name": "process-messages",
    "parameters": {
        "input": "projects/${PROJECT}/topics/user-events",
        "output": "projects/${PROJECT}/datasets/analytics/tables/processed_users"
    },
    "environment": {
        "tempLocation": "gs://${BUCKET}/temp",
        "zone": "us-central1-a"
    }
}
```

#### 3\. Deployment Script

```
#!/bin/bash

# Set up GCP project
gcloud config set project ${PROJECT_ID}

# Initialize and apply Terraform
terraform init
terraform apply -auto-approve

# Deploy Dataflow job
gcloud dataflow jobs run process-messages \
    --gcs-location=${TEMPLATE_PATH} \
    --parameters="input=${TOPIC},output=${TABLE}"
```

### Infrastructure Generation Process

1. **Analysis Phase**

   - Parse pipeline definition
   - Identify required resources
   - Determine dependencies



2. **Generation Phase**

   - Create IaC configurations
   - Generate service templates
   - Produce deployment scripts



3. **Validation Phase**

   - Verify resource configurations
   - Check dependencies
   - Validate permissions

### Configuration Options

```py
# Infrastructure generation configuration
config = {
    "provider": "gcp",
    "project": "my-project",
    "region": "us-central1",
    "options": {
        "terraform_version": "1.0.0",
        "state_bucket": "tf-state-bucket",
        "auto_approve": True
    }
}

generator = InfrastructureGenerator(config)
```

### Best Practices

1. **Resource Naming**

   - Use consistent naming conventions
   - Include environment identifiers
   - Consider resource limits



2. **Security**

   - Follow principle of least privilege
   - Use service accounts
   - Encrypt sensitive data



3. **Cost Management**

   - Set resource limits
   - Use appropriate machine types
   - Configure auto-scaling



4. **Monitoring**

   - Enable resource logging
   - Set up alerts
   - Monitor costs

### Supported Resource Types

#### GCP

- **Sources**
  - PubSub Topics
  - Cloud Storage
  - Cloud SQL
- **Processing**
  - Dataflow
  - Cloud Functions
  - Cloud Run
- **Sinks**
  - BigQuery
  - Cloud Storage
  - Cloud SQL

## Architecture

### 1\. Component System

- **Sources**: Data input components (Kafka, Files, Databases)
- **Transformations**: Data processing components
- **Sinks**: Data output components (BigQuery, GCS, Databases)

### 2\. Pipeline Orchestration

- Component validation
- Pipeline DAG construction
- Execution flow management
- Resource management

### 3\. Execution Engines

- Apache Beam support
- Databricks support
- Local execution mode

## Current Features

### 1\. Decorator-based Component Definition

```py
@source("kafka")
@transform
@sink("bigquery")
```

### 2\. Pipeline Construction

- Intuitive operator-based syntax (\>\>)
- Automatic component linking
- Pipeline validation

### 3\. Basic Data Flow

- Source data reading
- Transformation application
- Sink writing

## Planned Features

### 1\. Data Processing

- [x] Basic transformation support
- [ ] Batch processing
- [ ] Stream processing
- [ ] Window operations
- [ ] Custom operators

### 2\. Error Handling

- [ ] Retry mechanisms
- [ ] Dead letter queues
- [ ] Error logging
- [ ] Circuit breakers
- [ ] Fallback strategies

### 3\. Validation

- [ ] Schema validation
- [ ] Data quality checks
- [ ] Pipeline structure validation
- [ ] Configuration validation

### 4\. Monitoring & Observability

- [ ] Performance metrics
- [ ] Pipeline status tracking
- [ ] Logging system
- [ ] Alert mechanisms
- [ ] Dashboard integration

### 5\. Scalability Features

- [ ] Parallel processing
- [ ] Distributed execution
- [ ] Resource optimization
- [ ] Load balancing
- [ ] Backpressure handling

### 6\. Advanced Features

- [ ] Pipeline templating
- [ ] Component reusability
- [ ] Pipeline versioning
- [ ] Hot reloading
- [ ] A/B testing support

### 7\. Connectors

#### Sources

- [ ] Apache Kafka
- [ ] Files (CSV, JSON, Parquet)
- [ ] REST APIs
- [ ] Databases (SQL, NoSQL)
- [ ] Cloud Storage

#### Sinks

- [ ] BigQuery
- [ ] Cloud Storage
- [ ] Databases
- [ ] Message Queues
- [ ] APIs

## Usage Examples

### 1\. Basic ETL Pipeline

```py
@source("file")
def read_csv(path):
    return {"path": path, "format": "csv"}

@transform
def filter_data(data, condition):
    return filter(condition, data)

@sink("bigquery")
def write_to_bq(table):
    return {"table": table}

pipeline = (
    read_csv("data.csv")
    >> filter_data(lambda x: x['age'] > 25)
    >> write_to_bq("filtered_users")
)
```

### 2\. Streaming Pipeline

```py
@source("kafka")
def read_stream(topic):
    return {"topic": topic}

@transform
def process_stream(data):
    return transform_logic(data)

@sink("kafka")
def write_stream(topic):
    return {"topic": topic}

pipeline = (
    read_stream("input")
    >> process_stream()
    >> write_stream("output")
)
```

## Best Practices

### 1\. Pipeline Design

- Keep transformations atomic
- Use appropriate batch sizes
- Implement proper error handling
- Monitor pipeline performance
- Validate data at critical points

### 2\. Performance Optimization

- Use batch processing where appropriate
- Implement caching strategies
- Optimize resource usage
- Use parallel processing when possible

### 3\. Error Handling

- Always implement retry logic
- Use dead letter queues
- Log errors appropriately
- Set up alerts for critical failures

## Contribution Guidelines

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit pull request
5. Follow code style guidelines

## Installation

```
pip install simple-etl-pipeline
```

## License

MIT License

## Support

- GitHub Issues
- Documentation
- Community Forum
