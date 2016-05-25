import Tests

print( '\n=== Running asynchronous tests ===\n')

Tests.AsynchronousTests.runTests()

print( '\n=== Running synchronous tests ===')

Tests.SynchronousTests.runTests()
