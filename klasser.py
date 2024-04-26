# -*- coding: utf-8 -*-
# klasser.py - Fil som inneholder klassene som tas i bruk i spillet

import pygame as pg
import random as rd
import math as m

# Matklasse
class Mat:
    # Klasse for å lage matobjekter
    
    def __init__(self, x: int, y: int, radius: int, vindusobjekt):
        '''
            Konstruktør
            
            @param x (int), @param y (int): x- og y-koordinater
            @param radius (int): radius til maten
            @param vindusobjekt: vindusobjekt hvor maten skal tegnes
        '''
        self.x = x
        self.y = y
        self.radius = radius
        self.vindusobjekt = vindusobjekt
        
    def tegn(self):
        # Funksjon som tegner maten
        
        pg.draw.circle(self.vindusobjekt, (0,100,0), (self.x, self.y), self.radius)


# Spillerklasse
class Spiller:
    # Klasse for å lage spillerobjekter
    
    def __init__(self, x: int, y: int, radius: int, fart: int, taster: list, altTaster: list, vindu, farge: tuple=(0, 0, 0)):
        '''
            Konstruktør
            
            @ param x, y, radius, fart: Koordinater, radius til spilleren og farten til spilleren
            @param taster (list): Liste med taster for å bevege spilleren
            @param altTaster (list): Liste med alternative taster for å bevege spilleren
            @param vindu: Vindusobjekt
            @param farge (tuple): Farge til spilleren (Satt til svart som standard)
            
        '''
        self.x = x
        self.y = y
        self.radius = radius
        self.fart = fart
        self.taster = taster
        self.altTaster = altTaster
        self.vindu = vindu
        self.farge = farge
        self.retning = 0


    def flytt(self):
        # Funksjon som flytter spilleren basert på tastetrykk
        
        trykkede_taster = pg.key.get_pressed()

        # Flytt mot venstre
        if trykkede_taster[self.taster[2]] or trykkede_taster[self.altTaster[2]]:
            self.retning = 2
            self.x -= self.fart
            if ((self.x - self.radius) < 0):
                self.x += self.fart
                self.retning = 3

        # Flytt mot høyre
        if trykkede_taster[self.taster[3]] or trykkede_taster[self.altTaster[3]]:
            self.retning = 3
            self.x += self.fart    
            if ((self.x + self.radius) >= self.vindu.get_width()):
                self.x -= self.fart
                self.retning = 2

        # Flytt opp
        if trykkede_taster[self.taster[0]] or trykkede_taster[self.altTaster[0]]:
            self.retning = 0
            self.y -= self.fart
            if ((self.y - self.radius) < 0):
                self.y += self.fart
                self.retning = 1

        # Flytt ned
        if trykkede_taster[self.taster[1]] or trykkede_taster[self.altTaster[1]]:
            self.retning = 1
            self.y += self.fart
            if ((self.y + self.radius) >= self.vindu.get_height()):
                self.y -= self.fart
                self.retning = 0

        

    def tegn(self):
        # Funksjon som tegner spilleren og armene hans i riktig retning
        
        if self.retning == 0: # Opp
            pg.draw.circle(self.vindu, self.farge, (self.x, self.y), self.radius)
            pg.draw.circle(self.vindu, self.farge, (self.x+self.radius, self.y-self.radius), self.radius//4)
            pg.draw.circle(self.vindu, self.farge, (self.x-self.radius, self.y-self.radius), self.radius//4)
        elif self.retning == 1: # Ned
            pg.draw.circle(self.vindu, self.farge, (self.x, self.y), self.radius)
            pg.draw.circle(self.vindu, self.farge, (self.x+self.radius, self.y+self.radius), self.radius//4)
            pg.draw.circle(self.vindu, self.farge, (self.x-self.radius, self.y+self.radius), self.radius//4)
        elif self.retning == 2: # Venstre
            pg.draw.circle(self.vindu, self.farge, (self.x, self.y), self.radius)
            pg.draw.circle(self.vindu, self.farge, (self.x-self.radius, self.y-self.radius), self.radius//4)
            pg.draw.circle(self.vindu, self.farge, (self.x-self.radius, self.y+self.radius), self.radius//4)
        elif self.retning == 3:   # Høyre
            pg.draw.circle(self.vindu, self.farge, (self.x, self.y), self.radius)
            pg.draw.circle(self.vindu, self.farge, (self.x+self.radius, self.y-self.radius), self.radius//4)
            pg.draw.circle(self.vindu, self.farge, (self.x+self.radius, self.y+self.radius), self.radius//4)


# Maurklasse
class Maur:
    # Klasse for å lage maurobjekter
    def __init__(self, x: int, y: int, vinkel: int, fart: int, radius: int, vindusobjekt):
        '''
            Konstruktør for Maur-klassen
            
            @param x (int): x-koordinatet til mauren
            @param y (int): y-koordinatet til mauren
            @param vinkel (int): Startvinkelen til mauren, angitt i grader
            @param fart (int): Farten til mauren
            @param radius (int): Radiusen til mauren
            @param vindusobjekt: Vindusobjektet som mauren skal tegnes på
        '''
        
        self.x = x
        self.y = y
        self.vinkel = vinkel
        self.fart = fart
        self.dx = m.cos(m.radians(self.vinkel))*self.fart
        self.dy = -m.sin(m.radians(self.vinkel))*self.fart
        self.radius = radius
        self.midRadius = round(self.radius*0.8)
        self.vindusobjekt = vindusobjekt
        self.harMat = False

        
    def tegn(self):
        # Tegner mauren på skjermen
        # Hvis mauren har mat, tegnes en ekstra sirkel for å vise dette
        
        pg.draw.circle(self.vindusobjekt, (0, 0, 0), (self.x, self.y), self.radius)
        pg.draw.circle(self.vindusobjekt, (0, 0, 0), (self.x+((self.dx/self.fart)*self.radius), self.y+((self.dy/self.fart)*self.radius)), self.midRadius)
        pg.draw.circle(self.vindusobjekt, (0, 0, 0), (self.x+2*((self.dx/self.fart)*self.radius), self.y+2*((self.dy/self.fart)*self.radius)), self.radius)
        if self.harMat == True:
            pg.draw.circle(self.vindusobjekt, (0, 100, 0), (self.x+3*((self.dx/self.fart)*self.radius), self.y+3*((self.dy/self.fart)*self.radius)), self.radius+2)

        
    
    def flytt(self, vandingsGrad: float):
        # Flytter mauren
        # Kollisjon med kanten av vinduet håndteres også, og hvis mauren har mat, beveger den seg annerledes.
        # Vandingsgrad er en verdi som bestemmer hvor mye vinkelen endrer seg med tilfedig
        
        vEndring = rd.uniform(-3*vandingsGrad, 3*vandingsGrad)
        self.vinkel += vEndring
        
        # Oppdaterer dekomponert Fartsvektor med ny vinkel
        self.dx = m.cos(m.radians(self.vinkel)) * self.fart
        self.dy = -round(m.sin(m.radians(self.vinkel)),4) * self.fart
        
        
        # Sjekk kollisjon med kant
        if (self.x + self.radius) + self.dx >= self.vindusobjekt.get_width():
            self.x = self.vindusobjekt.get_width() - self.radius
            self.vinkel = 180 - self.vinkel
        elif (self.x - self.radius) + self.dx <= 0:
            self.x = self.radius
            self.vinkel = 180 - self.vinkel

        if (self.y + self.radius) + self.dy >= self.vindusobjekt.get_height():
            self.y = self.vindusobjekt.get_height() - self.radius
            self.vinkel = -self.vinkel
        elif (self.y - self.radius) + self.dy <= 0:
            self.y = self.radius
            self.vinkel = -self.vinkel
    
        # Flytt    
        self.x += self.dx
        self.y += self.dy
        

class simMaur(Maur):
    # Klasse som arver fra Maur klassene og funksjonene er like bortsett fra gaMot()
    
    def __init__(self, x, y, vinkel, fart, radius, vindusobjekt):
        super().__init__(x, y, vinkel, fart, radius, vindusobjekt)

    def tegn(self):
        return super().tegn()

    def flytt(self, vandingsGrad: float):
        return super().flytt(vandingsGrad)

    def gaMot(self, x: int, y: int):
        '''
            Funksjon som finner vinkelen til en annen posisjon
            og får mauren til å go dit
            
            @param x (int): x-koordinat til annen posisjon
            @param y (int): y-koordinat til annen posisjon
        '''
        posX = x
        posY = y
        vinkel = m.atan2(posX-self.x, posY-self.y) # Finner vikel i radianer
        vinkel = m.degrees(vinkel)-90
        self.vinkel = vinkel
        
        # Oppdaterer Fartsvektor med ny vinkel
        self.dx = m.cos(m.radians(self.vinkel)) * self.fart
        self.dy = -round(m.sin(m.radians(self.vinkel)),4) * self.fart
        
        # Flytt    
        self.x += self.dx
        self.y += self.dy