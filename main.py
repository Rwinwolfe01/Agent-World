import pygame
import sys
import random

from agents.agent import Agent
from world.map import WorldMap
from world.pathfinding import Pathfinder

# =========================================================
# INITIALIZATION
# =========================================================

pygame.init()


# =========================================================
# WINDOW
# =========================================================

WIDTH = 1400
HEIGHT = 800

WORLD_WIDTH = 1050
PANEL_WIDTH = WIDTH - WORLD_WIDTH

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agent World")

clock = pygame.time.Clock()


# =========================================================
# COLORS
# =========================================================

SKY = (135, 190, 225)
GRASS = (92, 150, 82)

ROAD = (65, 65, 68)
ROAD_LINE = (220, 190, 70)

BUILDING = (190, 150, 110)
BUILDING_DARK = (150, 110, 80)
ROOF = (120, 65, 55)

PARK = (70, 125, 65)
TREE = (40, 110, 50)
TREE_TRUNK = (100, 70, 40)

SQUARE = (175, 165, 145)
SQUARE_EDGE = (130, 120, 105)

WHITE = (245, 245, 245)
BLACK = (25, 25, 25)

PANEL = (28, 30, 34)

CHAT_GREEN = (70, 210, 110)
CHAT_BLUE = (80, 150, 255)
CHAT_YELLOW = (240, 200, 70)
CHAT_PURPLE = (180, 100, 240)
CHAT_RED = (240, 80, 80)


# =========================================================
# FONTS
# =========================================================

font = pygame.font.SysFont("arial", 20)
small_font = pygame.font.SysFont("arial", 16)
title_font = pygame.font.SysFont("arial", 28, bold=True)


# =========================================================
# HELPER
# =========================================================

def draw_text(
    surface,
    value,
    x,
    y,
    font_obj=font,
    color=WHITE
):
    surface.blit(
        font_obj.render(
            value,
            True,
            color
        ),
        (x, y)
    )


# =========================================================
# BUILDINGS
# =========================================================

def building(
    x,
    y,
    width,
    height,
    name
):

    # Building body
    pygame.draw.rect(
        screen,
        BUILDING,
        (
            x,
            y,
            width,
            height
        )
    )

    # Building border
    pygame.draw.rect(
        screen,
        BUILDING_DARK,
        (
            x,
            y,
            width,
            height
        ),
        3
    )

    # Roof
    pygame.draw.polygon(
        screen,
        ROOF,
        [
            (x - 10, y),
            (
                x + width // 2,
                y - 35
            ),
            (x + width + 10, y)
        ]
    )

    # Two windows
    window_positions = [
        (
            x + 25,
            y + 25
        ),
        (
            x + width - 50,
            y + 25
        )
    ]

    for wx, wy in window_positions:

        pygame.draw.rect(
            screen,
            (80, 150, 180),
            (
                wx,
                wy,
                18,
                20
            )
        )

        pygame.draw.rect(
            screen,
            BLACK,
            (
                wx,
                wy,
                18,
                20
            ),
            1
        )

    # Building name
    draw_text(
        screen,
        name,
        x + 10,
        y + height - 30,
        small_font,
        BLACK
    )


# =========================================================
# TREES
# =========================================================

def tree(x, y):

    # Trunk
    pygame.draw.rect(
        screen,
        TREE_TRUNK,
        (
            x - 5,
            y + 18,
            10,
            30
        )
    )

    # Leaves
    pygame.draw.circle(
        screen,
        TREE,
        (
            x,
            y
        ),
        25
    )


# =========================================================
# CENTRAL SQUARE
# =========================================================

SQUARE_CENTER = (
    450,
    590
)

SQUARE_RADIUS = 100

SQUARE_RECT = pygame.Rect(
    SQUARE_CENTER[0] - SQUARE_RADIUS,
    SQUARE_CENTER[1] - SQUARE_RADIUS,
    SQUARE_RADIUS * 2,
    SQUARE_RADIUS * 2
)


def draw_square():

    # Empty circular square
    pygame.draw.circle(
        screen,
        SQUARE,
        SQUARE_CENTER,
        SQUARE_RADIUS
    )

    # Border
    pygame.draw.circle(
        screen,
        SQUARE_EDGE,
        SQUARE_CENTER,
        SQUARE_RADIUS,
        5
    )

    # Label
    draw_text(
        screen,
        "CENTRAL SQUARE",
        SQUARE_CENTER[0] - 70,
        SQUARE_CENTER[1] - 10,
        small_font,
        BLACK
    )

# =========================================================
# WORLD
# =========================================================

world = WorldMap()

pathfinder = Pathfinder(world)


# =========================================================
# CREATE AGENTS
# =========================================================

agents = [

    # CHATGPT
    Agent("GPT-1", "ChatGPT", CHAT_GREEN, 250, 550),
    Agent("GPT-2", "ChatGPT", CHAT_GREEN, 280, 650),
    Agent("GPT-3", "ChatGPT", CHAT_GREEN, 350, 550),

    # CLAUDE
    Agent("Claude-1", "Claude", CHAT_BLUE, 650, 450),
    Agent("Claude-2", "Claude", CHAT_BLUE, 760, 550),
    Agent("Claude-3", "Claude", CHAT_BLUE, 850, 520),

    # GEMINI
    Agent("Gemini-1", "Gemini", CHAT_YELLOW, 250, 350),
    Agent("Gemini-2", "Gemini", CHAT_YELLOW, 350, 250),
    Agent("Gemini-3", "Gemini", CHAT_YELLOW, 650, 250),

    # GROK
    Agent("Grok-1", "Grok", CHAT_PURPLE, 650, 550),
    Agent("Grok-2", "Grok", CHAT_PURPLE, 850, 550),
    Agent("Grok-3", "Grok", CHAT_PURPLE, 950, 500),

    # DEEPSEEK
    Agent("DeepSeek-1", "DeepSeek", CHAT_RED, 250, 500),
    Agent("DeepSeek-2", "DeepSeek", CHAT_RED, 350, 700),
    Agent("DeepSeek-3", "DeepSeek", CHAT_RED, 650, 700),
]



# =========================================================
# CHAT
# =========================================================

messages = [

    (
        "GPT-1",
        "Hello everyone!",
        CHAT_GREEN
    ),

    (
        "Claude-1",
        "Hi. Nice city.",
        CHAT_BLUE
    ),

    (
        "Gemini-2",
        "Does anyone know this place?",
        CHAT_YELLOW
    ),

    (
        "Grok-1",
        "I don't think I've seen it before.",
        CHAT_PURPLE
    ),

    (
        "DeepSeek-2",
        "Let's explore.",
        CHAT_RED
    )
]


# =========================================================
# NEWS
# =========================================================

news = [

    "GPT-1 opened a conversation.",
    "Gemini-2 is exploring the city.",
    "Grok-1 visited the park."
]


# =========================================================
# EVENT LOG
# =========================================================

events = [

    "12:01 GPT-1 moved to the office.",
    "12:02 Claude-2 entered the shop.",
    "12:03 Gemini-2 started a conversation.",
    "12:04 Grok-1 entered the park.",
    "12:05 DeepSeek-2 moved toward HOME."
]


# =========================================================
# MAIN LOOP
# =========================================================

running = True

while running:

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        # -------------------------------------------------
        # CLOSE WINDOW
        # -------------------------------------------------

        if event.type == pygame.QUIT:

            running = False

        # -------------------------------------------------
        # MOUSE
        # -------------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Only world area
            if mouse_x < WORLD_WIDTH:

                # -----------------------------------------
                # CENTRAL SQUARE
                # -----------------------------------------
                if SQUARE_RECT.collidepoint(
                    mouse_x,
                    mouse_y
                ):

                    for agent in agents:

                        target_x = random.randint(
                            SQUARE_CENTER[0] - 70,
                            SQUARE_CENTER[0] + 70
                        )

                        target_y = random.randint(
                            SQUARE_CENTER[1] - 70,
                            SQUARE_CENTER[1] + 70
                        )

                        path = pathfinder.find_path(
                            agent.x,
                            agent.y,
                            target_x,
                            target_y
                        )

                        agent.follow_path(
                            path
                        )

    # =====================================================
    # UPDATE AGENTS
    # =====================================================

    for agent in agents:

        agent.update(world)

    decision = agent.brain.update(
            world,
            pathfinder
        )

    if decision:

            print(
                f"[BRAIN] {agent.name} decided to go to {decision}"
            )

    # =====================================================
    # SKY
    # =====================================================

    screen.fill(SKY)

    # =====================================================
    # GRASS
    # =====================================================

    pygame.draw.rect(
        screen,
        GRASS,
        (
            0,
            250,
            WORLD_WIDTH,
            HEIGHT - 250
        )
    )

    # =====================================================
    # MAIN ROAD
    # =====================================================

    pygame.draw.rect(
        screen,
        ROAD,
        (
            0,
            430,
            WORLD_WIDTH,
            100
        )
    )

    # Road markings
    for x in range(
        0,
        WORLD_WIDTH,
        60
    ):

        pygame.draw.rect(
            screen,
            ROAD_LINE,
            (
                x,
                478,
                35,
                5
            )
        )

    # =====================================================
    # SIDE ROAD
    # =====================================================

    pygame.draw.rect(
        screen,
        ROAD,
        (
            300,
            250,
            80,
            550
        )
    )

    # =====================================================
    # BUILDINGS
    # =====================================================

    building(
        60,
        310,
        170,
        110,
        "HOME"
    )

    building(
        430,
        290,
        180,
        140,
        "OFFICE"
    )

    building(
        690,
        300,
        150,
        120,
        "SHOP"
    )

    building(
        870,
        270,
        130,
        150,
        "HOSPITAL"
    )

    building(
        70,
        570,
        150,
        120,
        "HOME"
    )

    building(
        700,
        590,
        190,
        110,
        "FACTORY"
    )

    # =====================================================
    # PARK
    # =====================================================

    pygame.draw.rect(
        screen,
        PARK,
        (
            420,
            720,
            220,
            80
        )
    )

    draw_text(
        screen,
        "PARK",
        510,
        755,
        small_font
    )

    tree(
        450,
        760
    )

    tree(
        550,
        740
    )

    tree(
        610,
        770
    )

    # =====================================================
    # CENTRAL SQUARE
    # =====================================================

    draw_square()

    # =====================================================
    # NEWS BILLBOARD
    # =====================================================

    billboard = pygame.Rect(
        40,
        70,
        390,
        130
    )

    pygame.draw.rect(
        screen,
        BLACK,
        billboard
    )

    pygame.draw.rect(
        screen,
        (230, 190, 60),
        billboard,
        4
    )

    draw_text(
        screen,
        "CITY NEWS",
        60,
        85,
        title_font,
        (255, 210, 70)
    )

    for i, line in enumerate(news):

        draw_text(
            screen,
            "• " + line,
            60,
            130 + i * 22,
            small_font
        )

    # =====================================================
    # AGENTS
    # =====================================================

    for agent in agents:

        agent.draw(
            screen,
            small_font
        )

    # =====================================================
    # RIGHT PANEL
    # =====================================================

    pygame.draw.rect(
        screen,
        PANEL,
        (
            WORLD_WIDTH,
            0,
            PANEL_WIDTH,
            HEIGHT
        )
    )

    pygame.draw.line(
        screen,
        (80, 80, 80),
        (
            WORLD_WIDTH,
            0
        ),
        (
            WORLD_WIDTH,
            HEIGHT
        ),
        2
    )

    # =====================================================
    # LIVE CHAT
    # =====================================================

    draw_text(
        screen,
        "LIVE CHAT",
        WORLD_WIDTH + 25,
        25,
        title_font
    )

    y = 80

    for sender, message, color in messages:

        pygame.draw.circle(
            screen,
            color,
            (
                WORLD_WIDTH + 30,
                y + 8
            ),
            6
        )

        draw_text(
            screen,
            sender,
            WORLD_WIDTH + 45,
            y,
            small_font,
            color
        )

        draw_text(
            screen,
            message,
            WORLD_WIDTH + 45,
            y + 22,
            small_font
        )

        y += 65

    # =====================================================
    # EVENT LOG
    # =====================================================

    pygame.draw.line(
        screen,
        (80, 80, 80),
        (
            WORLD_WIDTH + 20,
            450
        ),
        (
            WIDTH - 20,
            450
        ),
        1
    )

    draw_text(
        screen,
        "EVENT LOG",
        WORLD_WIDTH + 25,
        475,
        title_font
    )

    y = 530

    for event_text in events:

        draw_text(
            screen,
            event_text,
            WORLD_WIDTH + 25,
            y,
            small_font
        )

        y += 28

    # =====================================================
    # DISPLAY
    # =====================================================

    pygame.display.flip()

    clock.tick(60)


# =========================================================
# EXIT
# =========================================================

pygame.quit()
sys.exit()