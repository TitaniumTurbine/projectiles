import pygame
from pygame.locals import *
import tkinter as tk
import math
        
pygame.init()

window = pygame.display.set_mode((800,450), pygame.RESIZABLE)
pygame.display.set_caption("Projectiles")

gui = tk.Tk()
gui.title("Projectiles Settings")


class projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = False
        self.velocity = [0,0]

    def move(self):
        self.x += self.velocity[0]*10/144
        self.y += self.velocity[1]*10/144

class planet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 6
        self.gravity = 500

running = True

global enableTrails
global bounce
global collide

def invertBounce():
    global bounce
    bounce = not bounce
    bounceToggle = tk.Button(gui, text="Bounce: " + str(bounce), command=lambda : invertBounce())
    bounceToggle.grid(row=1, column=0)

def invertTrails():
    global enableTrails
    enableTrails = not enableTrails
    trailToggle = tk.Button(gui, text="Trails: " + str(enableTrails), command=lambda : invertTrails())
    trailToggle.grid(row=1, column=1)

def invertCollide():
    global collide
    collide = not collide
    collideToggle = tk.Button(gui, text="Particle Collisions: " + str(collide), command=lambda : invertCollide())
    collideToggle.grid(row=1, column=2)

def clear():
    global activeProjectiles
    global planets
    window.fill((0,0,0))
    activeProjectiles = []
    planets = []

enableTrails = True
bounce = False
collide = False

gravity = tk.Scale(gui, label="Gravity", from_=0, to=15, resolution=0.1, orient="horizontal", length=200)
gravity.grid(row=0, column=0)
gravity.set(9.8)

airResistance = tk.Scale(gui, label="Air Resistance", from_=0, to=1, resolution=0.1, orient="horizontal", length=200)
airResistance.grid(row=0, column=1)
airResistance.set(0)

collisionEnergyLoss = tk.Scale(gui, label="Bounce Energy Loss", from_=0.9, to=5, resolution=0.1, orient="horizontal", length=200)
collisionEnergyLoss.grid(row=0, column=2)
collisionEnergyLoss.set(1.3)

bounceToggle = tk.Button(gui, text="Bounce: " + str(bounce), command=lambda : invertBounce())
bounceToggle.grid(row=1, column=0)

trailToggle = tk.Button(gui, text="Trails: " + str(enableTrails), command=lambda : invertTrails())
trailToggle.grid(row=1, column=1)

collideToggle = tk.Button(gui, text="Particle Collisions: " + str(collide), command=lambda : invertCollide())
collideToggle.grid(row=1, column=2)

clearButton = tk.Button(gui, text="Clear", command=lambda : clear())
clearButton.grid(row=3, column=0)

activeProjectiles = []
planets = []

textFont = pygame.font.SysFont("Arial", 22)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == K_SPACE:
            clear()
        if event.type == pygame.KEYDOWN and event.key == K_1:
            invertBounce()
        if event.type == pygame.KEYDOWN and event.key == K_2:
            invertTrails()
        if event.type == pygame.KEYDOWN and event.key == K_3:
            invertCollide()

    if enableTrails == False:
        window.fill((0,0,0))

    
            
    if pygame.mouse.get_pressed()[0] == 1 and len(activeProjectiles) > 0 and activeProjectiles[-1].active == False:
        activeProjectiles[-1].velocity = [(pygame.mouse.get_pos()[0] - activeProjectiles[-1].x)/3, (pygame.mouse.get_pos()[1] - activeProjectiles[-1].y)/3]
        activeProjectiles[-1].active = True

    if pygame.mouse.get_pressed()[2] == 1:
        flag = False
        for proj in activeProjectiles:
            if proj.x == pygame.mouse.get_pos()[0] and proj.y == pygame.mouse.get_pos()[1]:
                flag = True
                
        if flag == False:
            if len(activeProjectiles) > 0 and activeProjectiles[-1].active == False:
                activeProjectiles.remove(activeProjectiles[-1])
            newProjectile = projectile(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            activeProjectiles.append(newProjectile)

    if pygame.mouse.get_pressed()[1] == 1:
        flag = False
        for p in planets:
                if p.x == pygame.mouse.get_pos()[0] and p.y == pygame.mouse.get_pos()[1]:
                    flag = True
        if flag == False:
            planets.append(planet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]))
    

    for proj in activeProjectiles:
        if proj.active == True:
            proj.velocity[1] += gravity.get()*10/144
            proj.velocity[0] -= proj.velocity[0]*airResistance.get()/44.2
            proj.velocity[1] -= proj.velocity[1]*airResistance.get()/44.2
            proj.move()
            for p in planets:
                if p.x > proj.x:
                    x = (p.x - proj.x)
                else:
                    x = proj.x - p.x
                if p.y > proj.y:
                    y = (p.y - proj.y)
                else:
                    y = proj.y - p.y

                r = math.sqrt(x*x + y*y)
                forceX = (p.gravity*x) / (r*r*r)
                forceY = (p.gravity*y) / (r*r*r)

                if p.x > proj.x:
                    proj.velocity[0] += forceX
                else:
                    proj.velocity[0] -= forceX
                if p.y > proj.y:
                    proj.velocity[1] += forceY
                else:
                    proj.velocity[1] -= forceY

                if r < p.radius:
                    activeProjectiles.remove(proj)
                    p.gravity += 1
                
            if bounce == True:
                if proj.x >= 798 and proj.velocity[0] > 0:
                    proj.velocity[0] = -(proj.velocity[0]/collisionEnergyLoss.get())
                elif proj.x <= 0 and proj.velocity[0] < 0:
                    proj.velocity[0] = -(proj.velocity[0]/collisionEnergyLoss.get())
                if proj.y >= 448 and proj.velocity[1] > 0:
                    proj.velocity[1] = -(proj.velocity[1]/collisionEnergyLoss.get())
                elif proj.y <= 27 and proj.velocity[1] < 0:
                    proj.velocity[1] = -(proj.velocity[1]/collisionEnergyLoss.get())

            if proj.x >= 810 or proj.x <= -10 or proj.y >= 460 or proj.y <= 17:
                activeProjectiles.remove(proj)

            if collide == True:
                for proj2 in activeProjectiles:
                    if proj2 != proj and proj2.active == True:
                        if proj.x <= proj2.x+2 and proj.x+2 >= proj2.x and proj.y <= proj2.y+2 and proj.y+2 >= proj2.y:
                            proj.velocity[0] = (proj.velocity[0] + proj2.velocity[0]) / (2)
                            proj2.velocity[0] = (proj2.velocity[0] + proj.velocity[0]) / (2)
                            proj.velocity[1] = (proj.velocity[1] + proj2.velocity[1]) / (2)
                            proj2.velocity[1] = (proj2.velocity[1] + proj.velocity[1]) / (2)

                            

            pygame.draw.rect(window, (255,255,255), pygame.Rect(proj.x, proj.y, 2, 2))

    for p in planets:
        pygame.draw.circle(window,(255,255,255),(p.x,p.y),p.radius)


    pygame.draw.rect(window, (150,150,150), pygame.Rect(0, 0, 800, 27))
    
    if bounce == False:
        bounceText = textFont.render("Bounce: OFF", True, (255,0,0))
    else:
        bounceText = textFont.render("Bounce: ON", True, (0,255,0))
    window.blit(bounceText, (0, 0))

    if enableTrails == False:
        trailText = textFont.render("Trails: OFF", True, (255,0,0))
    else:
        trailText = textFont.render("Trails: ON", True, (0,255,0))
    window.blit(trailText, (120, 0))

    if collide == False:
        collisionText = textFont.render("Particle Collisions: OFF", True, (255,0,0))
    else:
        collisionText = textFont.render("Particle Collisions: ON", True, (0,255,0))
    window.blit(collisionText, (225, 0))

    pygame.display.flip()
    pygame.time.Clock().tick(144)
    gui.update()
gui.mainloop()
