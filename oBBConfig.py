# Filename: oBBConfig.py
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
import logging

class SCREEN_CONFIG:
    SCREEN_W        =   640
    SCREEN_H        =   480
    FULLSCREEN      =   False
    FRAMERATE       =   60

class GAME_CONFIG:
    SPEED           =   1.0
    ZOOM_START      =   1.0
    XVERSCHIEBUNG   =   320
    YVERSCHIEBUNG   =   300
    PYMUNK_STEPS    =   5
    GRAVITY         =   (0.0, -900.0)
    PYMUNK_topleft       =   -10000, -10000
    PYMUNK_bottomright   =   10000, 100000
    

class INPUT_CONFIG:
    ZOOM_IN_MOUSE   =   4 #scroll up
    ZOOM_OUT_MOUSE  =   5 #scroll down

    ZOOM_IN_KEY     = pygame.K_PLUS
    ZOOM_OUT_KEY    = pygame.K_MINUS

    DeltaZOOM_IN    = 0.05
    DeltaZOOM_OUT   = -0.05

    SIMULATE_ON_OFF = pygame.K_r
    START_TRAIN     = pygame.K_t

class DEVELOPMENT:
    LOGGINGLEVEL = logging.DEBUG



