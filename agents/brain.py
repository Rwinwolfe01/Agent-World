import random
import time


class AgentBrain:

    def __init__(self, agent):

        self.agent = agent

        # How often the agent makes a new decision
        self.decision_interval = random.uniform(
            3.0,
            7.0
        )

        self.last_decision = time.time()

        # Available actions
        self.available_locations = [
            "HOME_1",
            "OFFICE",
            "SHOP",
            "HOSPITAL",
            "HOME_2",
            "FACTORY",
            "PARK",
            "CENTRAL_SQUARE"
        ]

    # =====================================================
    # DECISION TIMER
    # =====================================================

    def should_decide(self):

        current_time = time.time()

        if (
            current_time -
            self.last_decision
            >=
            self.decision_interval
        ):

            return True

        return False

    # =====================================================
    # MAKE DECISION
    # =====================================================

    def decide(
        self,
        world,
        pathfinder
    ):

        self.last_decision = time.time()

        self.decision_interval = random.uniform(
            3.0,
            7.0
        )

        # Don't choose current location
        possible_locations = [
            location
            for location in self.available_locations
            if location != self.agent.current_location
        ]

        if not possible_locations:

            return None

        destination = random.choice(
            possible_locations
        )

        success = self.agent.go_to(
            destination,
            world,
            pathfinder
        )

        if success:

            return destination

        return None

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        world,
        pathfinder
    ):

        # Agent is already walking
        if self.agent.state == "WALKING":

            return None

        # Agent is blocked
        if self.agent.state == "BLOCKED":

            self.agent.state = "IDLE"

        # Time to make a decision
        if self.should_decide():

            return self.decide(
                world,
                pathfinder
            )

        return None