import arcade
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

player_x = 60
player_y = 0
jump_h = 0
shift = 0
up = -20

hit_d = False
hit_l = False
hit_r = False

up_pressed = False
down_pressed = False
left_pressed = False
right_pressed = False

start = False
intro = True

height_increments = [38, 72, 102, 128, 150, 168, 182]
block_height = [38, 110, 212]
block_left_side = [160, 360, 230]
block_right_side = [240, 440, 310]


def on_update(delta_time):
    global up_pressed, left_pressed, right_pressed, player_x, start

    if up_pressed:
        start = True

    if left_pressed and not hit_l and start:
        player_x -= 8

    if right_pressed and not hit_r and start:
        player_x += 8

    if start:
        check_hit()
        jumping()
        sounds()


def check_hit():
    global hit_d, hit_l, hit_r, player_x, player_y, jump_h

    hit_d = False
    hit_r = False
    hit_l = False

    if player_x <= 60:
        hit_l = True
    if player_x >= 740:
        hit_r = True
    for i in range(len(block_left_side)):
        if block_left_side[i] < player_x < block_right_side[i] and jump_h + player_y == block_height[i]:
            hit_d = True
        elif player_y + jump_h <= 0:
            hit_d = True

    if player_y < 0:
        player_y = 0


def jumping():
    global hit_d, jump_h, player_y, up

    if hit_d and up > 0:
        up = -20
        player_y += jump_h
        jump_h = 0

    jump_h = 0.5 * -up ** 2 + 200
    up += 1

    print(player_y, player_x, jump_h)


def new_platforms():
    pass


def menu():

    if intro:
        arcade.draw_rectangle_filled(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.color.PINK)
        arcade.draw_rectangle_filled(400, SCREEN_HEIGHT//2, 400, 100, arcade.color.PINK_LACE)
        text_start = "Click space to start"
        arcade.draw_text(text_start, 300, SCREEN_HEIGHT//2, arcade.color.BLACK, 18)


def sounds():
    pass
    #file = "Laser Gun Sound Effects All Sounds.mp3"
    #os.system("mpg123" + file)


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
    global player_x, player_y, jump_h, shift
    arcade.start_render()

    draw_snow_person(player_x, player_y + jump_h - shift)

    arcade.draw_rectangle_filled(200, 19 - shift, 80, 38, arcade.color.BLACK)
    arcade.draw_rectangle_filled(400, 91 - shift, 80, 38, arcade.color.BLACK)
    arcade.draw_rectangle_filled(270, 193 - shift, 80, 38, arcade.color.BLACK)

    menu()


def on_key_press(key, modifiers):
    global up_pressed, down_pressed, right_pressed, left_pressed, intro
    if key == arcade.key.W:
        up_pressed = True
    if key == arcade.key.S:
        down_pressed = True
    if key == arcade.key.A:
        left_pressed = True
    if key == arcade.key.D:
        right_pressed = True
    if key == arcade.key.SPACE:
        intro = False


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
