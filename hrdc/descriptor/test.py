def descriptor_expected(test_case, descriptor, expected_code):
    from ..stream import optimizer, formatter, comparer
    from . import streamer

    output = comparer.ExpectedStream(test_case, expected_code)
    output = optimizer.Optimizer.new(output)
    visitor = streamer.Streamer(output)
    descriptor.accept(visitor)
    output.close()
