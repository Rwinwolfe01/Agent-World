import pygame
import math

from world.collision import can_move
from agents.brain import AgentBrain


class Agent:

    def __init__(
        self,
        name,
        model,
        color,
        x,
        y
    ):

        self.name = name
        self.model = model
        self.color = color

        self.x = float(x)
        self.y = float(y)

        self.target_x = float(x)
        self.target_y = float(y)

        self.speed = 1.8

        self.state = "IDLE"

        self.path = []
        self.path_index = 0

        # Current location
        self.current_location = None

        # Destination
        self.destination = None
        self.brain = AgentBrain(self)

    # =====================================================
    # GO TO LOCATION
    # =====================================================

    def go_to(
        self,
        location_name,
        world,
        pathfinder
    ):

        position = world.get_location_position(
            location_name
        )

        if position is None:

            self.state = "BLOCKED"

            return False

        target_x, target_y = position

        path = pathfinder.find_path(
            self.x,
            self.y,
            target_x,
            target_y
        )

        if not path:

            self.state = "BLOCKED"

            return False

        self.destination = location_name

        self.path = path

        self.path_index = 0

        self.state = "WALKING"

        return True

    # =====================================================
    # DIRECT MOVEMENT
    # =====================================================

    def move_to(
        self,
        x,
        y
    ):

        self.target_x = float(x)
        self.target_y = float(y)

        self.path = []
        self.path_index = 0

        self.destination = None

        self.state = "WALKING"

    # =====================================================
    # FOLLOW PATH
    # =====================================================

    def follow_path(
        self,
        path
    ):

        self.path = path

        self.path_index = 0

        if self.path:

            self.state = "WALKING"

        else:

            self.state = "BLOCKED"

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        world_map
    ):

        if self.path:

            if self.path_index >= len(
                self.path
            ):

                self.path = []

                self.state = "IDLE"

                if self.destination:

                    self.current_location = (
                        self.destination
                    )

                    self.destination = None

                return

            self.target_x, self.target_y = (
                self.path[self.path_index]
            )

        # -------------------------------------------------
        # DISTANCE
        # -------------------------------------------------

        dx = (
            self.target_x -
            self.x
        )

        dy = (
            self.target_y -
            self.y
        )

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        # -------------------------------------------------
        # REACHED TARGET
        # -------------------------------------------------

        if distance <= 3:

            if self.path:

                self.path_index += 1

                if self.path_index >= len(
                    self.path
                ):

                    self.path = []

                    self.state = "IDLE"

                    if self.destination:

                        self.current_location = (
                            self.destination
                        )

                        self.destination = None

            else:

                self.x = self.target_x
                self.y = self.target_y

                self.state = "IDLE"

            return

        # -------------------------------------------------
        # DIRECTION
        # -------------------------------------------------

        direction_x = dx / distance
        direction_y = dy / distance

        next_x = (
            self.x +
            direction_x *
            self.speed
        )

        next_y = (
            self.y +
            direction_y *
            self.speed
        )

        # -------------------------------------------------
        # COLLISION
        # -------------------------------------------------

        if can_move(
            world_map,
            next_x,
            next_y
        ):

            self.x = next_x
            self.y = next_y

        else:

            self.state = "BLOCKED"

            self.path = []

    # =====================================================
    # DRAW
    # =====================================================

    def draw(
        self,
        screen,
        font
    ):

        position = (
            int(self.x),
            int(self.y)
        )

        pygame.draw.circle(
            screen,
            self.color,
            position,
            8
        )

        pygame.draw.circle(
            screen,
            (20, 20, 20),
            position,
            9,
            2
        )

        label = font.render(
            self.name,
            True,
            (245, 245, 245)
        )

        screen.blit(
            label,
            (
                int(self.x) + 12,
                int(self.y) - 10
            )
        )