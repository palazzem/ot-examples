from ext import tracer
from ext.active_span_source import (
    AsyncioActiveSpanSource,
    ThreadActiveSpanSource,
)

from examples import asyncio, multi_threaded


# use a specific ActiveSpanSource implementation


if __name__ == '__main__':
    # asyncio examples
    tracer._active_span_source = AsyncioActiveSpanSource()
    asyncio.coroutine_continue_propagation()
    asyncio.coroutine_with_callbacks()

    # multi-threaded examples
    tracer._active_span_source = ThreadActiveSpanSource()
    multi_threaded.main_thread_instrumented_only()
    multi_threaded.main_thread_instrumented_children_continue()
    multi_threaded.main_thread_instrumented_children_not_continue()
    multi_threaded.main_thread_not_instrumented_children()
