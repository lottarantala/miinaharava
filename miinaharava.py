#Lotta Rantala, Janette Schönberg, Ella Marjamaa
import haravasto as h
import random as r
import time as t

kentta = {
    "leveys" : 0,
    "korkeus" : 0,
    "miinat" : 0,
    "liput" : [],
    "miinojen_koordinaatit" : []
}

statistiikka = {
    "aloitus" : 0,
    "lopetus" : 0,
    "kesto" : 0,
    "kesto_vuoroissa" : 0,
    "tulos" : None,
    "kierros_aika" : 0,
    "pelin_ajankohta" : None
}

tila = {
    "kentta": [],
    "kentta_piilossa" : []
}

def haluatko_pelata():
    print("Tervetuloa pelaamaan miinaharavaa made by Janette, Lotta ja Ella :-)")

    while True:
        print("Kirjoita X pelataksesi ja T, jos haluat tarkastella tilastoja. Voit myös lopettaa pelin kirjoittamalla E. ")
        valinta = input("Valinta: ").lower()
        if valinta == "x":
            statistiikka["kesto_vuoroissa"] = 0
            kentta["liput"] = []
            kentta["miinojen_koordinaatit"] = []
            aloita_peli()
            pelin_aloitus()
            main()
        elif valinta == "t":
            avaa_tulokset("tulokset.txt")
        elif valinta == "e":
            print("Heippa!")
            break
        else:
            print("Kirjoita X, T tai E")
    
def kysy_leveys():
    print("Valitse kentän leveys väliltä 8-100")
    while True:
        try:
            kentta_leveys = int(input("Kentän leveys: "))   
        except ValueError:
            print("Ei tuo ole kokonaisluku you silly goose!")
            continue
        if kentta_leveys < 8:
            print("Valitsemasi luku on liian pieni")
        elif kentta_leveys > 100:
            print("Valitsemasi luku on liian suuri")
        else:
            break
    
    kentta["leveys"] = kentta_leveys
    return kentta_leveys

def kysy_korkeus():
    print("Valitse kentän korkeus väliltä 8-100")
    while True:
        try:
            kentta_korkeus = int(input("Kentän korkeus: "))                          
        except ValueError:
            print("Ei tuo ole kokonaisluku you silly goose!")
            continue
        if kentta_korkeus < 8:
            print("Valitsemasi luku on liian pieni")                
        elif kentta_korkeus > 100:
            print("Valitsemasi luku on liian suuri")
        else:
            break

    kentta["korkeus"] = kentta_korkeus
    return kentta_korkeus
                
def kysy_miinojen_maara():            
    print("Valitse miinojen lukumäärä")
    while True:
        try:
            miinojen_maara = int(input("Miinojen lukumäärä: "))                          
        except ValueError:
            print("Ei tuo ole kokonaisluku you silly goose!")
            continue
        if miinojen_maara >= kentta["leveys"] * kentta["korkeus"]:
            print("Annoit liikaa miinoja!")               
        elif miinojen_maara <= 0:
            print("Miinojen määrä ei voi olla nolla tai negatiivinen!")
        else:
            break

    kentta["miinat"] = miinojen_maara
    return miinojen_maara
    
def piirra_kentta():
    h.tyhjaa_ikkuna()
    h.piirra_tausta()
    h.aloita_ruutujen_piirto()
    for rivi, i in enumerate(tila["kentta"]):
        for sarake, merkki in enumerate(i):
            h.lisaa_piirrettava_ruutu(merkki, 40*sarake, 40*rivi)
    h.piirra_ruudut()

def hiiri_kasittelija(x, y, painike, muokkaus):
    
    x = int(x / 40)
    y = int(y / 40)
    painike = int(painike)
    muokkaus = int(muokkaus)
   
    if painike == h.HIIRI_VASEN:
        #laskee vain peliruudun sisällä painetut vuorot, ei muualla ikkunassa painettuja
        if 0 <= y <= kentta["korkeus"] and 0 <= x <= kentta["leveys"]:
            statistiikka["kesto_vuoroissa"] = statistiikka["kesto_vuoroissa"] + 1
            ruudun_avaus(x, y)       
    elif painike == h.HIIRI_OIKEA:
        if 0 <= y <= kentta["korkeus"] and 0 <= x <= kentta["leveys"]:
            statistiikka["kesto_vuoroissa"] = statistiikka["kesto_vuoroissa"] + 1
            lippu(x, y)

def pelin_aloitus():
    kentta_1 = []
    kentta_2 = []
    for rivi in range(kentta["korkeus"]):
        kentta_1.append([])
        kentta_2.append([])
        for sarake in range(kentta["leveys"]):
            kentta_1[-1].append(" ")
            kentta_2[-1].append(" ")
    tila["kentta"] = kentta_1
    tila["kentta_piilossa"] = kentta_2

    jaljella = []
    for y in range(kentta["korkeus"]):
        for x in range(kentta["leveys"]):
            jaljella.append((x, y))
    miinoita(tila["kentta_piilossa"], jaljella, kentta["miinat"])
    numeroi_kentta(tila["kentta_piilossa"])
    
def ruudun_avaus(x, y):
    #jos ruudussa on miina, paljastaa koko kentän
    if tila["kentta_piilossa"][y][x] == "x":
        havio()
        tila["kentta"] = tila["kentta_piilossa"]
        piirra_kentta()    
    #jos ruudussa ei ole miina
    elif tila["kentta_piilossa"] != "x":
        #jos turvallinen ruutu, tulvatäyttö
        if tila["kentta"][y][x] == " ":
            tulvataytto(tila["kentta"], x, y)
        #lippu
        elif tila["kentta"][y][x] == "f":
            tila["kentta"][y][x] = "f"
        #numeroruutu
        elif tila["kentta"] != "0":
            tila["kentta"][y][x] = tila["kentta_piilossa"][y][x]

def miinoita(lista, vapaat, lkm):  
    for i in range(lkm):
        koordinaatit = r.choice(vapaat)
        y = koordinaatit[1]
        x = koordinaatit[0]
        lista[y][x] = "x"
        vapaat.remove(koordinaatit)
        kentta["miinojen_koordinaatit"].append((x, y))

def laske_miinat(x, y, lista):
    miinat = 0
    x_rajat = {x, x - 1, x + 1}
    y_rajat = {y, y - 1, y + 1}
    for y, i in enumerate(lista):
        for x, ruutu in enumerate(i):
            if y in y_rajat and x in x_rajat and ruutu == "x":
                miinat = miinat + 1
    return miinat

def numeroi_kentta(lista):
    for y, rivi in enumerate(lista):
        for x, merkki in enumerate(rivi):
            if merkki != "x":
                numero = laske_miinat(x, y, lista)
                lista[y][x] = "{}".format(numero)

def aloita_peli():
    kysy_leveys()
    kysy_korkeus()
    kysy_miinojen_maara()
    print("Valitsit kentän leveydeksi {}, korkeudeksi {} sekä miinojen lukumääräksi {}".format(
        kentta["leveys"], kentta["korkeus"], kentta["miinat"]))

def tulvataytto(lista, x, y):
    if y >= len(lista) or x >= len(lista[0]):
        return
    if lista[y][x] == "x" and lista[y][x] == "f":
        return 

    tutkittavat = [(x, y)]
    
    while tutkittavat:
        tutkittava = tutkittavat.pop(-1)
        tutkittava_x, tutkittava_y = tutkittava
        lista[tutkittava_y][tutkittava_x] = tila["kentta_piilossa"][tutkittava_y][tutkittava_x]
        if lista[tutkittava_y][tutkittava_x] == "0":
            for rivi in range(tutkittava_y-1, tutkittava_y+2):
                for sarake in range(tutkittava_x-1, tutkittava_x+2):
                    if 0 < rivi < len(lista) and 0 < sarake < len(lista[0]):
                        lista[rivi][sarake] = tila["kentta_piilossa"][rivi][sarake]
                        if lista[rivi][sarake] == "0":
                            tutkittavat.append((sarake, rivi))

def lippu(x, y):
    #laittaa lipun
    if tila["kentta"][y][x] == " ":
        tila["kentta"][y][x] = "f"
        kentta["liput"].append((x, y))
        voitto()
    #poistaa lipun
    elif tila["kentta"][y][x] == "f":
        tila["kentta"][y][x] = " "
        kentta["liput"].remove((x, y))
        voitto()
    else:
        print("Ei voi asettaa lippua tähän ruutuun")

def voitto():
    #tarkistaa onko peli voitettu
    #https://www.stechies.com/compare-lists-python-using-set-cmp-function/
    if set(kentta["miinojen_koordinaatit"]) == set(kentta["liput"]):
        h.lopeta()
        print("Voitit pelin! :)")
        aika_lopetus()
        print("Pelisi kesti {} minuuttia".format(statistiikka["kesto"]))
        statistiikka["tulos"] = "voitto"
        tallenna_tulokset("tulokset.txt")
    
def havio():
    #h.lopeta()
    print("Hävisit pelin :(")
    aika_lopetus()
    print("Pelisi kesti {} minuuttia".format(statistiikka["kesto"]))
    statistiikka["tulos"] = "häviö"
    tallenna_tulokset("tulokset.txt")

def main():
    h.lataa_kuvat(r"C:\Users\lotta\Desktop\OA\spritet.zip\spritet")
    h.luo_ikkuna(40*kentta["leveys"], 40*kentta["korkeus"])
    h.aseta_piirto_kasittelija(piirra_kentta)
    h.aseta_hiiri_kasittelija(hiiri_kasittelija)
    aika_aloitus()
    h.aloita()

#https://docs.python.org/3/library/time.html
#https://www.programiz.com/python-programming/time

def aika_aloitus():
    statistiikka["aloitus"] = t.time()
    statistiikka["pelin_ajankohta"] = t.ctime()
    return statistiikka["aloitus"], statistiikka["pelin_ajankohta"]

def aika_lopetus():
    statistiikka["lopetus"] = t.time()
    statistiikka["kesto"] = int((statistiikka["lopetus"] - statistiikka["aloitus"]) / 60)
    return statistiikka["kesto"], statistiikka["lopetus"]

def avaa_tulokset(nimi):
    try:
        with open(nimi, "r") as lahde:
            for rivi in lahde.readlines():
                print(rivi)
    except IOError:
        print("Tiedostoa ei voitu avata. Yritä uudelleen.")
    
def tallenna_tulokset(nimi):
    try:
        with open (nimi, "a") as tulos:
            tulos.write("{paivamaara}: {tulos}, kesto {kesto} minuuttia ja {vuorot} vuoroa, kentän koko {leveys}x{korkeus}, {miinat} miinaa \n".format(
                paivamaara=statistiikka["pelin_ajankohta"],\
                kesto=statistiikka["kesto"],\
                vuorot=statistiikka["kesto_vuoroissa"],\
                tulos=statistiikka["tulos"],\
                leveys=kentta["leveys"],\
                korkeus=kentta["korkeus"],\
                miinat=kentta["miinat"]))
    except IOError:
        print("Tilastoja ei voitu tallentaa")
     
if __name__ == "__main__":
    haluatko_pelata()