from tornado.stack_context import StackContextInconsistentError, _state


class TracerStackContext(object):
    """A context manager that can be used to persist local states.
    It must be used everytime a Tornado's handler or coroutine is traced.
    It is meant to work like a traditional ``StackContext``, preserving the
    state across asynchronous calls.

    An ActiveSpan attached to a ``TracerStackContext`` is not shared between
    different threads.

    This simple implementation follows the suggestions provided here:
    https://github.com/tornadoweb/tornado/issues/1063

    This implementation is outside the scope of OpenTracing. Probably it's
    something that may be provided by vendors or by the framework itself.
    """
    def __init__(self):
        self.active = True
        self.data = {}

    def enter(self):
        """Required to preserve the ``StackContext`` interface"""
        pass

    def exit(self, type, value, traceback):
        """Required to preserve the ``StackContext`` interface"""
        pass

    def __enter__(self):
        self.old_contexts = _state.contexts
        self.new_contexts = (self.old_contexts[0] + (self,), self)
        _state.contexts = self.new_contexts
        return self

    def __exit__(self, type, value, traceback):
        final_contexts = _state.contexts
        _state.contexts = self.old_contexts

        if final_contexts is not self.new_contexts:
            raise StackContextInconsistentError(
                'stack_context inconsistency (may be caused by yield '
                'within a "with TracerStackContext" block)')

        # break the reference to allow faster GC on CPython
        self.new_contexts = None

    def deactivate(self):
        self.active = False

    @classmethod
    def current_data(cls):
        """Return the data for the current context. This method can be
        used inside a Tornado coroutine to retrieve and use the current
        tracing context.
        """
        for ctx in reversed(_state.contexts[0]):
            if isinstance(ctx, cls) and ctx.active:
                return ctx.data
