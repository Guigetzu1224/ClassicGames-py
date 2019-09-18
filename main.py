import arcade
import time
import random


# Set up screen playing space
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "First Game"
SPRITE_SCALING = 0.15
SCORE = 0
PIPE_SCALE = 4
SEPARATION_FACTOR = 250

# Generate player class constraints such that the pawn can not leave the screen.
class Player(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH-1
        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
        elif self.bottom < 0:
            self.bottom = 0



# TODO: Get this as a smooth animation? Not sure if that is something that i'd like to do.
def animate_angle(sprite,angle):
    if angle > 0 and sprite.angle<angle:
        for i in range(angle):
            sprite.angle = i
    elif angle > 0 and sprite.angle<angle:
        for i in range(angle):
            sprite.angle = angle-i



class MyGame(arcade.Window):

    def __init__(self,width,height):
        super().__init__(width,height)
        # Importing of sounds:
        self.flap = arcade.Sound('sfx_wing.wav')
        self.die = arcade.Sound('sfx_die.wav')
        self.point = arcade.Sound('sfx_point.wav')
        self.die = arcade.Sound('sfx_hit.wav')
        self.background = None
        # Setting up the arcade and all variables associated with it
        self.player_list = None
        self.sprite_list = None
        self.score = None
        self.MOVEMENT_SPEED_X = 0
        self.MOVEMENT_SPEED_Y = 0
        self.apple = None
        self.counter = 0
        self.score = 0


    def setup(self):
        # Setting up the arcade and all variables associated with it
        self.player_list = None
        self.sprite_list = None
        self.score = None
        self.MOVEMENT_SPEED_X = 0
        self.MOVEMENT_SPEED_Y = 0
        self.apple = None
        self.counter = 0
        self.score = 0

        # Starting to append sprites and players to the list of characters
        self.player_list = arcade.SpriteList()
        self.player_sprite = Player("bird.png",SPRITE_SCALING)
        self.apple = arcade.Sprite("pipe.png",SPRITE_SCALING*PIPE_SCALE)
        self.apple2 = arcade.Sprite("pipe.png",SPRITE_SCALING*PIPE_SCALE)
        self.player_sprite.center_y = SCREEN_HEIGHT/2
        self.player_sprite.center_x = SCREEN_WIDTH/5
        self.player_list.append(self.player_sprite)
        self.player_list.append(self.apple)
        self.player_list.append(self.apple2)

        self.apple.won = False
        self.apple2.won = False
        self.apple.center_y = random.randint(0,int(self.apple.height/2))
        self.apple.center_x = SCREEN_WIDTH + self.apple.width
        self.apple2.angle = 180  # Rotate 180 deg.
        self.apple2.bottom = self.apple.top + SEPARATION_FACTOR

        self.apple2.center_x = SCREEN_WIDTH + self.apple.width
        self.apple.placement = "bottom"
        self.apple2.placement= "top"

        self.background = arcade.load_texture('flp-brd-wlp.png')


    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.player_list.draw()
        start_y = SCREEN_HEIGHT*8/9
        start_x = SCREEN_WIDTH*4/5
        arcade.draw_point(start_x, start_y, arcade.color.AMAZON, 5)
        arcade.draw_text(str(self.score),
                         start_x, start_y, arcade.color.BLACK, 14)


    def update(self, delta_time):

        # Generation of all the player sprite properties
        self.player_sprite.change_x = self.MOVEMENT_SPEED_X
        self.player_sprite.change_y = self.MOVEMENT_SPEED_Y
        self.player_list.update()
        self.MOVEMENT_SPEED_Y = self.MOVEMENT_SPEED_Y - 0.35
        self.MOVEMENT_SPEED_X = self.MOVEMENT_SPEED_X
        self.counter = self.counter + 1
        if self.player_sprite.angle > -45:
            self.player_sprite.angle = self.player_sprite.angle - 3

        # Generation of all the new sprites
        if self.counter == 90:
            Temporary = len(self.player_list)
            TemporarySprite = arcade.Sprite("pipe.png",SPRITE_SCALING*PIPE_SCALE)
            TemporarySprite2 = arcade.Sprite("pipe.png",SPRITE_SCALING*PIPE_SCALE)
            self.player_list.append(TemporarySprite)
            self.player_list.append(TemporarySprite2)
            TemporarySprite.center_y = random.randint(0, int(TemporarySprite.height / 2))
            TemporarySprite.center_x = SCREEN_WIDTH + TemporarySprite.width
            TemporarySprite2.angle = 180  # Rotate 180 deg.
            TemporarySprite2.bottom = TemporarySprite.top + SEPARATION_FACTOR
            TemporarySprite2.center_x = SCREEN_WIDTH+ TemporarySprite.width
            TemporarySprite.placement = "bottom"
            TemporarySprite2.placement = "top"
            self.counter = self.counter * 0
            TemporarySprite.won = False
            TemporarySprite2.won = False





        # Generation of the score board
        start_y = SCREEN_HEIGHT * 8 / 9  # Nominal value for positioning the score board
        start_x = SCREEN_WIDTH * 4 / 5   # Nomianl value for positioning the score board
        arcade.draw_text(str(self.score),
                         start_x, start_y, arcade.color.BLACK, 30)

        for sprite in self.player_list[1:]:
            sprite.center_x = sprite.center_x - 3

            if self.player_sprite.collides_with_list(self.player_list):

                self.die.play()
                time.sleep(2)
                self.setup()
            elif self.player_sprite.right > sprite.left and self.player_sprite.bottom > sprite.top and self.player_sprite.left > sprite.right and sprite.won == False:
                self.score = self.score + 1
                sprite.won = True
                self.point.play()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            self.MOVEMENT_SPEED_Y = 5
            self.flap.play()
            animate_angle(self.player_sprite,45)
        elif key == arcade.key.DOWN:
            self.MOVEMENT_SPEED_Y = self.MOVEMENT_SPEED_Y

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP:
            self.MOVEMENT_SPEED_Y = self.MOVEMENT_SPEED_Y
        elif key == arcade.key.DOWN:
            self.MOVEMENT_SPEED_Y = self.MOVEMENT_SPEED_Y


window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
window.setup()
arcade.run()