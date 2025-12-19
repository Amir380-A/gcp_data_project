{% docs __overview__ %}

# GCP Cloud-Native Analytics Platform

This documentation describes a **cloud-native data and machine learning platform built on Google Cloud Platform**.

## Data Flow
- Source data is ingested into **BigQuery (ecomm dataset)**
- Transformations are managed using **dbt (staging → marts)**
- Analytics are exposed via **Looker Studio**
- Machine learning models are trained using **Vertex AI AutoML**
- Real-time predictions are served via **Pub/Sub and Cloud Run**

## Data Modeling Layers

### Raw
Read-only source tables ingested into BigQuery.

### Marts
- Fact and dimension tables
- Optimized for BI and ML consumption
- Stable grains and documented metrics

## Machine Learning
- Feature engineering performed in dbt marts
- AutoML classification model predicts lead conversion
- Deployed to Vertex AI endpoints

## CI/CD
- dbt models and tests executed via Cloud Build
- dbt Docs auto-generated and deployed to GCS

{% enddocs %}

