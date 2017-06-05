"""Context propagation examples when using greenlet based
concurrent programming.
"""
import gevent

from ext import tracer, helpers


def main_greenlet_instrumented_only():
    """The main greenlet is instrumented but not its children."""
    def do_some_work():
        # code executed in children greenlets; they don't have an ActiveSpan
        assert tracer.active_span_source.active_span() is None

    # code executed in the main greenlet
    with tracer.start_active(operation_name='main_greenlet') as span:
        greenlets = [gevent.spawn(do_some_work) for _ in range(5)]
        gevent.joinall(greenlets)


def main_greenlet_instrumented_children_continue():
    """The main greenlet is instrumented and when it spawns
    new greenlets, they continue the main greenlet trace.
    """
    def do_some_work():
        # code executed in children greenlets; it must continue
        # the trace started in another greenlet
        assert tracer.active_span_source.active_span() is not None
        with tracer.start_active(operation_name='child_greenlet') as span:
            pass

    # code executed in the main greenlet
    with tracer.start_active(operation_name='main_greenlet') as span:
        greenlets = [helpers.TracedGreenlet.spawn(do_some_work) for _ in range(5)]
        gevent.joinall(greenlets)


def main_greenlet_instrumented_children_not_continue():
    """The main greenlet is instrumented and when it spawns
    new greenlets, they don't continue the main greenlet trace.
    Each greenlet has its own trace.
    """
    def do_some_work():
        # code executed in children greenlets; it doesn't continue
        # the trace started in another greenlet
        assert tracer.active_span_source.active_span() is None
        with tracer.start_active(operation_name='child_greenlet') as span:
            pass

    # code executed in the main greenlet
    with tracer.start_active(operation_name='main_greenlet') as span:
        greenlets = [gevent.spawn(do_some_work) for _ in range(5)]

    # don't wait for greenlets execution
    gevent.joinall(greenlets)


def main_greenlet_not_instrumented_children():
    """The main greenlet is not instrumented but its children
    are, each children has its own trace.
    """
    def do_some_work():
        # code executed in children greenlets; it doesn't continue
        # the trace started in another greenlet
        assert tracer.active_span_source.active_span() is None
        with tracer.start_active(operation_name='child_greenlet') as span:
            pass

    # code executed in the main greenlet
    greenlets = [gevent.spawn(do_some_work) for _ in range(5)]
    gevent.joinall(greenlets)
