# OpenTracing Python Proposal

This repository includes a proposal to extend the OpenTracing Python API so
that the in-process context propagation can be handled by specific implementations.
A set of examples and over-simplified implementations are provided as a proof
of concepts to open discussion about pros and cons for this proposal.

The repository is structured as follows:
* `proposal/tracer.py`: includes the `TracerProposal` that should be part of the
  `Tracer` class in the `opentracing` library;
* `proposal/active_span_source.py`: includes the core of this proposal with some
  implementations; it's meant to become part of the OT API so that Tracer developers
  have some primitives to implement automatic in-process propagation
* `proposal/helpers.py`: includes a `TracedThread` that *may* be part of the proposal;
  while it's required to run the examples, we may keep it as an open question if it's
  a good idea having that in the OT core or not. Anyway, something similar is required
  otherwise there is no way with the current API to specify how to propagate (or not)
  the context to a new thread. We should take in consideration that the same rule
  is applied for `gevent` so a `TracedGreenlet` may be required in the future.
* `threaded_examples.py` and `asyncio_examples.py` are examples that use the proposal
  API. Some `assert` are here as a proof of concept that it's working (even if we
  don't have a complete implementation in this repository). Each example uses
  a different `ActiveSpanSource`.
