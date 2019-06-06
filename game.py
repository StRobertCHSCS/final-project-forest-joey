import arcade
from random import randint

screen_width = 800
screen_height = 600

player_x = 60
player_y = 0
jump_h = 0
up = -20

hit_d = False
hit_l = False
hit_r = False

left_pressed = False
right_pressed = False

start = False
intro = True

height_increments = [38, 72, 102, 128, 150]
lateral_direction = [1, -1]

block_height = [38, 110, 212]
block_left_side = [160, 360, 230]
block_right_side = [240, 440, 310]

shift = 0
block_count = 3
high_score = 0


def on_update(delta_time):
    global left_pressed, right_pressed, player_x, start, block_count

    if not intro:
        start = True

    if left_pressed and not hit_l and start:
        player_x -= 8

    if right_pressed and not hit_r and start:
        player_x += 8

    if start:
        reset()
        block_count = len(block_height) - 1
        check_hit()
        sounds()
        jumping()
        new_platforms()
        shifting()


def check_hit():
    global hit_d, hit_l, hit_r, player_x, player_y, jump_h, block_count

    hit_d = False
    hit_r = False
    hit_l = False

    if player_x <= 10:
        hit_l = True
    if player_x >= 790:
        hit_r = True
    for i in range(block_count + 1):
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


def new_platforms():
    global block_height, block_left_side, block_right_side, block_count

    if (block_height[block_count] - player_y) < 350:

        if block_left_side[block_count] <= 150:
            lateral_v = 1
            new_height = block_height[block_count] + height_increments[randint(2, 4)]
        elif block_right_side[block_count] >= 570:
            lateral_v = -1
            new_height = block_height[block_count] + height_increments[randint(2, 4)]
        else:
            lateral_v = lateral_direction[randint(0, 1)]
            new_height = block_height[block_count] + height_increments[randint(0, 4)]

        lateral_d = randint(8, 20) * 10

        block_height.append(new_height)
        block_left_side.append(block_left_side[block_count] + lateral_d * lateral_v)
        block_right_side.append(block_right_side[block_count] + lateral_d * lateral_v)


def shifting():
    global shift

    if player_y - shift > 200:
        shift += 5


def menu():
    texture = arcade.load_texture("images/space.jpg")
    texture_logo = arcade.load_texture("images/splogo (2).jpg")

    if intro:
        arcade.draw_texture_rectangle(screen_width // 2, screen_height // 2, 0.625 * texture.width,
                                      0.625 * texture.height, texture, 0)
        arcade.draw_texture_rectangle(400, 450, 0.3 * texture_logo.width, 0.3 * texture_logo.height, texture_logo, 0)
        text_start = "Click                    to start"
        arcade.draw_text(text_start, 260, 450, arcade.color.WHITE, 24, font_name='Calibri')
        high_score_txt = "High score: " + str(high_score)
        arcade.draw_text(high_score_txt, 500, 100, arcade.color.WHITE, 24, font_name='Calibri')


def score():
    global high_score
    if start:
        arcade.draw_text(str(int(player_y)), 360, 550, arcade.color.BLACK, 36)

    if player_y > high_score:
        high_score = int(player_y)


def losing_screen():
    if player_y + jump_h - shift < 0:

        arcade.draw_rectangle_filled(screen_width // 2, screen_height // 2, screen_width, screen_height,
                                     arcade.color.GREEN)
        arcade.draw_rectangle_filled(400, screen_height // 2, 400, 100, arcade.color.PINK_LACE)
        text_start = "you crashed"
        arcade.draw_text(text_start, 300, screen_height // 2, arcade.color.BLACK, 18)


def reset():
    global intro, start, block_height, block_left_side, block_right_side, player_y, player_x, jump_h, up, shift

    if player_y + jump_h - shift < 0:

        start = False
        intro = True

        for i in range(block_count - 2):
            del block_height[3]
            del block_right_side[3]
            del block_left_side[3]
        player_y = 0
        player_x = 60
        jump_h = 0
        up = -20
        shift = 0


def sounds():
    pass
    # file = "Laser Gun Sound Effects All Sounds.mp3"
    # os.system("mpg123" + file)


def character(x, y):

    arcade.draw_circle_filled(x, y + 10, 10, arcade.color.RED)


def on_draw():
    global player_x, player_y, jump_h, shift
    arcade.start_render()

    if block_count < 6:
        beginning = 0
    else:
        beginning = block_count - 6

    for i in range(beginning, block_count):
        arcade.draw_rectangle_filled(block_left_side[i] + 40, block_height[i] - 5 - shift, 80, 10, arcade.color.BLACK)

    character(player_x, player_y + jump_h - shift)

    score()
    menu()
    losing_screen()


def on_key_press(key, modifiers):
    global right_pressed, left_pressed, intro
    if key == arcade.key.A:
        left_pressed = True
    if key == arcade.key.D:
        right_pressed = True
    if key == arcade.key.SPACE:
        intro = False


def on_key_release(key, modifiers):
    global right_pressed, left_pressed
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
