'''
Created on Aug 15, 2014

@author: Thomas Boose 
(c) copyright Thomas Boose 2014-2015 (thomas at boose dot nl)
'''
# print "Hello run20.py" 

import string
import random
import sys
import ast

# prognaam = str(sys.argv[1]) + '\n'
fnaam = str(sys.argv[1])
with open(fnaam) as f:
	programma = f.read() + 'xxx\n'


fnaam= str(sys.argv[2])  
with open(fnaam) as f:
	doolhof	 = f.read()

fnaam= str(sys.argv[3])  
with open(fnaam) as f:
	kostenStr = f.read()

kostenKaart = ast.literal_eval(str(kostenStr))

debuglevel = 1 #print kosten en baten = 1; print status = 2;  print targets = 4

doeterniettoe = '\n \t'

def logItem(text):
    
    if text.__class__.__name__.lower() == "status": 
        if debuglevel & 2:
            print text
    else:
        if text[0:6].lower() == 'kosten' and debuglevel & 1:
            print text
        if text[0:5].lower() == 'bonus' and debuglevel & 1:
            print text
        if text[0:5].lower() == 'start' and debuglevel & 1:
            print text
        if text[0:4].lower() == 'eind' and debuglevel & 1:
            print text
        if text[0:3].lower() == 'bom' and debuglevel & 1:
            print text
        if text[0:4].lower() == 'boem' and debuglevel & 1:
            print text
        if text[0:4].lower() == 'stuk' and debuglevel & 2:
            print text
            
        if text[0:4].lower() == "doel" and debuglevel & 1:
            print text
        if text[0:6].lower() == "nieuwe" and debuglevel & 1:
            print text
        if text[0:12].lower() == "uitzondering" and debuglevel & 1:
            print text
        
        
        
        

def getWoord(status):
     
    while status.cursor < len(programma) and programma[status.cursor] in doeterniettoe:
        status.cursor += 1
        if status.cursor == len(programma) -1:
            status.einde = True
    woord = ''
    
    while not status.einde and programma[status.cursor] not in doeterniettoe:
        woord = woord + programma[status.cursor]
        status.cursor += 1
        if status.cursor == len(programma) -1:
            status.einde = True    
    return woord

def verwerkGebruik(status):
    wat = getWoord(status);
    status.ingebruik.append(wat)
    print wat 
    if len(wat) == 1:
        status.waarde[wat] = 0
    if wat in string.ascii_letters:
        status.kapitaal -= status.kostenKaart['declVariabele']
        logItem ("kosten voor declaratie variabele '" + wat + "': " + str(status.kostenKaart['declVariabele'])) 
    else:
        status.kapitaal -= status.kostenKaart['decl' + wat[0].upper() + wat[1:]]
        logItem("kosten voor declaratie '" + wat + "': " + str(status.kostenKaart['decl' + wat[0].upper() + wat[1:]]))  


def verwerkSeconde(status):
    index = 0
    moetWeg = []
    for index in range(len(status.bommen)):
        if status.bommen[index][1] == 0:
            logItem("boem op :" + str(status.bommen[index][0]))
            status.cells[status.bommen[index][0][0]][status.bommen[index][0][1]] = "O0"
            if status.bommen[index][0] == status.location:
                status.einde = True
                status.kapitaal -= 65535
                status.resultaat = "Stuk door bom"
                logItem("stuk door bom op " + str(status.location))
            moetWeg.append(index)
        else:
            status.bommen[index] = [status.bommen[index][0],status.bommen[index][1] - 1]
    for index in sorted(moetWeg, reverse=True):
        del status.bommen[index]
    
    if status.cells[status.location[0]][status.location[1]][0].lower() == "r":
        if int(status.cells[status.location[0]][status.location[1]][1]) == 0:
            status.zetDirection(status.direction + random.randint(0,3))
            logItem("nieuwe willekeurige richting = " + str(status.direction))
        else:
            status.zetDirection(status.direction + int(status.cells[status.location[0]][status.location[1]][1]))
            logItem("nieuwe richting na draaien = " + str(status.direction))

    status.seconden += 1
               
def verwerkNieuwePositie(status):
    if status.location == status.targets[0]:
        status.targets.remove(status.location)
        logItem("doel " + str(status.location) + " bereikt.")
        if len(status.targets) == 0:
            status.resultaat = "Doel bereikt binnen budget"

    if status.cells[status.location[0]][status.location[1]][0].lower() == "d":
        status.zetKleur(4)

    if status.cells[status.location[0]][status.location[1]][0].lower() == "s":
        status.zetKleur(0)
    
    if status.cells[status.location[0]][status.location[1]][0].lower() == "c":
        status.zetKleur(int(status.cells[status.location[0]][status.location[1]][1]))
                
    if status.cells[status.location[0]][status.location[1]][0].lower() == "e":
        status.zetKleur(4)
        status.kapitaal += 2 ** int(status.cells[status.location[0]][status.location[1]][1])
        logItem ("bonus van " + str(2 ** int(status.cells[status.location[0]][status.location[1]][1])) + " gepakt.")
        status.cells[status.location[0]][status.location[1]] = "C4"

    if status.cells[status.location[0]][status.location[1]][0].lower() == "r":
        status.zetKleur(2)

    if status.cells[status.location[0]][status.location[1]][0].lower() == "b":
        status.zetKleur(0)
        status.bommen.append([status.location,int(status.cells[status.location[0]][status.location[1]][1])])
        logItem ("bom geactiveerd. Tijd = " + str(status.cells[status.location[0]][status.location[1]][1]) + " sec.")

def verwerkStapVooruit(status):
    waarheen = status.location
    if int(status.direction) == 0:
        waarheen = [waarheen[0]-1, waarheen[1]]
    if int(status.direction) == 1:
        waarheen = [waarheen[0], waarheen[1]+1]        
    if int(status.direction) == 2:
        waarheen = [waarheen[0]+1, waarheen[1]]
    if int(status.direction) == 3:
        waarheen = [waarheen[0], waarheen[1]-1]
        
    if waarheen[0] < 0 or waarheen[0] > 19 or waarheen[1] < 0 or waarheen[1] > 19:
        logItem ('uitzondering: Uit the Glade gelopen! [' + str(waarheen[0]) + ',' + str(waarheen[1]) + ']\nThe rule say\'s: "Don\'t enter the maze"')
        raise Exception('uitzondering: Uit the Glade gelopen! [' + str(waarheen[0]) + ',' + str(waarheen[1]) + ']\nThe rule say\'s: "Don\'t enter the maze"')
    
    if status.cells[waarheen[0]][waarheen[1]][0].lower() in 'csbder':
        status.location = waarheen
        status.kapitaal -= status.kostenKaart['stapVooruit'] 
        logItem ("kosten voor stap vooruit: " + str(status.kostenKaart['stapVooruit']) + " naar: [" + str(waarheen[0]) +"," + str(waarheen[1]) + "]")

        verwerkNieuwePositie(status)
    else: # dus o
        status.kapitaal -= status.kostenKaart['duw']
        logItem ("kosten voor botsen / duwen: " + str(status.kostenKaart['duw']))
    verwerkSeconde(status)

def verwerkStapAchteruit(status):
    waarheen = status.location
    if int(status.direction) == 2:
        waarheen = [waarheen[0]-1, waarheen[1]]
    if int(status.direction) == 3:
        waarheen = [waarheen[0], waarheen[1]+1]        
    if int(status.direction) == 0:
        waarheen = [waarheen[0]+1, waarheen[1]]
    if int(status.direction) == 1:
        waarheen = [waarheen[0], waarheen[1]-1]
        
    if status.cells[waarheen[0]][waarheen[1]][0].lower() in 'csbder':
        status.location = waarheen
        status.kapitaal -= status.kostenKaart['stapAchteruit'] 
        logItem ("kosten voor stap achteruit: " + str(status.kostenKaart['stapAchteruit']) + " naar: [" + str(waarheen[0]) +"," + str(waarheen[1]) + "]")

        verwerkNieuwePositie(status)
    else: # dus o
        status.kapitaal -= status.kostenKaart['duw']
        logItem ("kosten voor botsen / duwen: " + str(status.kostenKaart['duw']))
    verwerkSeconde(status)




def verwerkDraaiRechts(status):
    status.zetDirection(status.direction + 1)
    status.kapitaal -= status.kostenKaart['draaiRechts'] 
    logItem ("kosten voor het draaien naar rechts: " + str(status.kostenKaart['draaiRechts']))
    verwerkSeconde(status)

def verwerkDraaiLinks(status):
    status.zetDirection(status.direction - 1)
    status.kapitaal -= status.kostenKaart['draaiLinks'] 
    logItem ("kosten voor het draaien naar links: " + str(status.kostenKaart['draaiLinks']))
    verwerkSeconde(status)

def verwerkExpressie(status):
    woord = getWoord(status)
    if woord.isdigit():
        waarde = int(woord)
    if woord in status.ingebruik:
        waarde = status.waarde[woord]
        if woord.lower() == 'kleuroog':
            status.kapitaal -= status.kostenKaart['kleurOog']
            logItem ("kosten voor gebruik kleur-oog: " + str(status.kostenKaart['kleurOog']))
        if woord.lower() == 'zwoog':
            status.kapitaal -= status.kostenKaart['zwOog']
            logItem ("kosten voor gebruik zwart-wit-oog: " + str(status.kostenKaart['zwOog']))
        if woord.lower() == 'kompas':
            status.kapitaal -= status.kostenKaart['kompas']
            logItem ("kosten voor gebruik kompas: " + str(status.kostenKaart['kompas']))
    cursor = status.cursor
    operator = getWoord(status)
    while operator in '+-*/%' and operator != '':
        status.kapitaal -= status.kostenKaart['operatie']
        logItem ("kosten voor de " + operator + " operatie: " + str(status.kostenKaart['operatie']))

        woord = getWoord(status)
        if woord.isdigit():
            erbij = int(woord)
        if woord in status.ingebruik:
            erbij = status.waarde[woord]
        if operator == '+':
            waarde += erbij
        if operator == '-':
            waarde -= erbij
        if operator == '*':
            waarde *= erbij
        if operator == '/':
            waarde /= erbij
        if operator == '%':
            waarde = waarde % erbij
        cursor = status.cursor
        operator = getWoord(status)
    status.cursor = cursor
    return waarde

def verwerkToekenning(status, letter):
    if getWoord(status) != '=':
        logItem ("uitzondering: Verwacht = bij een toekenning")
        raise Exception("uitzondering: Verwacht = bij een toekenning")
    else:
        if not letter in status.ingebruik:
            logItem ("uitzondering: Variabele " + letter + " niet geinitialiseerd")
            raise Exception("uitzondering: Variabele " + letter + " niet geinitialiseerd")
        else:
            status.waarde[letter] = verwerkExpressie(status)
            status.kapitaal -= status.kostenKaart['toewijzing']
            logItem ("kosten voor het toewijzen van een waarde: " + str(status.waarde[letter]) + " aan " + letter + ": " + str(status.kostenKaart['toewijzing']))

def doeBlok(status):
    if getWoord(status) != "{":
        logItem ("uitzondering: Een blok staat altijd tussen { en }")
        raise Exception("uitzondering: Een blok staat altijd tussen { en }")
    else:
        while status.kapitaal > 0 and len(status.targets) > 0 and not status.einde:
            doeStap(status)
            logItem(status)
            
        if len(status.targets) > 0:
            status.einde = False

def skipBlok(status):
    if len(status.targets) > 0:
        nextwoord = getWoord(status)
        stop = 1        
        while stop > 0 and nextwoord != '': 
            nextwoord = getWoord(status) 
            if nextwoord == "}":
                stop -= 1
            if nextwoord == "{":
                stop += 1
            
def verwerkAls(status):
    links = verwerkExpressie(status)
    operator = getWoord(status)
    rechts = verwerkExpressie(status)
    
    if operator == '==':
        uitslag = links == rechts
    if operator == '!=':
        uitslag = links != rechts
    if operator == '<':
        uitslag = links < rechts
    if operator == '>':
        uitslag = links > rechts

    status.kapitaal -= status.kostenKaart['vergelijking']
    logItem ("kosten voor het vergelijken: " + str(status.kostenKaart['vergelijking']))
    
    if uitslag and not status.einde and len(status.targets) > 0 and status.kapitaal > 0 :
        doeBlok(status)
                    
        alsCursor = status.cursor
        if getWoord(status) == 'anders':
            skipBlok(status)
        else:
            status.cursor = alsCursor
    
    if not uitslag and not status.einde and len(status.targets) > 0 and status.kapitaal > 0 :
        skipBlok(status)
                    
        alsCursor = status.cursor
        if getWoord(status) == 'anders':
            doeBlok(status)
        else:
            status.cursor = alsCursor
            
            
def verwerkZolang(status):
    cursor = status.cursor
    links = verwerkExpressie(status)
    operator = getWoord(status)
    rechts = verwerkExpressie(status)
    
    if operator == '==':
        uitslag = links == rechts
    if operator == '!=':
        uitslag = links != rechts
    if operator == '<':
        uitslag = links < rechts
    if operator == '>':
        uitslag = links > rechts
    status.kapitaal -= status.kostenKaart['vergelijking']
    logItem ("kosten voor het vergelijken: " + str(status.kostenKaart['vergelijking']))
    
    while uitslag and len(status.targets) > 0 and status.kapitaal > 0 and not status.einde:
        
        doeBlok(status)
        
        if status.kapitaal > 0 and len(status.targets) > 0 and not status.einde:
            status.cursor = cursor
            links = verwerkExpressie(status)
            operator = getWoord(status)
            rechts = verwerkExpressie(status)
            
            if operator == '==':
                uitslag = links == rechts
            if operator == '!=':
                uitslag = links != rechts
            if operator == '<':
                uitslag = links < rechts
            if operator == '>':
                uitslag = links > rechts
            status.kapitaal -= status.kostenKaart['vergelijking']
            logItem ("kosten voor het vergelijken: " + str(status.kostenKaart['vergelijking']))

    if status.kapitaal > 0 and len(status.targets) > 0 and not status.einde:
        skipBlok(status)
        

def doeStap(status):

    woord = getWoord(status)
    if woord.lower() == "gebruik":
        verwerkGebruik(status)

    if woord.lower() in string.ascii_letters and woord != '': 
        verwerkToekenning(status, woord.lower())
        
    if woord.lower() == "zolang":
        verwerkZolang(status)
    if woord.lower() == "als":
        verwerkAls(status)
    if woord.lower() == "stapvooruit":
        verwerkStapVooruit(status)
    if woord.lower() == "stapachteruit":
        verwerkStapAchteruit(status)
    if woord.lower() == "springpaardlinks":
        verwerkSpringPaardLinks(status)
    if woord.lower() == "springpaardrechts":
	verwerkSpringPaardRechts(status)
    if woord.lower() == "draailinks":
        verwerkDraaiLinks(status)
    if woord.lower() == "draairechts":
        verwerkDraaiRechts(status)
    if woord.lower() == "}":
        status.einde = True

def chunks(line, n):
    toreturn = []
    for i in xrange(0, len(line), n):
        toreturn.append(line[i:i+n])
    return toreturn		
		
		
class Status(object):
    
    def __str__(self):
        return str(self.cursor) + " " + str(self.kapitaal) + " " + str(self.direction) + " " + str(self.targets) + " " + str(self.einde) + " " + str(self.seconden)  \
            + " " + str(self.ingebruik) + " " + str(self.location) + " '" + programma[self.cursor:self.cursor + 40].replace("\n"," ") + "'"

    def findStartEnDoelEnBommen(self):
        '''Zoek in een verzameling van 20 bij 20 cellen het startpunt, 
        de startrichting en de doelen die bereikt moeten worden'''
        
        foundStart = False
        foundTargets = 0    
        targets = [[21,21]] * 10
        foundBonuses = 0    
        bonuses = [[21,21]] * 10
        self.bommen = []
        self.location = [0,0]
        self.direction = 0
        self.resultaat = ""
        
        for i in range(0,20):
            for j in range(0,20):
		print i,j,self.cells[i][j]
                if self.cells[i][j][0].upper() == 'E':
                    print "[" + self.cells[i][j][1] + "]"
                    if bonuses[int(self.cells[i][j][1])] == [21,21]:
                        foundBonuses += 1
                        bonuses[int(self.cells[i][j][1])] = [i,j]
                    else:
                        logItem ("uitzondering: Bonus " + self.cells[i][j][1] + " is dubbel gedefinieerd op [" + str(i) + ", " + str(j) + "]")
                        raise Exception("uitzondering: Bonus " + self.cells[i][j][1] + " is dubbel gedefinieerd op [" + str(i) + ", " + str(j) + "]")
                if self.cells[i][j][0].upper() == 'D':
                    if targets[int(self.cells[i][j][1])] == [21,21]:
                        foundTargets += 1
                        targets[int(self.cells[i][j][1])] = [i,j]
                    else:
                        logItem ("uitzondering: Doel " + self.cells[i][j][1] + " is dubbel gedefinieerd op [" + str(i) + ", " + str(j) + "]") 
                        raise Exception("uitzondering: Doel " + self.cells[i][j][1] + " is dubbel gedefinieerd op [" + str(i) + ", " + str(j) + "]") 
                if self.cells[i][j][0].upper() == 'S':
                    if foundStart:
                        logItem ("uitzondering: Twee startplaatsen in het doolhof")
                        raise Exception("uitzondering: Twee startplaatsen in het doolhof")
                    else:
                        self.location = [i,j]
                        self.zetDirection(int(self.cells[i][j][1]))
                        foundStart = True     
                              
        if not foundStart:
            logItem ("uitzondering: Geen startplaatsen in het doolhof")
            raise Exception("uitzondering: Geen startplaatsen in het doolhof")
        else:
            if 0 < foundTargets < 10:
                newTargets = []
                for target in targets:
                    if target != [21,21]:
                        newTargets.append(target)
                self.targets = newTargets
            else:
                logItem ("uitzondering: Geen of meer dan 10 doelen gevonden")
                raise Exception("uitzondering: Geen of meer dan 10 doelen gevonden")



    def createCells(self):
        lines = self.doolhof.split('\n')
        print len(lines) 
	self.cells = []
        
        for line in lines:
            print "[" + line + "]"
            self.cells.append(chunks(line, 2))
	    print self.cells
    def getWaarde(self,wat):
        if wat == "kleurOog":
            return self.kleur
        if wat == "zwOog":
            if self.kleur == 0:
                return 0
            else:
                return 1
        if wat == "kompas":
            return self.direction
    
    def zetKleur(self, kleur):
        self.kleur = kleur 
        self.waarde["kleurOog"] = self.getWaarde("kleurOog")
        self.waarde["zwOog"] = self.getWaarde("zwOog")

    def zetDirection(self, direction):
        self.direction = direction % 4 
        self.waarde["kompas"] = self.getWaarde("kompas")
        
    def __init__(self):
        self.doolhof = doolhof
        self.ingebruik = []
        self.einde = False
        self.createCells()
        self.waarde = {}
        self.findStartEnDoelEnBommen()
        self.cursor = 0
        self.kostenKaart = kostenKaart
        self.seconden = 0
        self.kapitaal = kostenKaart["startKapitaal"]
        print "start kapitaal: " + str(self.kapitaal)
        self.kapitaal -= (str(programma).lower().count("zolang") * int(kostenKaart["zolang"] ))
        print "kosten zolang: " + str(str(programma).lower().count("zolang")) + " * " + str(kostenKaart["zolang"])
        self.kapitaal -= (str(programma).lower().count("als") * int(kostenKaart["als"] ))
        print "kosten als: " + str(str(programma).lower().count("als")) + " * " + str(kostenKaart["als"])
        self.kapitaal -= ((str(programma).lower().count("stap") + str(programma).lower().count("draai")) * int(kostenKaart["opdracht"] ))
        print "kosten opdracht: " + str(int(str(programma).lower().count("stap")) + int(str(programma).lower().count("draai"))) + " * " + str(kostenKaart["opdracht"])
        self.kapitaal -= (str(programma).lower().count(" = ") * int(kostenKaart["toekenning"] ))
        print "kosten toekenning: " + str(str(programma).lower().count(" = ")) + " * " + str(kostenKaart["toekenning"])
        self.zetKleur(0)
        
        
if __name__ == '__main__':

    status = Status()
    logItem (status)
    
    while status.kapitaal > 0 and len(status.targets) > 0 and not status.einde:
        #status = doeStap(status)
        doeStap(status)
        logItem( status)
    logItem ('eind kapitaal :' + str(status.kapitaal))
    if status.resultaat == "" and status.kapitaal <= 0:
        status.resultaat = "Budget op"
    logItem (status)
    print status.resultaat 
    


