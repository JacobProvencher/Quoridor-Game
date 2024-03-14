import argparse
import turtle
import quoridor as qdor
def analyser_commande():
    
    #Pour analyser la ligne de commande

    parser = argparse.ArgumentParser(description="Jeu Quoridor - phase3")
    parser.add_argument('-l', '--lister',
                       help="Lister les identifiants de vos 20 dernières parties.", action="store_true")
    parser.add_argument("-a", action="store_true", help="pour jouer en mode automatique contre le serveur avec le nom idul")
    parser.add_argument("-x", action="store_true", help="pour jouer en mode manuel contre le serveur avec le nom idul, mais avec un affichage dans une fenêtre graphique")
    parser.add_argument('idul', help="IDUL du joueur.")
    parser.add_argument("-ax", action="store_true", help="pour jouer en mode automatique contre le serveur avec le nom idul, mais avec un affichage dans une fenêtre graphique")
    return parser.parse_args()
b = analyser_commande()
if b.ax:
    print('jeux automatique avec affichage graphique')
       

    screen = turtle.Screen()
    screen.title("Jeu Quoridor")
    screen.setup(width=385, height=385)
    screen.reset()
    screen.setworldcoordinates(-1, 0, 20, 20)
    screen.bgcolor('grey')

    tuile = turtle.Turtle()
    tuile.shape('square')
    tuile.color('black')
    tuile.shapesize(1.3, 1.3, 1)
    tuile.speed(0)
    tuile.penup()
    damier = [(x, y) for x in range(1, 18, 2) for y in range(1, 18, 2)]

    for x, y in damier:
        tuile.goto(x, y)
        tuile.stamp()


    # player
    player = turtle.Turtle()
    player.penup()
    player.hideturtle()
    player.goto(5*2-1, 1*2-1)
    player.speed(0)
    player.shape('circle')
    player.color('red')
    # opponent
    oppo = turtle.Turtle()
    oppo.penup()
    oppo.hideturtle()
    oppo.goto(5*2-1, 9*2-1)
    oppo.speed(0)
    oppo.shape('square')
    oppo.color('blue')
    # Murs horizontaux
    mh = turtle.Turtle()
    mh.pencolor('yellow')
    mh.pensize(10)
    mh.hideturtle()
    mh.penup()
    mh.speed(0)
    # Murs verticaux
    mv = turtle.Turtle()
    mv.pencolor('yellow')
    mv.pensize(10)
    mv.hideturtle()
    mv.penup()
    mv.speed(0)

    player.showturtle(); oppo.showturtle()

    def afficher(etat):
        joueurs = [joueur['pos'] for joueur in etat['joueurs']]
        murh, murv = etat['murs']['horizontaux'], etat['murs']['verticaux']
        # Position des joueurs
        player.goto(joueurs[0][0]*2-1, joueurs[0][1]*2-1)
        oppo.goto(joueurs[1][0]*2-1, joueurs[1][1]*2-1)
        # Murs horizontaux
        # Cela ne peut pas rester comme ca puisque ca ne permet
        # pas de commencer une partie avec un damier prédéfini
        if len(murh) > 0:
            x, y = murh[-1]
            mh.goto(x*2-1.5, y*2-2)
            mh.pendown()
            mh.goto(x*2+1.5, y*2-2)
            mh.penup()
        else:
            for x, y in murh:
                mh.goto(x*2-1.5, y*2-2)
                mh.pendown()
                mh.goto(x*2+1.5, y*2-2)
                mh.penup()
        # Murs verticaux
        # Cela ne peut pas rester comme ca puisque ca ne permet
        # pas de commencer une partie avec un damier prédéfini
        if len(murv) > 0:
            x, y = murv[-1]
            mv.goto(x*2-2, y*2-1.5)
            mv.pendown()
            mv.goto(x*2-2, y*2+1.5)
            mv.penup()
        else:
            for x, y in murv:
                mv.goto(x*2-2, y*2-1.5)
                mv.pendown()
                mv.goto(x*2-2, y*2+1.5)
                mv.penup()
    game = qdor.Quoridor(['Pascal', 'Jacob'])
    afficher(game.état_partie())
    joueur = 1
    while True:
        game.jouer_coup(joueur)
        afficher(game.état_partie())
        if game.partie_terminée():
            winner = game.partie_terminée()
            print(f'Le gagnant est {winner}!')
            break
        joueur = joueur % 2 + 1
    turtle.mainloop()
elif b.x:
    print('jeux manuel affichage graphique')

elif b.a:
    print('jeux automatique sans affichage graphique')
else:
    print('jeu  manuel avec le serveur')
    #essai de commit