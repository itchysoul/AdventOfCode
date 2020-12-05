
import pytest
from Day11 import Grid


class TestIntegration:
    @classmethod
    def max_power(cls, grid_serial_number, size=300):
        grid = Grid(size=size, grid_serial_number=grid_serial_number)
        return grid.max_power_top_left_coordinate()

    def test_18(self):
        assert TestIntegration.max_power(18) == '<90,269,16>'

    def test_42(self):
        assert TestIntegration.max_power(42) == '<232,251,12>'

    def test_5177(self):
        assert TestIntegration.max_power(5177) == '<231,135,8>'

