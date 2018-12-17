# -*- coding:utf-8 -*-

############################################
# Title: Lykos (module de création de jeu) #
# Author: Simon Breil & Raphaël Castillo   #
# License: GPL                             #
############################################

# * Importations

from tkinter import * # Importe le module "tkinter" pour l'interface graphique du jeu

# * Déclarations

class Game(): # On crée la classe du jeu
    """
    Représente le jeu lui-même.
    • title : titre du jeu (facultatif)
    """
    def __init__(self, title="Kintermon"): # Initialisation de l'instance et de ses attributs
        self.fighters, self.moves, self.title = {}, {}, title # Affectation des attributs
        self.info = _GameState(self)
    def __repr__(self): # Représentation du jeu sous forme d'une chaîne de caractères (le titre "title" du jeu)
        return self.title # On retourne le titre "title" du jeu
    def _addFighter(self, fighter):
        self.fighters.update({fighter.name: fighter})
    def _addMove(self, move):
        self.moves.update({move.name: move})
    def _next(self):
        pass
    def endGame(self): # Met fin au jeu
        self.sendBanner("Fin du jeu", True) # On affiche le message de fin du jeu
        self.app.stop() # On arrête l'exécution du jeu

class Application():
    """
    Représente l'application du jeu.
    • game : objet jeu auquel l'application est lié
    • title : titre de l'application (facultatif)
    • icon : chemin (relatif ou absolu) vers l'icone au format ICO à afficher dans la barre d'application de la fenêtre (facultatif).
    (le titre de l'application sera égal au titre du jeu si non spécifié)
    """
    def __init__(self, game, title=None, icon="assets/favicon.ico"):
        width, height = 1080, 700 # Dimensions de la fenêtre
        self.title, self.icon, self.colorTheme = (title or game.title, icon, "#eeeeee")
        self.core = Tk() # Création de la fenêtre
        self.hide() # Masquage de la fenêtre
        self.core.title(self.title) # Définition de son titre
        self.core.geometry(str(width) + "x" + str(height)) # Définition de ses dimensions
        self.core.wm_resizable(False, False) # On empêche son redimensionnement
        self.core.config(bg=self.colorTheme)
        self._centerize(self.core, width, height)
        ### Création de l'interface ###
        self.fs = _FightScreen(self, game)
        ### Création de l'interface ###
        try:
            self.core.iconbitmap(icon)
        except IOError:
            print("Erreur lors de la recherche de l'icône.")
        game.app = self # On met l'application et le jeu en relation
    def splash(self, width=None, height=None, image="assets/splash.png", duration=2500, bg="black"):
        """
        Affiche un splash-screen customisable (formats pris en charge : XBM, PGM, PPM, GIF et PNG).
        • width : largeur du splash-screen en pixels (facultatif)
        • height : hauteur du splash-screen en pixels (facultatif)
        (la hauteur et la largeur s'adaptent en fonction des dimensions de l'image si non spécifiées)
        • image : chemin (relatif ou absolu) vers l'image à afficher (facultatif)
        • duration : durée de l'affichage du splash-screen en millisecondes (facultatif)
        • bg : couleur de l'arrière-plan du splash-screen
        """
        def closeSpl():
            self.spl.withdraw()
            self.spl.quit()
        try:
            splashFile = PhotoImage(file=image)
            self.spl = Toplevel()
            self._centerize(self.spl, width or splashFile.width(), height or splashFile.height())
            self.spl.overrideredirect(1) # Retire la barre d'application de la fenêtre
            self.spl.config(bg=bg)
            Label(master=self.spl, image=splashFile).place(x=-2, y=-2)
        except:
            print("Erreur : impossible de définir une image pour le splash-screen.")
        self.spl.after(duration, closeSpl)
        self.spl.mainloop()
    def _centerize(self, window, reqWidth=None, reqHeight=None):
        """
        Centre la fenêtre passée en argument.
        • window : objet fenêtre à centrer
        • reqWidth : largeur de la fenêtre à centrer (facultatif)
        • reqHeight : hauteur de la fenêtre à centrer (facultatif)
        (la plupart du temps, il n'est pas nécessaire de spécifier les dimensions de la fenêtre ; reqWidth et reqHeight peuvent cependant s'avérer utiles dans certains cas)
        """
        try:
            if (not reqWidth) or (not reqHeight):
                width, height = window.winfo_width(), window.winfo_height()
            else:
                width, height = reqWidth, reqHeight
            horPos, verPos = (window.winfo_screenwidth() - width) // 2, (window.winfo_screenheight() - height) // 2

            window.geometry(str(width) + "x" + str(height) + "+" + str(horPos) + "+" + str(verPos))
        except:
            print("Échec lors de la tentative de centrage de l'objet fenêtre.")
    def setColor(self, color):
        """
        Définit la couleur d'arrière-plan de l'application.
        • color : couleur de l'arrière-plan
        """
        self.colorTheme = color
        self.core.config(bg=color)
    @property
    def width(self):
        "Retourne la largeur en pixels de la fenêtre d'application."
        return self.core.winfo_width()
    @property
    def height(self):
        "Retourne la hauteur en pixels de la fenêtre d'application."
        return self.core.winfo_height()
    def show(self):
        "Ré-affiche la fenêtre d'application dans le cas où elle n'était pas visible avant."
        self.core.deiconify()
    def hide(self):
        "Masque la fenêtre d'application sans terminer son processus d'exécution."
        self.core.withdraw()
    def start(self):
        "Lance l'application ainsi que son gestionnaire d'évènements."
        self.show()
        self.core.lift()
        self.core.mainloop()
    def stop(self):
        "Termine le processus d'exécution de l'application."
        self.core.destroy()

class _Interface():
    """
    Représente l'interface du jeu.
    """
    def __init__(self, game):
        pass

class _GameState():
    """
    Représente l'ensemble des informations en temps réel concernant le jeu.
    • game : jeu auquel est liée la base d'informations

    +--------------------------+
    | Informations disponibles |
    +--------------------------+

    -> numRound : numéro du tour actuel. Se réinitialise à la fin de chaque combat.
    -> turn : booléen indiquant si c'est le tour du deuxième combattant (celui de droite) ou non.
    (en cours d'écriture...)
    """
    def __init__(self, game):
        self.game = game

        ### Infos de jeu ###

        self.numRound = 0
        self.turn = False # Quand il s'agit du deuxième combattant (combattant de droite), "turn" devient True.

        ### Infos de jeu ###

class _FightScreen():
    """
    Représente l'écran de combat. Systématiquement créé à l'appel de la méthode Application.start() et accessible depuis l'attribut Application.fs.
    Dimensions : 700x350 pixels.
    • app : application à laquelle est lié l'écran de combat.
    • game : jeu auquel l'écran de combat est lié.
    """
    def __init__(self, app, game):
        self.master = app.core
        self.game = game
        self.content = Canvas(self.master, width=700, height=350, bd=2, relief="solid")
        self.fighters = [None, None]
        can = self.content
        can.place(x=0, y=0)
        self.setBackground("assets/background.png")
    def create(self, fighter, isEnemy=False):
        """
        Ajoute un combattant à l'écran de jeu.
        • fighter : objet combattant à ajouter
        • isEnemy : booléen qui détermine le rôle du combattant (adversaire ou non) (facultatif)
        """
        self.fighters[isEnemy] = fighter # On ajoute le combattant à la liste des combattants sur l'écran
        if fighter.sprite.width() > 150:
            fighter.sprite = self._scaleToWidth(fighter.sprite, 150)
        spriteWidth = fighter.sprite.width()
        x, y = 550 if isEnemy else spriteWidth, 300
        f, c = self.fighters[isEnemy], self.content

        ### Dessins ###

        f.gItems.update({"shadow": c.create_oval(x - spriteWidth / 2, y - 15, x + spriteWidth / 2, y + 15, fill="black", outline=None)}) # Dessin de l'ombre
        f.gItems.update({"sprite": c.create_image(x, y, image=f.sprite, anchor=S)}) # Dessin du sprite       
        f.gItems.update({"LifeBarBg": c.create_rectangle(x - spriteWidth / 2, y-200, x + spriteWidth / 2, y -185, fill= "red", width = 3) })  # Fond barre HP
        f.gItems.update({"LifeBar": c.create_rectangle(x - spriteWidth / 2, y-200, x + spriteWidth / 3, y-185, fill = "#45CF8B", width=0)}) # Création de la barre de vie 
        # ? Ajouter barre de vie, stats, etc.

        ### Dessins ###

    def _scaleToWidth(self, image, width):
        """
        Redimensionne sur place l'objet image passé en argument à la largeur (en pixels) passée elle aussi en argument.
        • image : objet image à redimensionner (et non le chemin !)
        • width : largeur (en pixels) souhaitée
        """
        try:
            oldWidth = image.width()
            newImage = image.zoom(width // 10)
            newImage = newImage.subsample(oldWidth // 10)
            return newImage
        except:
            print("Erreur : mémoire tampon insuffisante.")
            return image
    def setBackground(self, image):
        """
        Redéfinit l'arrière-plan de l'écran de jeu.
        • image : chemin (relatif ou absolu) vers l'image à définir en tant qu'arrière-plan
        """
        self.background = PhotoImage(file=image)
        bg = self.content.create_image(4, 4, image=self.background, anchor=NW)
        self.content.lower(bg)

class Fighter():
    """
    Représente un combattant.
    • game : jeu duquel vient le combattant
    • name : nom que porte le combattant
    • moves : liste (dont la longueur est égale à 4) des capacités que peut utiliser le combattant (facultatif)
    • sprite : objet image qui représente le combattant (facultatif)
    • stats : dictionnaire des quatres caractéristiques du combattant (facultatif), à savoir : les points de vie "HP", l'attaque "ATK", la défense "DEF" et la vitesse d'attaque "SPD". Ces caractéristiques sont à 100 par défaut.
    """
    def __init__(self, game, name, moves=None, sprite="assets/sprite_error.png", stats={"HP": 100, "ATK": 100, "DEF": 100, "SPD": 100}):
        self.game, self.name, self.moves, self.stats = (game, name, moves, stats)
        self.game._addFighter(self)
        self.gItems = {}
        try:
            self.sprite = PhotoImage(file=sprite)
        except:
            self.sprite = PhotoImage(file="assets/sprite_error.png")
            
class Move():
    """
    Représente une capacité.
    • game : jeu duquel vient la capacité
    • name : nom que porte la capacité
    • description : description de la capacité
    • action : action que réalise la capacité
    • pu : nombre maximal d'utilisations de la capacité
    • sprite : chemin (relatif ou absolu) vers l'image à définir en tant qu'arrière-plan
    """
    def __init__(self, game, name, description, action, pu, image):
        self.name, self.game, self.description, self.action, self.pu, self.image = (name, game, description, action, pu, image)
        self.game._addMove(self)
