"""Context propagation examples when dealing with multi-threaded
applications.

TODO: provide a better description for each example describing
the exact use case.
"""
import threading

from proposal import tracer, helpers
from proposal.active_span_source import ThreadActiveSpanSource


# set the ThreadActiveSpanSource for those examples
# TODO: move this init somewhere else
tracer._active_span_source = ThreadActiveSpanSource()


def main_thread_instrumented_only():
    """The main thread is instrumented but not its children."""
    def do_some_work():
        # code executed in children threads; they don't have an ActiveSpan
        assert tracer.active_span_source.active_span() is None

    # code executed in the main thread
    with tracer.start_active(operation_name='main_thread') as span:
        threads = [threading.Thread(target=do_some_work) for _ in range(5)]
        for t in threads:
            t.start()

        # ...do more work in the main thread...
        for t in threads:
            t.join(timeout=1)


def main_thread_instrumented_children_continue():
    """The main thread is instrumented and when it spawns
    new threads, they continue the main thread trace.
    """
    def do_some_work():
        # code executed in children threads; it must continue
        # the trace started in another thread
        assert tracer.active_span_source.active_span() is not None
        with tracer.start_active(operation_name='child_thread') as span:
            pass

    # code executed in the main thread
    with tracer.start_active(operation_name='main_thread') as span:
        threads = [helpers.TracedThread(target=do_some_work) for _ in range(5)]
        for t in threads:
            t.start()

        # ...do more work in the main thread...
        for t in threads:
            t.join(timeout=1)


def main_thread_instrumented_children_not_continue():
    """The main thread is instrumented and when it spawns
    new threads, they don't continue the main thread trace.
    Each thread has its own trace.
    """
    def do_some_work():
        # code executed in children threads; it doesn't continue
        # the trace started in another thread
        assert tracer.active_span_source.active_span() is None
        with tracer.start_active(operation_name='child_thread') as span:
            pass

    # code executed in the main thread
    with tracer.start_active(operation_name='main_thread') as span:
        threads = [threading.Thread(target=do_some_work) for _ in range(5)]
        for t in threads:
            t.start()

        # ...do more work in the main thread...

    for t in threads:
        t.join(timeout=1)


def main_thread_not_instrumented_children():
    """The main thread is not instrumented but its children
    are, each children has its own trace.
    """
    def do_some_work():
        # code executed in children threads; it doesn't continue
        # the trace started in another thread
        assert tracer.active_span_source.active_span() is None
        with tracer.start_active(operation_name='child_thread') as span:
            pass

    # code executed in the main thread
    threads = [threading.Thread(target=do_some_work) for _ in range(5)]
    for t in threads:
        t.start()

    # ...do more work in the main thread...
    for t in threads:
        t.join(timeout=1)


# will be moved somewhere else to keep the module only with examples
if __name__ == '__main__':
    main_thread_instrumented_only()
    main_thread_instrumented_children_continue()
    main_thread_instrumented_children_not_continue()
    main_thread_not_instrumented_children()