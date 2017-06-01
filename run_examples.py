from examples import asyncio, multi_threaded


if __name__ == '__main__':
    # asyncio examples
    asyncio.coroutine_continue_propagation()
    asyncio.coroutine_with_callbacks()

    # multi-threaded examples
    multi_threaded.main_thread_instrumented_only()
    multi_threaded.main_thread_instrumented_children_continue()
    multi_threaded.main_thread_instrumented_children_not_continue()
    multi_threaded.main_thread_not_instrumented_children()
