from proposal import Span as ProposalMixin

from basictracer.span import BasicSpan


class Span(ProposalMixin, BasicSpan):
    """Class that extends the BasicSpan reference implementation
    with the proposal API"""
    pass
