import random
import turtle


CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 24
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
STEP_DELAY_MS = 95

BACKGROUND = "#121418"
GRID_DARK = "#181d23"
GRID_LIGHT = "#1f2630"
SNAKE_HEAD = "#7cff6b"
SNAKE_BODY = "#43d65c"
SNAKE_SHADOW = "#249642"
FOOD = "#ff4d6d"
TEXT = "#e8f0f2"


def pixel_to_screen(cell):
    x, y = cell
    screen_x = -SCREEN_WIDTH // 2 + x * CELL_SIZE + CELL_SIZE // 2
    screen_y = -SCREEN_HEIGHT // 2 + y * CELL_SIZE + CELL_SIZE // 2
    return screen_x, screen_y


class PixelSnakeGame:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Pixel Snake")
        self.screen.bgcolor(BACKGROUND)
        self.screen.setup(SCREEN_WIDTH + 40, SCREEN_HEIGHT + 80)
        self.screen.tracer(False)

        self.drawer = self.make_turtle()
        self.hud = self.make_turtle()

        self.snake = []
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food = (0, 0)
        self.score = 0
        self.high_score = 0
        self.game_over = False

        self.bind_keys()
        self.reset()

    def make_turtle(self):
        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        pen.penup()
        return pen

    def bind_keys(self):
        self.screen.listen()
        self.screen.onkeypress(lambda: self.turn(0, 1), "Up")
        self.screen.onkeypress(lambda: self.turn(0, -1), "Down")
        self.screen.onkeypress(lambda: self.turn(-1, 0), "Left")
        self.screen.onkeypress(lambda: self.turn(1, 0), "Right")
        self.screen.onkeypress(lambda: self.turn(0, 1), "w")
        self.screen.onkeypress(lambda: self.turn(0, -1), "s")
        self.screen.onkeypress(lambda: self.turn(-1, 0), "a")
        self.screen.onkeypress(lambda: self.turn(1, 0), "d")
        self.screen.onkeypress(self.reset, "space")

    def reset(self):
        center = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.snake = [
            center,
            (center[0] - 1, center[1]),
            (center[0] - 2, center[1]),
        ]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.place_food()
        self.draw()
        self.screen.ontimer(self.step, STEP_DELAY_MS)

    def turn(self, dx, dy):
        if self.game_over:
            return

        current_dx, current_dy = self.direction
        if (dx, dy) != (-current_dx, -current_dy):
            self.next_direction = (dx, dy)

    def place_food(self):
        open_cells = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in self.snake
        ]
        self.food = random.choice(open_cells)

    def step(self):
        if self.game_over:
            self.draw()
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        hit_wall = not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT)
        hit_self = new_head in self.snake

        if hit_wall or hit_self:
            self.game_over = True
            self.high_score = max(self.high_score, self.score)
            self.draw()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.high_score = max(self.high_score, self.score)
            self.place_food()
        else:
            self.snake.pop()

        self.draw()
        self.screen.ontimer(self.step, STEP_DELAY_MS)

    def draw_square(self, cell, color, inset=1):
        x, y = pixel_to_screen(cell)
        half = CELL_SIZE // 2 - inset
        self.drawer.goto(x - half, y - half)
        self.drawer.color(color)
        self.drawer.begin_fill()
        for _ in range(4):
            self.drawer.forward(half * 2)
            self.drawer.left(90)
        self.drawer.end_fill()

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = GRID_LIGHT if (x + y) % 2 == 0 else GRID_DARK
                self.draw_square((x, y), color, inset=0)

    def draw_snake(self):
        for index, cell in enumerate(reversed(self.snake)):
            color = SNAKE_HEAD if cell == self.snake[0] else SNAKE_BODY
            self.draw_square(cell, SNAKE_SHADOW, inset=1)

            x, y = pixel_to_screen(cell)
            self.drawer.goto(x - 8, y - 6)
            self.drawer.color(color)
            self.drawer.begin_fill()
            for _ in range(4):
                self.drawer.forward(14)
                self.drawer.left(90)
            self.drawer.end_fill()

            if index % 2 == 0 and cell != self.snake[0]:
                self.draw_square(cell, "#8dff83", inset=7)

        self.draw_head_face()

    def draw_head_face(self):
        head = self.snake[0]
        x, y = pixel_to_screen(head)
        dx, dy = self.direction

        if dx:
            eye_offsets = [(dx * 5, 4), (dx * 5, -4)]
        else:
            eye_offsets = [(-4, dy * 5), (4, dy * 5)]

        self.drawer.color("#0d1413")
        for ox, oy in eye_offsets:
            self.drawer.goto(x + ox - 2, y + oy - 2)
            self.drawer.begin_fill()
            for _ in range(4):
                self.drawer.forward(4)
                self.drawer.left(90)
            self.drawer.end_fill()

    def draw_food(self):
        self.draw_square(self.food, "#8c1830", inset=1)
        self.draw_square(self.food, FOOD, inset=4)

        x, y = pixel_to_screen(self.food)
        self.drawer.goto(x - 2, y + 2)
        self.drawer.color("#ffd2dc")
        self.drawer.begin_fill()
        for _ in range(4):
            self.drawer.forward(4)
            self.drawer.left(90)
        self.drawer.end_fill()

    def draw_border(self):
        self.drawer.goto(-SCREEN_WIDTH // 2, -SCREEN_HEIGHT // 2)
        self.drawer.color("#344052")
        self.drawer.pensize(4)
        self.drawer.pendown()
        for _ in range(2):
            self.drawer.forward(SCREEN_WIDTH)
            self.drawer.left(90)
            self.drawer.forward(SCREEN_HEIGHT)
            self.drawer.left(90)
        self.drawer.penup()
        self.drawer.pensize(1)

    def draw_hud(self):
        self.hud.clear()
        self.hud.color(TEXT)
        self.hud.goto(-SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 16)
        self.hud.write(
            f"SCORE {self.score}   BEST {self.high_score}",
            align="left",
            font=("Courier", 16, "bold"),
        )

        if self.game_over:
            self.hud.goto(0, 8)
            self.hud.write(
                "GAME OVER",
                align="center",
                font=("Courier", 30, "bold"),
            )
            self.hud.goto(0, -28)
            self.hud.write(
                "PRESS SPACE",
                align="center",
                font=("Courier", 16, "bold"),
            )

    def draw(self):
        self.drawer.clear()
        self.draw_grid()
        self.draw_border()
        self.draw_food()
        self.draw_snake()
        self.draw_hud()
        self.screen.update()

    def run(self):
        self.screen.mainloop()


if __name__ == "__main__":
    PixelSnakeGame().run()
