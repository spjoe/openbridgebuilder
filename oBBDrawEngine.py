# Filename: oBBGDrawEngine.py
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
import math, sys, random
import logging
import oBBConfig as conf
from pymunk import Vec2d


class DrawEngine:
    def __init__(self, screen_size, zoomfactor,xverschiebung,yverschiebung, game ):

        self.logger = logging.getLogger('DrawEngine')
        self.logger.setLevel(conf.DEVELOPMENT.LOGGINGLEVEL)
        
        self.zoomfactor = zoomfactor

        self.xverschiebung = xverschiebung
        self.yverschiebung = yverschiebung

        self.game = game
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]

        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.background = pygame.Surface(screen_size).convert()
        self.background.fill([80,80,80])
        self.screen.blit(self.background, self.background.get_rect())

        self.clock = pygame.time.Clock()
        self.show_help = True

        self.font = pygame.font.Font(None, 32)
        self.font_xxl = pygame.font.Font(None, 38)
    
        

        self.rects = []

    def translate(self,rel):
        self.xverschiebung += rel[0] 
        self.yverschiebung += rel[1] 

    def zoom(self, delta, pos):
        if delta < 0 and self.zoomfactor <= 0.4:
            return
        self.zoomfactor += delta  

    def clear(self):
        self.screen.fill([0,0,0])
        self.flip()

    def set_info(self, txt):
        """ Create the Surface for the Infotext at the Upper Left Corner 
            Parameter: txt == str()
        """
        txt = txt.splitlines()
        self.infostr_surface = pygame.Surface((500, 800))
        self.infostr_surface.fill((255,255,255))
        self.infostr_surface.set_colorkey((255,255,255))
        
        y = 0
        for line in txt:
            if len(line.strip()) == 0:
                y += 16
            else:
                text = self.font.render(line, 1,THECOLORS["black"])
                self.infostr_surface.blit(text, (0,y))
                y += 26

    def draw_catchpoint(self,catchpoint):
        # Get Ball Infos
        r = 10 * self.zoomfactor
        p = self.position_to_pygame(catchpoint.body.position)

        self.rects.append(pygame.draw.circle(self.screen, (0,0,255), p, int(r), 3))
    def draw_line(self, pos1, pos2):
        posf = self.position_to_pygame(Pos(pos1[0],pos1[1]))
        poss = self.position_to_pygame(Pos(pos2[0],pos2[1]))
        self.rects.append(pygame.draw.line(self.screen,(0,255,0),posf,poss,1))

    def draw_balls(self, balls, width=3):
        for shape in balls:
            # Get Ball Infos
            r = shape.radius * self.zoomfactor
            p = self.position_to_pygame(shape.body.position)
            rot = shape.body.rotation_vector
        
            # Draw Ball
            #p = int(), int(self.flipy(v.y))
            self.rects.append(pygame.draw.circle(self.screen, shape.color, p, int(r), width))
    
            # Draw Rotation Vector
            p2 = Vec2d(rot.x, -rot.y) * r * 0.9
            pygame.draw.aaline(self.screen, shape.color2, p, p+p2, 2)

    def position_to_pygame(self,p):
        """Small hack to convert pymunk to pygame coordinates"""
        return int(p.x * self.zoomfactor + self.xverschiebung), int(-p.y * self.zoomfactor + self.screen_height + self.yverschiebung)

    def points_to_pygame(self,points):
        newpoints = []
        for p in points:
            pos = Pos(p[0],p[1])
            newpoint = self.position_to_pygame(pos)
            newpoints.append(newpoint)
        return newpoints

    def position_to_pymunk(self,pos):
        x = (pos[0] - self.xverschiebung) / self.zoomfactor
        y = -((pos[1] - self.yverschiebung - self.screen_height) / self.zoomfactor)
        return x,y #+ self.screen_height

    def draw_physic_poly(self,points,color):
        newpoints = self.points_to_pygame(points)
        self.rects.append(pygame.draw.polygon(self.screen, color,points ))

    def draw_physic_beams(self, beams):
        for beam in beams:            points = self.points_to_pygame(beam.get_points())
            self.draw_physic_poly(points,(0,255,0))
            #self.logger.debug(points)

    def draw_grid(self):
        
        for i in range(-10000,10000,100):
            pX = self.xverschiebung + i * self.zoomfactor
            if pX > 0 and pX < conf.SCREEN_CONFIG.SCREEN_W:
                width = 2
                if i == 0: width = 4
                self.rects.append(pygame.draw.line(self.screen, \
                                (0,0,0), \
                                (pX,0),(pX,conf.SCREEN_CONFIG.SCREEN_H),width ))

        for i in range(-10000,10000,100):
            pY = int(i * self.zoomfactor  + self.screen_height + self.yverschiebung)
            if pY > 0 and pY < conf.SCREEN_CONFIG.SCREEN_H:
                width = 2
                if i == 0: width = 4
                self.rects.append(pygame.draw.line(self.screen, \
                                (0,0,0), \
                                (0,pY),(conf.SCREEN_CONFIG.SCREEN_W,pY),width ))

        for i in range(-10000,10000,10):
            pX = self.xverschiebung + i * self.zoomfactor
            if pX > 0 and pX < conf.SCREEN_CONFIG.SCREEN_W:
                self.rects.append(pygame.draw.line(self.screen, \
                                (0,0,0), \
                                (pX,0),(pX,conf.SCREEN_CONFIG.SCREEN_H),1 ))

        for i in range(-10000,10000,10):
            pY = int(i * self.zoomfactor + self.screen_height  + self.yverschiebung)
            if pY > 0 and pY < conf.SCREEN_CONFIG.SCREEN_H:
                self.rects.append(pygame.draw.line(self.screen, \
                                (0,0,0), \
                                (0,pY),(conf.SCREEN_CONFIG.SCREEN_W,pY),1 ))


    def draw_physic_static(self, static_lines):
        for line in static_lines:
                body = line.body
                pv1 = body.position + line.a.rotated(math.degrees(body.angle))
                pv2 = body.position + line.b.rotated(math.degrees(body.angle))
                p1 = self.position_to_pygame(pv1)
                p2 = self.position_to_pygame(pv2)
                
                self.rects.append(pygame.draw.lines(self.screen, THECOLORS["lightgray"], False, [p1,p2],3))

    def clear_rects(self, rects):
        for rect in rects:
            self.screen.blit(self.background,rect,rect)
    
    def nearstpos(self,pos):
        pymunkpos = self.position_to_pymunk(pos)
        divx,restx = divmod(pymunkpos[0] , 10)
        divy,resty = divmod(pymunkpos[1] , 10)
        x = 0
        y = 0
        if restx < 5:
            x = divx * 10
        else:
            x = (divx + 1) * 10

        if resty < 5:
            y = divy * 10
        else:
            y = (divy + 1) * 10

        return x,y#self.position_to_pygame(Pos(x,y))

    def drawphysic(self,surface):
        ns = pygame.transform.scale(surface,\
                (conf.GAME_CONFIG.PYMUNK_SIZEX*self.zoomfactor,\
                conf.GAME_CONFIG.PYMUNK_SIZEY*self.zoomfactor))
        self.screen.blit(ns, (self.xverschiebung,self.yverschiebung))

    def common_draw(self,beams,static,balls,achsen):
        self.clear_rects(self.rects)
        self.rects = []
        self.draw_grid()
        self.draw_physic_beams(beams)
        self.draw_physic_static(static)
        self.draw_balls(balls)
        self.draw_balls(achsen, 0)
        if self.show_help:
            self.rects.append(self.screen.blit(self.infostr_surface, (10,10)))

    def over_achse(self,pos,achsen):
        for achse in achsen:
            matchpos = self.position_to_pygame(achse.body.position)
            if  matchpos[0] + 15 > pos[0] and \
                matchpos[1] + 15 > pos[1] and \
                matchpos[0] - 15 < pos[0] and \
                matchpos[1] - 15 < pos[1]:
                return achse

        return None
        
    def flip(self):
        self.clock.tick(conf.SCREEN_CONFIG.FRAMERATE)
        pygame.display.flip()
        
class Pos:
    def __init__(self,x,y):
        self.x = x
        self.y = y
