from core.decorators import source, transform, sink
from typing import List
from core.orchestrator import PipelineOrchestrator

if __name__ == "__main__":
    # Define components
    @source("kafka")
    def read_from_kafka(topic: str, servers: str):
        return {
            "topic": topic,
            "bootstrap_servers": servers
        }

    @transform
    def clean_data(columns: List[str]):
        return {
            "columns": columns
        }

    @sink("bigquery")
    def write_to_bq(dataset: str, table: str):
        return {
            "dataset": dataset,
            "table": table
        }

    # Construct pipeline
    pipeline = (
        read_from_kafka("users", "localhost:9092")
        >> clean_data(["name", "email"])
        >> write_to_bq("analytics", "processed_users")
    )

    # Initialize orchestrator
    orchestrator = PipelineOrchestrator()

    # Validate and build execution graph
    try:
        orchestrator.validate_pipeline(pipeline)
        execution_graph = orchestrator.build_execution_graph()
        print("Pipeline validated successfully!")
        print("Execution graph:", execution_graph)
    except ValueError as e:
        print(f"Pipeline validation failed: {str(e)}")
