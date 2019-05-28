import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

jump_h = 0
shift = 0

hit_d = False
hit_l = False
hit_r = False

up_pressed = False
down_pressed = False
left_pressed = False
right_pressed = False
jump = False

height_increments = [38, 72, 102, 128, 150, 168, 182]
block_height = []
block_left_side = []
block_right_side = []


def on_update(delta_time):
    global up_pressed, down_pressed, left_pressed, right_pressed, player_x, player_y
    global jump, hit_d, hit_l, hit_r, jump_h, up, down

    for i in range(len(block_left_side)):
        for n in range(len(height_increments)):
            if block_left_side[i] < player_x < block_right_side[i] and jump_h == height_increments[n]:
                hit_d = True
            elif player_y + jump_h == 0:
                hit_d = True
    
    if player_y + jump_h <= 0:
        hit_d = True
    elif 160 < player_x < 240 and jump_h + player_y == 38:
        hit_d = True
    elif 360 < player_x < 440 and jump_h + player_y == 110:
        hit_d = True
    elif 230 < player_x < 310 and jump_h + player_y == 212:
        hit_d = True
    else:
        hit_d = False

    if up_pressed:
        if not jump:
            jump = True
        else:
            pass

    if hit_d and jump:
        print("yes")

    if jump:
        if hit_d and up > 0:
            up = -20
            player_y += jump_h
            jump_h = 0
        down = 0
        jump_h = 0.5 * -up ** 2 + 200
        up += 1

        print(player_y, player_x, jump_h)

    if player_y < 0:
        player_y = 0

    if left_pressed:
        player_x -= 8

    if right_pressed:
        player_x += 8


# Create a value that our snow_person1_x will start at.
player_x = 50
player_y = 0
up = -20
down = 0


def platforms(x, y):
    arcade.draw_rectangle_filled(200, 19, 80, 38, arcade.color.BLACK)
    arcade.draw_rectangle_filled(350, 57, 80, 38, arcade.color.BLACK)
    arcade.draw_rectangle_filled(275, 57, 80, 38, arcade.color.BLACK)


def draw_snow_person(x, y):
    """ Draw a snow person """

    # Draw a point at x, y for reference
    arcade.draw_point(x, y, arcade.color.RED, 5)

    # Snow
    arcade.draw_circle_filled(x, 60 + y, 60, arcade.color.WHITE)
    arcade.draw_circle_filled(x, 140 + y, 50, arcade.color.WHITE)
    arcade.draw_circle_filled(x, 200 + y, 40, arcade.color.WHITE)

    # Eyes
    arcade.draw_circle_filled(x - 15, 210 + y, 5, arcade.color.BLACK)
    arcade.draw_circle_filled(x + 15, 210 + y, 5, arcade.color.BLACK)


def on_draw():
    global player_x, player_y
    arcade.start_render()

    draw_snow_person(player_x, player_y + jump_h)
    arcade.draw_rectangle_filled(200, 19, 80, 38, arcade.color.BLACK)
    arcade.draw_rectangle_filled(400, 91, 80, 38, arcade.color.BLACK)
    arcade.draw_rectangle_filled(270, 193, 80, 38, arcade.color.BLACK)


def on_key_press(key, modifiers):
    global up_pressed, down_pressed, right_pressed, left_pressed
    if key == arcade.key.W:
        up_pressed = True
    if key == arcade.key.S:
        down_pressed = True
    if key == arcade.key.A:
        left_pressed = True
    if key == arcade.key.D:
        right_pressed = True


def on_key_release(key, modifiers):
    global up_pressed, down_pressed, right_pressed, left_pressed
    if key == arcade.key.W:
        up_pressed = False
    if key == arcade.key.S:
        down_pressed = False
    if key == arcade.key.A:
        left_pressed = False
    if key == arcade.key.D:
        right_pressed = False


def setup():
    arcade.open_window(800, 600, "My Arcade Game")
    arcade.set_background_color(arcade.color.BLUE)
    arcade.schedule(on_update, 1/60)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release

    arcade.run()


if __name__ == '__main__':
    setup()