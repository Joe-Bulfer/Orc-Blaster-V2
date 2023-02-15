import pygame, sys, os, time

pygame.init()
clock = pygame.time.Clock()

screen_width = 900  # specifies the window dimensions
screen_height = 500

win = pygame.display.set_mode((screen_width,screen_height)) # creates the window
pygame.display.set_caption('Orc Blaster V2') # This creates the caption on the top of the window

title_orc = pygame.transform.scale((pygame.image.load("space_jam_files/orc.xcf")),(300,200)) # static image on main menu screen

settings_active = False # placeholder for what will be used to change to the settings menu
  
class menu_tab: # Creates the menu text
    def __init__(self,text,x,y):
        self.text = text
        self.x = x
        self.y = y

    def display(self):
        blue_rect = pygame.Rect(self.x-12,self.y,214,50) # rectangles appear behind text 
        pygame.draw.rect(win,(0,0,50),blue_rect)
        self.rect = pygame.Rect(self.x-7,self.y+5,205,40  ) #instead of a border fot the black rect, I made a slightly larger blue rect behind it
        pygame.draw.rect(win,(0,0,0),self.rect)

        font = pygame.font.Font('space_jam_files/Audiowide-Regular.ttf',25)
        text = font.render(self.text,False,'White')
        win.blit(text,(self.x,self.y+5))

        x_img = (pygame.image.load("space_jam_files/X_post.xcf")) # X appears when mouse hovers over each tab
        hover_x = pygame.transform.scale(x_img,(25,37))

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            win.blit(hover_x,(self.x+155,self.y+5))

class main_text: # for the main menu title text, settings "Speed is" text, game over text and pause text
    def __init__(self,text,x,y):
        self.text = text
        self.x = x
        self.y = y

    def display(self):
        # white_rect = pygame.Rect(self.x,self.y+15,260,30) # I may decide to use this backround/rects for the main text
        # pygame.draw.rect(win,"white",white_rect)
        font = pygame.font.Font('space_jam_files/Audiowide-Regular.ttf',40)
        text = font.render(self.text,False,"white")
        win.blit(text,(self.x,self.y+5))


class background():                 # class creates backround which moves downward, giving the player the illusion of moving though space
    def __init__(self,img_path,speed): 
        self.img_path = img_path        
        self.speed = speed          # speed of the moving backround
        self.width = screen_width   # width and height matches dimensions of window to the background image
        self.height = screen_height 

        self.scroll = 0  # the speed is added to this variable in every loop, then added to the backround y position, moving it downward continously per frame/loop

    def display(self):

        bg_img = pygame.image.load(os.path.join(self.img_path))
        bg = pygame.transform.scale(bg_img,(self.width,self.height)) # fits image to window dimensions
        self.scroll += self.speed
        win.blit(bg,(0,self.scroll)) # Two identicle bg images are blitted on top of eachother, both moving downward
        win.blit(bg, (0,-self.height + self.scroll))

        if self.scroll >= self.height: # when bg image moves too far down, its reseted to the top (0), this creates a loop of an infinitely moving backround
            self.scroll = 0
    def pause_bg(self):
        self.speed = 0
    def unpause_bg(self):
        self.speed = 2


# this class^ which generates a moving background, is very convenient, as the game is developed, levels will be made--
# --which each are located on a specific planet or part of space, requiring a unique backround
menu_bg= background('space_jam_files/black_bg.jpg',0.5)
game_active_bg = background('space_jam_files/black_bg.jpg',2) # simply choose image and speed and you have your background, automatically fitted to the screen, speed = 0 for still image
pause_bg = background('space_jam_files/black_bg.jpg',0)

class entity(): # having an entity class which player and orc class will inherit from clears up code, and is better structured and optimized                              
    def __init__(self,x,y,width,height,health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
    
    def draw(self, img_path):  # blits the orc and spaceship/player on the screen
        self.img = pygame.image.load(img_path)
        self.surf = pygame.transform.scale(self.img,(self.width,self.height))
        win.blit(self.surf,(self.x,self.y))

    def draw_orc_health_bar(self): # the health bar will appear above the orc, following it as it moves
        if self.health >= 0:
            health_rect_green = pygame.Rect(self.x+23,self.y,self.health,10)  
            health_rect_red = pygame.Rect(self.x+23,self.y,100,10)  
            pygame.draw.rect(win,(100,0,0),health_rect_red)
            pygame.draw.rect(win,(50,100,0),health_rect_green)
    def draw_sp_health_bar(self): # main spaceship healthbar is static, at the bottom of the screen
        if self.health >= 0:
            health_rect_green = pygame.Rect(0,490,self.health,10)  
            health_rect_red = pygame.Rect(0,490,screen_width,10)  
            pygame.draw.rect(win,(100,0,0),health_rect_red)
            pygame.draw.rect(win,(50,100,0),health_rect_green)
            ''' technically two health bars are drawn overlapping eachother, 
            the green bar shrinks with lowering health, showing more of the 
            red bar (play game to visualize this) '''

class enemy(entity):
    def __init__(self,x,y,width,height,health):
        super().__init__(x,y,width,height,health) # super is a method used to inherit from entity class
        self.x_vel = 1
        self.y_vel = 1
    def spawn(self): # I may add a spawn method which slowly moves the enemy onto the screen, from outside the window
        pass         # The orc will already be drawn with the draw method outside the screen (i.e x=-50,y=-50)
                     # then the spawn method will moves it onto the screen, once in place, the movement and attack method will be called

class Orc(enemy):
    def __init__(self,x,y,width,height,health):
        super().__init__(x,y,width,height,health) # also inherits from the entity class
        self.orc_speed = 0 # placeholders
        self.orc_vel = 0
    def move(self): # this movement pattern has the orc follow the player, and moves very dynamic
        if self.x >= ga_sp_1.x:
            self.orc_vel += -0.05
            self.orc_speed += self.orc_vel
            self.x += self.orc_speed
            if self.x >= ga_sp_1.x:
                self.orc_vel = 0 # resets the velocity when it crosses player
        if self.x <= ga_sp_1.x:
            self.orc_vel += 0.05
            self.orc_speed += self.orc_vel
            self.x += self.orc_speed
            if self.x <= ga_sp_1.x: # resets the velocity when it crosses player
                self.orc_vel = 0
        # these if statements reset the velocity to zero when the orc bounces off the edges of the screen
        if self.x >= 770:
            self.orc_vel = -.5
            self.x = 770
        if self.x <= 0:
            self.orc_vel = .5
            self.x = 0
    def attack(self): # enemy attack mechanic under progress
        pass
        
pause_text = main_text("Paused",350,200)
class player(entity):
    def __init__(self,x,y,width,height,health):
        super().__init__(x,y,width,height,health) # inherits from the entity class

    def movement(self):
        self.right = False
        self.left = False
        self.firing = False
        keys = pygame.key.get_pressed() # get_ pressed returns current state of the key
        if keys[pygame.K_LEFT]:
            self.left = True
            self.right = False
        elif keys[pygame.K_RIGHT]:
            self.right = True
            self.left = False
        else:
            self.right = False
            self.left = False
        if self.right == True:
            self.x += 5
        if self.left == True:
            self.x -= 5
        if self.x <= 0: # keeps the player on the screen
            self.x = 0
        if self.x >= 830: # keeps the player on the screen
            self.x = 830
        if settings_active == True: # keeps the spaceship on the left side of the screen in the settings menu
            if self.x >= 310:
                self.x = 310

    def attack(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.firing= True
        else:
            self.firing = False
        if self.firing ==True:
            laser_rect = pygame.Rect(self.x + 33,-20,4,424) # creates rect for laser which checks collision with orc
            pygame.draw.rect(win,(255,0,0),(laser_rect)) # blits laser on screen
            
# I wrote this pause funtion a long time ago which was the most diffucult code I have ever written. 
# I will try to review it sometime and explain the logic in the future. Game development is very complex.
def pause():  
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False


                elif key[pygame.K_q]:
                    pygame.quit()
                    quit()
        game_active_bg.pause_bg()
        pause_text.display()
        pygame.display.update()
        clock.tick(10)

# ga is game active, sp is spaceship
# these create the respective objects with the exact starting position on the screen
ga_sp_1 = player(400,380,70,100,900)
ga_sp_2 = player(400,380,70,100,900)
orc = Orc(400,30,150,100,100)

# main menu objects
play_tab = menu_tab("Play Game",100,100)
settings_tab = menu_tab("Settings",100,160)
quit_tab = menu_tab("Quit",100,220)

# settings menu objects
settings_swap_tab = menu_tab("Change Ship",400,30,)
settings_add_tab = menu_tab("Add Speed",400,90,)
settings_lower_tab = menu_tab("Lower Speed",400,150,)
settings_back_tab = menu_tab("Go Back",400,210,)

speed_text = main_text("Speed is",100,80) # This text will always display

speed_50_text = main_text("50",150,120) # settings menu is under progress if add or lower speed, a different speed text will display
speed_100_text = main_text("100",150,120) # if add or lower speed, a different speed text will display
speed_150_text = main_text("150",150,120)

settings_sp_1 = player(140,200,100,130,900) # this sp will only use draw method, to stay static as an image on the screen
settings_sp_2 = player(140,200,100,130,900)

menu_active = True
game_active = False
settings_active = False
sp_1 = True # spaceship 1 is default
sp_2 = False # once player changes sp in settings, another sp_2 is called


# main game loop. I will add more comments in the future as I continue reviewing

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause()

    if menu_active == True:
        # menu options on the right side
        menu_bg.display()
        play_tab.display()
        settings_tab.display()
        quit_tab.display()
        # Orc Blaster text and orc image on right side
        title_card = pygame.transform.scale(pygame.image.load("space_jam_files/orc_blaster_title.png"),(250,280))
        win.blit(title_card,(480,70))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_tab.rect.collidepoint(pygame.mouse.get_pos()): # gives the ingame option of exiting, besides clicking window X
                pygame.quit()
                exit()
            if play_tab.rect.collidepoint(pygame.mouse.get_pos()): # starts game
                game_active = True
                menu_active = False
            if settings_tab.rect.collidepoint(pygame.mouse.get_pos()): # opens settings menu
                settings_active = True


    if game_active == True:
        menu_active = False
        game_active_bg.unpause_bg()
        if sp_1 == True:
            sp_2 = False
            game_active_bg.display()
            ga_sp_1.draw('space_jam_files\/spaceship.png')
            ga_sp_1.movement()
            ga_sp_1.attack()
            ga_sp_1.draw_sp_health_bar()
        if sp_2 == True:
            sp_1 = False
            ga_sp_2.draw('space_jam_files\/sp_2.xcf')
            ga_sp_2.movement()
            ga_sp_2.attack()
            ga_sp_2.draw_sp_health_bar()
        orc.draw('space_jam_files\/orc.xcf')
        orc.move()
        orc.attack()
        orc.draw_orc_health_bar() 
        

    if settings_active == True:
        menu_active = False
        menu_bg.display()
        settings_swap_tab.display()
        settings_add_tab.display()
        settings_lower_tab.display()
        settings_back_tab.display()
        
        
        speed_text.display()
        speed_50_text.display()
        # if speed_50 == True:
        #     speed_50_text.display()
        # if speed_100 == True:
        #     speed_100_text.display()
        # if speed_150 == True:
        #     speed_150_text.display()
        if sp_1 == True:
            sp_2 = False
            settings_sp_1.draw('space_jam_files\/spaceship.png')
        elif sp_2 == True:
            sp_1 = False
            settings_sp_2.draw('space_jam_files\/sp_2.xcf')
        if event.type == pygame.MOUSEBUTTONDOWN: # goes back to the main menu
            if settings_back_tab.rect.collidepoint(pygame.mouse.get_pos()):
                menu_active = True
                settings_active = False
                game_active = False
            if settings_swap_tab.rect.collidepoint(pygame.mouse.get_pos()):
                sp_2 = True
                sp_1 = False # under progress, can only switch sp once currently
                

            
        

    clock.tick(60)
    pygame.display.update()
