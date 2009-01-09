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
from os.path import isfile

###############################################################################
#############################Game Class Muhaha!################################
###############################################################################
class Game:
    def __init__(self):

        self.logger = logging.getLogger('GameLoop')
        self.logger.setLevel(conf.DEVELOPMENT.LOGGINGLEVEL)

        self.quit = False
        self.simulate = False
        self.drawbeam = False
        self.drawline = False

        #Draw Engine
        size = conf.SCREEN_CONFIG.SCREEN_W, conf.SCREEN_CONFIG.SCREEN_H
        zoom = conf.GAME_CONFIG.ZOOM_START
        xver = conf.GAME_CONFIG.XVERSCHIEBUNG
        yver = conf.GAME_CONFIG.YVERSCHIEBUNG
        self.drawengine = oBBDrawEngine.DrawEngine(size,zoom,xver,yver,self)
        self.drawengine.set_info("LMB: draw Beam\nRMB: move Background\n\
scrollupdown: zoom\nr: Runs simulation\n\
t: start train\ns: Screenshot\nh: toggle this help")
        

        ### Physics Engine
        self.physicengine = oBBPhysicEngine.PhysicEngine(conf.GAME_CONFIG.GRAVITY)
        #self.physicengine.set_info("Test")

        self.load_level_1()

        self.Change = False
        self.GetInputfn = self.CommonGetInput
        self.Drawfn = self.GameDraw
        self.Movefn = self.GameMove

    def clear(self):
        self.walls = []
        self.beams = []
        self.balls = []
        self.achsen = []
        self.catchpoints = []
        self.lastcatchpoint = None
        self.physicengine.clear()
        self.filecounter = 0
   
    def load_level_1(self):
        self.clear()
        wall = self.physicengine.add_wall((-10000.0, 50.0), (-50.0, 50.0))
        self.walls.append(wall)
        wall = self.physicengine.add_wall((-50.0, 50.0), (100.0, -100.0))
        self.walls.append(wall)
        wall = self.physicengine.add_wall((100.0, -100.0), (250.0, 50.0))
        self.walls.append(wall)
        wall = self.physicengine.add_wall((250.0, 50.0), (10000.0, 50.0))
        self.walls.append(wall)
        achse = self.physicengine.add_achse((-50.0, 50.0))
        self.achsen.append(achse)
        achse = self.physicengine.add_achse((250.0, 50.0))
        self.achsen.append(achse)
        achse = self.physicengine.add_achse((20.0, -20.0))
        self.achsen.append(achse)
        achse = self.physicengine.add_achse((180.0, -20.0))
        self.achsen.append(achse)

    
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
                    #ball = self.physicengine.add_ball(self.drawengine.position_to_pymunk(event.pos))
                    #self.balls.append(ball)
                    tmp = self.drawengine.over_achse(event.pos, self.achsen)
                    if tmp != None:
                        self.drawbeam = True
                        self.anpos = tmp.body.position
                        self.curachse = tmp
                else:
                    self.common_event(event)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1 and self.drawbeam:
                    endpos = self.drawengine.nearstpos(event.pos)
                    beam = self.physicengine.add_beam(self.anpos, endpos)
                    self.beams.append(beam)
                    self.physicengine.add_beam_to_achse(beam,self.curachse)
                    pyendpos = self.drawengine.position_to_pygame(Vec2d(endpos[0],endpos[1]))
                    tmp = self.drawengine.over_achse(pyendpos, self.achsen)
                    if tmp != None:
                        self.physicengine.add_beam_to_achse(beam,tmp)
                    else:
                        achse = self.physicengine.add_achse(endpos, False)
                        self.physicengine.add_beam_to_achse(beam,achse)
                        self.achsen.append(achse)
                    
                    self.drawbeam = False
                    self.drawline = False
                    
            elif event.type == MOUSEMOTION:
                if event.buttons[2] == 1 or event.buttons[1] == 1:
                    self.drawengine.translate(event.rel)
                elif event.buttons[0] == 1 and self.drawbeam:
                    pos = self.drawengine.nearstpos(event.pos)
                    self.drawline = True
                    self.endpos = pos
                    
                else:
                    tmp = self.drawengine.over_achse(event.pos, self.achsen)
                    if tmp != None:
                        if self.lastcatchpoint == None:
                            self.catchpoints.append(tmp)
                            self.lastcatchpoint = tmp
                    else:
                        if self.lastcatchpoint != None:
                            self.catchpoints.remove(self.lastcatchpoint)
                            self.lastcatchpoint = None
            elif event.type == KEYDOWN:
                if event.key == conf.INPUT_CONFIG.ZOOM_IN_KEY:
                    self.drawengine.zoom(conf.INPUT_CONFIG.DeltaZOOM_IN * 5,(0,0))
                elif event.key == conf.INPUT_CONFIG.ZOOM_OUT_KEY:
                    self.drawengine.zoom(conf.INPUT_CONFIG.DeltaZOOM_OUT * 5,(0,0))
                elif event.key == conf.INPUT_CONFIG.SIMULATE_ON_OFF:
                    self.physicengine.run_physics = not self.physicengine.run_physics
                elif event.key == conf.INPUT_CONFIG.START_TRAIN:
                    self.starttrain = True

                elif event.key == pygame.K_s:
                    self.screenshot("blatest")
                elif event.key == pygame.K_h:
                    self.drawengine.show_help = not self.drawengine.show_help
                else:
                    self.common_event(event)
            else:
                self.common_event(event)

    def screenshot(self, filename='screenshot', ext='png'):
            
        if filename[-4:-3] == ".": filename = filename[:-4]
        elif filename[-3:-2] == ".": filename = filename[:-3]

        fn = self.save_surface(self.drawengine.screen, "snapshots/%s" % filename, ext)
        self.logger.info("Saved as: %s" % fn)


    def save_surface(self, surface, fn='surface', ext='png'):

        fullname = None
        while fullname == None or isfile(fullname):
            self.filecounter += 1
            z = "0" * (5-len(str(self.filecounter)))
            fullname = "%s_%s%i.%s" % (fn, z, self.filecounter, ext)
            
        pygame.image.save(surface, fullname)
        return fullname


    def Changefn(self):
        if not self.Change:
            return
        self.logger.debug("Change:::")


    def GameDraw(self):
        self.drawengine.common_draw(self.beams,self.walls,self.balls, self.achsen)
        if self.lastcatchpoint != None:
            self.drawengine.draw_catchpoint(self.lastcatchpoint)  
        if self.drawline:
            self.drawengine.draw_line(self.anpos, self.endpos)
        pygame.display.set_caption("elements: %i | fps: %s" % 
                (self.physicengine.get_element_count(), 
                str(int(self.drawengine.clock.get_fps()))))
        self.drawengine.flip() 

    def GameMove(self):
        self.physicengine.update(conf.SCREEN_CONFIG.FRAMERATE, conf.GAME_CONFIG.PYMUNK_STEPS)

    def run(self):
        """Main Game Loop"""
        while not self.quit:
            self.GetInputfn()
            self.Drawfn()
            self.Movefn()
            self.Changefn()
            
        pygame.quit()
