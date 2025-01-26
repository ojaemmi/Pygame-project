import pygame
import random


# Initiating game
pygame.init()
kello = pygame.time.Clock()

# Creating constants
naytto_leveys, naytto_korkeus = 840, 680
robo_nopeus = 5
hirvio_nopeus = 3

# Creating screen and headline
naytto = pygame.display.set_mode((naytto_leveys, naytto_korkeus))
pygame.display.set_caption("Kolikkojahti")

# Uploading pictures
robo_kuva = pygame.image.load("robo.png")
kolikko_kuva = pygame.image.load("kolikko.png")
hirvio_kuva = pygame.image.load("hirvio.png")
ovi_kuva = pygame.image.load("ovi.png")

# Muutetaan robotin kokoa, helpottaa pelaamista ja tekee vaikeista tasoista pelattavia
# Changing the size of the robot, making gameplay easier and higher levels playable
robo_kuva = pygame.transform.scale(robo_kuva, (40,50)) 
leveys, korkeus = robo_kuva.get_width(), robo_kuva.get_height()



# Robo-class, responsible for the movement and drawing of the robot
###########################
class Robo:
    def __init__(self):
        # Creating a rectangle for robot and intiating place
        self.rect = robo_kuva.get_rect()
        self.rect.topleft = (0, naytto_korkeus-korkeus)
    
    # Moving-function:
    def liike(self, napit):
        if napit[pygame.K_LEFT] and self.rect.left > 0:                # To left
            self.rect.x -= robo_nopeus
        if napit[pygame.K_RIGHT] and self.rect.right < naytto_leveys:  # To right
            self.rect.x += robo_nopeus
        if napit[pygame.K_UP] and self.rect.top > 0:                   # Up
            self.rect.y -= robo_nopeus
        if napit[pygame.K_DOWN] and self.rect.bottom < naytto_korkeus: # Down
            self.rect.y += robo_nopeus
        
    # Drawing-function
    def piirto(self):
        naytto.blit(robo_kuva,self.rect.topleft)


# Hirvio-class, responsible for the movement and drawing of the monster
###########################
class Hirvio:
    def __init__(self):
        self.rect = hirvio_kuva.get_rect()
        # Choosing an arbitrary location (x-direction is limited so that the player doesn't lose immediately after leveling up)
        self.rect.topleft = (random.randint(0, naytto_leveys / 2), random.randint(0, naytto_korkeus - self.rect.height))
        self.suunta = random.choice([-1, 1])  # Arbitrary direction to left or right

    def liike(self):
        self.rect.x += self.suunta * hirvio_nopeus
        # Monster changes direction after hitting a wall
        if self.rect.left <= 0 or self.rect.right >= naytto_leveys:
            self.suunta *= -1

    # Drawing-function
    def piirto(self):
        naytto.blit(hirvio_kuva, self.rect.topleft)

    # Function that initiates a new place for each monster, used when leveling up
    def uusi_paikka(self):
        self.rect.topleft = (random.randint(0, naytto_leveys / 2),random.randint(0, naytto_korkeus - self.rect.height))


# Kolikko-class, responsible for the drawing of the coin
###########################
class Kolikko:
    def __init__(self):
        self.rect = kolikko_kuva.get_rect()
        # Arbitrary location
        self.rect.topleft = (random.randint(0, naytto_leveys - self.rect.width), random.randint(0, naytto_korkeus - self.rect.height))
    
    def piirto(self):
        naytto.blit(kolikko_kuva, self.rect.topleft)


# Ovi-class, responsible for the drawing of the door for leveling up
###########################
class Ovi:
    def __init__(self):
        self.rect = ovi_kuva.get_rect()
        self.rect.topleft = (naytto_leveys-self.rect.width,random.randint(0, naytto_korkeus - self.rect.height))

    def piirto(self):
        naytto.blit(ovi_kuva,self.rect.topleft)


# Game variables
robo = Robo()
hirviot = [Hirvio()]
kolikot = [Kolikko() for _ in range(3)]
ovi = Ovi()
keratyt_kolikot = 3
taso = 1
pisteet = 0

# Lastly a function that creates a new game, where each constant in initiated again
###########################
def uusi_peli():
    global robo, hirviot, kolikot, ovi, keratyt_kolikot, taso, pisteet
    robo = Robo()
    hirviot = [Hirvio()]
    kolikot = [Kolikko() for _ in range(3)]
    ovi = Ovi()
    keratyt_kolikot = 3
    taso = 1
    pisteet = 0


# Main loop
while True:
    napit = pygame.key.get_pressed()
    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:
            exit()

    robo.liike(napit)

    for hirvio in hirviot:
        hirvio.liike()
    
    # Checking collision with coins
    for kolikko in kolikot[:]:
        if robo.rect.colliderect(kolikko.rect):
            pisteet += 1
            keratyt_kolikot -= 1
            kolikot.remove(kolikko)   # Removing collected coins

    # Checking collision with door, only available if all coins are collected
    if robo.rect.colliderect(ovi.rect) and keratyt_kolikot == 0:
        taso += 1
        keratyt_kolikot = 3
        kolikot = [Kolikko() for _ in range(3)]  # Zeroing coins
        hirviot.append(Hirvio())                 # Every new level has a new monster of Hirviö-class
        ovi = Ovi()                              # Creating a new door
        for hirvio in hirviot[:]:
            hirvio.uusi_paikka()                 # Initiating new arbitrary locations for monsters on each level


    # Checking collision with monsters
    for hirvio in hirviot[:]:
        if robo.rect.colliderect(hirvio.rect):
            naytto.fill((0, 0, 0))               # Emptyibg the screen
            fontti = pygame.font.Font(None, 30)
    
            # Message when lost
            viesti = f"Hävisit!  Pisteet: {pisteet}   Taso: {taso}"
            teksti = fontti.render(viesti, True, (255, 255, 255))
            teksti_rect = teksti.get_rect(center=(naytto_leveys // 2, naytto_korkeus // 2))

            # Message for a new game + instructions
            uusipeli_viesti = "Aloita uusi peli painamalla Enter"
            uusipeli_teksti = fontti.render(uusipeli_viesti, True, (255, 255, 255))
            uusipeli_teksti_rect = uusipeli_teksti.get_rect(center=(naytto_leveys // 2, naytto_korkeus // 2 + 60))
            naytto.blit(uusipeli_teksti, uusipeli_teksti_rect)

            # Red rectangle with the messages
            pygame.draw.rect(naytto, (255, 0, 0), (teksti_rect.x - 20, teksti_rect.y - 20, teksti_rect.width + 40, teksti_rect.height + 40))
            naytto.blit(teksti, teksti_rect)

            pygame.display.flip()  # Updating the screen

            # Creating new Main loop and 'Waiting' loop, that waits for the player to press Enter
            odotetaan_aloitusta = True
            while odotetaan_aloitusta:
                for tapahtuma in pygame.event.get():
                    if tapahtuma.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if tapahtuma.type == pygame.KEYDOWN:
                        if tapahtuma.key == pygame.K_RETURN:    # Checking if Enter is pressed
                            uusi_peli()                         
                            odotetaan_aloitusta = False         # Exiting 'Waiting'-loop
            break                                               # Exiting Main loop and starting a new game


    # Creating a white screen and drawing each object
    naytto.fill((255, 255, 255))
    robo.piirto()
    for hirvio in hirviot:
        hirvio.piirto()
    for kolikko in kolikot:
        kolikko.piirto()
    ovi.piirto()

    # Drawing points, level, and the amount of coins collected on each level
    fontti = pygame.font.Font(None, 30)
    pisteet_teksti = fontti.render(f"Pisteet: {pisteet}", True, (0, 0, 0))
    kolikot_teksti = fontti.render(f"Kolikot: {keratyt_kolikot}", True, (0, 0, 0))
    taso_teksti = fontti.render(f"Taso: {taso}", True, (0, 0, 0))
    naytto.blit(pisteet_teksti, (10, 10))
    naytto.blit(taso_teksti, (10, 40))
    naytto.blit(kolikot_teksti, (10, 70))

    # Updating screen and clock
    pygame.display.flip()
    kello.tick(60)