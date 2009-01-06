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
        self.background.fill([255,255,255])
        self.physicscreen = pygame.Surface((conf.GAME_CONFIG.PYMUNK_SIZEX,conf.GAME_CONFIG.PYMUNK_SIZEY)).convert()

        self.clock = pygame.time.Clock()

        self.rects = []

    def translate(self,rel):
        self.xverschiebung += rel[0]
        self.yverschiebung += rel[1]

    def zoom(self, delta, pos):
        self.zoomfactor += delta   

    def clear(self):
        self.screen.fill([0,0,0])
        self.flip()

    def position_to_pygame(self,p):
        """Small hack to convert pymunk to pygame coordinates"""
        return int(p.x * self.zoomfactor + self.xverschiebung), int(p.y * self.zoomfactor + self.yverschiebung)

    def points_to_pygame(self,points):
        newpoints = []
        for p in points:
            pos = Pos(p[0],p[1])
            newpoint = self.position_to_pygame(pos)
            newpoints.append(newpoint)
        return newpoints

    def draw_physic_poly(self,points,color):
        newpoints = self.points_to_pygame(points)
        self.rects.append(pygame.draw.polygon(self.screen, color,points ))

    def draw_physic_beams(self, beams):
        for beam in beams:            points = self.points_to_pygame(beam.get_points())
            self.draw_physic_poly(points,(0,255,0))
            self.logger.debug(points)

    def draw_physic_static(self, static_lines):
        for line in static_lines:
                body = line.body
                pv1 = body.position + line.a.rotated(math.degrees(body.angle))
                pv2 = body.position + line.b.rotated(math.degrees(body.angle))
                p1 = self.position_to_pygame(pv1)
                p2 = self.position_to_pygame(pv2)
                
                self.rects.append(pygame.draw.lines(self.screen, THECOLORS["lightgray"], False, [p1,p2]))

    def clear_rects(self, rects):
        for rect in rects:
            self.screen.blit(self.background,rect,rect)

    def drawphysic(self,surface):
        ns = pygame.transform.scale(surface,\
                (conf.GAME_CONFIG.PYMUNK_SIZEX*self.zoomfactor,\
                conf.GAME_CONFIG.PYMUNK_SIZEY*self.zoomfactor))
        self.screen.blit(ns, (self.xverschiebung,self.yverschiebung))

    def common_draw(self,beams,static):
        self.clear_rects(self.rects)
        self.rects = []
        #self.draw_physic_beams(beams)
        #self.draw_physic_static(static)
        self.clock.tick(conf.SCREEN_CONFIG.FRAMERATE)
    def flip(self):
        pygame.display.flip()
        
class Pos:
    def __init__(self,x,y):
        self.x = x
        self.y = y
