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
instructions_number = 0

start = False
intro = True
lost = False
direction = True

height_increments = [38, 72, 102, 128, 150]
lateral_direction = [1, -1]

block_height = [38, 110, 212]
block_left_side = [160, 360, 230]
block_right_side = [240, 440, 310]

shift = 0
block_count = 3
high_score = 0
time = 0
count = 0

laser_sound = arcade.load_sound("sounds/3538.mp3")
splat_sound = arcade.load_sound("sounds/pihtas.mp3")
whoosh_sound = arcade.load_sound("sounds/whoosh.mp3")
meep_sound = arcade.load_sound("sounds/meepbeep.mp3")

texture_stars = arcade.load_texture("images/starrr.png")
texture_logo = arcade.load_texture("images/splogogo.png")
texture_ship = arcade.load_texture("images/zoomwoom.png")
texture_died = arcade.load_texture("images/splotplat.png")

texture_spicy = arcade.load_texture("images/chilli.png")
texture_pepper = arcade.load_texture("images/jalapeno.png")
texture_moss = arcade.load_texture("images/moss_plat.png")

ship_x = 0
ship_y = 550
char_x = 710
char_y = 470


def on_update(delta_time):
    """
    calls all functions and controls lateral payer movement

    :return: (int) the x position of the character
    """
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
        jumping()
        new_platforms()
        shifting()


def check_hit():
    """
    detects collisions between the character and its environment

    :return: (bool) if the character has collided and where the collision occurred
    """
    global hit_d, hit_l, hit_r, player_x, player_y, jump_h, block_count

    hit_d = False
    hit_r = False
    hit_l = False

    # checks to see if the character has hit the edge of the screen
    if player_x <= 20:
        hit_l = True
    if player_x >= 780:
        hit_r = True

    # a loop to check if the character has hit any platform or the bottom of the screen
    # gathers the coordinates of obstacles from related lists (block_height, block_left_side, Block_right_side)
    for i in range(beginning, count + 1):
        if block_left_side[i] < player_x < block_right_side[i] and jump_h + player_y == block_height[i]:
            hit_d = True
        elif player_y + jump_h <= 0:
            hit_d = True


def jumping():
    """
        uses a quadratic equation to animate a jumping motion

        :return: (float) the vertical position of the character
    """
    global hit_d, jump_h, player_y, up, count

    # resets the base from which the character will jump from once it has landed on a platform
    # keeps track of how many platforms the character has landed on
    if hit_d and up > 0:
        if jump_h != 0:
            count += 1
        up = -20
        player_y += jump_h
        jump_h = 0
        # arcade.play_sound(laser_sound)

    jump_h = 0.5 * -up ** 2 + 200
    up += 1


def new_platforms():
    """
    randomly generates new platforms for the character to land on

    :return: (int, list) the new horizontal and vertical positions of the platforms
    """
    global block_height, block_left_side, block_right_side, block_count

    # generate a new platform only if the player is within 350 pixels of the highest patform
    if (block_height[block_count] - player_y) < 350:

        # ensures that no platforms are generated completely off the screen
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

        # appends new values to lists
        block_height.append(new_height)
        block_left_side.append(block_left_side[block_count] + lateral_d * lateral_v)
        block_right_side.append(block_right_side[block_count] + lateral_d * lateral_v)


def shifting():
    """
        shift the screen down as the player progresses up through the game

        :return: (int) the amount in which the program will shift the screen down
    """
    global shift

    if player_y - shift > 200:
        shift += 5


def reset():
    """
        reset values to restart the game once the player has lost

        :return: (int, bool) the original values of all parameters
    """
    global block_height, block_left_side, block_right_side, player_y, player_x, jump_h
    global intro, start, up, shift, lost, count

    # if the character falls below the screen, reset all game parameters and display the losing screen
    if player_y + jump_h - shift < 0:

        # arcade.play_sound(splat_sound)

        start = False
        intro = True
        lost = True

        # delete all the information about previously generated platforms
        for i in range(block_count - 2):
            del block_height[3]
            del block_right_side[3]
            del block_left_side[3]

        # resets parameters for the location of the character
        player_y = 0
        player_x = 60
        jump_h = 0
        up = -20
        shift = 0
        count = 0


def on_draw():
    """
    updates all the visual aspects of the game and renders appropriate graphics

    :return: the drawing of the character and platforms
    """
    global player_x, player_y, jump_h, shift, beginning

    arcade.start_render()

    # displays only the last 8 platforms to save computing power
    if block_count < 8:
        beginning = 0
    else:
        beginning = block_count - 8

    # draws the platforms
    for i in range(beginning, block_count):
        arcade.draw_texture_rectangle(block_left_side[i] + 40, block_height[i] - 5 - shift, 0.3 * texture_moss.width,
                                      0.3 * texture_moss.height, texture_moss, 0)

    character(player_x, player_y + jump_h - shift + 30)

    score()
    menu()
    instructions_1()
    losing_screen()


def character(x, y):
    """
    keeps track of the player's score and their high score

    :param x: x coordinate of the character
    :param y: y coordinate of the character
    :return: (int) current and high score of the player
    """
    global direction

    if left_pressed:
        direction = False
    if right_pressed:
        direction = True

    # makes the character face the direction of travel
    if direction:
        arcade.draw_texture_rectangle(x, y, 0.15 * texture_spicy.width, 0.15 * texture_spicy.height, texture_spicy)
    if not direction:
        arcade.draw_texture_rectangle(x, y, 0.15 * texture_pepper.width, 0.15 * texture_pepper.height, texture_pepper)


def score():
    """
    keeps track of the player's score and their high score

    :return: (int) current and high score of the player
    """
    global high_score

    # tracks the score of he player based on the y value of the character
    if start:
        arcade.draw_text(str(int(player_y)), 360, 550, arcade.color.BLACK, 36)

    if player_y > high_score:
        high_score = int(player_y)


def menu():
    """
    sets up the menu screen
    """

    # if the game is not running, display the menu screen
    if intro and instructions_number == 0:
        arcade.draw_texture_rectangle(screen_width // 2, screen_height // 2, 1 * texture_stars.width,
                                      1 * texture_stars.height, texture_stars, 0)
        arcade.draw_texture_rectangle(700, 500, 0.8 * texture_ship.width, 0.8 * texture_ship.height, texture_ship, -25)

        arcade.draw_rectangle_filled(440, 320, 400, 70, arcade.color.ORANGE, 0)
        text_start = "{0:^27}".format("Click SPACE to start!")
        arcade.draw_text(text_start, 250, 305, arcade.color.WHITE, 24, font_name='Comic Sans MS')

        high_score_txt = "High score: " + str(high_score)
        arcade.draw_text(high_score_txt, 330, 110, arcade.color.WHITE, 24, font_name='Comic Sans MS')

        arcade.draw_rectangle_filled(430, 220, 480, 70, arcade.color.ORANGE, 0)
        text_instructions = "Click ENTER for instructions"
        arcade.draw_text(text_instructions, 210, 210, arcade.color.WHITE, 24, font_name='Comic Sans MS')

        arcade.draw_texture_rectangle(300, 390, 0.2 * texture_spicy.width, 0.2 * texture_spicy.height, texture_spicy)


def instructions_1():
    """
    animates and displays the instruction screens

    :return: (int) the coordinated of the ship and character
    """
    global instructions_number, ship_x, ship_y, char_x, char_y

    if 0 < instructions_number < 4:
        arcade.draw_texture_rectangle(screen_width // 2, screen_height // 2, texture_stars.width,
                                      texture_stars.height, texture_stars, 0)

    # displays the first set on instructions
    if instructions_number == 1:
        # stops the ship, draws the light triangle, and moves the character down
        if ship_x == 700 and char_y != 100:
            arcade.draw_triangle_filled(710, 500, 400, 200, 700, 100, arcade.color.BABY_BLUE)
            arcade.draw_texture_rectangle(700, 480, 0.8 * texture_ship.width, 0.8 * texture_ship.height,
                                          texture_ship, -25)
            char_x -= 3
            char_y -= 5
            arcade.draw_texture_rectangle(char_x, char_y, 0.15 * texture_pepper.width,
                                          0.15 * texture_pepper.height, texture_pepper)

        # moves the ship towards the right
        elif ship_x != 700 and char_y != 100:
            arcade.draw_rectangle_filled(470, 100, 50, 50, arcade.color.BLACK)
            ship_x += 10
            ship_y -= 1

        # moves the ship off the screen, draws the first text panel
        else:
            ship_x += 10
            ship_y -= 1
            arcade.draw_texture_rectangle(490, 100,
                                          0.15 * texture_pepper.width, 0.15 * texture_pepper.height, texture_pepper)
            text_panel_1()

        arcade.draw_texture_rectangle(ship_x, ship_y, 0.8 * texture_ship.width, 0.8 * texture_ship.height,
                                      texture_ship, -25)

    # draws the second text pane;
    if instructions_number == 2:
        text_panel_2()
        arcade.draw_texture_rectangle(600, 260, 0.3 * texture_spicy.width, 0.3 * texture_spicy.height, texture_spicy)

    # draws the third text panel
    if instructions_number == 3:
        text_panel_3()
        arcade.draw_texture_rectangle(500, 260, 0.3 * texture_spicy.width, 0.3 * texture_spicy.height, texture_spicy)

    # resets the text panels
    if instructions_number > 3:
        instructions_number = 0
        ship_x = 0
        ship_y = 550
        char_x = 710
        char_y = 470


def text_panel_1():
    """
    the first instruction panel
    """

    arcade.draw_rectangle_filled(230, 210, 270, 70, arcade.color.ORANGE)
    text_hi = "This is Sploogy"
    arcade.draw_text(text_hi, 100, 200, arcade.color.WHITE, 24, font_name='Comic Sans MS')

    help_txt = "Press ENTER to continue"
    arcade.draw_text(help_txt, 500, 50, arcade.color.WHITE, 16, font_name='Comic Sans MS')


def text_panel_2():
    """
    the second instruction panel
    """

    arcade.draw_rectangle_filled(330, 470, 510, 160, arcade.color.ORANGE)
    text_help = "Help Sploogy explore planet" '\n' " Earth by jumping higher and" '\n' "higher on the blocks"
    arcade.draw_text(text_help, 100, 430, arcade.color.WHITE, 24, font_name='Comic Sans MS')

    arcade.draw_rectangle_filled(280, 180, 400, 100, arcade.color.ORANGE)
    text_move = "Press the arrow keys to" '\n' "move left and right"
    arcade.draw_text(text_move, 100, 150, arcade.color.WHITE, 24, font_name='Comic Sans MS')

    help_txt = "Press ENTER to continue"
    arcade.draw_text(help_txt, 500, 50, arcade.color.WHITE, 16, font_name='Comic Sans MS')


def text_panel_3():
    """
    the third instruction panel
    """

    arcade.draw_rectangle_filled(360, 180, 550, 100, arcade.color.ORANGE)
    text_go = "Let's Go!"
    text_press = "Press 'ENTER' to return to menu"
    arcade.draw_text(text_go, 100, 190, arcade.color.WHITE, 24, font_name='Comic Sans MS')
    arcade.draw_text(text_press, 100, 140, arcade.color.WHITE, 24, font_name='Comic Sans MS')


def losing_screen():
    """
    sets up the losing screen

    :return: (int) the time until the screen will revert to the main menu
    """
    global time, lost

    # draw the losing screen
    if lost:
        time += 1

        arcade.draw_texture_rectangle(screen_width // 2, screen_height // 2, 1 * texture_stars.width,
                                      1 * texture_stars.height, texture_stars, 0)
        arcade.draw_rectangle_filled(400, screen_height // 2, 400, 100, arcade.color.WHITE)
        text_start = "Whoops, You Slipped and Died"
        arcade.draw_text(text_start, 250, 290, arcade.color.BLACK, 18)
        arcade.draw_texture_rectangle(400, 150, 0.5 * texture_died.width, 0.5 * texture_died.height, texture_died, 0)

    # the losing screen will disappear in one second and revert to the menu screen without user interference
    # if the user presses the space bar they will immediately start a new game
    if time > 60:
        time = 0
        lost = False
    elif start:
        time = 0
        lost = False


def on_key_press(key, modifiers):
    """
    detects if any keys have been pressed

    :return: (bool) the specific key that has been pressed
    """
    global right_pressed, left_pressed, intro, instructions_number

    if key == arcade.key.LEFT:
        left_pressed = True
    if key == arcade.key.RIGHT:
        right_pressed = True
    if key == arcade.key.SPACE:
        intro = False
    if key == arcade.key.ENTER:
        instructions_number += 1


def on_key_release(key, modifiers):
    """
    detects if any keys have been released

    :return: (bool) the specific key that has been released
    """
    global right_pressed, left_pressed

    if key == arcade.key.LEFT:
        left_pressed = False
    if key == arcade.key.RIGHT:
        right_pressed = False


def setup():
    """
    opens a window and sets up the window

    :return: calls the program
    """
    arcade.open_window(800, 600, "My Arcade Game")
    arcade.set_background_color(arcade.color.BLUE_GRAY)
    arcade.draw_texture_rectangle(screen_width // 2, screen_height // 2,
                                  screen_width, screen_width, texture_stars, 0)
    arcade.schedule(on_update, 1/60)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release

    arcade.run()


if __name__ == '__main__':
    setup()
