# -*- coding: utf-8 -*-
# unngaMaurSpill.py - Spill hvor man skal komme til mål uten å treffe maurene

import pygame as pg
from klasser import Spiller, Maur
from elementer import Knapp, ErRekord
import math as m
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d)


def finnAvstand(k1: tuple, k2: tuple):
    '''
        Funksjon for å finne avstand mellom to posisjoner på formen (x, y)
        @param k1 (tuple): Første koordinat
        @param k2 (tuple): Andre koordinat
    '''

    xAvstand2 = (k1[0] - k2[0])**2  # x-avstand^2
    yAvstand2 = (k1[1] - k2[1])**2  # y-avstand^2
    avstand = m.sqrt(xAvstand2 + yAvstand2)
    return avstand

def lagMaur(antall: int, vindusobjekt, x: int, y: int, fart: int = 1, radius: int = 5):
    '''
        Lager en liste med maurobjekter og returnerer denne listen

        @param antall (int): Antall maurobjekter som skal opprettes
        @param vindusobjekt: Vindusobjektet der maurene skal tegnes
        @param x (int): x-koordinatet der maurene skal plasseres
        @param y (int): y-koordinatet der maurene skal plasseres
        @param fart (int): Farten til maurene (standardverdi: 1)
        @param radius (int): Radiusen til maurene (standardverdi: 5)

        @return maurListe (list): En liste med maurobjekter opprettet med angitte parametere
    '''
    
    gradEndring = 360/antall
    maurListe = []
    
    for i in range(antall):
        maur = Maur(x, y, i*gradEndring, fart, radius, vindusobjekt)
        maurListe.append(maur)
        
    return maurListe


def unngaHoved(menyCallback, rundetall: int):
    # Hovedfunksjonen til spillet
    # Kjøres med et rundetall som blant annet bestemmer vanskelighetsgrad
    #
    # @param rundetall (int): Hvilken runde spilleren er på
     
    pg.init()
    pg.font.init()
    menyType = "spill"

    bevTaster = [K_UP, K_DOWN, K_LEFT, K_RIGHT]
    altBevTaster = [K_w, K_s, K_a, K_d]

    litenFont = pg.font.SysFont('Comic Sans MS', 30)

    storForhold = [1920, 1080]
    vindu = pg.display.set_mode(storForhold, pg.FULLSCREEN)
    vinduBredde = vindu.get_width()
    vinduHoyde = vindu.get_height()

    startPos = (vinduBredde//2, vinduHoyde//2)
    
    # Etter runde 5, blir det ikke flere maur, men de beveger seg raskere
    if rundetall < 6:
        maurListe = lagMaur(round(rundetall*0.1 * 100), vindu, startPos[0]+vinduBredde//4, startPos[1], 0.3, 4)
        maurListe += lagMaur(round(rundetall*0.1 * 100), vindu, startPos[0]-vinduBredde//4, startPos[1], 0.3, 4)
    else:
        maurListe = lagMaur(round(5*0.1 * 100), vindu, startPos[0]+vinduBredde//4, startPos[1], 0.5, 4)
        maurListe += lagMaur(round(5*0.1 * 100), vindu, startPos[0]-vinduBredde//4, startPos[1], 0.5, 4)
    
    radius = 18
    spiller = Spiller(radius*3, vinduHoyde-radius*3, radius, 0.8, bevTaster, altBevTaster, vindu, (100, 0, 0))
    
    menyKnapp = Knapp((105, 176, 205), vinduBredde//2, 40, 140, 40, vindu, "Hovedmeny", 20)
    menyKnapp2 = Knapp((105, 176, 205), vinduBredde//2+100, vinduHoyde//2+50, 140, 40, vindu, "Hovedmeny", 20)

    provIgjenKnapp = Knapp((105, 176, 205), vinduBredde//2-100, vinduHoyde//2+50, 140, 40, vindu, "Prøv igjen", 20)

    maalBilde = pg.image.load("Filer/MaalBilde.png")
    maalBilde = pg.transform.rotozoom(maalBilde, 0, 0.2)

    runde = f"Runde {rundetall}"
    rundeTekst = litenFont.render((runde), False, (0,0,0))
    rundeTekstPos1 = ((vinduBredde//2) - (litenFont.size(runde)[0]//2), 40+(litenFont.size(runde)[1]//2))
    rundeTekstPos2 = ((vinduBredde//2) - (litenFont.size(runde)[0]//2), (vinduHoyde//2) + (litenFont.size(runde)[1]//2) - 100)

    # Spill-løkke
    fortsett = True
    
    while fortsett:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                fortsett = True
        
        vindu.fill((135, 206, 235))
        
        if menyType == "spill":
            vindu.blit(rundeTekst, rundeTekstPos1)
            
            menyKnapp.tegn()

            spiller.flytt()
            spiller.tegn()

            spillerPos = (spiller.x, spiller.y)

            vindu.blit(maalBilde, (vinduBredde - 55 - (maalBilde.get_width()/2), 55 - (maalBilde.get_height()/2)))
            
            spillerPos = (spiller.x, spiller.y)
            if finnAvstand(spillerPos, (vinduBredde, 0)) < 120:
                rundetall += 1
                unngaHoved(menyCallback, rundetall) # Starter neste runde når spiller kommer
                break                               # nær målet
                
            for maur in maurListe:
                maur.flytt(1.5)
                maur.tegn()
                maurPos = (maur.x, maur.y)
                if finnAvstand(maurPos, spillerPos) < spiller.radius + maur.radius:
                    ErRekord(rundetall, "rekorder.json", "unngaSpill")
                    menyType = "info"
                    break

            if menyKnapp.erOver(pg.mouse.get_pos()):    # Sjekker om menyknappen blir klikket
                if pg.mouse.get_pressed()[0]:
                    ErRekord(rundetall, "rekorder.json", "unngaSpill")
                    menyCallback()  # Kjører "callback" funksjonen --> Går tilbake til menyen
                    break           # Bruker break for å ende spill-løkken

        if menyType == "info":
            vindu.blit(rundeTekst, rundeTekstPos2)
            menyKnapp2.tegn()
            provIgjenKnapp.tegn()

            if menyKnapp2.erOver(pg.mouse.get_pos()):    # Sjekker om menyknappen blir klikket
                if pg.mouse.get_pressed()[0]:
                    ErRekord(rundetall, "rekorder.json", "unngaSpill")
                    menyCallback()  # Kjører "callback" funksjonen --> Går tilbake til menyen
                    break           # Bruker break for å ende spill-løkken

            if provIgjenKnapp.erOver(pg.mouse.get_pos()):    # Sjekker om prøvigjen-knappen blir klikket
                if pg.mouse.get_pressed()[0]:
                    unngaHoved(menyCallback, 1)
                    break

            
        
        

        pg.display.flip()
    pg.quit()