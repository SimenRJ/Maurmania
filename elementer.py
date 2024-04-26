# -*- coding: utf-8 -*-
# elementer.py - Fil som inneholder elementer og funksjoner som tas i bruk i spillet (Knapper, glidere osv.)

import pygame as pg
import json


def ErRekord(naaVerdi: float, filnavn: str, typeRekord: str, rekordForm: str = "over"):  
    '''
        Funksjon som sjekker om nåværende verdi er større enn forrige rekord
        Dersom det er en ny rekord, setter den rekorden til
        nåværende verdi og lagrer den til json filen
        deretter returnerer den "True"
        
        @param naaVerdi (float): Nåværende verdi (tid i simulering og rundetall i unngåspillet)
        @param filnavn (str): Navn på filen med rekordene (rekorder.json i dette tilfelle)
        @param typeRekord (str): Hvilken rekord det angår. Velger hvilken del
                                 av jsonfilen som leses/endres
        @param rekordForm (str): Rekordform. Om målet er lavt eller høyt tall (over eller under)
        
        Return: Returnerer True dersom det er en ny rekord og False dersom det ikke er det
    '''
    filbane = f"Filer/{filnavn}" 
    
    with open(filbane) as fil:
        rekorder = json.load(fil)
    
    if rekorder[typeRekord] == 0:
        rekorder[typeRekord] = naaVerdi
    
    elif rekordForm == "over":
        if naaVerdi >= rekorder[typeRekord]:
            rekorder[typeRekord] = naaVerdi
        else:
            return False
    else:
        if naaVerdi <= rekorder[typeRekord]:
            rekorder[typeRekord] = naaVerdi
        else:
            return False


    with open(filbane, 'w') as fil:
        json.dump(rekorder, fil)
    
    return True


class Knapp:
    # En klasse for å lage knapper
    def __init__(self, farge: tuple, x: int, y: int, bredde: int, hoyde: int, vindu, tekst: str = "", tekststorelse: int = 40, tekstBoksTekst: str = ""):
        '''
            Konstruktør for klassen
            @param farge (tuple): Farge til knapp i form av tuple
            @param x (int) og @param y (int): x- og y-koordinat til knappen
            @param bredde (int), @param hoyde (int): Bredde og høyde til knappen
            @param vindu: vindusobjekt fra pygame
            @param tekst (str): Tekst som skal stå på knappen dersom det skal stå noe
            @param tekststorelse (int): størrelse på teksten
            @param tekstBoksTekst (str): Teksten i boksen som kommer når man holder over knappen (på de knappene som har det)
        '''
        
        self.farge = farge
        self.vanligFarge = farge
        self.overFarge = tuple(x+20 for x in self.vanligFarge)
        self.bredde = bredde
        self.hoyde = hoyde
        self.x = x - self.bredde//2 # Endrer x- og y-verdi for å få sentrum
        self.y = y - self.hoyde//2  # i knappen ved oppgit x og y verdi
        self.tekst = tekst
        self.tekststor = tekststorelse
        self.vindu = vindu
        self.tekstBT = tekstBoksTekst

    def tegn(self, ramme: tuple = None):
        # Funksjon for å tegne knappen
        # @param ramme (tuple): Farge på ramme dersom knappen skal ha en
        
        if ramme:
            pg.draw.rect(self.vindu, ramme, (self.x-2, self.y-2, self.bredde+4, self.hoyde+4), 0, 6)
            
        pg.draw.rect(self.vindu, self.farge, (self.x, self.y, self.bredde, self.hoyde), 0, 6)
        
        if self.tekst != "":
            font = pg.font.SysFont("Comic Sans MS", self.tekststor)
            tekst = font.render(self.tekst, 1, (0, 0, 0))
            self.vindu.blit(tekst, (self.x + (self.bredde/2 - tekst.get_width()/2), self.y + (self.hoyde/2 - tekst.get_height()/2)))

    def erOver(self, pos):
        '''
            Funksjon som sjekker om musen er over knappen
            Viser tekstboks dersom knappen har det og endrer fagen på knappen
            
            @param pos (tuple): Posisjonen til musen        
        '''
        
        if pos[0] > self.x and pos[0] < self.x + self.bredde and pos[1] > self.y and pos[1] < self.y + self.hoyde:
            if self.tekstBT != "":
                font = pg.font.SysFont("Comic Sans MS", self.tekststor//2)
                tekst = font.render(self.tekstBT, 1, (0, 0, 0))
                vinduBredde = self.vindu.get_width()
                TekstBPos = (vinduBredde//2-self.bredde/2, self.y-self.hoyde*2)
                
                pg.draw.rect(self.vindu, self.farge, (TekstBPos[0]-self.bredde/2, TekstBPos[1], self.bredde*2, self.hoyde), 0, 6)

                self.vindu.blit(tekst, (TekstBPos[0] + (self.bredde/2 - tekst.get_width()/2), TekstBPos[1] + (self.hoyde/2 - tekst.get_height()/2)))
                
            self.farge = self.overFarge
            return True
        else:
            self.farge = self.vanligFarge
            return False



class Glider:
    # En klasse for å lage glidere
    def __init__(self, pos: tuple, stor: tuple, knappBredde: int, startVerdi: float, min: int, maks: int, vindu):
        '''
            Konstruktør
            Lager rektangler til glideren
            
            @param pos (tuple): Posisjonen til glideren, angitt som en tuple med (x, y)-koordinater.
            @param stor (tuple): Størrelsen til glideren, angitt som en tuple med (bredde, høyde).
            @param knappBredde (int): Bredden til den flyttbare knappen på glideren.
            @param startVerdi (float): Startverdien til glideren.
            @param min (int): Minimumsverdien glideren kan ha.
            @param maks (int): Maksimumsverdien glideren kan ha.
            @param vindu: Vindusobjekt fra pygame hvor glideren skal vises.      
        '''
        
        self.pos = pos
        self.stor = stor
        self.kBredde = knappBredde
        self.vindu = vindu
        
        self.glider_v_pos = self.pos[0] - (self.stor[0]//2)
        self.glider_h_pos = self.pos[0] + (self.stor[0]//2)
        self.glider_top_pos = self.pos[1] - (self.stor[1]//2)
        
        self.min = min
        self.maks = maks
        self.sVerdi = (self.glider_h_pos-self.glider_v_pos) * startVerdi    # Prosent
        
        self.boks = pg.Rect(self.glider_v_pos, self.glider_top_pos, self.stor[0], self.stor[1])
        self.knapp = pg.Rect(self.glider_v_pos + self.sVerdi-(self.kBredde//2), self.glider_top_pos, self.kBredde, self.stor[1])
        
    def flytt(self, musPos):
        # Funksjon som flytter knappen på glideren til musposisjonen
        # @param musPos (tuple): Posisjonen til musen
        
        self.knapp.centerx = musPos[0]
        
    def tegn(self):
        # Funksjon som tegner glideren
        
        self.tegnBoks = pg.Rect(self.glider_v_pos-(self.kBredde//2), self.glider_top_pos, self.stor[0]+self.kBredde, self.stor[1])
        pg.draw.rect(self.vindu, (95, 166, 195), self.tegnBoks, 0, 6)
        pg.draw.rect(self.vindu, (105, 176, 205), self.boks, 0, 6)
        pg.draw.rect(self.vindu, (125, 196, 225), self.knapp, 0, 10)
        
    def finnVerdi(self):
        # Funksjon som finner og returnerer verdien til knappens posisjon på glideren
        
        verdiMulighet = self.glider_h_pos - self.glider_v_pos - 1
        knappVerdi = self.knapp.centerx - self.glider_v_pos
        
        return round((knappVerdi/verdiMulighet) * (self.maks-self.min) + self.min, 2)