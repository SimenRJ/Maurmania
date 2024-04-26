# -*- coding: utf-8 -*-
# simuleringSpill.py - Spill hvor man endrer verdier for å se hvor lant tid maurene bruker på å hente maten

import pygame as pg
from klasser import Mat, simMaur
from elementer import Knapp, ErRekord
import math as m
import random as rd

def nyRekordTekst(font, vindu, vH: int, vB: int):
    '''
        Funksjon som viser "Ny rekord!" i spillet
        
        @param font: font til teksten
        @param vindu: vindusobjektet i pygame
        @param vH (int): vinduhøyde
        @param vB (int): vindubredde 
    '''

    rekordStr = "Ny rekord!"
    rekordT = font.render((rekordStr), False, (0,0,0))
    rekordTPos = ((vB//2) - (font.size(rekordStr)[0]/2), (vH//2) - (font.size(rekordStr)[1]/2) - 80)

    vindu.blit(rekordT, rekordTPos)

def finnAvstand(obj1: object, obj2: object):
    '''
        Funksjon som finner avstand mellom to objekter og
        returnerer avstanden
        
        @param obj1 (object): objekt 1
        @param obj2 (object): objekt 2
    '''
    xAvstand2 = (obj1[0] - obj2[0])**2  # x-avstand^2
    yAvstand2 = (obj1[1] - obj2[1])**2  # y-avstand^2
    avstand = m.sqrt(xAvstand2 + yAvstand2)
    return avstand

def naerMat(maur: object, matListe: list):
    '''
        Funksjon som sjekker hvilken matsamling som er nærest mauren
        Den sjekker deretter om mauren er under 10 piksler fra maten
        Hvis den er det, slettes maten og mauren får variabelen "harMat" satt til sant
        
        Dersom matsamlingen er tom, slettes den fra matlisten
        
        @param maur (object): maurobjekt
        @param matListe (list): liste over matsamling som inneholder matobjekter
    '''
    
    naermest = (0, 10000)

    for i in range(len(matListe)):
        matSamling = matListe[i]
        avstand = finnAvstand((maur.x, maur.y), matSamling[0])  # Finner avstanden mellom mauren og matsamlingen

        if avstand < naermest[1]:
            naermest = (i, avstand)

    matSamling = matListe[naermest[0]]
    for mat in matSamling[1:]:
        matPos = (mat.x, mat.y)

        avstand = finnAvstand((maur.x, maur.y), matPos)

        if avstand <= 10:
            if maur.harMat == False:
                matSamling.remove(mat)
                maur.harMat = True
            if len(matSamling) == 1:
                matListe.remove(matSamling) 

def blirSett(maur: object, matListe: list):
    '''
        Funksjon som sjekker om maten blir sett av mauren.
        Hvis avstanden mellom mauren og maten er under 150 og mauren ikke har mat fra før,
        vil naerMat funksjonen kjøres (den vil sjekke om maten blir "plukket opp")
        Dersom avstanden er mellom 200 og 45, vil den "se maten" og derfor returnere "True" og
        posisjonen til maten
        
        Den "ser ikke maten" når den er under 45, da dette får mauren til å gå tilfeldig rundt i matområdet.
        
        @param maur (object): maurobjekt
        @param matListe (list): liste over matsamling som inneholder matobjekter
        
        Return: funksjonen returnerer tre ting:
        Første element er "True" eller "False" utifra om mauren ser maten eller ikke
        Andre og tredje element er x- og y-koordinatet til maten. Dersom mauren ikke ser noe mat,
        er disse "None".
    '''
    for mat in matListe:
        matX = mat[0][0]
        matY = mat[0][1]

        avstand = finnAvstand((maur.x, maur.y), (matX, matY))

        if maur.harMat == True:
            return False, None, None

        if avstand < 150:
            naerMat(maur, matListe)

        if avstand < 200 and avstand > 45:
            return True, matX, matY
            
    return False, None, None

def lagMaur(antall: int, vindusobjekt, x: int, y: int, fart: int = 1, radius: int = 5):
    '''
        Funksjon som lager maurobjekter og setter dem til å gå utover i en sirkel
        Deretter puttes de i en maurliste
        
        @param antall (int): Antall maur som skal lages
        @param vindusobjekt: pygame vindu
        @param x (int) og @param y (int): x- og y-koordinat til midten av maursirkelen
        @param fart (int): farten til maurene
        @param radius (int): radius til maurene
    '''
    
    gradEndring = 360/antall
    maurListe = []
    
    for i in range(antall):
        maur = simMaur(x, y, i*gradEndring, fart, radius, vindusobjekt)
        maurListe.append(maur)
        
    return maurListe


def lagMat(antall: int, x: int, y: int, spredGrad: int, radius: int, matListe: list, vindusobjekt):
    '''
    Funksjonen lager en matsamling med matobjekter som legger inn i
    en matliste.
    
    @param antall (int): antall matobjekter som skal lages
    @param x, param y (int): x og y kordinater til matsamlingen
    @param spredGrad (int): grad av tilfeldig endring i posisjon til matobjektene
    @param radius (int): radius til matobjektene
    @param matListe (list): liste som matsamlingene skal legges inn i
    @param vindusobjekt: vindusobjektet laget med pygame
    '''
    
    matSamling = [(x, y)]
    
    for i in range(antall):
        x = x + rd.randint(-spredGrad//2, spredGrad//2)
        y = y + rd.randint(-spredGrad//2, spredGrad//2)
        
        mat = Mat(x, y, radius, vindusobjekt)
        matSamling.append(mat)

    matListe.append(matSamling)


def simHoved(menyCallback, vandringsGrad: float):
    '''
    Hovedfunksjonen til programmet som initialiserer pygame-vinduet og inneholder spill-løkken til simuleringen.
    Funksjonen tar inn en "callback" funksjon for å kunne returnere til hovedmenyen uten å
    få problemer med importering.
    
    @param menyCallback (function): Hovedfunksjonen til menyprogram (hovedmeny.py)
    @param vandringsGrad (float): Verdi for vandringsgrad til maur fra hovedmenyen
    '''
    
    pg.init()
    pg.font.init()

    storForhold = [1920, 1080]

    vindu = pg.display.set_mode(storForhold, pg.FULLSCREEN)
    vinduBredde = vindu.get_width()
    vinduHoyde = vindu.get_height()
    
    litenFont = pg.font.SysFont('Comic Sans MS', 30)
    storFont = pg.font.SysFont('Comic Sans MS', 100)
    
    menyKnapp = Knapp((105, 176, 205), vinduBredde//2, 40, 140, 40, vindu, "Hovedmeny", 20)

    maurHjemPos = (vinduBredde-200, vinduHoyde-200)
    totAntMat = 100
    matIHjem = 0

    matListe = []
    maurListe = lagMaur(100, vindu, maurHjemPos[0], maurHjemPos[1], 1, 4)
    
    lagMat(totAntMat//2, 100, 400, 4, 6, matListe, vindu)
    lagMat(totAntMat//2, 600, 100, 4, 6, matListe, vindu)

    
    startTid = pg.time.get_ticks()      # Starttid i ms
    

    # Spill-løkke
    fortsett = True
    while fortsett:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                fortsett = False
        
        vindu.fill((135, 206, 235))

        if matIHjem < totAntMat:    # Sjekker om all maten er i hjemmet til maurene
            NaaTid = pg.time.get_ticks()    # Nåtid i millisekunder
            tidSek = round(((NaaTid - startTid))/1000, 2)
            tidBrukt =  f"{tidSek: .2f}"
            
            tidTekst = litenFont.render(tidBrukt, False, (0,0,0))
            vindu.blit(tidTekst, (10, 10))    

        else:
            # Endrer knappen- og tekstens posisjon og størrelse
            # Lagrer også rekorden
            if ErRekord(tidSek, "rekorder.json", "simulering", "under"):    # Sjekker om det er en rekord,
                nyRekordTekst(litenFont, vindu, vinduHoyde, vinduBredde)    # lagrer rekorden og skriver tekstene
            menyKnapp.bredde = 160
            menyKnapp.hoyde = 60
            menyKnapp.y = (vinduHoyde//2+40) + (menyKnapp.hoyde/2)
            tidTekst = storFont.render(tidBrukt, False, (0,0,0))
            tidTPos = (vinduBredde//2 - (storFont.size(str(tidBrukt))[0]/2), vinduHoyde//2 - (storFont.size(str(tidBrukt))[1]/2))
            vindu.blit(tidTekst, tidTPos)    

        
        for matSamling in matListe:
            for mat in matSamling[1:]:
                mat.tegn()
        
        menyKnapp.tegn()
        
        for maur in maurListe:
            sett, x, y = blirSett(maur, matListe)
            if sett:
                maur.gaMot(x, y)    # Går mot mat
            else:
                if maur.harMat == True:
                    maur.gaMot(maurHjemPos[0], maurHjemPos[1])  # Går mot maurtue
                else:
                    maur.flytt(vandringsGrad)   # Vandringsgrad fra menyen

            # Sjekker om mauren er hjemme og har mat
            if finnAvstand((maur.x, maur.y), maurHjemPos) < 20 and maur.harMat == True:
                maur.harMat = False
                matIHjem += 1           # Legger fra seg maten i maurtuen

            maur.tegn()

        # Lager Maurtuen
        MatIHjemTekst = litenFont.render(str(matIHjem), False, (0,0,0))
        pg.draw.circle(vindu, (100, 100, 0), maurHjemPos, 35)
        vindu.blit(MatIHjemTekst, (maurHjemPos[0] - (litenFont.size(str(matIHjem))[0]/2), maurHjemPos[1] - (litenFont.size(str(matIHjem))[1]/2)))
        
        
        if menyKnapp.erOver(pg.mouse.get_pos()):    # Sjekker om menyknappen blir klikket
            if pg.mouse.get_pressed()[0]:
                menyCallback()                      # Kjører "callback" funksjonen --> Går tilbake til menyen
                break                               # Bruker break for å ende spill-løkken
                

        
        pg.display.flip()

    
    
    pg.quit()

