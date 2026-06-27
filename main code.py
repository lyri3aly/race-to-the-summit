import math # used for car movement calculations
import pygame
import asyncio
pygame.init()
# pygame initialization

size = width, height = 1000, 700 # fixed display size
screen = pygame.display.set_mode(size)
myClock = pygame.time.Clock()

# colours
white = (255, 255, 255)
black = (0, 0, 0)
gray = (213, 221, 219)
skyblue = (98, 157, 186)
weirdblue = (91, 131, 139)
granite = (84, 105, 92)
darkbluegreen = (30, 61, 60)
forestgreen = (47, 65, 39)
armygreen = (72, 91, 51)
mildgreen = (97, 116, 62)
muddygreen = (87, 94, 54)
greenishsunflower = (87, 94, 54)

# times
startTime = 0
elapsedTime = 0
finalTime = 0

# image setups
# logo
logo = pygame.image.load("images/logo.png")

# arrows
leftarrow = pygame.image.load("images/left arrow.png")
leftarrowWidth = int(leftarrow.get_width() / 7)
leftarrowHeight = int(leftarrow.get_height() / 7)
leftarrow = pygame.transform.scale(leftarrow, (leftarrowWidth, leftarrowHeight)) # makes sure the arrows are not huge
rightarrow = pygame.image.load("images/right arrow.png")
rightarrowWidth = int(rightarrow.get_width() / 7)
rightarrowHeight = int(rightarrow.get_height() / 7)
rightarrow = pygame.transform.scale(rightarrow, (rightarrowWidth, rightarrowHeight))

# win screen
winScreen = pygame.image.load("images/win screen.png")

# helpScreen/instructions screen
helpScreen = pygame.image.load("images/help.png")

# road
roadW, roadH = 5000, 10000
road = pygame.image.load("images/road.png")
road = pygame.transform.scale(road, (roadW, roadH))
noroad = pygame.image.load("images/no road.png")
noroad = pygame.transform.scale(noroad, (roadW, roadH))
noroadmask = pygame.mask.from_surface(noroad) # instead of rect, mask goes pixel by pixel and is more accurate for my uneven and irregular roads
noroadRect = noroad.get_rect() # still get rect to be able to use the x and y variables

# car
whitePreview = pygame.image.load("images/white car.png")
yellowPreview = pygame.image.load("images/yellow car.png")
bluePreview = pygame.image.load("images/blue car.png")
carWidth = int(whitePreview.get_width() / 8)
carHeight = int(whitePreview.get_height() / 8)
whiteGame = pygame.transform.scale(whitePreview, (carWidth, carHeight))
yellowGame = pygame.transform.scale(yellowPreview, (carWidth, carHeight))
blueGame = pygame.transform.scale(bluePreview, (carWidth, carHeight))
car = whiteGame
carX = 4850
carY = 19500

# car physics
carAngle = 0.0
carSpeed = 0.0
acceleration = 0.06 # dialed down so the car doesn't start going to fast and makes the game harder
friction = 0.9
minX, minY = 25, 0
maxX = 10000
maxY = 100000000

# state variables
menu = 0
game = 1
helpState = 2
carDesign = 3
winState = 4
quitGame = 5
state = menu
startedalready = False # used to make sure timer doesn't restart in the middle of the game just for going back to the menu

# car design screen, same concept as the state and menu
carChoice = 0
selectedCar = 0
previewList = [whitePreview, yellowPreview, bluePreview]
gameList = [whiteGame, yellowGame, blueGame]

def drawMenu(screen, mx, my, button, state):
    # responsible for drawing the game menu 
    global startTime, startedalready # startTime is used elsewhere in the game, in another function
    screen.fill(gray)
    screen.blit(logo, (242, -125))

    # variables to determine where each option goes (+ addition for even spacing, I was getting tired of doing math every time)
    x = width / 3; y1 = 270 + 20; y2 = 395 + 20; y3 = 520 + 20
    blockW = 300; blockH = 100

    stateList = [carDesign, game, helpState]
    textList = ["Car Design", "Play", "Help"]
    blockList = [pygame.Rect(x, y1, blockW, blockH), 
                 pygame.Rect(x, y2, blockW, blockH), 
                 pygame.Rect(x, y3, blockW, blockH)]
    # all the states, texts, and pygame.Rect setups
    
    for i in range(len(blockList)):
        # goes through each item in the blockList to setup the menu more easily using variables
        blockValue = blockList[i]
        text = pygame.font.SysFont(None, 60).render(textList[i], 1, black)
        textWidth, textHeight = pygame.font.SysFont(None, 60).size(textList[i])
        textX = blockValue[0] + (blockW - textWidth) / 2
        textY = blockValue[1] + (blockH - textHeight) / 2

        pygame.draw.rect(screen, skyblue, blockValue)
        screen.blit(text, (textX, textY, textWidth, textHeight))

        if blockValue.collidepoint(mx, my):
            # is the mouse inside the blockValue rectangle (for each rect, for i in range)?
            pygame.draw.rect(screen, darkbluegreen, blockValue, 2)
            if button == 1:
                state = stateList[i]

    # below is the same code, same concept, without the variables because I wanted to put the Exit button seperately
    pygame.draw.rect(screen, skyblue, pygame.Rect(35, 600, 130, 70))
    screen.blit(pygame.font.SysFont(None, 60).render("Quit", 1, black), (55, 616, 120, 60))
    if pygame.Rect(35, 600, 130, 70).collidepoint(mx, my):
        pygame.draw.rect(screen, darkbluegreen, pygame.Rect(35, 600, 130, 70), 2)
        if button == 1:
            state = quitGame

    if state == game and startedalready == False:
        startTime = pygame.time.get_ticks() # gets the number of milliseconds since the game option has been clicked, used for time tracking and stopwatch later on
        startedalready = True
    return state

def drawDesigncar(screen, button, state, mx, my):
    global carChoice, car, selectedCar
    screen.fill(skyblue)

    # creating a rectangle for the arrows to be able to move them easier and detect clicks
    leftRect = leftarrow.get_rect(topleft = (10, 327))
    rightRect = rightarrow.get_rect(topleft = (920, 333))

    screen.blit(leftarrow, leftRect)
    screen.blit(rightarrow, rightRect)

    screen.blit(previewList[carChoice], (150, 100))

    selectRect = pygame.Rect(400, 480, 200, 80)
    pygame.draw.rect(screen, darkbluegreen, selectRect)

    # select button
    font = pygame.font.SysFont(None, 50)
    text = font.render("select", True, white)

    # centering the text perfectly, I later gave up on thinking too much about math and started finding the coordinates manually
    textX = selectRect.x + (selectRect.width - text.get_width()) / 2
    textY = selectRect.y + (selectRect.height - text.get_height()) / 2

    screen.blit(text, (textX, textY))

    if button == 1:
        # moving through the different car options
        if leftRect.collidepoint(mx, my):
            carChoice -= 1
            if carChoice < 0:
                carChoice = len(previewList) - 1
                # if the next value in the list is -1 (doesn't exist), go back to the last (3 - 1 = 2)
        if rightRect.collidepoint(mx, my):
            carChoice += 1
            if carChoice >= len(previewList):
                carChoice = 0
        if selectRect.collidepoint(mx, my):
            # finalizing selected car
            selectedCar = carChoice
            car = gameList[selectedCar]
            state = menu

        if button == 3:
            state = menu

    return state

def drawGame(button, state):
    global carX, carY, carAngle, speed, turnSpeed, carCenterX, carCenterY, cameraX, cameraY, width, height, carMask, noroadmask, noroadRect, carRect, finalTime
    
    # turning milliseconds into seconds
    elapsedTime = (pygame.time.get_ticks() - startTime) / 1000

    # car physics
    if carForward:
        speed += acceleration
        # gradually increase speed by acceleration, so the longer you hold your arrow keys, the faster the car accelerates
    elif carDown:
        speed -= acceleration
        # the other way around but going down/back
    else: 
        speed *= friction
        # use friction to slow the car down like in real life
    if abs(speed) < 0.06:
        speed = 0
        # don't want speed to be continuosly getting smaller but never reaching 0
    if carLeft:
        turnSpeed += acceleration
        carAngle += turnSpeed
    elif carRight:
        turnSpeed += acceleration
        carAngle -= turnSpeed
    else:
        turnSpeed *= friction
    if abs(turnSpeed) < 0.06:
        turnSpeed = 0
    # all the above same thing but for turning

    # turn the stored carAngles into radians so that python can do the math properly
    radians = math.radians(carAngle)

    # calculate the exact direction (coordinates) the car is moving using cos and sin, cosine for the X value and sine for the Y value
    carX += speed * math.cos(radians)
    carY -= speed * math.sin(radians)

    # car position, makes sure the car stays inside the image, technically, this is not needed as the car cannot physically go past the boundaries due to the collision detection (unless user is willing to push the car through a ditch for a few hours)
    carX = max(minX, min(carX, maxX))
    carY = max(minY, min(carY, maxY - carHeight))

    # camera tracking and boundaries
    carCenterX = (carX + carWidth) / 2
    carCenterY = (carY + carHeight) / 2

    # creating the actual image of the car after it has been rotated
    rotatedCar = pygame.transform.rotate(car, carAngle)

    # collision detection, masking again to better operate with the road masking
    carRect = rotatedCar.get_rect(center = (carCenterX, carCenterY))
    carMask = pygame.mask.from_surface(rotatedCar)

    if noroadmask.overlap(carMask, (carRect.x, carRect.y)):
        # if the two items overlap, the car will go backwards and decrease its speed until friction manually slows it down
        speed *= -1
        speed -= acceleration * 0.2
        speed *= friction
        if abs(speed) < 0.9:
            speed = 0

    # set restraints for the camera to center and fixate on
    cameraX = int(carCenterX - width / 2)
    cameraY = int(carCenterY - height / 2)

    # use those restraints to define the boundaries of the camera so that the camera is unable to go beyond the map, technically, this wouldn't normally be used either
    cameraX = max(0, min(cameraX, roadW - width))
    cameraY = max(0, min(cameraY, roadH - height))

    # the camera doesn't actually move, it moves the road images in the other direction so that it seems like the camera is moving
    screen.blit(road, (-cameraX, -cameraY))
    screen.blit(noroad, (-cameraX, -cameraY))

    # the timer/stopwatch in the top left corner
    font = pygame.font.SysFont(None, 50)
    timerText = font.render("Time: " + str(round(elapsedTime, 1)) + "s", True, white) # round, rounds the float to one digit as specified by the elapsedTime, 1
    screen.blit(timerText, (20, 20))

    if carY < 20:
        # detect if the user has finished the game
        if finalTime == 0:
            finalTime = elapsedTime
        state = winState

    if button == 3:
        state = menu
    return state

def drawhelp(screen, mx, my, button, state):
    screen.fill(weirdblue)
    screen.blit(helpScreen, (0, 0))
    if button == 3:
        state = menu
    return state

def drawWin(screen, button, state):
    # win screen
    screen.fill(forestgreen)
    screen.blit(winScreen, (0, 0))

    # display the final time in the designated rect on "win screen.png"
    font = pygame.font.SysFont(None, 50)
    text = font.render("Final Time: " + str(round(finalTime, 1)) + "s", True, white)
    screen.blit(text, (358, 450))

    if button == 3:
        state = menu
    return state

# set everything to false for the game loop
carForward = False
carDown = False
carLeft = False
carRight = False
speed = 0
turnSpeed = 0
running = True

mx, my, button = 0, 0, 0
async def main():
    global running, state, mx, my, button
    global carForward, carDown, carLeft, carRight
    global speed, turnSpeed
    global carAngle, carX, carY

    while running:

        # ---------------- EVENTS ----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                button = event.button

            if event.type == pygame.MOUSEMOTION:
                mx, my = event.pos

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    carForward = True
                if event.key == pygame.K_DOWN:
                    carDown = True
                if event.key == pygame.K_LEFT:
                    carLeft = True
                if event.key == pygame.K_RIGHT:
                    carRight = True
                if event.key == pygame.K_r:
                    carX = 4850
                    carY = 19500
                    carAngle = 0.0
                    speed = 0
                    turnSpeed = 0

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    carForward = False
                if event.key == pygame.K_DOWN:
                    carDown = False
                if event.key == pygame.K_LEFT:
                    carLeft = False
                if event.key == pygame.K_RIGHT:
                    carRight = False

        # ---------------- STATES ----------------
        if state == menu:
            state = drawMenu(screen, mx, my, button, state)

        elif state == game:
            state = drawGame(button, state)

            rotatedCar = pygame.transform.rotate(car, carAngle)
            boundingbox = rotatedCar.get_rect(
                center=(carCenterX - cameraX, carCenterY - cameraY)
            )
            screen.blit(rotatedCar, boundingbox)

        elif state == helpState:
            state = drawhelp(screen, mx, my, button, state)

        elif state == carDesign:
            state = drawDesigncar(screen, button, state, mx, my)

        elif state == winState:
            state = drawWin(screen, button, state)

        else:
            running = False

        pygame.display.flip()
        button = 0
        myClock.tick(60)

        # REQUIRED for pygbag (prevents freeze)
        await asyncio.sleep(0)

asyncio.run(main())
