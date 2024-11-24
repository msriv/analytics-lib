from functools import wraps
from typing import Callable, Dict, Optional, Any

class PipelineComponent:
    def __init__(
        self,
        name: str,
        component_type: str,
        func: Callable,
        config: Optional[Dict] = None,
    ):
        self.name = name
        self.component_type = component_type
        self.func = func
        self.config = config
        self.next = None
        self.previous = None

    def __rshift__(self, other: 'PipelineComponent') -> 'PipelineComponent':
        """Enable >> operator for pipeline construction"""
        self.next = other
        other.previous = self
        return other

    def __rrshift__(self, other: 'PipelineComponent') -> 'PipelineComponent':
        """Enable right shift for pipeline construction"""
        other.next = self
        self.previous = other
        return self

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Make the component callable"""
        return self.func(*args, **kwargs)

    def get_first_component(self) -> 'PipelineComponent':
        """Get the first component in the pipeline"""
        current = self
        while current.previous:
            current = current.previous
        return current


class SourceComponent(PipelineComponent):
    def __init__(
        self,
        name: str,
        source_type: str,
        func: Callable,
        config: Dict
    ):
        super().__init__(name, "source", func, config)
        self.source_type = source_type

class TransformComponent(PipelineComponent):
    def __init__(
        self,
        name: str,
        func: Callable,
        config: Optional[Dict] = None
    ):
        super().__init__(name, "transform", func, config)

class SinkComponent(PipelineComponent):
    def __init__(
        self,
        name: str,
        sink_type: str,
        func: Callable,
        config: Dict
    ):
        super().__init__(name, "sink", func, config)
        self.sink_type = sink_type

def source(source_type: str):
    """Decorator for source components"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> SourceComponent:
            config = func(*args, **kwargs)
            return SourceComponent(
                name=func.__name__,
                source_type=source_type,
                func=func,
                config=config
            )
        return wrapper
    return decorator

def transform(func: Callable):
    """Decorator for transformation components"""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> TransformComponent:
        return TransformComponent(
            name=func.__name__,
            func=func,
            config={"args": args, "kwargs": kwargs}
        )
    return wrapper

def sink(sink_type: str):
    """Decorator for sink components"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> SinkComponent:
            config = func(*args, **kwargs)
            return SinkComponent(
                name=func.__name__,
                sink_type=sink_type,
                func=func,
                config=config
            )
        return wrapper
    return decorator
