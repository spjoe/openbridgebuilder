import pygame
from pygame.locals import *
from pygame.color import *
import pymunk as pm
from pymunk import Vec2d
import math, sys, random
import logging


logging.basicConfig(level=logging.DEBUG)

###############################################################################
#############################Game Class Muhaha!################################
###############################################################################
class Game:
    
    FRAME_RATE = 60

    SCREEN_W = 640
    SCREEN_H = 480

    def __init__(self):

        self.logger = logging.getLogger('GameLogger')
        self.logger.setLevel(logging.DEBUG)
        
        self.running = False
        self.quit = False
        self.zoomfactor = 1.00

        self.xverschiebung = 0.0
        self.yverschiebung = 0.0

        pygame.init()
        size = Game.SCREEN_W, Game.SCREEN_H
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()

        ### Physics stuff
        pm.init_pymunk()
        self.space = pm.Space()
        self.space.gravity = Vec2d(0.0, -900.0)
        
        self.space.resize_static_hash()
        self.space.resize_active_hash()

        self.space.set_default_collisionpair_func(self.coll_func, self.screen)

        self.beams = []

        mass = 10
        offset = Vec2d(0.0,0.0)
        self.vertices = [(100.0, 300.0),(100,330),(200,330),(200,300)]
        inertia = pm.moment_for_poly(mass, self.vertices, offset)
        body = pm.Body(mass, inertia)
        x = random.randint(115,350)
        body.position = x, 400
        shape = pm.Poly(body, self.vertices, offset)
        self.space.add(body, shape)
        self.beams.append(shape)

        self.Change = False
        self.GetInputfn = self.CommonGetInput
        self.Movefn = self.CommonMove
        self.CollisionDetectionfn = self.CommonCollisonDetection
        self.Drawfn = self.CommonDraw

        self.allSprites = pygame.sprite.Group()

        self.background = pygame.Surface(size).convert()

        self.rects = []

        static_body = pm.Body(pm.inf, pm.inf)
        self.static_lines = [pm.Segment(static_body, (111.0, 280.0), (407.0, 246.0), 0.0)
                    ,pm.Segment(static_body, (407.0, 246.0), (407.0, 343.0), 0.0)
                    ]    
        self.space.add_static(self.static_lines)
    
        
    def position_to_pygame(self,p):
        """Small hack to convert pymunk to pygame coordinates"""
        return int(p.x * self.zoomfactor + self.xverschiebung), int(-p.y * self.zoomfactor + Game.SCREEN_H + self.yverschiebung)

    def points_to_pygame(self,points):
        newpoints = []
        for p in points:
            pos = Pos(p[0],p[1])
            newpoint = self.position_to_pygame(pos)
            newpoints.append(newpoint)
        return newpoints

    def coll_func(self,shapeA, shapeB, contacts, normal_coef, screen):
        """Draw a circle at the contact, with larger radius for greater collisions"""
        for c in contacts:
            r = int(max( 3, abs(c.distance*5) ))
            p = self.position_to_pygame(c.position)
            self.rects.append(pygame.draw.circle(screen, THECOLORS["red"], p, r, 0))
        return True
 
    def common_event(self,event):
        if event.type == pygame.QUIT or \
        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.logger.debug ("Exit the Programm")
            self.quit = True
        else:
            self.logger.debug (event)
    

    def CommonGetInput(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.zoomfactor += 0.05
                    self.zoompoint = event.pos
                    self.zoomchanged = True
                    self.InZoom = True
                elif event.button == 5:
                    if self.zoomfactor > 0.4:
                        self.zoomfactor -= 0.05
                        self.zoompoint = event.pos
                        self.zoomchanged = True
            elif event.type == MOUSEMOTION:
                if event.buttons[2] == 1 or event.buttons[1] == 1:
                    self.xverschiebung += event.rel[0]
                    self.yverschiebung += event.rel[1]
            else:
                self.common_event(event)
    
    def CommonMove(self): 
        self.allSprites.update()          

    def CommonCollisonDetection(self):
        pass

    def CommonDraw(self):
        for rect in self.rects:
            self.screen.blit(self.background,rect,rect)

        self.rects = []
        for beam in self.beams:
            #if ball.body.position.y < 200: balls_to_remove.append(ball)

            points = self.points_to_pygame(beam.get_points())
      
            
            self.rects.append(pygame.draw.polygon(self.screen, (0,255,0),points ))
            #pygame.draw.circle(self.screen, THECOLORS["blue"], p, int(beam.radius), 2)
        for line in self.static_lines:
            body = line.body
            pv1 = body.position + line.a.rotated(math.degrees(body.angle))
            pv2 = body.position + line.b.rotated(math.degrees(body.angle))
            p1 = self.position_to_pygame(pv1)
            p2 = self.position_to_pygame(pv2)
            
            self.rects.append(pygame.draw.lines(self.screen, THECOLORS["lightgray"], False, [p1,p2]))

           

        dt = 1.0/60.0
        for x in range(1):
            self.space.step(dt)

        pygame.display.flip()

        pygame.display.set_caption("fps: " + str(self.clock.get_fps()))


    def Changefn(self):
        if not self.Change:
            return
        self.logger.debug("Change:::")

    def run(self):
        """Main Game Loop"""
        self.running = True
        while not self.quit:
            self.GetInputfn()
            self.Movefn()
            self.CollisionDetectionfn()
            self.Drawfn()
            self.Changefn()
            self.clock.tick(Game.FRAME_RATE)
        pygame.quit()

class Pos:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
if __name__ == '__main__':
    game = Game()
    game.run()
###############################################################################
##############################Global Functions#################################
###############################################################################
def load_sound(name):
    class NoneSound:
        def play(self,n=1): pass
        def stop(self): pass
    if not pygame.mixer:
        return NoneSound()
    #return NoneSound()
    fullname = os.path.join('data',name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print "Error: can not load sound: ", fullname
        raise SystemExit, message
    return sound

def load_image(name):
    fullname = os.path.join("data", name)
    img = pygame.image.load(fullname)
    return img.convert(img)

###############################################################################
#############################Beginn of Evil :-)################################
###############################################################################
if __name__=='__main__':
    logging.info ("Programm gestartet")
    game = Game()
    game.run()
    logging.info ("Programm beendet")
