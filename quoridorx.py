"module nécessaire a l'héritage"
import turtle
import quoridor

def tracerpolygone(ronnie, poly):
    "À l'aide de la tortue ronnie, tracer un polygone "
    ronnie.penup()
    ronnie.color('black')
    ronnie.width(3)
    ronnie.goto(poly[0])
    ronnie.pendown()
    for pos in poly[1:]:
        ronnie.goto(pos)

class QuoridorX(quoridor.Quoridor):
    """Ce module permet de faire l'affichage graphique du jeu Quoridor"""
    def __init__(self, joueurs, murs=None):
        """
        Initialiser une partie de Quoridor avec les joueurs et les murs spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        :param joueurs: un itérable de deux joueurs dont le premier est toujours celui qui
        débute la partie. Un joueur est soit une chaîne de caractères soit un dictionnaire.
        Dans le cas d'une chaîne, il s'agit du nom du joueur. Selon le rang du joueur dans
        l'itérable, sa position est soit (5,1) soit (5,9), et chaque joueur peut initialement
        placer 10 murs. Dans le cas où l'argument est un dictionnaire, celui-ci doit contenir
        une clé 'nom' identifiant le joueur, une clé 'murs' spécifiant le nombre de murs qu'il
        peut encore placer, et une clé 'pos' qui spécifie sa position (x, y) actuelle.

        :param murs: un dictionnaire contenant une clé 'horizontaux' associée à la liste des
        positions (x, y) des murs horizontaux, et une clé 'verticaux' associée à la liste des
        positions (x, y) des murs verticaux. Par défaut, il n'y a aucun mur placé sur le jeu.

        """
        super().__init__(joueurs, murs)
        joe = turtle.Turtle(visible=None)
        joe.shape(None)
        joe.speed(0)
        n = 35
        for c in range(10):
            tracerpolygone(joe, ((-(9-2*c)*n, -9*n), (-(9-2*c)*n, 9*n)))
            tracerpolygone(joe, ((9*n, -(9-2*c)*n), (-9*n, -(9-2*c)*n)))

        # Screen
        fen = turtle.Screen()
        fen.title('Jeu Quoridor')
        fen.bgcolor('grey')
        fen.setup(width=22*n, height=22*n)
        

        # Turtle : pierre, benoit et marc
        self.pierre = turtle.Turtle(shape='square')
        self.pierre.penup()
        self.pierre.shapesize(0.075*n)
        self.pierre.color('black')
        self.pierre.speed(0)
        self.pierre.right(90)
        self.pierre.forward(8*n)
        self.benoit = turtle.Turtle(shape='circle')
        self.benoit.penup()
        self.benoit.shapesize(0.075*n)
        self.benoit.color('black')
        self.benoit.speed(0)
        self.benoit.left(90)
        self.benoit.forward(8*n)
        self.marc = turtle.Turtle(visible=None)
        self.marc.penup()

        # Déplacement de marc
        for a in range(1, 10):
            self.marc.goto(-10*n+a*2*n, 9*n)
            self.marc.write(str(a), align='center', font=('arial', 27, 'bold'))
        for a in range(1, 10):
            self.marc.goto(-10*n, -11*n+3+2*n*a)
            self.marc.write(str(a), align='center', font=('arial', 27, 'bold'))
        self.afficher()

    def afficher(self):
        "permet d'afficher dans un fenetre graphique les actualisation du jeu"
        n = 35
        etat = self.état_partie()
        a = list(j for j in etat['joueurs'])

        # Positionnement des joueurs
        self.pierre.goto(-10*n + 2*n*(a[0]['pos'][0]), -10*n + 2*n*(a[0]['pos'][1]))
        self.benoit.goto(-10*n + 2*n*(a[1]['pos'][0]), -10*n + 2*n*(a[1]['pos'][1]))

        for mur in etat['murs']['horizontaux']:
            robert = turtle.Turtle(visible=None)
            robert.pensize(0.6*n)
            robert.speed(0)
            robert.pencolor('white')
            robert.penup()
            robert.goto(-10.5*n+2*n*mur[0], -11*n+2*n*mur[1])
            robert.pendown()
            robert.forward(3*n)

        for mur in etat['murs']['verticaux']:
            lucien = turtle.Turtle(visible=None)
            lucien.pensize(0.6*n)
            lucien.speed(0)
            lucien.pencolor('white')
            lucien.penup()
            lucien.goto(-11*n+2*n*mur[0], -10.5*n+2*n*mur[1])
            lucien.pendown()
            lucien.left(90)
            lucien.forward(3*n)
