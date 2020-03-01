import sys, os, pygame, random

# Definisco il metodo che utilizzero' per cercare i file nelle relative
# sottocartelle.
def percorsoFile(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

# Definisco le impostazioni base del gioco (modificabili a patto che
# si aggiungano eventuali immagini e/o liste di parole).
def regoleDiGioco():
    #Numero di tentativi a disposizione dell'utente
    global tentativi 
    tentativi = 6

    #Parola che l'utente dovra' indovinare
    global parolaCasuale 
    parolaCasuale = list(random.choice(elencoParole)) 

    #Parola che verra' visualizzata all'utente
    global lettereIndovinate 
    lettereIndovinate = []
    for i in range(0, len(parolaCasuale)):
        lettereIndovinate.append('_ ')

    #Elenco di lettere errate
    global lettereSbagliate 
    lettereSbagliate = [] 

    #Numero di errori commessi dall'utente
    global erroriUtente 
    erroriUtente = 0 

def impostazioniBase():
    #Imposto la dimensione della schermata
    global width
    width = 800

    global height
    height = 600

    size = (width, height)
    
    #Definisco il bianco
    global bianco 
    bianco = (255, 255, 255)

    #Definisco il nero
    global nero 
    nero = (0, 0, 0)

    #Imposto le dimensioni precedentemente definite alla schermata
    global schermata 
    schermata = pygame.display.set_mode(size)

    #Imposto il nome da visualizzare
    pygame.display.set_caption("Impiccato")

    #Imposto il font
    global font 
    font = pygame.font.SysFont("Courier New", 30)

    #Lo utilizzo per renderizzare i caratteri alla schermata
    global testoSchermata 
    testoSchermata = {"saluto" :  font.render, "invio" : font.render, "parola selezionata" : font.render, 
                    "parola da indovinare" : font.render, "lettere sbagliate" : font.render, "indovina lettera" : font.render,
                    "messaggio vittoria" : font.render, "messaggio sconfitta" : font.render, "gioca di nuovo" : font.render,}

    #Associo ad ogni stringa una schermata
    global stringheSchermata
    stringheSchermata = {"benvenuto" : "schermataBenvenuto", "impiccato" : "schermataImpiccato", "vittoria" : "schermataVittoria",
                     "sconfitta" : "schermataSconfitta", "rigioca" : "schermataRigioca",}

    #Imposto un puntatore che mi permttera' di muovermi tra le schermate
    global puntatoreSchermata
    puntatoreSchermata = stringheSchermata["benvenuto"]

    #Ad ogni stringa associo un metodo
    global selezioneSchermata
    selezioneSchermata= {"schermataBenvenuto" : schermataBenvenuto, "schermataImpiccato" : schermataImpiccato, "schermataVittoria" : schermataVittoria,
                    "schermataSconfitta" : schermataSconfitta, "schermataRigioca" : schermataRigioca,}

    #Lo uso per inizializzare le impostazioni di gioco ad ogni nuova partita
    global flagSupporto
    flagSupporto = True

    #Lo utilizzo per non far ripetere la musica nella schermata finale
    global flagMusica
    flagMusica = True

# Metodo che mi server per accedere al vocabolario ed alle immagini
def caricamentoRisorse():
    fileParole = percorsoFile(os.path.join('Vocabolario', 'lista.txt'))

    global elencoParole 
    elencoParole = open(fileParole).readlines()
    elencoParole = [word.lower().rstrip("\n") for word in elencoParole]

    tentativo0 = pygame.image.load(os.path.join('Immagini', '0.png'))
    tentativo1 = pygame.image.load(os.path.join('Immagini', '1.png'))
    tentativo2 = pygame.image.load(os.path.join('Immagini', '2.png'))
    tentativo3 = pygame.image.load(os.path.join('Immagini', '3.png'))
    tentativo4 = pygame.image.load(os.path.join('Immagini', '4.png'))
    tentativo5 = pygame.image.load(os.path.join('Immagini', '5.png'))
    tentativo6 = pygame.image.load(os.path.join('Immagini', '6.png'))

    global disegnoImpiccato
    disegnoImpiccato = [tentativo0, tentativo1, tentativo2, tentativo3, tentativo4, tentativo5, tentativo6]

# Prima schermata, nella quale inizializzo il gioco e do il benvenuto all'utente
def schermataBenvenuto(event):
    global puntatoreSchermata
    global flagSupporto

    if flagSupporto: 
        regoleDiGioco()

    flagSupporto = False
    pygame.init()
    schermata.blit(testoSchermata["saluto"]("Benvenuto!", 1, bianco),(100,100))
        
    schermata.blit(testoSchermata["invio"]("Premi INVIO per continuare...", 1, bianco),(100,150))

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            puntatoreSchermata = stringheSchermata["impiccato"]

# Metodo che stampa e controlla se l'utente ha indovinato tutte le lettere
# Se non dovesse averlo fatto chiede un input
def schermataImpiccato(event):
    global puntatoreSchermata

    #Stampo la corretta immagine in base al numero di risposte errate
    stampaImpiccato()
    #Stampo l'elenco delle lettere indovinate
    stampaLettereIndovinate()
    #Stampo l'elenco delle lettere errate
    stampaLettereSbagliate()

    #Se l'utente ha vinto/perso mi sposto di schermata
    if lettereIndovinate == parolaCasuale:
        puntatoreSchermata = stringheSchermata["vittoria"]
  
    elif erroriUtente == tentativi:
        puntatoreSchermata = stringheSchermata["sconfitta"]

    else:
        chiediLettera()

        if event.type == pygame.KEYDOWN:

            if event.unicode.isalpha():

                letter = pygame.key.name(event.key)
        
                controlloLettera(letter)


# Se l'utente ha vinto faccio partire una musica e successivamente stampo un messaggio.
# Ha inoltre la possibilita' di giocare una nuova partita
def schermataVittoria(event):
    global puntatoreSchermata
    global flagMusica

    stampaImpiccato()

    #Senza questo controllo la musica si ripeterebbe all'infinito dato che siamo in un ciclo
    if flagMusica:
        musicaVittoria()

    flagMusica = False

    schermata.blit(testoSchermata["messaggio vittoria"]("CONGRATULAZIONI! HAI VINTO!", 1, bianco),(100,50))
    schermata.blit(testoSchermata["messaggio vittoria"]("La parola e' '" + ''.join(lettereIndovinate) + "'", 1, bianco),(100,100))
    schermata.blit(testoSchermata["invio"]("Premi SPAZIO per continuare...", 1, bianco),(100,150))


    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            puntatoreSchermata = stringheSchermata["rigioca"]

# Se l'utente ha perso faccio partire una musica e successivamente stampo un messaggio.
# Ha inoltre la possibilita' di giocare una nuova partita
def schermataSconfitta(event):
    global puntatoreSchermata
    global flagMusica

    stampaImpiccato()
    stampaLettereIndovinate()
    stampaLettereSbagliate()

    schermata.blit(testoSchermata["messaggio sconfitta"]("Game Over. La parola era '" + ''.join(parolaCasuale) + "'", 1, bianco),(100,50))
    schermata.blit(testoSchermata["invio"]("Premi SPAZIO per continuare...", 1, bianco),(100,100))

    # Senza questo controllo la musica si ripeterebbe all'infinito dato che siamo in un ciclo
    if flagMusica:
        musicaSconfitta()

    flagMusica = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            puntatoreSchermata = stringheSchermata["rigioca"]

# Schermata successiva alla vittoria/sconfitta, qui l'utente ha la possibilita'
# di chiudere il programma o di rigiocare
def schermataRigioca(event):
    global flagSupporto
    global puntatoreSchermata
    global flagMusica

    schermata.blit(testoSchermata["gioca di nuovo"]("Vuoi giocare di nuovo? S/N... ", 1, bianco),(width - 750, height - 100))

    if event.type == pygame.KEYDOWN:
        if event.unicode.isalpha():
            choice = pygame.key.name(event.key)
    
            if choice == "n" or choice == "N":
                sys.exit()
            #Mi preparo per inizializzare nuovamente il gioco
            flagSupporto = True
            flagMusica = True
            #Mi sposto in un'altra schermata
            puntatoreSchermata = stringheSchermata["benvenuto"]

# Attendo un input dall'utente
def chiediLettera():
    schermata.blit(testoSchermata["indovina lettera"]("Indovina una lettera: ", 1, bianco), (width - 750, height - 100))

# Stampo le lettere che non figurano nella parola estratta
def stampaLettereSbagliate():
    schermata.blit(testoSchermata["lettere sbagliate"](''.join(lettereSbagliate), 1, bianco), (width - 200, height - 100))

# Stampo le lettere indovinate dall'utente
def stampaLettereIndovinate():
    text = testoSchermata["parola da indovinare"](''.join(lettereIndovinate), 1, bianco)
    schermata.blit(text, [width / 2 - text.get_rect().width / 2, 150])

# Disegno l'impiccato in base al numero di errori dell'utente
def stampaImpiccato():
    schermata.blit(disegnoImpiccato[erroriUtente], [width / 2 - disegnoImpiccato[erroriUtente].get_rect().width / 2,
                  height / 2 - disegnoImpiccato[erroriUtente].get_rect().height / 2])

# Ripulisco la schermata
def pulisciSchermata():
    schermata.fill(nero)

# Aggiungo la lettere (sbagliata) estratta dall'utente alla relativa lista
def lettereEstratte(letter):
    lettereSbagliate.append(letter)

# Eseguo la musica in caso di vittoria
def musicaVittoria():
    pygame.mixer.music.load("Suoni/victory.mid")
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play()

# Eseguo la musica in caso di sconfitta
def musicaSconfitta():
    pygame.mixer.music.load("Suoni/gameover.mid")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()

# Controllo la lettera che ha scelto l'utente
def controlloLettera(letter):
    global erroriUtente

    indices = [i for i, x in enumerate(parolaCasuale) if x == letter]
    #Se non e' presente la aggiungo nella relativa lista e incremento gli errori
    if not indices:
        if letter not in lettereSbagliate:
            lettereEstratte(letter)
            erroriUtente += 1
    # Aggiungo la lettera estratta tra quelle indovinate
    for index in indices:
        lettereIndovinate[index] = letter


def main():
    pygame.init()
    pygame.font.init()

    caricamentoRisorse()
    impostazioniBase()

    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        pulisciSchermata()

        selezioneSchermata[puntatoreSchermata](event)

        pygame.display.flip()

if __name__ == '__main__': 
    main()