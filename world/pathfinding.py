import heapq
import math


class Pathfinder:

    def __init__(self, world_map, cell_size=20):

        self.world = world_map
        self.cell_size = cell_size

        self.cols = world_map.width // cell_size
        self.rows = world_map.height // cell_size

        self.grid = self._build_grid()

    # =====================================================
    # BUILD GRID
    # =====================================================

    def _build_grid(self):

        grid = []

        for row in range(self.rows):

            current_row = []

            for col in range(self.cols):

                x = col * self.cell_size + self.cell_size / 2
                y = row * self.cell_size + self.cell_size / 2

                blocked = self.world.is_blocked(x, y)

                current_row.append(
                    not blocked
                )

            grid.append(current_row)

        return grid

    # =====================================================
    # WORLD -> GRID
    # =====================================================

    def world_to_grid(self, x, y):

        col = int(x // self.cell_size)
        row = int(y // self.cell_size)

        col = max(
            0,
            min(self.cols - 1, col)
        )

        row = max(
            0,
            min(self.rows - 1, row)
        )

        return (
            col,
            row
        )

    # =====================================================
    # GRID -> WORLD
    # =====================================================

    def grid_to_world(self, col, row):

        return (
            col * self.cell_size + self.cell_size / 2,
            row * self.cell_size + self.cell_size / 2
        )

    # =====================================================
    # HEURISTIC
    # =====================================================

    def heuristic(self, a, b):

        return (
            abs(a[0] - b[0]) +
            abs(a[1] - b[1])
        )

    # =====================================================
    # NEIGHBORS
    # =====================================================

    def get_neighbors(self, node):

        col, row = node

        directions = [

            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),

            # Diagonal movement
            (1, 1),
            (-1, -1),
            (1, -1),
            (-1, 1)
        ]

        neighbors = []

        for dx, dy in directions:

            new_col = col + dx
            new_row = row + dy

            if not (
                0 <= new_col < self.cols
                and
                0 <= new_row < self.rows
            ):
                continue

            if not self.grid[new_row][new_col]:
                continue

            # Prevent diagonal corner cutting
            if dx != 0 and dy != 0:

                if not self.grid[row][new_col]:
                    continue

                if not self.grid[new_row][col]:
                    continue

            neighbors.append(
                (
                    new_col,
                    new_row
                )
            )

        return neighbors

    # =====================================================
    # A*
    # =====================================================

    def find_path(
        self,
        start_x,
        start_y,
        target_x,
        target_y
    ):

        start = self.world_to_grid(
            start_x,
            start_y
        )

        goal = self.world_to_grid(
            target_x,
            target_y
        )

        # Goal blocked
        if not self.grid[goal[1]][goal[0]]:

            return []

        # Start blocked
        if not self.grid[start[1]][start[0]]:

            return []

        open_set = []

        heapq.heappush(
            open_set,
            (
                0,
                start
            )
        )

        came_from = {}

        g_score = {
            start: 0
        }

        f_score = {
            start: self.heuristic(
                start,
                goal
            )
        }

        while open_set:

            _, current = heapq.heappop(
                open_set
            )

            # Goal reached
            if current == goal:

                return self._reconstruct_path(
                    came_from,
                    current
                )

            for neighbor in self.get_neighbors(
                current
            ):

                dx = abs(
                    neighbor[0] - current[0]
                )

                dy = abs(
                    neighbor[1] - current[1]
                )

                if dx == 1 and dy == 1:

                    movement_cost = 1.414

                else:

                    movement_cost = 1

                tentative_g = (
                    g_score[current]
                    +
                    movement_cost
                )

                if (
                    neighbor not in g_score
                    or
                    tentative_g < g_score[neighbor]
                ):

                    came_from[neighbor] = current

                    g_score[neighbor] = tentative_g

                    f_score[neighbor] = (
                        tentative_g
                        +
                        self.heuristic(
                            neighbor,
                            goal
                        )
                    )

                    heapq.heappush(
                        open_set,
                        (
                            f_score[neighbor],
                            neighbor
                        )
                    )

        return []

    # =====================================================
    # RECONSTRUCT
    # =====================================================

    def _reconstruct_path(
        self,
        came_from,
        current
    ):

        path = [
            current
        ]

        while current in came_from:

            current = came_from[current]

            path.append(
                current
            )

        path.reverse()

        return [
            self.grid_to_world(
                col,
                row
            )
            for col, row in path
        ]