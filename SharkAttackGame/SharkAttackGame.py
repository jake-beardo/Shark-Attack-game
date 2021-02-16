import pygame
import pygame.ftfont
import time
import math
import random
import sys


pygame.init()
pygame.font.init()
# The screen width and height
# Shows name at top of pygame window and displays a background image

DisplayWidth = 800
DisplayHeight = 600
Screen = pygame.display.set_mode((DisplayWidth, DisplayHeight))
pygame.display.set_caption("Shark Attack")
clock = pygame.time.Clock()
BackgroundImage = pygame.image.load("Background.png").convert_alpha()

HighscoreFile1 = "highscore.txt"
HighscoreFile2 = "highscore2.txt"
HighscoreFile3 = "highscore3.txt"


# checks Highest score file to see if there currently is a highscore
with open(HighscoreFile1, "r") as LD:
    try:
        Highscore1 = int(LD.read())
    except:
        Highscore1 = 0

with open(HighscoreFile2, "r") as LD:
    try:
        Highscore2 = int(LD.read())
    except:
        Highscore2 = 0

with open(HighscoreFile3, "r") as LD:
    try:
        Highscore3 = int(LD.read())
    except:
        Highscore3 = 0
# GRB colours saved for later use in the game
Black = (0,0,0)
White = (255,255,255)
Red = (255,0,0)
DarkRed = (200, 0,0)
Blue = (0,100,255)
DarkBlue = (0,0,200)
Green = (0, 200,0)
BrightGreen = (0,255,0)
Violet = (238,130,238)
Magenta = (255,0,255)


# Import Pictures of fish
Fish1 = "Fish1.png"
Fish1First = "Fish1First.png"
Fish2 = "Fish2.png"
Fish3 = "Fish3.png"
Fish4 = "Fish4.png"
Fish4First = "Fish4First.png"
Fish5 = "Fish5.png"

# Import music and sound FX
BiteSound = pygame.mixer.Sound("BiteFX.wav")
NomSound = pygame.mixer.Sound("NOM.wav")
OuchSound = pygame.mixer.Sound("Ouch.wav")
Music = pygame.mixer.music.load("SharkAttackMusic.wav")
pygame.mixer.music.play(-1)

class Fish(object):
    # Initiation phase for the class to define varibles using some of the given parameters
    def __init__(self, Screen, FishType, StartX, FishWidth, FishHeight,StartVel):

        self.display = Screen

        self.x = StartX
        self.startx = StartX
        self.y = random.randrange(0, (DisplayHeight - 300))

        self.width = FishWidth
        self.height = FishHeight

        self.type = FishType

        self.imageinit = pygame.image.load(FishType).convert_alpha()
        self.image = pygame.transform.scale(self.imageinit, (int(self.width), int(self.height)))

        self.vel = StartVel
        self.vely = random.randrange(-5, 5)

        self.hitbox = (self.x, self.y, self.width, self.height)
    # Updates variables such as position and velocity of fish
    def update(self):
        #Fish Starting on left hand side and moving across to right
        # uses the fist if statement since it must have positive velocity in the x axis
        #  to move in that direction
        if self.vel > 0:
            self.x += self.vel

            if self.x > DisplayWidth:
                self.x = self.startx
                self.y = random.randrange(0, (DisplayHeight - 50))

        elif self.vel < 0 and self.type != Fish4:
            self.x += self.vel

            if self.x < 0:
                self.x = self.startx
                self.y = random.randrange(0, (DisplayHeight - 50))

        if self.type == Fish4:
            self.x += self.vel
            self.y += self.vely
            if self.x < 0:
                self.x = self.startx
                self.y = random.randrange(0, (DisplayHeight - 50))
                self.vely = random.randrange(-5, 5)


    def render(self, Screen):
        # Renders the fish to the pygame window
        self.image = pygame.transform.scale(self.imageinit, (int(self.width), int(self.height)))
        Screen.blit(self.image, (self.x, self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)

        # Uncomment Bellow to see hitboxes for when shark is able to eat fish
        # the Majority of the fish has to be contained within
        #  the hitbox of the shark to score
        #pygame.draw.rect(Screen, (255,0,0), self.hitbox, 2)




class Shark(object):
    # Gathers Varibles for the shark object
    def __init__(self, Screen, SharkWidth, SharkHeight, GameMode):
        self.display = Screen

        #self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.mode = GameMode
        if self.mode == True:
            self.width = SharkWidth
            self.height = SharkHeight
            self.x = int(DisplayWidth * 0.45)


            self.image = pygame.image.load("SharkLeft.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

            self.changex = 0
            self.changey = 0

            # Fisrt if statement is for big shark the second for baby shark to change the hitboxes appropriately
            if self.width >= 250:
                self.y = int(DisplayHeight * 0.72)
                self.hitbox = (self.x + 75, self.y + 50, self.width - 100, self.height - 350)
            elif self.width < 250:
                self.y = int(DisplayHeight * 0.8)
                self.hitbox = (self.x + 10, self.y + 40 , self. width - 10, self.height - 100)

        elif self.mode == False:
            self.width = SharkHeight
            self.height = SharkWidth

            self.x = int(DisplayWidth * 0.7)
            self.y = random.randrange(0, (DisplayHeight - 300))

            self.image = pygame.image.load("SharkRight.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

            self.changex = 0
            self.changey = 0

            self.hitbox = (self.x, self.y, self.width, self.height-200)


    def update(self,Fish=False):
        #Event Handling phase
        if self.mode == True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.changex = -5
                    elif event.key == pygame.K_RIGHT:
                        self.changex = 5
                    elif event.key == pygame.K_UP:
                        self.changey = 20

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.changex = 0


            if self.x < -70:
                self.x = -70
            if self.x > DisplayWidth - (self.width - 30):
                self.x = DisplayWidth - (self.width - 30)

            if self.y <= -50:
                self.changey = -5
            if self.width >= 250:
                if self.y >= (DisplayHeight * 0.72):
                    self.y = (DisplayHeight * 0.72)

            elif self.width < 250:
                if self.y >= (DisplayHeight * 0.8):
                    self.y = (DisplayHeight * 0.8)

            self.x += self.changex
            self.y -= self.changey

        elif self.mode == False:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.changey = -5
                    elif event.key == pygame.K_DOWN:
                        self.changey = 5

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.changey = 0

            if self.y <= -50:
                self.y = -50
            if self.y >= (DisplayHeight * 0.72):
                self.y = (DisplayHeight * 0.72)

            self.y += self.changey




    def render(self, Screen):
        Screen.blit(self.image, (self.x, self.y))
        if self.width >= 250 and self.mode == True:
            self.hitbox = (self.x + 75, self.y + 50, self.width - 100, self.height - 350)
        elif self.width < 250 and self.mode == True:
            self.hitbox = (self.x + 38, self.y + 35, self.width - 38, self.height - 200)

        elif self.mode == False:
            self.hitbox = (self.x + 80, self.y + 30, self.width - 350, self.height - 100)


        # Uncomment Bellow to see hitboxes for when shark is able to eat fish

        pygame.draw.rect(Screen, (255,0,0), self.hitbox, 2)


def text_objects(DisplayText, font):
    # Function used to create text boxes and renders Certian text such as game title,
    # Buttons  and end screen
    TextSurface = font.render(DisplayText, True, Black)
    return TextSurface, TextSurface.get_rect()

def blit_large_text(text, pos):
    # Displays large piece of text on  start screen
    # this function insures a new line is made when text reaches a certian point on the screen
    # and makes sure text doesnt overlap by taking into account the max height of the words
    # It does this by converting each new line into a list of words then adds spaces which are the width of font

    TextFont = pygame.font.Font("KoolFont.ttf", 25)
    words = [word.split(' ') for word in text.splitlines()]
    space = TextFont.size(' ')[0]
    MaxWidth, MaxHeight = (DisplayWidth - 300), DisplayHeight
    x, y = pos
    for line in words:
        for word in line:
            WordSurface = TextFont.render(word, 0, Black)
            WordWidth, WordHeight = WordSurface.get_size()
            if x + WordWidth >= MaxWidth:
                x = pos[0]  # resets the position of x after new line needs to be made
                y += WordHeight  # adds the word height to the y so text isn"t written on top of each other
            Screen.blit(WordSurface, (x, y))
            x += WordWidth + space
        x = pos[0]
        y += WordHeight

def timer(TimeLeft, Count, HS):
    # Displays a timer in the top left of the screen counting up in seconds
    TimerText = pygame.font.Font("KoolFont.ttf", 25)
    TimerText = TimerText.render("Time Remaining: " + str(60 - TimeLeft) + " seconds", True, Black)
    Screen.blit(TimerText, (0, 30))
    # This can be changed to make the game longer or shorter
    if TimeLeft >= 60:
        end_screen(Count, HS)

def fish_ate(Count):
    # renders score to screen in top left while playing the game
    ScoreFont = pygame.font.Font("KoolFont.ttf", 25)
    ScoreText = ScoreFont.render("Score: " + str(Count), True, Black)
    Screen.blit(ScoreText, (0,0))

def button(msg, x, y , width, height, InactiveColour, ActiveColour, Choice = None):
    # Draws butttons and makes them seem interactive to user by changing colour when mouse hovers
    # over the button
    # uses if statements to decide what occurs when the mouse  clicks a button
    pygame.init()
    Mouse = pygame.mouse.get_pos()
    Click = pygame.mouse.get_pressed()
    if x + width > Mouse[0] > x and y + height > Mouse[1] > y:
        pygame.draw.rect(Screen, ActiveColour, (x, y, width, height))
        if Click[0] == 1 and Choice != None:
            if Choice == "StartGame":
                mode = True
                main(mode)
            elif Choice == "BabyShark":
                mode = False
                main(mode)

            elif Choice == "HeadFirst":
                head_first()

            elif Choice == "QuitGame":
                pygame.quit()
    else:
        pygame.draw.rect(Screen, InactiveColour, (x, y, width, height))

    ButtonText = pygame.font.Font("KoolFont.ttf", 20)
    TextSurf, TextRect = text_objects(msg, ButtonText)
    TextRect.center = ((x + (width / 2)), (y + (height / 2)))
    Screen.blit(TextSurf, TextRect)

def start_screen():
    # This function opens the first window, displays the background with the title, various interactive buttons
    # and a picture of each fish and references the score each fish is worth
    # it also displays the current highscore
    Start = True
    while Start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        Screen.blit(BackgroundImage, (0, 0))
        LargeText = pygame.font.Font("MarkerFont.ttf", 120)
        PointsFont = pygame.font.Font("KoolFont.ttf", 20)
        HighscoreFont = pygame.font.Font("KoolFont.ttf", 30)
        TextSurf, TextRect = text_objects("Shark Attack", LargeText)
        TextRect.center = ((DisplayWidth // 2), (DisplayHeight // 2))
        Screen.blit(TextSurf, TextRect)

        TextSurf, TextRect = text_objects("Highscore: " + str(Highscore1), HighscoreFont)
        TextRect.center = (105, 20)
        Screen.blit(TextSurf, TextRect)

        LargePieceOfText = "you have 1 minute to eat as many high scoring fish as possible\n" \
                           "use the left, right and up keys on your keyboardto catch the fish in the sharks mouth" \
                           "\nalso try baby shark for more of a challenge or headfirst using the up and down keys"

        blit_large_text(LargePieceOfText, (8, 45))


        Fish1Text = PointsFont.render("-4 points = ", True, Red)

        Fish1Image = pygame.image.load(Fish1).convert_alpha()
        Fish1Image = pygame.transform.scale(Fish1Image, (int(70), int(60)))

        Screen.blit(Fish1Text, ((DisplayWidth - 200), 24))
        Screen.blit(Fish1Image, (DisplayWidth - 100, 8))

        Fish2Text = PointsFont.render("3 points = ", True, Black)

        Fish2Image = pygame.image.load(Fish2).convert_alpha()
        Fish2Image = pygame.transform.scale(Fish2Image, (int(70), int(60)))

        Screen.blit(Fish2Text, ((DisplayWidth - 200), 94))
        Screen.blit(Fish2Image, (DisplayWidth - 100, 70))

        Fish3Text = PointsFont.render("3 points = ", True, Black)

        Fish3Image = pygame.image.load(Fish3).convert_alpha()
        Fish3Image = pygame.transform.scale(Fish3Image, (int(70), int(60)))

        Screen.blit(Fish3Text, ((DisplayWidth - 200), 155))
        Screen.blit(Fish3Image, (DisplayWidth - 100, 132))

        Fish4Text = PointsFont.render("4 points = ", True, Black)

        Fish4Image = pygame.image.load(Fish4).convert_alpha()
        Fish4Image = pygame.transform.scale(Fish4Image, (int(70), int(60)))

        Screen.blit(Fish4Text, ((DisplayWidth - 200), 210))
        Screen.blit(Fish4Image, (DisplayWidth - 100, 190))

        Fish5Text = PointsFont.render("7 points = ", True, BrightGreen)

        Fish5Image = pygame.image.load(Fish5).convert_alpha()
        Fish5Image = pygame.transform.scale(Fish5Image, (int(100), int(80)))

        Screen.blit(Fish5Text, ((DisplayWidth - 400), 24))
        Screen.blit(Fish5Image, (DisplayWidth - 300, 8))

        button("Play Game", 10, 450, 150, 75, Green, BrightGreen, "StartGame")
        button("Play Headfirst", 210, 450, 150, 75, Magenta, Violet, "HeadFirst")
        button("Play Baby Shark", 420, 450, 170, 75, DarkBlue, Blue, "BabyShark")
        button("Quit", 640, 450, 150, 75, DarkRed, Red, "QuitGame")

        pygame.display.update()
        clock.tick(20)

def load_data(Count, HS):
    # Loads Highscores to find previous scores ... if there are any previous scores
    if HS == Highscore1:
        if Count > Highscore1:
            with open(HighscoreFile1, "w") as LD:
                LD.write(str(Count))
    elif HS == Highscore2:
        if Count > Highscore2:
            with open(HighscoreFile2, "w") as LD:
                LD.write(str(Count))
    elif HS == Highscore3:
        if Count > Highscore3:
            with open(HighscoreFile3, "w") as LD:
                LD.write(str(Count))
def end_screen(Count, HS):
    #after time is up the game ends and automatically takes you to this screen
    # Displays a message saying times up along with the users score and the highestscore
    # Also has buttons giving the user the option to play again or to quit
    load_data(Count, HS)

    End = True

    while End:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        Screen.blit(BackgroundImage, (0, 0))
        LargeText = pygame.font.Font("MarkerFont.ttf", 100)
        TextSurf, TextRect = text_objects("Time's Up!", LargeText)
        TextRect.center = ((DisplayWidth // 2), 100)

        Screen.blit(TextSurf, TextRect)

        TextSurf, TextRect = text_objects("You Scored: " + str(Count), LargeText)
        TextRect.center = ((DisplayWidth // 2), 300)
        Screen.blit(TextSurf, TextRect)

        if HS == Highscore1:

            if Count >= Highscore1:
                TextSurf, TextRect = text_objects("Highscore: " + str(Count), LargeText)
                TextRect.center = ((DisplayWidth // 2), 200)
                Screen.blit(TextSurf, TextRect)

            else:
                TextSurf, TextRect = text_objects("Highscore: " + str(Highscore1), LargeText)
                TextRect.center = ((DisplayWidth // 2), 200)
                Screen.blit(TextSurf, TextRect)

        elif HS == Highscore2:
            if Count >= Highscore2:
                TextSurf, TextRect = text_objects("Highscore: " + str(Count), LargeText)
                TextRect.center = ((DisplayWidth // 2), 200)
                Screen.blit(TextSurf, TextRect)

            else:
                TextSurf, TextRect = text_objects("Highscore: " + str(Highscore2), LargeText)
                TextRect.center = ((DisplayWidth // 2), 200)
                Screen.blit(TextSurf, TextRect)

        elif HS == Highscore3:
            if Count >= Highscore3:
                TextSurf, TextRect = text_objects("Highscore: " + str(Count), LargeText)
                TextRect.center = ((DisplayWidth // 2), 200)
                Screen.blit(TextSurf, TextRect)

            else:
                TextSurf, TextRect = text_objects("Highscore: " + str(Highscore3), LargeText)
                TextRect.center = ((DisplayWidth // 2), 200)
                Screen.blit(TextSurf, TextRect)

        button("Play Game", 10, 450, 150, 75, Green, BrightGreen, "StartGame")
        button("Play Headfirst", 210, 450, 150, 75, Magenta, Violet, "HeadFirst")
        button("Play Baby Shark", 420, 450, 170, 75, DarkBlue, Blue, "BabyShark")
        button("Quit", 640, 450, 150, 75, DarkRed, Red, "QuitGame")

        pygame.display.update()

def main(Mode):

    pygame.init()
    # The screen width and height
    DisplayWidth = 800
    DisplayHeight = 600
    Screen = pygame.display.set_mode((DisplayWidth, DisplayHeight))

    pygame.display.set_caption("Shark Attack")

    clock = pygame.time.Clock()

    BackgroundImage = pygame.image.load("Background.png").convert_alpha()

    FPS = 100

    Fish1 = "Fish1.png"
    Fish2 = "Fish2.png"
    Fish4 = "Fish4.png"
    Fish5 = "Fish5.png"

    score = 0
    time = 0

    if Mode == True:
        shark = Shark(Screen, 300, 500, GameMode=True)
        HS = Highscore1

    elif Mode == False:
        shark = Shark(Screen, 200, 300, GameMode=True)
        HS = Highscore2

    #Fish(Screen, FishType, StartX, FishWidth, FishHeight, StartVel)
    fish5 = Fish(Screen, FishType=Fish5, StartX=-3000, FishWidth=50, FishHeight=40,StartVel=9)
    fish1 = Fish(Screen, FishType=Fish1, StartX=1200, FishWidth=100, FishHeight=80,StartVel=-7)
    fish3 = Fish(Screen, FishType=Fish3, StartX=-300, FishWidth=74, FishHeight=60, StartVel=3)
    fish2 = Fish(Screen, FishType=Fish2, StartX=-400, FishWidth=75, FishHeight=60,StartVel=3)
    fish4 = Fish(Screen, FishType=Fish4, StartX=1600, FishWidth=60, FishHeight=60,StartVel=-6)


    Running = True

    while Running:
        #Frames Per Second Limiting
        Seconds = clock.tick(FPS)/1000.0
        time += Seconds
        DisplayTimer = int(time)
        #Time = pygame.time.get_ticks()//1000
        #DisplayTimer = Time


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False


        Screen.blit(BackgroundImage, (0, 0))

        #object updating phase
        fish1.update()
        shark.update()
        fish5.update()

        fish2.update()
        fish3.update()
        fish4.update()

        #renders each of the objects to the screen in real time
        shark.render(Screen)
        fish1.render(Screen)
        fish5.render(Screen)
        fish2.render(Screen)
        fish3.render(Screen)
        fish4.render(Screen)

        # Determines whether the fish hit box come into contact with the shark hit box if so
        # a noise is played abd points are added or subtracted from the score
        # and fish velocity changes and the size may also change
        # also resets the x and y position of the fish
        if shark.hitbox[0] < fish1.hitbox[0] + fish1.hitbox[2] and shark.hitbox[0] + shark.hitbox[2] > fish1.hitbox[0]:
            if shark.hitbox[1] + shark.hitbox[3] > fish1.hitbox[1] + fish1.hitbox[3] and shark.hitbox[1] < fish1.hitbox[1]:
                print("hit")
                OuchSound.play()
                fish1.x = -100
                score -= 4
                # increases the speed of the fish
                fish1.vel -= 0.5
                # make fish smaller and easier to eat
                fish1.width -= int(fish1.width * 0.05)
                fish1.height -= int(fish1.width * 0.05)

                if fish1.width <= 35 or fish1.height <= 30:
                    fish1.width = 35
                    fish1.height = 30

        if shark.hitbox[0] < fish2.hitbox[0] + fish2.hitbox[2] and shark.hitbox[0] + shark.hitbox[2] > fish2.hitbox[0]:
            if shark.hitbox[1] + shark.hitbox[3] > fish2.hitbox[1] + fish2.hitbox[3] and shark.hitbox[1] < fish2.hitbox[1]:
                print("hit")
                BiteSound.play()
                fish2.x = 900
                score += 3
                # increases the speed of the fish
                fish2.vel += 0.8
                # make fish bigger and harder to eat
                fish2.width += (fish2.width * 0.3)
                fish2.height += (fish2.height * 0.3)

                if fish2.width >= 110 or fish2.height >= 95:
                    fish2.width = 110
                    fish2.height = 95


        if shark.hitbox[0] < fish3.hitbox[0] + fish3.hitbox[2] and shark.hitbox[0] + shark.hitbox[2] > fish3.hitbox[0]:
            if shark.hitbox[1] + shark.hitbox[3] > fish3.hitbox[1] + fish3.hitbox[3] and shark.hitbox[1] < fish3.hitbox[1]:
                print("hit")
                BiteSound.play()
                fish3.x = 900
                score += 3
                # increases the speed of the fish to increase difficulty
                fish3.vel += 0.8
                # make fish bigger and harder to eat
                fish3.width += (fish3.width * 0.075)
                fish3.height += (fish3.height * 0.075)

                if fish3.width >= 110 or fish3.height >= 100:
                    fish3.width = 110
                    fish3.height = 90



        if shark.hitbox[0] < fish4.hitbox[0] + fish4.hitbox[2] and shark.hitbox[0] + shark.hitbox[2] > fish4.hitbox[0]:
            if shark.hitbox[1] + shark.hitbox[3] > fish4.hitbox[1] + fish4.hitbox[3]\
                    and shark.hitbox[1] < fish4.hitbox[1]:
                print("hit")
                BiteSound.play()
                fish4.x = -100
                score += 4
                # increases the speed of the fish
                fish4.vel -= 0.3
                # make fish smaller and harder to eat
                # FishWidth += (score * 0.8)
                # FishHeight += (score * 0.8)

        if shark.hitbox[0] < fish5.hitbox[0] + fish5.hitbox[2] and shark.hitbox[0] + shark.hitbox[2] > fish5.hitbox[0]:
            if shark.hitbox[1] + shark.hitbox[3] > fish5.hitbox[1] + fish5.hitbox[3] and shark.hitbox[1] < fish5.hitbox[1]:
                print("hit")
                NomSound.play()
                fish5.x = 900
                score += 7
                # increases the speed of the fish
                fish5.vel += 1

                # make fish smaller and harder to eat
                # FishWidth += (score * 0.8)
                # FishHeight += (score * 0.8)
        # calls the fuctions to display score and time
        fish_ate(score)
        timer(DisplayTimer, score, HS)

        # updated the display of the screen for example if a fish is hit it will remove the fish from the display
        #screen by reseting its x position
        pygame.display.update()

def head_first():
    pygame.init()
    # The screen width and height
    DisplayWidth = 800
    DisplayHeight = 600
    Screen = pygame.display.set_mode((DisplayWidth, DisplayHeight))

    pygame.display.set_caption("Shark Attack")

    clock = pygame.time.Clock()

    BackgroundImage = pygame.image.load("Background.png").convert_alpha()

    FPS = 100

    Fish1First = "Fish1First.png"
    Fish2 = "Fish2.png"
    Fish4First = "Fish4First.png"
    Fish5 = "Fish5.png"


    score = 0
    time = 0
    HS = Highscore3

    shark = Shark(Screen, 300, 500, GameMode=False)
    # Fish(Screen, FishType, StartX, FishWidth, FishHeight, StartVel)
    fish5 = Fish(Screen, FishType=Fish5, StartX=-3000, FishWidth=50, FishHeight=40, StartVel=9)
    fish1 = Fish(Screen, FishType=Fish1First, StartX=-700, FishWidth=100, FishHeight=80, StartVel=7)
    fish3 = Fish(Screen, FishType=Fish3, StartX=-300, FishWidth=74, FishHeight=60, StartVel=3)
    fish2 = Fish(Screen, FishType=Fish2, StartX=-400, FishWidth=75, FishHeight=60, StartVel=3)
    fish4 = Fish(Screen, FishType=Fish4First, StartX=-500, FishWidth=60, FishHeight=60, StartVel=6)

    Running = True

    while Running:
        # Frames Per Second Limiting
        Seconds = clock.tick(FPS) / 1000.0
        time += Seconds
        DisplayTimer = int(time)
        # Time = pygame.time.get_ticks()//1000
        # DisplayTimer = Time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False

        Screen.blit(BackgroundImage, (0, 0))

        # object updating phase
        fish1.update()
        shark.update()
        fish5.update()

        fish2.update()
        fish3.update()
        fish4.update()

        # renders each of the objects to the screen in real time
        shark.render(Screen)
        fish1.render(Screen)
        fish5.render(Screen)
        fish2.render(Screen)
        fish3.render(Screen)
        fish4.render(Screen)

        # Determines whether the fish hit box come into contact with the shark hit box if so
        # a noise is played abd points are added or subtracted from the score
        # and fish velocity changes and the size may also change
        # also resets the x and y position of the fish
        if shark.hitbox[0] < fish1.hitbox[0] + fish1.hitbox[2] and shark.hitbox[0] + shark.hitbox[2] > fish1.hitbox[0]:
            if shark.hitbox[1] + shark.hitbox[3] > fish1.hitbox[1] + fish1.hitbox[3] and shark.hitbox[1] < fish1.hitbox[
                1]:
                print("hit")
                OuchSound.play()
                fish1.x = -100
                score -= 4
                # increases the speed of the fish
                fish1.vel += 0.5
                # make fish smaller and easier to eat
                fish1.width += int(fish1.width * 0.1)
                fish1.height += int(fish1.height * 0.1)

                if fish1.width <= 35 or fish1.height <= 30:
                    fish1.width = 35
                    fish1.height = 30

        if shark.hitbox[0] < fish2.hitbox[0] + fish2.hitbox[2] and shark.hitbox[0] + shark.hitbox[2] > fish2.hitbox[0]:
            if shark.hitbox[1] + shark.hitbox[3] > fish2.hitbox[1] + fish2.hitbox[3] and shark.hitbox[1] < fish2.hitbox[
                1]:
                print("hit")
                BiteSound.play()
                fish2.x = 900
                score += 3
                # increases the speed of the fish
                fish2.vel += 0.8
                # make fish bigger and harder to eat
                fish2.width += (fish2.width * 0.3)
                fish2.height += (fish2.height * 0.3)

                if fish2.width >= 110 or fish2.height >= 95:
                    fish2.width = 110
                    fish2.height = 95

        if shark.hitbox[0] < fish3.hitbox[0] + fish3.hitbox[2] and shark.hitbox[0] + shark.hitbox[2] > fish3.hitbox[0]:
            if shark.hitbox[1] + shark.hitbox[3] > fish3.hitbox[1] + fish3.hitbox[3] and shark.hitbox[1] < fish3.hitbox[
                1]:
                print("hit")
                BiteSound.play()
                fish3.x = 900
                score += 3
                # increases the speed of the fish to increase difficulty
                fish3.vel += 0.8
                # make fish bigger and harder to eat
                fish3.width += (fish3.width * 0.5)
                fish3.height += (fish3.width * 0.5)

                if fish3.width >= 110 or fish3.height >= 100:
                    fish3.width = 110
                    fish3.height = 90

        if shark.hitbox[0] < fish4.hitbox[0] + fish4.hitbox[2] and shark.hitbox[0] + shark.hitbox[2] > fish4.hitbox[0]:
            if shark.hitbox[1] + shark.hitbox[3] > fish4.hitbox[1] + fish4.hitbox[3] \
                    and shark.hitbox[1] < fish4.hitbox[1]:
                print("hit")
                BiteSound.play()
                fish4.x = -100
                score += 4
                # increases the speed of the fish
                fish4.vel += 0.3
                # make fish smaller and harder to eat
                # FishWidth += (score * 0.8)
                # FishHeight += (score * 0.8)

        if shark.hitbox[0] < fish5.hitbox[0] + fish5.hitbox[2] and shark.hitbox[0] + shark.hitbox[2] > fish5.hitbox[0]:
            if shark.hitbox[1] + shark.hitbox[3] > fish5.hitbox[1] + fish5.hitbox[3] and shark.hitbox[1] < fish5.hitbox[
                1]:
                print("hit")
                NomSound.play()
                fish5.x = 900
                score += 7
                # increases the speed of the fish
                fish5.vel += 1

                # make fish smaller and harder to eat
                # FishWidth += (score * 0.8)
                # FishHeight += (score * 0.8)
        # calls the fuctions to display score and time
        fish_ate(score)
        timer(DisplayTimer, score, HS)
        # updated the display of the screen for example if a fish is hit it will remove the fish from the display
        # screen by reseting its x position
        pygame.display.update()
start_screen()

pygame.quit()
quit()
