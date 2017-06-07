class LogRecorder():
    """Recorder implementation that logs in the stdout a pretty
    printed representation of the recorded `Span`. This is used
    in the `DebugTracer` to check the right parenting when
    playing with examples.
    """

    def record_span(self, span):
        """Return a human readable version of the Span"""

        lines = [
            ('name', span.operation_name),
            ('id', span._context.span_id),
            ('trace_id', span._context.trace_id),
            ('parent_id', span.parent_id),
            ('start', span.start_time),
            ('end', '' if not span.duration else span.start_time + span.duration),
            ('duration', '%fs' % (span.duration or 0)),
            ('tags', '')
        ]

        lines.extend((' ', '%s:%s' % kv) for kv in sorted(span.tags.items()))
        print('=' * 10)
        print('\n'.join('%10s %s' % l for l in lines))
