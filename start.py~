#!/usr/bin/env python
# Filename: start.py
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
import sys
import os
import logging

from pygame.locals import *

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
        self.zoomchanged = True
        self.zoompoint = 0, 0
        self.InZoom = False
        self.gravity = 9.80665
        self.c_rect = None
        self.t_rect = None

        self.catchpoint = (0,0)
        self.endcatchpoint = (0,0)
        self.drawcatchpoint = False
        self.colorcatchpoint = (0,0,0)
        self.buttondown = False

        self.simulatemode = 0

        pygame.init()

        if not pygame.font: 
            logger.warning( 'fonts disabled' )
        if not pygame.mixer: 
            logger.warning( 'sound disabled' )

        size = Game.SCREEN_W, Game.SCREEN_H
        #self.window = pygame.display.set_mode(size, pygame.FULLSCREEN)
        self.window = pygame.display.set_mode(size)
        pygame.display.set_caption('Open Bridge Builder') 
        self.screen = pygame.display.get_surface()

        self.background = pygame.Surface(size).convert()
        self.backgroundgrid = BackgroundGrid()

        self.clock = pygame.time.Clock()

        # Set Start Funktions #
        self.Change = False
        self.GetInputfn = self.CommonGetInput
        self.Movefn = self.CommonMove
        self.CollisionDetectionfn = self.CommonCollisonDetection
        self.Drawfn = self.CommonDraw
       
        # Set Test Sprite #
        self.allSprites = pygame.sprite.Group()
        self.testtraeger = Traeger(self,2 , 2, 3, 3)
        test2 = Traeger(self,5 , 1, 8, 1)
        test3 = Traeger(self,5 , 1, 5, 5)
        test4 = Traeger(self,8 , 1, 8, 5)
        test5 = Traeger(self,5 , 5, 8, 5)
        test6 = Traeger(self,5 , 5, 8, 1)
        test7 = Traeger(self,5,  1, 8, 5)
        self.allSprites.add(self.testtraeger)
        self.allSprites.add(test2)
        self.allSprites.add(test3)
        self.allSprites.add(test4)
        self.allSprites.add(test5)
        self.allSprites.add(test6)
        self.allSprites.add(test7)
        self.isDirtyGroup = pygame.sprite.Group()
        self.isVisibleGroup = pygame.sprite.Group()
 
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
                elif event.button == 1:
                    if self.drawcatchpoint == True:
                        self.traegerpos = self.catchpoint
                        self.begintraeger = True
                else:
                    self.common_event(event)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if self.begintraeger == True:
                        self.buttondown = False
                        self.allSprites.add(Traeger(self,self.upos[0] , self.upos[1], self.endupos[0], self.endupos[1]))
                else:
                    self.common_event(event)
                
            elif event.type == MOUSEMOTION:
                if event.buttons[2] == 1 or event.buttons[1]:
                    self.backgroundgrid.translate(event.rel)
                    self.zoomchanged = True
                elif event.buttons[0] == 1:
                    tmp = self.backgroundgrid.InGridCatch(event.pos)
                    isIn = tmp[0]
                    pos = tmp[1]
                    col = tmp[2]
                    upos = tmp[3]
                    if isIn == True and self.begintraeger == True:
                        self.endcatchpoint = pos
                        self.drawcatchpoint = True
                        self.colorcatchpoint = col
                        self.endupos = upos
                        self.buttondown = True
                    else:
                        self.drawcatchpoint = False
                else:
                    tmp = self.backgroundgrid.InGridCatch(event.pos)
                    isIn = tmp[0]
                    pos = tmp[1]
                    col = tmp[2]
                    upos = tmp[3]
                    if isIn == True:
                        self.catchpoint = pos
                        self.drawcatchpoint = True
                        self.colorcatchpoint = col
                        self.upos = upos
                    else:
                        self.drawcatchpoint = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.simulatemode = ~self.simulatemode
                    self.logger.debug(self.simulatemode)
                else:
                    self.common_event(event)
            else:
                self.common_event(event)
    
    def CommonMove(self): 
        self.allSprites.update()          

    def CommonCollisonDetection(self):
        pass

    def CommonDraw(self):
        if self.zoomchanged == True:
            self.background.fill((0,0,0))
            self.background.blit(self.backgroundgrid\
                                     .getGrid(self.zoomfactor, \
                                              self.zoompoint , \
                                              self.InZoom),[0,0])
            self.screen.blit(self.background,[0,0])
            self.allSprites.draw(self.screen)
            self.zoomchanged = False
            self.InZoom = False
        else:

            if self.c_rect != None:
                self.screen.blit(self.background, self.c_rect, self.c_rect)
            if self.t_rect != None:
                self.screen.blit(self.background, self.t_rect, self.t_rect)

            if self.buttondown == True:
                self.t_rect = pygame.draw.line(self.screen, (0,255,0), self.catchpoint,self.endcatchpoint)
            if self.drawcatchpoint == True:
                self.c_rect = pygame.draw.circle(self.screen, self.colorcatchpoint , self.catchpoint, 4 * self.zoomfactor)

            self.allSprites.clear(self.screen, self.background)
            self.allSprites.draw(self.screen)# sollte mit dirty sein
           
        pygame.display.flip()


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

###############################################################################
############################Background Grid####################################
###############################################################################
class BackgroundGrid:
    UNITS_X = 100
    UNITS_Y = 50    
    
    pUNITSIZE_X = 50
    pUNITSIZE_Y = 50

    COLOR = 130, 130, 130
    COLOR_SMALL = 70,70,70

    def __init__(self):
        self.pfirstBendx = -400
        self.pfirstBendy = -200 #p for Pixel u for Unit
        self.zoomfactor = 1.00
        self.zoompoint = 0,0
        self.backgroundgrid = pygame.Surface((Game.SCREEN_W, Game.SCREEN_H))\
                                    .convert()

    def translate(self, tr):
        self.pfirstBendx += tr[0]
        self.pfirstBendy += tr[1]
        
    def getGrid(self, zoomfactor, zoompoint, InZoom ):
        self.zoomfactor = zoomfactor
        self.zoompoint = zoompoint
        self.pzoompointX = self.zoompoint[0]
        self.pzoompointY = self.zoompoint[1]
        if InZoom == True:
            tmpzoom = self.zoomfactor - 0.05
        else:
            tmpzoom = self.zoomfactor
        pDX = -self.pfirstBendx + self.pzoompointX
        self.uzoompointX = pDX / (BackgroundGrid.pUNITSIZE_X * tmpzoom)
        pDY = -self.pfirstBendy + self.pzoompointY
        self.uzoompointY = pDY / (BackgroundGrid.pUNITSIZE_Y * tmpzoom)

        logging.debug(self.uzoompointX)
        logging.debug(self.uzoompointY)


        if InZoom == True:
            self.pfirstBendx = self.pzoompointX - (pDX + pDX * 0.05)
            self.pfirstBendy = self.pzoompointY - (pDY + pDY * 0.05)
        #else:
        #    self.pfirstBendx = self.pzoompointX - (pDX - pDX * 0.025)
        #    self.pfirstBendy = self.pzoompointY - (pDY - pDY * 0.025)


        self.backgroundgrid = pygame.Surface((Game.SCREEN_W, Game.SCREEN_H))\
                                    .convert()

        for i in range(0,BackgroundGrid.UNITS_X):
            pX = self.pfirstBendx + i * BackgroundGrid.pUNITSIZE_X * zoomfactor
            if pX > 0 and pX < Game.SCREEN_W:
                pygame.draw.line(self.backgroundgrid, \
                                BackgroundGrid.COLOR, \
                                (pX,0),(pX,Game.SCREEN_H),2 )
                for j in range (1, 5, 1):
                    X = pX - j * 0.2 * BackgroundGrid.pUNITSIZE_X * zoomfactor
                    pygame.draw.line(self.backgroundgrid, \
                                    BackgroundGrid.COLOR_SMALL, \
                                    (X ,0),(X,Game.SCREEN_H),1 )

        for i in range(0,BackgroundGrid.UNITS_Y):
            pY = self.pfirstBendy + i * BackgroundGrid.pUNITSIZE_Y * zoomfactor
            if pY > 0 and pY < Game.SCREEN_H:
                pygame.draw.line(self.backgroundgrid, \
                                BackgroundGrid.COLOR, \
                                (0,pY),(Game.SCREEN_W,pY),2 )
                for j in range (1, 5, 1):
                    Y = pY - j * 0.2 * BackgroundGrid.pUNITSIZE_Y * zoomfactor
                    pygame.draw.line(self.backgroundgrid, \
                                    BackgroundGrid.COLOR_SMALL, \
                                    (0,Y),(Game.SCREEN_W,Y),1 )

        return self.backgroundgrid
        
    def GetBeamRect(self, t):
        tmp_rect = t.rect
        tmp_rect.topleft =  self.pfirstBendx \
                              + min(t.ustartx, t.uendx) \
                              * BackgroundGrid.pUNITSIZE_X \
                              * self.zoomfactor \
                          , self.pfirstBendy  \
                              + min(t.ustarty, t.uendy) \
                              * BackgroundGrid.pUNITSIZE_Y \
                              * self.zoomfactor

        tmp_rect.width = t.uwidth \
                         * BackgroundGrid.pUNITSIZE_X \
                         * self.zoomfactor
        tmp_rect.height = t.uheight \
                          * self.zoomfactor
        return tmp_rect
    

    def GetImage(self,t):

        if t.uwidth == 0:
            image = pygame\
                .Surface([Traeger.T_HEIGHT * t.game.zoomfactor \
                          , t.uheight * BackgroundGrid.pUNITSIZE_Y * t.game.zoomfactor]) \
                .convert()
            image.fill((0,255,0))
            return image

        if t.uheight == 0:
            image = pygame\
                .Surface([t.uwidth * BackgroundGrid.pUNITSIZE_X * t.game.zoomfactor \
                          , Traeger.T_HEIGHT * t.game.zoomfactor]) \
                .convert()
            image.fill((0,255,0))
            return image
            
        image = pygame\
            .Surface([t.uwidth * BackgroundGrid.pUNITSIZE_X * t.game.zoomfactor \
                      , t.uheight * BackgroundGrid.pUNITSIZE_Y * t.game.zoomfactor]) \
            .convert()
        image.set_colorkey((0,0,0))
        image.fill((0,0,0))

        if(t.ustartx < t.uendx and t.ustarty < t.uendy) or (t.ustartx > t.uendx and t.ustarty > t.uendy):
            pygame.draw.line(image, (0,255,0) ,(0,0),(image.get_rect().width, image.get_rect().height), 5)
        else:
            pygame.draw.line(image, (0,255,0) ,(0,image.get_rect().height),(image.get_rect().width,0 ), 5)

        return image
        

    def InGridCatch(self,ppos):
        pposX = ppos[0]
        pposY = ppos[1]
        pDX = -self.pfirstBendx + pposX
        uposX = pDX / (BackgroundGrid.pUNITSIZE_X * self.zoomfactor)
        pDY = -self.pfirstBendy + pposY
        uposY = pDY / (BackgroundGrid.pUNITSIZE_Y * self.zoomfactor)
        
        ruposX = round(uposX,0)
        ruposY = round(uposY,0)
        ret = (False,(0,0),(0,0,0), (0,0))
        if (ruposX + 0.1) > uposX and (ruposX - 0.1) < uposX and (ruposY + 0.1) > uposY and (ruposY - 0.1) < uposY:
            pX = self.pfirstBendx + ruposX * BackgroundGrid.pUNITSIZE_X * self.zoomfactor
            pY = self.pfirstBendy + ruposY * BackgroundGrid.pUNITSIZE_Y * self.zoomfactor
            ret = (True,(pX,pY),(255,0,0), (ruposX,ruposY))
            return ret
        for i in range(-2,3):
            for j in range(-2,3):
                if (ruposX + (i * 0.2) + 0.05) > uposX \
                    and (ruposX + (i * 0.2) - 0.05) < uposX \
                    and (ruposY + (j * 0.2) + 0.05) > uposY \
                    and (ruposY + (j * 0.2) - 0.05) < uposY:
                    pX = self.pfirstBendx + (ruposX + i * 0.2) * BackgroundGrid.pUNITSIZE_X * self.zoomfactor
                    pY = self.pfirstBendy + (ruposY + j * 0.2) * BackgroundGrid.pUNITSIZE_Y * self.zoomfactor
                    ret = (True,(pX,pY),(0,255,0),(ruposX + i * 0.2,ruposY + j * 0.2))
                    break

        return ret

         
        
        
###############################################################################
################################Traeger########################################
###############################################################################
class Traeger(pygame.sprite.DirtySprite):

    T_HEIGHT = 5

    def __init__(self, game, ustartx, ustarty,  uendx, uendy):
        pygame.sprite.DirtySprite.__init__(self)


        self.game = game

        self.ustartx = ustartx
        self.ustarty = ustarty
        self.uendx = uendx
        self.uendy = uendy
        self.uwidth = abs ( max(ustartx,uendx) - min(ustartx, uendx) )
        self.uheight = abs ( max(ustarty,uendy) - min(ustarty, uendy) )
        self.image = game.backgroundgrid.GetImage(self)
        
        self.rect = self.image.get_rect()
        self.rect = game.backgroundgrid.GetBeamRect(self)

        self.drehimpuls = 0
        self.geschwindigkeitvektor = (0,0)

        game.logger.debug(self.image)
        game.logger.debug(self.rect)
        
        
    
    def update(self):
        pass
        #self.y += 0.02

        #if self.y > Game.SCREEN_H:
        #    self.y = 0

        tmp_r = self.rect
        
        self.image = game.backgroundgrid.GetImage(self)
        self.rect = game.backgroundgrid.GetBeamRect(self)
        #self.game.logger.debug(self.image)
        #self.game.logger.debug(self.rect)
        if(tmp_r != self.rect):
            self.game.logger.debug(self.image)
            self.game.logger.debug(self.rect)

        if self.game.simulatemode != 0:
            #self.game.logger.debug("test")
            self.ustarty += 0.1
            self.uendy += 0.1

        #self.game.isDirtyGroup.add(self)

        #self.game.logger.debug(self.rect.width)

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
