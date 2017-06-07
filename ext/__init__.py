from .tracer import DebugTracer
from .recorder import LogRecorder


# Global variable that should be initialized to an instance of real tracer.
tracer = DebugTracer(recorder=LogRecorder())
