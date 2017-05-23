from opentracing.tracer import Tracer as OTBaseTracer


class Tracer(OTBaseTracer):
    """Tracer class that provides some extension to the base OpenTracing
    API for Python. This class must define all new / updated API
    so that they can be used in some examples.

    Defined methods must be implemented as noop for the moment.
    """
    pass
