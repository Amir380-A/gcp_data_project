from airflow import DAG
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="gcs_to_bigquery_pipeline_v7",
    start_date=datetime(2025, 12, 22),
    schedule="@monthly",
    catchup=False,
    tags=["gcs", "bigquery", "dbt"],
) as dag:

    wait_for_orders = GCSObjectExistenceSensor(
        task_id="wait_for_gcs_file",
        bucket="raw-data-bucket-amir",
        object="orders",
        timeout=600,
        poke_interval=30,
    )

    load_to_bigquery = GCSToBigQueryOperator(
        task_id="load_orders_to_bigquery",
        bucket="raw-data-bucket-amir",
        source_objects=["orders"],
        destination_project_dataset_table="data-pipeline-478808.dbt.orders",
        source_format="CSV",
        skip_leading_rows=1,
        autodetect=False,
        schema_fields=[
            {"name": "order_id", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "user_id", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "status", "type": "STRING", "mode": "NULLABLE"},
            {"name": "gender", "type": "STRING", "mode": "NULLABLE"},
            {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "returned_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "shipped_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "delivered_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "num_of_item", "type": "INTEGER", "mode": "NULLABLE"},
        ],
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_APPEND",
    )



    wait_for_order_items = GCSObjectExistenceSensor(
        task_id="wait_for_order_items_file",
        bucket="raw-data-bucket-amir",
        object="order_items",
        timeout=600,
        poke_interval=30,
    )

    load_order_items = GCSToBigQueryOperator(
        task_id="load_order_items_to_bigquery",
        bucket="raw-data-bucket-amir",
        source_objects=["order_items"],
        destination_project_dataset_table="data-pipeline-478808.dbt.order_items",
        source_format="CSV",
        skip_leading_rows=1,
        autodetect=True,
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_APPEND",
    )
    wait_for_users = GCSObjectExistenceSensor(
        task_id="wait_for_users_file",
        bucket="raw-data-bucket-amir",
        object="users",
        timeout=600,
        poke_interval=30,
    )

    load_users = GCSToBigQueryOperator(
        task_id="load_users_to_bigquery",
        bucket="raw-data-bucket-amir",
        source_objects=["users"],
        destination_project_dataset_table="data-pipeline-478808.dbt.users",
        source_format="CSV",
        skip_leading_rows=1,
        autodetect=True,
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_APPEND",
    )

    wait_for_products = GCSObjectExistenceSensor(
        task_id="wait_for_products_file",
        bucket="raw-data-bucket-amir",
        object="products",
        timeout=600,
        poke_interval=30,
    )

    load_products = GCSToBigQueryOperator(
        task_id="load_products_to_bigquery",
        bucket="raw-data-bucket-amir",
        source_objects=["products"],
        destination_project_dataset_table="data-pipeline-478808.dbt.products",
        source_format="CSV",
        skip_leading_rows=1,
        autodetect=True,
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_APPEND",
    )

    wait_for_inventory_items = GCSObjectExistenceSensor(
        task_id="wait_for_inventory_items_file",
        bucket="raw-data-bucket-amir",
        object="inventory_items",
        timeout=600,
        poke_interval=30,
    )

    load_inventory_items = GCSToBigQueryOperator(
        task_id="load_inventory_items_to_bigquery",
        bucket="raw-data-bucket-amir",
        source_objects=["inventory_items"],
        destination_project_dataset_table="data-pipeline-478808.dbt.inventory_items",
        source_format="CSV",
        skip_leading_rows=1,
        autodetect=True,
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_APPEND",
    )

    wait_for_distribution_centers = GCSObjectExistenceSensor(
        task_id="wait_for_distribution_centers_file",
        bucket="raw-data-bucket-amir",
        object="distribution_centers",
        timeout=600,
        poke_interval=30,
    )

    load_distribution_centers = GCSToBigQueryOperator(
        task_id="load_distribution_centers_to_bigquery",
        bucket="raw-data-bucket-amir",
        source_objects=["distribution_centers"],
        destination_project_dataset_table="data-pipeline-478808.dbt.distribution_centers",
        source_format="CSV",
        skip_leading_rows=1,
        autodetect=True,
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_APPEND",
    )


    run_dbt = BashOperator(
        task_id="run_dbt_models",
        bash_command="""
        cd /workspace/dbt_project &&
        dbt source freshness &&
        dbt run &&
        dbt test
        """,
    )
    wait_for_users >> load_users
    wait_for_products >> load_products
    wait_for_inventory_items >> load_inventory_items
    wait_for_distribution_centers >> load_distribution_centers

    [
        load_to_bigquery,
        load_order_items,
        load_users,
        load_products,
        load_inventory_items,
        load_distribution_centers,
    ] >> run_dbt

