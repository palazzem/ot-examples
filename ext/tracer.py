from proposal import Tracer as ProposalMixin

from basictracer.tracer import BasicTracer


class DebugTracer(ProposalMixin, BasicTracer):
    """DebugTracer is a real implementation of an OpenTracing
    Tracer that uses the reference implementation extended with
    the Tracer proposal. It is used to run real examples with
    the extended API.
    """
    pass
