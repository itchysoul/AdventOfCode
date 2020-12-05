
from test_Day11 import TestIntegration
import pytest_benchmark  # provides benchmark fixture


def test_perf(benchmark):
    return benchmark(TestIntegration.max_power, 5177)