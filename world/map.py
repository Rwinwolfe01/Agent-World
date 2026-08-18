import pygame


class WorldMap:

    def __init__(self):

        self.width = 1050
        self.height = 800

        # =================================================
        # LOCATIONS
        # =================================================

        self.locations = {

            "HOME_1": {
                "rect": pygame.Rect(60, 310, 170, 110),
                "type": "HOME",
                "entrance": (250, 365)
            },

            "OFFICE": {
                "rect": pygame.Rect(430, 290, 180, 140),
                "type": "OFFICE",
                "entrance": (650, 365)
            },

            "SHOP": {
                "rect": pygame.Rect(690, 300, 150, 120),
                "type": "SHOP",
                "entrance": (665, 365)
            },

            "HOSPITAL": {
                "rect": pygame.Rect(870, 270, 130, 150),
                "type": "HOSPITAL",
                "entrance": (850, 365)
            },

            "HOME_2": {
                "rect": pygame.Rect(70, 570, 150, 120),
                "type": "HOME",
                "entrance": (250, 620)
            },

            "FACTORY": {
                "rect": pygame.Rect(700, 590, 190, 110),
                "type": "FACTORY",
                "entrance": (675, 640)
            },

            "PARK": {
                "rect": pygame.Rect(420, 720, 220, 80),
                "type": "PARK",
                "entrance": (530, 700)
            },

            "CENTRAL_SQUARE": {
                "rect": pygame.Rect(
                    350,
                    490,
                    200,
                    200
                ),
                "type": "SQUARE",
                "entrance": (450, 590)
            }
        }

        # =================================================
        # BUILDINGS
        # =================================================

        self.buildings = [

            self.locations["HOME_1"]["rect"],
            self.locations["OFFICE"]["rect"],
            self.locations["SHOP"]["rect"],
            self.locations["HOSPITAL"]["rect"],
            self.locations["HOME_2"]["rect"],
            self.locations["FACTORY"]["rect"]
        ]

        # =================================================
        # PARK
        # =================================================

        self.park = self.locations["PARK"]["rect"]

        # =================================================
        # CENTRAL SQUARE
        # =================================================

        self.square_center = (
            450,
            590
        )

        self.square_radius = 100

    # =====================================================
    # LOCATION
    # =====================================================

    def get_location(self, name):

        return self.locations.get(name)

    # =====================================================
    # LOCATION POSITION
    # =====================================================

    def get_location_position(self, name):

        location = self.get_location(name)

        if location is None:
            return None

        return location["entrance"]

    # =====================================================
    # WORLD BOUNDARY
    # =====================================================

    def is_inside_world(self, x, y):

        return (
            0 <= x <= self.width
            and
            0 <= y <= self.height
        )

    # =====================================================
    # COLLISION
    # =====================================================

    def is_blocked(self, x, y):

        point = pygame.Rect(
            int(x) - 5,
            int(y) - 5,
            10,
            10
        )

        for building in self.buildings:

            if building.colliderect(point):

                return True

        return False