import logging

log = logging.getLogger('advent')

class Cell:
    def __init__(self, x, y, grid_serial_number):
        self.x = x
        self.y = y
        self.cell_power = self.power(grid_serial_number)
        self.latest_square_score = self.cell_power

    def power(self, grid_serial_number):
        if self.x == 0 or self.y == 0:
            return None
        power_level = ((self.x + 10) * self.y + grid_serial_number) * (self.x + 10)
        return int(str(int(power_level))[-3]) - 5

    def __repr__(self):
        return f'<{self.x},{self.y}> power:{self.cell_power} -- square:{self.latest_square_score}'


class Grid:
    def __init__(self, size, grid_serial_number):
        self.size = size
        self.cells = [[Cell(x, y, grid_serial_number).cell_power
                           for x in range(size+1)]
                           for y in range(size+1)]
        self.sums = self.submatrix_sums()

    def submatrix_sums(self):
        # build matrix of size**2 where value of each cell is
        # sum of everything above and to left

        # dummy row to make 1-indexing easier below
        sums = [[None for _ in range(self.size + 1)]]
        # initialize first row
        sums.append([self.cells[1][x] for x in range(self.size + 1)])

        # dummy col
        for _ in range(self.size):
            sums.append([None])

        # add columns top to bottom
        for y in range(2, self.size + 1):
            sums[y].extend(
                [sums[y-1][x] + self.cells[y][x] for x in range(1, self.size + 1)]
            )
        # add rows left to right, cells to the left will already contain sum of everything
        # up and to the left
        for x in range(2, self.size + 1):
            for y in range(1, self.size + 1):
                sums[y][x] += sums[y][x-1]
        return sums

    def calculate_square(self, anchor_x, anchor_y, square_size):
        power = self.sums[anchor_y + square_size - 1][anchor_x + square_size - 1]
        if anchor_x > 1:
            power -= self.sums[anchor_y + square_size - 1][anchor_x - 1]
        if anchor_y > 1:
            power -= self.sums[anchor_y - 1][anchor_x + square_size - 1]
        if anchor_x > 1 and anchor_y > 1:
            power += self.sums[anchor_y - 1][anchor_x - 1]
        return power

    def max_power_top_left_coordinate(self):
        max_power = -1 * float('inf')
        for square_size in range(2, self.size + 1):
            current_square_size_max = -1 * float('inf')
            for x in range(1, self.size-square_size+1):
                for y in range(1, self.size-square_size+1):
                    current_square_power = self.calculate_square(x, y, square_size)
                    if current_square_power > current_square_size_max:
                        current_square_size_max = current_square_power
                    if current_square_power > max_power:
                        max_power = current_square_power
                        coordinate = f'<{x},{y},{square_size}>'
            print(square_size, coordinate, max_power, current_square_size_max)
            if current_square_size_max < max_power:
                print(current_square_power)
                return coordinate

if __name__=='__main__':
    log.info('Run directly')
    grid = Grid(size=300, grid_serial_number=5177)
    result = grid.max_power_top_left_coordinate()
    log.info(result)
    print(result)
else:
    log.info('Imported')
# 1.6 seconds using hash tables 1.45 seconds using arrays ...
 # much easier to read using hash tables

#  TODO:
# square size **2 1, 4, 9, 16
# say at size = 4 max_power = 16 and at size = 5 sub_max_power = 15,
# the new border added to squares at the next size step is (6*2-1)*4
# maximum sub_max_power at size = 6 == 15 + 44 = 59

# three ways to optimize:
# 1. break at maximum sub_max_power given prior max
# 2. break if maximum sub_max_power at next step < global max_power
# 3. note that for all parameters tested sum is strictly increasing with size until
# size that yields maximum sum, then strictly decreasing, so one can just stop as
# soon as sum at size n+1 < sum at size n --- no proof given
