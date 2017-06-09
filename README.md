# OpenTracing Python Proposal

This repository includes a proposal to extend the OpenTracing Python API so
that the in-process context propagation can be handled by specific implementations.
A set of examples and over-simplified implementations are provided as a proof
of concepts to open discussion about pros and cons of this proposal.

The repository is structured as follows:
* `proposal`: includes all that is part of the proposal; this is a backport of PR
   available in the main opentracing repository
* `ext`: includes simplified implementations that are used as a proof of concept.
  These implementations are used by examples available in this repository;
* `examples`: includes many simple and real use cases when dealing with different
  executions flow. Some of these examples may be extended and considered as
  unittests to validate if a `Tracer` implementation honors the specification.

## Run the examples

To run the examples, create a Python virtualenv and then::

    pip install -r requirements.txt
    python run_examples.py
    python run_server_example.py

Examples require Python 3.5+ because `asyncio` library is used in some of them.
