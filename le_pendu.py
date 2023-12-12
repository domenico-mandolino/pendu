import pygame
import sys
import random

pygame.init()

largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu du Pendu")

blanc = (255, 255, 255)
noir = (0, 0, 0)

police = pygame.font.Font(None, 36)

mots = []
with open("mots.txt") as fl:
    for ligne in fl:
        mots.append(ligne.rstrip("\n"))

images_pendu = [pygame.image.load(f"images_pendu/{i}.png") for i in range(8)]
taille_images_pendu = (largeur // 3, hauteur)
images_pendu_redimensionnees = [pygame.transform.scale(img, taille_images_pendu) for img in images_pendu]

bouton_play = pygame.image.load("images/play.png")
bouton_menu = pygame.image.load("images/menu.png")
bouton_music_on = pygame.image.load("images/music-on.png")
bouton_music_off = pygame.image.load("images/music-off.png")

# Charger l'image de victoire et la redimensionner
image_victoire = pygame.image.load("images_pendu/7bis.png")
image_victoire = pygame.transform.scale(image_victoire, taille_images_pendu)

# Charger la musique
pygame.mixer.music.load("musique/Forest Interlude - Donkey Kong Country 2 (SNES) Music Extended.mp3")
pygame.mixer.music.set_volume(0.5)  # Ajuster le volume si nécessaire

def choisir_mot():
    return random.choice(mots).upper()

def afficher_mot_cache(mot, lettres_trouvees):
    affichage = ''
    for lettre in mot:
        if lettre in lettres_trouvees:
            affichage += lettre + ' '
        else:
            affichage += '_ '
    return affichage.strip()

def jouer_pendu(difficulte):
    music_playing = True
    pygame.mixer.music.play(-1)  # Démarrer la musique en continu
    mot_a_deviner = choisir_mot()
    lettres_trouvees = set()
    lettres_utilisees = set()

    faux = 0

    running = True
    while running:
        fenetre.fill(noir)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                lettre = event.unicode.upper()
                if lettre.isalpha() and lettre not in lettres_utilisees:
                    lettres_utilisees.add(lettre)
                    if lettre in mot_a_deviner:
                        lettres_trouvees.add(lettre)
                    else:
                        faux += 1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if 0 <= x <= largeur // 3 and 0 <= y <= hauteur:
                    mot_a_deviner = choisir_mot()
                    lettres_trouvees = set()
                    lettres_utilisees = set()
                    faux = 0

                elif largeur // 3 <= x <= 2 * (largeur // 3) and 0 <= y <= hauteur:
                    running = False

                # Gestion du bouton de musique
                elif largeur - bouton_music_on.get_width() <= x <= largeur and 0 <= y <= bouton_music_on.get_height():
                    if music_playing:
                        pygame.mixer.music.stop()
                        fenetre.blit(bouton_music_off, (largeur - bouton_music_off.get_width(), 0))
                        music_playing = False
                    else:
                        pygame.mixer.music.play(-1)  # -1 pour répéter en continu
                        fenetre.blit(bouton_music_on, (largeur - bouton_music_on.get_width(), 0))
                        music_playing = True
                elif set(mot_a_deviner) == lettres_trouvees:
                    fenetre.blit(image_victoire, (0, 0))  # Afficher l'image spéciale de la victoire

        mot_affiche = afficher_mot_cache(mot_a_deviner, lettres_utilisees)
        texte_mot = police.render(mot_affiche, True, blanc)
        fenetre.blit(texte_mot, (largeur // 3, hauteur // 2 - texte_mot.get_height() // 2))

        texte_utilisees = police.render(f"Lettres utilisées: {' '.join(lettres_utilisees)}", True, blanc)
        fenetre.blit(texte_utilisees, (largeur // 3, hauteur // 2 + 50))

        if faux < len(images_pendu_redimensionnees):
            fenetre.blit(images_pendu_redimensionnees[faux], (0, 0))
        else:
            fenetre.blit(images_pendu_redimensionnees[-1], (0, 0))

        # Afficher les boutons "Play" et "Menu" en bas de l'écran
        fenetre.blit(bouton_play, (largeur // 5, hauteur - bouton_play.get_height()))
        fenetre.blit(bouton_menu, (3 * largeur // 5, hauteur - bouton_menu.get_height()))
        # Afficher le bouton de musique
        fenetre.blit(bouton_music_on, (largeur - bouton_music_on.get_width(), 0))

        pygame.display.flip()


    # Arrêter la musique lorsque la partie est terminée
    pygame.mixer.music.stop()

    return rectangles_options

def afficher_menu():
    fenetre.fill(noir)

    titre = police.render("Le Pendu:", True, blanc)
    fenetre.blit(titre, (largeur // 2 - titre.get_width() // 2, 50))

    options = ["Jouer", "Insérer un mot dans mots.txt", "Afficher le tableau des scores", "Quitter"]
    y_position = 150
    rectangles_options = []

    for option in options:
        texte_option = police.render(option, True, blanc)
        rect_option = texte_option.get_rect(center=(largeur // 2, y_position))
        fenetre.blit(texte_option, rect_option)
        rectangles_options.append(rect_option)
        y_position += 50

    pygame.display.flip()

    return rectangles_options

running = True

while running:
    rectangles_options = afficher_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect_option in enumerate(rectangles_options):
                if rect_option.collidepoint(event.pos):
                    if i == 0:
                        jouer_pendu("facile")
                    elif i == 1:
                        nouveau_mot = input("Entrez un nouveau mot à ajouter au fichier 'mots.txt': ").upper()
                        with open('mots.txt', 'a') as fichier:
                            fichier.write('\n' + nouveau_mot)
                    elif i == 2:
                        print("Afficher le tableau des scores")
                        afficher_scores()
                    elif i == 3:
                        running = False

pygame.quit()
sys.exit()








# import pygame
# import sys

# pygame.init()
# # pygame.time.clock()
# screen = pygame.display.set_mode((800, 600))
# my_surface = pygame.surface((800, 600))
# pygame.display.set_caption("Jeu du Pendu")
# timer = pygame.time.Clock()
# fond = pygame.image.load("/images/chalk-board.jpg")
# game_on = True


# # image = pygame.image.load("")
# while game_on:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             # game_on = False
#             pygame.quit()
#             sys.exit()
#     screen.fill(pygame.image;())
#     screen.blit(my_surface, (800,600))       
#     pygame.display.update()
#     timer.tick(60)


# #choisir le mot au hasard de la liste
# import random


# mots = []
# with open("mots.txt") as fl:
#     for ligne in fl:
#       mots.append(ligne.rstrip("\n"))
# mot = random.choice(mots)

# # les variables clefs
# lettres = []
# faux = 0
# trouve = False
# corp_plein = ["|", "O", "/", "|", "\\", "/", "\\"]
# corp = [" "," "," "," "," "," "," "]

# while not trouve:
#     # une lettre
#     trouve = True
#     print("  +-----+   ")
#     print("  |     {}  ".format(corp[0]))
#     print("  |     {}  ".format(corp[1]))
#     print("  |    {}{}{}".format(corp[2], corp[3], corp[4]))
#     print("  |    {} {} ".format(corp[5], corp[6]))
#     print("__|___      ")
   

#     for l in mot:
#        if l in lettres:
#           print(l, end=" ")
#        else:
#         trouve = False
#         print("_", end="")

#     print()
#     print("Lettres deja utilisés -", end="")
#     for l in lettres:
#        print(l,end="|")


#     if faux > 6:
#        print("Tu as perdu!")
#        break


#     if trouve:
#         print("Tu as gagné")
#         break

#     lettre = input("Entrez une lettre: ")
#     lettres.append(lettre)
    
#     if lettre not in mot:
#         corp[faux] = corp_plein[faux]
#         faux +=1 
        
#     # un mot?
#     # Gagner/perdu/continuer


# # Charger les mots depuis le fichier
# mots = []
# with open("mots.txt") as fl:
#     for ligne in fl:
#         mots.append(ligne.rstrip("\n"))
# mot = random.choice(mots)

# # Initialiser les variables clés
# lettres = set()
# faux = 0
# trouve = False
# corp_plein = ["|", "O", "/", "|", "\\", "/", "\\"]
# corp = [" "," "," "," "," "," "," "]

# while not trouve and faux < 6:
#     # Afficher l'image de fond
#     screen.blit(fond, (0, 0))

#     # ... (le reste du code reste inchangé)

#     pygame.display.update()

#     # Gestion des événements
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         elif event.type == pygame.KEYDOWN:
#             lettre = event.unicode.upper()
#             if lettre.isalpha() and lettre not in lettres:
#                 lettres.add(lettre)
#                 if lettre not in mot:
#                     faux += 1

#     # Vérifier si le mot a été trouvé
#     trouve = all(lettre in lettres for lettre in mot)

# # Afficher le résultat



