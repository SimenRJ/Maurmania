# -*- coding: utf-8 -*-
# hovedmeny.py - Hovedmenyen til hele spillet

import pygame as pg
from elementer import Knapp, Glider
import simuleringSpill
import unngaMaurSpill
import json
import os

def lagRekorderFil(filnavn: str):
    '''
        Funksjon som oppretter en json fil med rekorder
        dersom den ikke eksisterer allerede
        
        @param filnavn (str): navn til jsonfil med rekorder
    '''
    
    filbane = f"Filer/{filnavn}"
    if os.path.isfile(filbane):
        return
    
    rekorder = {
        "simulering": 0,
        "unngaSpill": 0
    }
    
    with open(filbane, 'w') as fil:
        json.dump(rekorder, fil)


def hentRekorder(filnavn: str):
    # Funksjon som henter rekordene fra en fil med filnavn
    #
    # @param filnavn (str): Navn på filen
    
    filbane = f"Filer/{filnavn}" 
    
    with open(filbane) as fil:
        rekorder = json.load(fil)

    return rekorder


def lagRekorderTekst(font, rekorder: dict, vindu):
    '''
        Funksjon som viser rekordene på hovedmenyen
        
        @param font: Fonten som brukes i pygame
        @param rekorder (dict): En ordbok med rekordene
        @param vindu: vindusobjektet fra pygame    
    '''
    
    vinduBredde = vindu.get_width()
    vinduHoyde = vindu.get_height()

    if rekorder["simulering"] != 0:
        simStr = "Rekord: " + str(rekorder["simulering"])
    else:
        simStr = "Ingen rekord enda"

    if rekorder["unngaSpill"] != 0:
        unngaStr = "Rekord: " + str(rekorder["unngaSpill"])
    else:
        unngaStr = "Ingen rekord enda"
    

    simT = font.render((simStr), False, (0,0,0)) # Tekst til rekorden på simuleringen
    unngaT = font.render((unngaStr), False, (0,0,0)) # Tekst til rekorden på unngåspillet

    simPos = ((vinduBredde//2) - (font.size(simStr)[0]//2) -200, (vinduHoyde//2) - (font.size(simStr)[1]//2)+ 300)
    unngaPos = ((vinduBredde//2) - (font.size(unngaStr)[0]//2) + 200, (vinduHoyde//2) - (font.size(unngaStr)[1]//2) + 300)

    vindu.blit(simT, simPos)
    vindu.blit(unngaT, unngaPos)


def knappKlikk(knapp: object):
    # Funksjon som tar inn en knapp som parameter og returnerer True dersom knappen blir klikket
    # og False dersom den ikke klikkes
    #
    # @param knapp (objekt): knapp som klikkes
    
    if knapp.erOver(pg.mouse.get_pos()):
            if pg.mouse.get_pressed()[0]:
                return True
    return False


def menyHoved():
    # Hovedfunksjonen til programmet
    
    rekordFilnavn = "rekorder.json"
    lagRekorderFil(rekordFilnavn)
        
    pg.init()
    pg.font.init()

    maurBilde = pg.image.load("Filer/maur1.png")
    maurBilde = pg.transform.rotozoom(maurBilde, 30, 0.1)
    
    storForhold = [1920, 1080]  
    vindu = pg.display.set_mode(storForhold, pg.FULLSCREEN)
    vinduBredde = vindu.get_width()
    vinduHoyde = vindu.get_height()
    
    spillNavn = "Maurmania"
    ekstraInfo = "- Diverse morsomme maurspill -"    
    storFont = pg.font.SysFont('Comic Sans MS', 100)
    litenFont = pg.font.SysFont('Comic Sans MS', 30)

    # Hovedmeny
    overT = storFont.render((spillNavn), False, (0,0,0))    # Tekst til overskrift
    underT = litenFont.render((ekstraInfo), False, (0,0,0)) # Tekst til under-overskrift
    overPos = ((vinduBredde//2) - (storFont.size(spillNavn)[0]//2), (vinduHoyde//4) - (storFont.size(spillNavn)[1]//2))
    underPos = ((vinduBredde//2) - (litenFont.size(ekstraInfo)[0]//2), (vinduHoyde//4) - (litenFont.size(ekstraInfo)[1]//2) + (storFont.size(spillNavn)[1])//2)

    simKnapp = Knapp((105, 176, 205), vinduBredde//2 - 200, vinduHoyde//2+200, 350, 80, vindu, "Maursimulering", 35, "Enkel simulering som viser tiden det tar for maurene å samle all maten.")
    unngaKnapp = Knapp((105, 176, 205), vinduBredde//2 + 200, vinduHoyde//2+200, 350, 80, vindu, "Unngå Maurene", 35, "Kom til mål uten å bli truffet av maurene. Økende vanskelighetsgrad.")
    
    lukkKnapp = Knapp((105, 176, 205), vinduBredde-80, 40, 80, 40, vindu, "Lukk", 20)
    tilbakeKnapp = Knapp((105, 176, 205), vinduBredde-160, vinduHoyde-100, 140, 80, vindu, "Tilbake", 30)
    
    vandringsGlider = Glider((vinduBredde//2, vinduHoyde//2+100), (400, 80), 50, 0.5, 0.5, 2.5, vindu)
    
    # Simulerings-meny
    startSimKnapp = Knapp((105, 176, 205), vinduBredde//2, vinduHoyde-100, 400, 80, vindu, "Start simulering")
    info1 = "Målet er å få maurene til å spise opp all maten så fort som mulig"
    info2 = " - Endre vandringsgraden for å oppnå kortest mulig tid - "
    info3 = " - Vandringsgrad vil si hvor mye maurene svinger frem og tilbake - "

    info1T = litenFont.render((info1), False, (0,0,0)) # Tekst til overskrift
    info2T = litenFont.render((info2), False, (0,0,0)) # Tekst til under-overskrift
    info3T = litenFont.render((info3), False, (0,0,0)) # Tekst til andre under-overskrift
    info1TPos = ((vinduBredde//2) - (litenFont.size(info1)[0]//2), (vinduHoyde*0.1) - (litenFont.size(info1)[1]//2))
    info2TPos = ((vinduBredde//2) - (litenFont.size(info2)[0]//2), (vinduHoyde*0.1) - (litenFont.size(info2)[1]//2) + (litenFont.size(info1)[1]))
    info3TPos = ((vinduBredde//2) - (litenFont.size(info3)[0]//2), (vinduHoyde*0.1) - (litenFont.size(info3)[1]//2) + (litenFont.size(info1)[1]) + (litenFont.size(info2)[1]))
    


    # Spill-løkke
    menyType = "hovedmeny"
    fortsett = True
    while fortsett:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                fortsett = False
        
        vindu.fill((135, 206, 235))
        
        if menyType == "hovedmeny":
            lagRekorderTekst(litenFont, hentRekorder(rekordFilnavn), vindu)

            vindu.blit(maurBilde, (vinduBredde/2 + 300 - (maurBilde.get_width()/2), 200 - (maurBilde.get_height()/2)))

            vindu.blit(overT, overPos)
            vindu.blit(underT, underPos)

            if knappKlikk(simKnapp):
                menyType = "sim"                
            
            if knappKlikk(unngaKnapp):
                unngaMaurSpill.unngaHoved(menyHoved, 1)  # Sender en "callback" funksjon til simulering.py
                break
                
            if knappKlikk(lukkKnapp):
                break

            simKnapp.tegn()
            unngaKnapp.tegn()
            lukkKnapp.tegn()
        
        elif menyType == "sim":
            vindu.blit(info1T, info1TPos)
            vindu.blit(info2T, info2TPos)
            vindu.blit(info3T, info3TPos)
            
            
            vGradVerdi = f"Vandringsgrad: {vandringsGlider.finnVerdi()}"
            vGradInfo = litenFont.render((vGradVerdi), False, (0,0,0)) # Tekst til under-overskrift
            vGradInfoPos = ((vinduBredde//2) - (litenFont.size(vGradVerdi)[0]//2), (vinduHoyde//2) - (litenFont.size(vGradVerdi)[1]//2))
            
            musPos = pg.mouse.get_pos()
            
            if vandringsGlider.boks.collidepoint(musPos) and pg.mouse.get_pressed()[0]:
                vandringsGlider.flytt(musPos)
                
            
            vandringsGlider.tegn()
            vindu.blit(vGradInfo, vGradInfoPos)
            
            
            if knappKlikk(startSimKnapp):
                simuleringSpill.simHoved(menyHoved, vandringsGlider.finnVerdi())  # Sender en "callback" funksjon til simulering.py
                break
            
            if knappKlikk(tilbakeKnapp):
                menyType = "hovedmeny"
                

            startSimKnapp.tegn()
            tilbakeKnapp.tegn()
            
    
        pg.display.flip()
   
    pg.quit()


menyHoved()
