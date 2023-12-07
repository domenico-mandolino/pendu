# import pygame

# pygame.init()

# screen = pygame.display.set_mode((500, 500))

# running =True 

# image = pygame.image.load("")
# while running :
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
# pygame.quit()



# program pour choisir le mot au hasard de la liste
import random


mots = []
with open("mots.txt") as fl:
    for ligne in fl:
      mots.append(ligne.rstrip("\n"))
mot = random.choice(mots)

# les variables clefs
lettres = []
faux = 0
trouve = False
corp_plein = ["|", "O", "/", "|", "\\", "/", "\\"]
corp = [" "," "," "," "," "," "," "]

while not trouve:
    # une lettre
    trouve = True
    print("  +-----+   ")
    print("  |     {}  ".format(corp[0]))
    print("  |     {}  ".format(corp[1]))
    print("  |    {}{}{}".format(corp[2], corp[3], corp[4]))
    print("  |    {} {} ".format(corp[5], corp[6]))
    print("__|___      ")
   

    for l in mot:
       if l in lettres:
          print(l, end=" ")
       else:
        trouve = False
        print("_", end="")

    print()
    print("Lettres deja utilisés -", end="")
    for l in lettres:
       print(l,end="|")


    if faux > 6:
       print("Tu as perdu!")
       break


    if trouve:
        print("Tu as gagné")
        break

    lettre = input("Entrez une lettre: ")
    lettres.append(lettre)
    
    if lettre not in mot:
        corp[faux] = corp_plein[faux]
        faux +=1 
        
    # un mot?
    # Gagner/perdu/continuer
   

