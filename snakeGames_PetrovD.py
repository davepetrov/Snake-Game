################################################################################################
#            Programmer: David P.                                                              #
#            Date: 11/16/2017                                                                  #
#            File Name: Snake_Game_DavidP.py                                                   #
#            Description: Snake Game                                                           #
#            Game Rules: - You will lose if you collide with yourself                          #
#                        - You will lose if the time reaches to 0                              #
#                        - If you eat too many poisionous apples, you will lose                #
#                        - Every 5 apples eaten, the speed of the game will increase           #
#                        - You cannot go backward into yourself                                #
#                        - Do not hit the borders/ obstacles or you will lose                  #
################################################################################################

#---------------------Variables---------------------#
import pygame                                                                           # Imports pygame
from random import randint,randrange                                                    # Imports randrange function and randint function from the random module
pygame.init()                                                                           # pygame  
pygame.mixer.init()                                                                     # pygame mixer 

ticker = pygame.time.Clock()                                                            # The timer (Timer/ticker)
fps=10                                                                                  # Frames per second to make it look retro
timer = 20                                                                              # Timer set to 20 originally. Will change throughout the game
HEIGHT = 600                                                                            # Height of the game screen
WIDTH  = 800                                                                            # Width of the game screen
screen=pygame.display.set_mode((WIDTH,HEIGHT))                                          # Game Screen
count=1

#The top left wall/obstacle and the bottom right wall/obstacle
x1,y1,w1,h1=300,0,40,200
x2,y2,w2,h2=540,400,40,200

#Colours using RGB
WHITE = (255,255,255)                                                                   # White colour
RED = (255,0,0)                                                                         # Red colour
GREEN = (0,255,0)                                                                       # Green colour
BLACK = (0,0,0)                                                                         # Black colour
GRAY = (25,25,25)                                                                       # Gray Colour
ORANGE = (255,120,0)                                                                    # Orange Colour
YELLOW = (255,255,0)                                                                    # Yellow Colour
VELVET = (185,24,40)                                                                    # Velvet Colour
VELVET_DARK = (124,25,35)                                                               # Dark Velvet Colour
outline=0

left,right,up,down=True,True,True,False                                                 # Sets the left, right, up booleans to true and down to false because the snake goes up at first.

#Fonts
regular_Font = pygame.font.SysFont("Ariel Black",30)                                    # Font of the timer
big_Font = pygame.font.SysFont("Ariel Black",70)                                        # Font of the score

#Images
startScreen = pygame.image.load("startScreen.png")                                      # Loads the main menu image
rulesButton = pygame.image.load("rulesButton.png")                                      # Loads the main menu start button image
rulesScreen = pygame.image.load("rulesScreen.png")                                      # Loads the main menu image
startButton = pygame.image.load("startButton.png")                                      # Loads the main menu start button image
background = pygame.image.load("background.png")                                        # Loads the background image
gameOver = pygame.image.load("gameOver.png")                                            # Loads the gameover image
gApple = pygame.image.load("gApple.png")                                                # Loads the good apple image
bApple = pygame.image.load("bApple.png")                                                # Loads the bad apple image

#Sounds
gameOverSound=pygame.mixer.Sound('gameOver.wav')                                        # Loads the game over sound          
biteSound=pygame.mixer.Sound('bite.wav')                                                # Lodas the eating sound


                                    #---------------------------------------#
                                    #           Snake's Properties          #
                                    #---------------------------------------#


gridSize=20                                                                             # Grid size
snake_Radius = int(gridSize/2)                                                          # Making the snake the size of the grid to fit in it
hSpeed = snake_Radius*2                                                                 # Making the snake follow the grid (Horizonal Speed)
vSpeed = snake_Radius*2                                                                 # Making the snake follow the grid (Vertical Speed)

speedX = 0                                                                              # Original speed of the snake (X)
speedY = -vSpeed                                                                        # Snake originally going up (Y)
segx = [int(WIDTH/2)]*3                                                                 # 3 Segments spawning in the middle of the screen (X)
segy = [HEIGHT, HEIGHT+vSpeed, HEIGHT+2*vSpeed]                                         # Snake spawning at the bottom of the screeen(Y)
segy[0]=HEIGHT-100
segmentCLR = (0,255,0)                                                                  # Snake colour (Not including the head)
headCLR = (0,120,0)                                                                     # Snake head colour
lengthSnake = 2                                                                         # Counts the number of segments on the screen
                                    #---------------------------------------#
                                    #         G/B APPLE Properties          #
                                    #---------------------------------------#

apple_Size=10                                                                           # apple radius in general                

gappleCLR=(YELLOW)                                                                      # Good apple colour
gapple_counter=0                                                                        # Good apple counter
gapple_Size= apple_Size                                                                 # Good apple radius

bappleCLR=(ORANGE)                                                                      # Bad apple colour
bapple_Size= apple_Size                                                                 # Bad apple radius

                                    #---------------------------------------#
                                    # function that redraws all objects     #
                                    #---------------------------------------#

def genGapple_x(quadrant):
                                                                                                                # This Function generates a new [X] coordinate for the [Good Apple] from one of the 5 sections
    if quadrant ==1:                                                                                            # Section 1
        gapple_x=randrange(20+gridSize,300-20+20-gridSize,gridSize)                                             # Generates the [X] coordinate
    elif quadrant ==2:                                                                                          # Section 2
        gapple_x=randrange(300,300+40,gridSize)                                                                 # Generates the [X] coordinate
    elif quadrant ==3:                                                                                          # Section 3 
        gapple_x=randrange(340+gridSize,340+200-gridSize,gridSize)                                              # Generates the [X] coordinate
    elif quadrant ==4:                                                                                          # Section 4 
        gapple_x=randrange(WIDTH-260,WIDTH-260+40,gridSize)                                                     # Generates the [X] coordinate
    elif quadrant ==5:                                                                                          # Section 5 
        gapple_x=randrange(WIDTH-220+gridSize,WIDTH-220+200-gridSize,gridSize)                                  # Generates the [X] coordinate
    return(gapple_x)                                                                                            # Returns the new [X] coordinate for the [Good Apple]

    
def genGapple_y(quadrant):
                                                                                                                # This Function generates a new [Y] coordinate for the [Good Apple] from one of the 5 sections    
    if quadrant ==1:                                                                                            # Section 1
        gapple_y=randrange(20+gridSize,HEIGHT-40+20-gridSize,gridSize)                                          # Generates the [Y] coordinate
    elif quadrant ==2:                                                                                          # Section 2
        gapple_y=randrange(200+gridSize,HEIGHT-20-gridSize,gridSize)                                            # Generates the [Y] coordinate
    elif quadrant ==3:                                                                                          # Section 3 
        gapple_y=randrange(20+gridSize,20+HEIGHT-40-gridSize,gridSize)                                          # Generates the [Y] coordinate
    elif quadrant ==4:                                                                                          # Section 4
        gapple_y=randrange(20+gridSize,HEIGHT-200-gridSize,gridSize)                                            # Generates the [Y] coordinate
    elif quadrant ==5:                                                                                          # Section 5
        gapple_y=randrange(20+gridSize,20+HEIGHT-40-gridSize,gridSize)                                          # Generates the [Y] coordinate
    return(gapple_y)                                                                                            # Returns the new [Y] coordinate for the [Good Apple]


def genBapple_x(quadrant):
                                                                                                                # This Function generates a new [X] coordinate for the [Good Apple] from one of the 5 sections
    if quadrant ==1:                                                                                            # Section 1
        bapple_x=randrange(20+gridSize,300-20+20-gridSize,gridSize)                                             # Generates the [X] coordinate
    elif quadrant ==2:                                                                                          # Section 2
        bapple_x=randrange(300,300+40,gridSize)                                                                 # Generates the [X] coordinate
    elif quadrant ==3:                                                                                          # Section 3 
        bapple_x=randrange(340+gridSize,340+200-gridSize,gridSize)                                              # Generates the [X] coordinate
    elif quadrant ==4:                                                                                          # Section 4 
        bapple_x=randrange(WIDTH-260,WIDTH-260+40,gridSize)                                                     # Generates the [X] coordinate
    elif quadrant ==5:                                                                                          # Section 5 
        bapple_x=randrange(WIDTH-220+gridSize,WIDTH-220+200-gridSize,gridSize)                                  # Generates the [X] coordinate
    return(bapple_x)                                                                                            # Returns the new [X] coordinate for the [Good Apple]

    
def genBapple_y(quadrant):
                                                                                                                # This Function generates a new [Y] coordinate for the [Good Apple] from one of the 5 sections    
    if quadrant ==1:                                                                                            # Section 1
        bapple_y=randrange(20+gridSize,HEIGHT-40+20-gridSize,gridSize)                                          # Generates the [Y] coordinate
    elif quadrant ==2:                                                                                          # Section 2
        bapple_y=randrange(200+gridSize,HEIGHT-20-gridSize,gridSize)                                            # Generates the [Y] coordinate
    elif quadrant ==3:                                                                                          # Section 3 
        bapple_y=randrange(20+gridSize,20+HEIGHT-40-gridSize,gridSize)                                          # Generates the [Y] coordinate
    elif quadrant ==4:                                                                                          # Section 4
        bapple_y=randrange(20+gridSize,HEIGHT-200-gridSize,gridSize)                                            # Generates the [Y] coordinate
    elif quadrant ==5:                                                                                          # Section 5
        bapple_y=randrange(20+gridSize,20+HEIGHT-40-gridSize,gridSize)                                          # Generates the [Y] coordinate
    return(bapple_y)                                                                                            # Returns the new [Y] coordinate for the [Good Apple]



genQuad_Gapple=randint(1,5)                                 # Generates a number between 1-5 since there are 5 sections where the apple can generate            - Before any collision with the apple
gapple_x=genGapple_x(genQuad_Gapple)                        # Takes 1 out of the 5 sections are sets it as a parameter for the [X] coordinate of the [gapple]   - Before any collision with the apple
gapple_y=genGapple_y(genQuad_Gapple)                        # Takes 1 out of the 5 sections are sets it as a parameter for the [Y] coordinate of the [gapple]   - Before any collision with the apple

genQuad_Bapple=randint(1,5)                                 # Generates a number between 1-5 since there are 5 sections where the apple can generate            - Before any collision with the apple
bapple_x=genBapple_x(genQuad_Bapple)                        # Takes 1 out of the 5 sections are sets it as a parameter for the [X] coordinate of the [bapple]   - Before any collision with the apple
bapple_y=genBapple_y(genQuad_Bapple)                        # Takes 1 out of the 5 sections are sets it as a parameter for the [Y] coordinate of the [bapple]   - Before any collision with the apple

 
def redraw_screen():
    screen.fill(VELVET)                                                                                          # Red fill behind the bacakground image
    for i in range(gridSize, WIDTH, gridSize):                                                                   # For loop for rows
        pygame.draw.line (screen, (197,40,55), (i,0), (i,600), 1)                                                # Draws the grid (background) [ROWS]
    for j in range(gridSize, HEIGHT, gridSize):                                                                  # For loop for columns
        pygame.draw.line (screen, (197,40,55), (0,j), (800,j), 1)                                                # Draws the grid (background) [COLUMNS]
    screen.blit(background, (0,0))                                                                               # Red background

    screen.blit(gApple, (int(gapple_x+gridSize/2)-10,int(gapple_y+gridSize/2)-10))                               # Draws the [gapple] and and instead of having it's point on the top left corner, it is set to the middle
    screen.blit(bApple, (int(bapple_x+gridSize/2)-10,int(bapple_y+gridSize/2)-10))                               # Draws the [bapple] and and instead of having it's point on the top left corner, it is set to the middle

    pygame.draw.rect(screen, VELVET_DARK, (x1,y1,w1,h1), outline)                                                # Rect 1 (Top left wall)
    pygame.draw.rect(screen, VELVET_DARK, (x2,y2,w2,h2), outline)                                                # Rect 2 (Bottom right wall)
    pygame.draw.rect(screen, VELVET_DARK, (0,0,20,HEIGHT), outline)                                              # Rect 3 (Left border)
    pygame.draw.rect(screen, VELVET_DARK, (0,0,WIDTH,20), outline)                                               # Rect 4 (Top border)
    pygame.draw.rect(screen, VELVET_DARK, (WIDTH-20,0,WIDTH-20,HEIGHT), outline)                                 # Rect 5 (Right border)
    pygame.draw.rect(screen, VELVET_DARK, (0,HEIGHT-20,WIDTH,20), outline)                                       # Rect 5 (Bottom border)
    
    timer_Text = regular_Font.render('Timer:'+(str(int(round(timer,0)))), 1, WHITE)                              # Timer text set - Using smaller font
    screen.blit(timer_Text,(50,50))                                                                              # Timer text print
    score_text = regular_Font.render('Score:'+(str(int(gapple_counter))), 1, WHITE)                              # Score text set - Using smaller font
    screen.blit(score_text,(50,80))                                                                              # Score text print
    
    for i in range(len(segx)):
        pygame.draw.circle(screen, headCLR, (segx[0]+int(gridSize/2), segy[0]+int(gridSize/2)), snake_Radius, outline)                   # Draws the head of the snake
        pygame.draw.circle(screen, segmentCLR, (segx[i]+int(gridSize/2), segy[i]+int(gridSize/2)), snake_Radius, outline)                # Draws the rest of the snake
    pygame.display.update()                                                                                                              # Display must be updated, in order to show the drawings


def gameOverScreen():                                                                                   # Game over function
    screen.blit(gameOver, (0,0))                                                                        # Game over image
    score_text = big_Font.render(str(int(gapple_counter)), 1, WHITE)                                    # Score text set - Using bigger font
    screen.blit(score_text,(450,325))                                                                   # Score text print
    pygame.display.update()                                                                             # Updates the image

                                                  
def mainMenuScreen():                                               # Main menu function
    screen.blit(startScreen, (0,0))                                 # Prints the main menu picture
    screen.blit(rulesButton, (132,424))                             # Prints the rules menu button picture
    pygame.display.update()                                         # Updates the image


def mainRulesScreen():                                              # Screen menu function
    screen.blit(rulesScreen, (0,0))                                 # Prints the rules picture
    screen.blit(startButton, (132,424))                             # Prints the start button picture
    pygame.display.update()                                         # Updates the image


                                    #---------------------------------------#
                                    #     The main program begins here      #
                                    #---------------------------------------#
inPlay = True
mainMenu = True

while mainMenu:                                                     # While true
    mainMenuScreen()                                                # Menu function / image
    for event in pygame.event.get():                                # For every event loop
        if event.type==pygame.MOUSEBUTTONDOWN:                      # If clicked on the button
            mx,my=pygame.mouse.get_pos()                            # Gets the position of the mouse
            if my>=424 and my<=544 and mx>=132 and mx<=669:         # The size of the button (anything between the dimensions)
                mainMenu= False                                     # Exits out of the function
                rules = True                                        # Opens the rules while loop


while rules:                                                        # While true
    mainRulesScreen()                                               # Rules function / image
    for event in pygame.event.get():                                # For every event loop
        if event.type==pygame.MOUSEBUTTONDOWN:                      # If clicked on the button
            mx,my=pygame.mouse.get_pos()                            # Gets the position of the mouse
            if my>=424 and my<=544 and mx>=132 and mx<=669:         # The size of the button (anything between the dimensions)
                rules= False                                        # Exits out of the function
                inPlay = True                                       # Starts the game

                                    #---------------------------------------#
                                    #          The game begins here         #
                                    #---------------------------------------#

while inPlay:                                                       # While the game is on
    ticker.tick(fps)                                                # Ticks the frames for the timer counter
    
    for event in pygame.event.get():                                # check for any events
        if event.type == pygame.QUIT:                               # If user clicked the X key on the top right
            pygame.quit()                                           # Flag that we are done so we exit this loop
    keys = pygame.key.get_pressed()
    
#---------------------Key Pressed---------------------#

    if keys[pygame.K_LEFT] and left==True:                          # If the left key is pressed     --------------------|
        speedX = -hSpeed                                            # Ball goes left                                     |
        speedY = 0                                                  # No Y changes                                       |
        right=False                                                 # Dont allow right movements                         |
        up,down=True,True                                           # Allow up and down movements                        |
                                                                    #                                                    |
    if keys[pygame.K_RIGHT] and right==True :                       # If the right key is pressed                        |
        speedX = hSpeed                                             # Ball goes right                                    |
        speedY = 0                                                  # No Y changes                                       |
        left=False                                                  # Dont allow left movements                          |
        up,down=True,True                                           # Allow up and down movements                        |           The booleans dont allow the player to
                                                                    #                                                    |---------- (^c)press the up button if the snake is going up 
    if keys[pygame.K_UP] and up==True:                              # If the up key is pressed                           |           (^c)and vice versa, and dont allow the player 
        speedX = 0                                                  # No X changes                                       |           (^c)to press the right button if the snake is 
        speedY = -vSpeed                                            # ball goes up                                       |           (^c)going left and vice versa.
        down=False                                                  # Dont down left movements                           |
        left,right=True,True                                        # Allow left and right movements                     |
                                                                    #                                                    |
    if keys[pygame.K_DOWN]and down==True:                           # If the down key is pressed                         |
        speedX = 0                                                  # No X changes                                       |
        speedY = vSpeed                                             # ball goes down                                     |
        up=False                                                    # Dont allow up movements                            |
        left,right=True,True                                        # Allow left and right movements     -----------------


#---------------------Border of the screen---------------------#
#Border        
    if segx[0] < 20 or segx[0] > WIDTH-20-snake_Radius or segy[0] < 20 or segy[0] > HEIGHT-20-snake_Radius :                         #If the ball is not on the screen (X axis)
        inPlay=False                                                                                                                 #Breaks out of the  in play while loop to go into the game over screen

#Rectangle 1
    if segx[0] < x1+w1-snake_Radius  and segx[0] > x1-snake_Radius and segy[0] < y1+h1-snake_Radius and segy[0] > y1-snake_Radius:   #If the ball is not on the screen (X axis)
        inPlay=False                                                                                                                 #Breaks out of the  in play while loop to go into the game over screen
        
#Rectangle 2        
    if segx[0] < x2+w2-snake_Radius  and segx[0] > x2-snake_Radius and segy[0] < y2+h2-snake_Radius and segy[0] > y2-snake_Radius:   #If the ball is not on the screen (X axis)
        inPlay=False                                                                                                                 #Breaks out of the  in play while loop to go into the game over screen
                
#---------------------Move all segments---------------------#
        
    for i in range(len(segx)-1,0,-1):                                         # start from the tail, and go backwards:
        segx[i]=segx[i-1]                                                     # Every segment takes the coordinates of the previous one (X)
        segy[i]=segy[i-1]                                                     # Every segment takes the coordinates of the previous one (X)
        
#---------------------Move the head---------------------#

    segx[0] = segx[0] + speedX                                                # Moves the head (X)
    segy[0] = segy[0] + speedY                                                # Moves the head (Y)

#---------------------Gameover scenarios---------------------#
         
    if timer<=0:                                                              # If timer gets to 0
        inPlay=False                                                          # Breaks out of the inplay while loop
        print('You ran out of time')

    if lengthSnake<=0:                                                        # If the snake has no body (Just the head):
        inPlay=False                                                          # Breaks out of the inplay while loop
        print('You starved to death - Length of the snake is 1 - No body')

#---------------------Collision with Gapple---------------------#
      
    for i in range (snake_Radius):
        if segx[0] == gapple_x + i  and segy[0] == gapple_y + i or segx[0] == gapple_x - i  and segy[0] == gapple_y - i:             # If the snake is inside the good apple
            segx.append(segx[-1])                                                                                                    # Appends the X of the segment
            segy.append(segy[-1])                                                                                                    # Appends the X of the segment
            genQuad_Gapple=randint(1,5)                                                                                              # Generates a number between 1-5 since there are 5 sections where the apple can generate
            gapple_x=genGapple_x(genQuad_Gapple)                                                                                     # Generates an X coordinate from the genGapple_x function
            gapple_y=genGapple_y(genQuad_Gapple)                                                                                     # Generates an Y coordinate from the genGapple_y function    
            gapple_counter +=1                                                                                                       # Adds 1 to the score 
            timer+=5                                                                                                                 # Increases 5 seconds for the timer count
            lengthSnake+=1                                                                                                           # Counts the number of segments - Ads one every time it hits of good apple   
            biteSound.play()                                                                                                         # Plays the eating sound

            if gapple_counter%5==0:                                                                                                  # For every time your score is a multiple of 5, the speed of the game increases 
                fps+=5                                                                                                               # (^cont.) Every time you move on through the game, it gets more difficult
        
#---------------------Collision with Poison apple (Bapple)---------------------#
    
    for i in range (snake_Radius):
        if segx[0] == bapple_x + i  and segy[0] == bapple_y + i or segx[0] == bapple_x - i  and segy[0] == bapple_y - i:             # If the snake head hits the bad apple
            segx.remove(segx[-1])                                                                                                    # Removes the X of the segment
            segy.remove(segy[-1])                                                                                                    # Removes the Y of the segment
            genQuad_Bapple=randint(1,5)                                                                                              # Generates a number between 1-5 since there are 5 sections where the apple can generate
            bapple_x=genBapple_x(genQuad_Bapple)                                                                                     # Generates an X coordinate from the genGapple_x function
            bapple_y=genBapple_y(genQuad_Bapple)                                                                                     # Generates an Y coordinate from the genGapple_y function    
            timer-=5                                                                                                                 # Removes 5 seconds from the timer
            lengthSnake-=1                                                                                                           # Counts the number of segments - Subtracts one every time it hits of bad apple                            
            biteSound.play()                                                                                                         # Plays the eating sound

#---------------------Collision with itself---------------------#
            
    for i in range(len(segx)-1,0,-1):                                         # Start from the tail, and go backwards
        if segx[0] == segx[i] and segy[0] == segy[i]:                         # If the head hits its self
            inPlay=False                                                      # Breaks out of the inplay while loop

#---------------------Redraws the game---------------------#
    if timer>0:                                                               # If timer is above 0
        redraw_screen()                                                       # Redraws the whole game
        timer-=1/fps                                                          # Continues the timer - Subtracts 1 from timer
        
#---------------------Everything out of the inPlay while loop---------------------#

gameOverScreen()                                                              # Sets the gameover function / image
gameOverSound.play()                                                          # Plays the gameover sound
pygame.time.delay(5000)                                                       # Set the delay to 5000 for the gameover function can last for 5 seconds
pygame.quit()                                                                 # always quit pygame when done!

