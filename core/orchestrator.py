from typing import List, Dict, Any
from .decorators import PipelineComponent

class PipelineOrchestrator:
    """Main orchestrator for pipeline execution"""

    def __init__(self):
        self.components: List[PipelineComponent] = []
        self.execution_graph: Dict[str, Dict[str, Any]] = {}
        self.validate_rules = {
            "source": ["transform", "sink"],
            "transform": ["transform", "sink"],
            "sink": []
        }

    def validate_pipeline(self, entry_point: PipelineComponent) -> None:
        """Validate the pipeline structure"""
        # Get the first component in the chain
        first_component = entry_point.get_first_component()
        current = first_component

        # Validate source starts the pipeline
        if current.component_type != "source":
            raise ValueError("Pipeline must start with a source component")

        while current:
            # Validate component connections
            if current.previous:
                self._validate_connection(current.previous, current)

            # Add to components list
            self.components.append(current)

            # Move to next component
            current = current.next

        # Validate pipeline ends with sink
        if self.components[-1].component_type != "sink":
            raise ValueError("Pipeline must end with a sink component")

    def _validate_connection(
        self,
        prev: PipelineComponent,
        current: PipelineComponent
    ) -> None:
        """Validate connection between two components"""
        if current.component_type not in self.validate_rules[prev.component_type]:
            raise ValueError(
                f"Invalid pipeline sequence: {prev.component_type} cannot be followed by {current.component_type}"
            )

    def build_execution_graph(self) -> Dict[str, Dict[str, Any]]:
        """Build the execution graph from components"""
        for component in self.components:
            self.execution_graph[component.name] = {
                'type': component.component_type,
                'next': component.next.name if component.next else None,
                'config': component.config,
                'component': component
            }
        return self.execution_graph
