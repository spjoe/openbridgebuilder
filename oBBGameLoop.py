# Filename: oBBGameLoop.py
# vim:set sts=4 et sw=4 ts=4 ci ai:
"""
Open Bridge Builder -- a python+pygame based remake of Bridge Builder

Copyright 2008 Camillo Dell'mour (cdellmour@gmail.com)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
USA
"""
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk as pm
from pymunk import Vec2d
import math, sys, random
import logging
import oBBPhysicEngine
import oBBDrawEngine
import oBBConfig as conf

###############################################################################
#############################Game Class Muhaha!################################
###############################################################################
class Game:
    def __init__(self):

        self.logger = logging.getLogger('GameLoop')
        self.logger.setLevel(conf.DEVELOPMENT.LOGGINGLEVEL)

        self.quit = False
        self.simulate = False

        #Draw Engine
        size = conf.SCREEN_CONFIG.SCREEN_W, conf.SCREEN_CONFIG.SCREEN_H
        zoom = conf.GAME_CONFIG.ZOOM_START
        xver = conf.GAME_CONFIG.XVERSCHIEBUNG
        yver = conf.GAME_CONFIG.YVERSCHIEBUNG
        self.drawengine = oBBDrawEngine.DrawEngine(size,zoom,xver,yver,self)
        

        ### Physics Engine
        self.physicengine = oBBPhysicEngine.PhysicEngine(conf.GAME_CONFIG.GRAVITY)
        self.physicengine.run_physics = False
        self.physicengine.set_info("Test")

        ### Testobjekte
        self.walls = []

        wall = self.physicengine.add_wall((111.0, 280.0), (407.0, 300.0))
        self.walls.append(wall)
        wall = self.physicengine.add_wall((407.0, 300.0), (407.0, 200.0))
        self.walls.append(wall)


        self.beams = []

        self.vertices = [(10.0, 30.0),(10.0,60.0),(100.0,60.0),(100.0,30.0),(10.0, 30.0)]
        self.vertices2 = [(10.0, 30.0), (100.0,30.0),(100.0,60.0),(10.0,60.0),(10.0, 30.0)]
        #vertices2 = [(100.0, 330.0),(100.0,300.0),(200.0,300.0),(200.0,330.0),(100.0,330.0)]
        beam = self.physicengine.add_poly(self.vertices)        
        self.beams.append(beam)

        

        self.Change = False
        self.GetInputfn = self.CommonGetInput
        #self.Movefn = self.CommonMove
        #self.CollisionDetectionfn = self.CommonCollisonDetection
        #self.Drawfn = self.CommonDraw
   
        
    
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
                if event.button == conf.INPUT_CONFIG.ZOOM_IN_MOUSE:
                    self.drawengine.zoom(conf.INPUT_CONFIG.DeltaZOOM_IN,event.pos)
                elif event.button == conf.INPUT_CONFIG.ZOOM_OUT_MOUSE:
                    self.drawengine.zoom(conf.INPUT_CONFIG.DeltaZOOM_OUT,event.pos)
                elif event.button == 1:
				    self.physicengine.add_ball(event.pos)
				    self.physicengine.add_poly(self.vertices2)
                else:
                    self.common_event(event)
            elif event.type == MOUSEMOTION:
                if event.buttons[2] == 1 or event.buttons[1] == 1:
                    self.drawengine.translate(event.rel)
                else:
                    self.common_event(event)
            elif event.type == KEYDOWN:
                if event.key == conf.INPUT_CONFIG.ZOOM_IN_KEY:
                    self.drawengine.zoom(conf.INPUT_CONFIG.DeltaZOOM_IN,event.pos)
                elif event.key == conf.INPUT_CONFIG.ZOOM_OUT_KEY:
                    self.drawengine.zoom(conf.INPUT_CONFIG.DeltaZOOM_OUT,event.pos)
                elif event.key == conf.INPUT_CONFIG.SIMULATE_ON_OFF:
                    self.physicengine.run_physics = not self.physicengine.run_physics
                elif event.key == conf.INPUT_CONFIG.START_TRAIN:
                    self.starttrain = True
                else:
                    self.common_event(event)
            else:
                self.common_event(event)

    def Changefn(self):
        if not self.Change:
            return
        self.logger.debug("Change:::")

    def run(self):
        """Main Game Loop"""
        while not self.quit:
            self.GetInputfn()
            #self.Movefn()
            #self.CollisionDetectionfn()
            #self.drawengine.common_draw(self.beams,self.walls)
            self.drawengine.screen.fill((255,255,255))
            self.drawengine.physicscreen.fill((70,70,70))
            self.physicengine.update(400, 1)
            
            self.physicengine.draw(self.drawengine.physicscreen)
            self.drawengine.drawphysic(self.drawengine.physicscreen)

            pygame.display.flip()
            
            pygame.display.set_caption("elements: %i | fps: %s" % 
                (self.physicengine.get_element_count(), 
                str(int(self.drawengine.clock.get_fps()))))

            

            #self.Changefn()
            
        pygame.quit()
