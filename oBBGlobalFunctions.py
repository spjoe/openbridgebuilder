# Filename: oBBGlobalFunctions.py
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
import pymunk as pm
import sys
import os

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
