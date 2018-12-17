# -*- coding:utf-8 -*-

#############################################
#  Title: Kintermon (jeu de démonstration)  #
#  Author: Simon Breil & Raphaël Castillo   #
#  License: GPL                             #
#############################################

# * Importations

from lykos import *
# * Déclarations

game = Game()
app = Application(game)

app.splash() 

charmander = Fighter(game, "Salamèche", None, "assets/charmander.png")
pikachu = Fighter(game, "Pikachu", None, "assets/pikachu.png")

app.fs.create(charmander)
app.fs.create(pikachu, isEnemy=True)

app.start()