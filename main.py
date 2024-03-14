"Argparse et api donne accès aux commandes qu'on a besoin"
import argparse
import api
import quoridor as Q
import quoridorx as x

def analyser_commande():
    "Initialise le argparse"
    parser = argparse.ArgumentParser(description='Jeu Quoridor - phase 1')
    parser.add_argument("-a", "--automatique", action="store_true",
                        help="Activer le mode automatique.")
    parser.add_argument("-x", "--graphique", action="store_true",
                        help="Activer le mode graphique.")
    parser.add_argument('idul', help="IDUL du joueur.")
    return parser.parse_args()

def partie_automatique(idul):
    "jouer une partie automatique"
    try:
        game = api.débuter_partie(idul)
    except RuntimeError as err:
        print(err)
    else:
        z = Q.Quoridor(game[1]['joueurs'], game[1]['murs'])
        print(z)
        idul = game[0]
        etat = game[1]
        while True:
            try:
                z = Q.Quoridor(etat['joueurs'], etat['murs'])
                pos = etat['joueurs'][0]['pos']
                mh = len(etat['murs']['horizontaux'])
                # Coup du joueur 1
                z.jouer_coup(1)
                jeu = z.état_partie()
                if pos == jeu['joueurs'][0]['pos']:
                    if mh == len(jeu['murs']['horizontaux']):
                        game = api.jouer_coup(idul, 'MV', jeu['murs']['verticaux'][-1])
                    else:
                        game = api.jouer_coup(idul, 'MH', jeu['murs']['horizontaux'][-1])
                else:
                    game = api.jouer_coup(idul, 'D', jeu['joueurs'][0]['pos'])

                # Affichage du damier
                z = Q.Quoridor(game['joueurs'], game['murs'])
                print(z)
                # Le nouvel etat de jeu est celui renvoyé par le serveur UL
                etat = game
            except Q.QuoridorError as err:
                print(err)
            except RuntimeError as err:
                print(err)
            except StopIteration as err:
                print(z)
                print(err)
                break

def partie_graphique(idul):
    "jouer une partie contre l'api en mode graphique"
    try:
        v = api.débuter_partie(idul)
    except RuntimeError as err:
        print(err)

    #Initialisation d'une classe Quoridorx et son affichage
    etatx = x.QuoridorX(v[1]['joueurs'], v[1]['murs'])
    etatx.afficher()
    cte = v[0]
    etat = v[1]
    while True:
        try:
            #Coup du joueur et de l'api
            type_coup = input('Veuillez choisir un type de coup (D, MH ou MV) : ')
            pos = input('Sélectionnez un point! (x, y) : ')
            etat = api.jouer_coup(cte, type_coup, pos)

            #puisque l'api a soulever les erreur s'il y avait une mauvaise
            #commande, il reste deux choix qu'on met en tuple
            if len(pos) == 6:
                posi = (int(pos[1]), int(pos[4]))
            else:
                posi = (int(pos[1]), int(pos[3]))

            #jouer le coup du joueur dans la classe Quoridorx
            #il est important de ne jamais initialiser de deuxieme classe Quoridorx
            #car le init crée une nouvelle planche de jeu
            if type_coup == 'D':
                etatx.déplacer_jeton(1, posi)
            elif type_coup == 'MH':
                etatx.placer_mur(1, posi, 'horizontal')
            elif type_coup == 'MV':
                etatx.placer_mur(1, posi, 'vertical')
            #jouer le coup de l'api dans la classe quoridor et l'afficher
            coup_api(etat, etatx)
        except StopIteration as err:
            print(err)
            break
        except Q.QuoridorError as err:
            print(err)
        except RuntimeError as err:
            print(err)

def partie_auto_graphique(idul):
    "jouer une partie automatique en mode graphique"
    try:
        v = api.débuter_partie(idul)
    except RuntimeError as err:
        print(err)
    #initialiser unc classe Quoridorx et l'afficher
    etatx = x.QuoridorX(v[1]['joueurs'], v[1]['murs'])
    etatx.afficher()
    cte = v[0]
    etat = v[1]
    while True:
        try:
            #jouer le coup de quoridorx et l'afficher
            pos = etat['joueurs'][0]['pos']
            mh = len(etat['murs']['horizontaux'])
            etatx.jouer_coup(1)
            etatx.afficher()
            #déterminer quel coup il a fait pour le faire dans L'api
            if pos == etatx.état_partie()['joueurs'][0]['pos']:
                if mh == len(etatx.état_partie()['murs']['horizontaux']):
                    etat = api.jouer_coup(cte, 'MV', etatx.état_partie()['murs']['verticaux'][-1])
                else:
                    etat = api.jouer_coup(cte, 'MH', etatx.état_partie()['murs']['horizontaux'][-1])
            else:
                etat = api.jouer_coup(cte, 'D', etatx.état_partie()['joueurs'][0]['pos'])
            #déterminer quel coup l'api a fait pour le faire faire a Quorridorx
            #il est important de ne jamais initialiser de deuxieme classe Quoridorx
            #car le init crée une nouvelle planche de jeu
            coup_api(etat, etatx)
        except StopIteration as err:
            print(err)
            break
        except Q.QuoridorError as err:
            print(err)
            break
        except RuntimeError as err:
            print(err)

def partie_ordinaire(idul):
    "jouer une partie contre l'api"
    try:
        game = api.débuter_partie(idul)
    except RuntimeError as err:
        print(err)
    else:
        print(Q.Quoridor(game[1]['joueurs'], game[1]['murs']))
        idul = game[0]
        while True:
            try:
                type_coup = input('Veuillez choisir un type de coup (D, MH ou MV) : ')
                pos = input('Sélectionnez un point! (x, y) : ')
                state = api.jouer_coup(idul, type_coup, pos)
                print(Q.Quoridor(state['joueurs'], state['murs']))
            except RuntimeError as err:
                print(err)
            except StopIteration as err:
                print(err)
                break

def coup_api(etat, etatx):
    "déterminer quel coup l'api a fait pour le faire faire a QuoridorX"
    pos = etat['joueurs'][1]['pos']
    mh = len(etat['murs']['horizontaux'])
    if pos == etatx.état_partie()['joueurs'][1]['pos']:
        if mh == len(etatx.état_partie()['murs']['horizontaux']):
            etatx.placer_mur(2, tuple(i for i in etat['murs']['verticaux'][-1]), 'vertical')
        else:
            pos = tuple(i for i in etat['murs']['horizontaux'][-1])
            etatx.placer_mur(2, pos, 'horizontal')
    else:
        etatx.déplacer_jeton(2, tuple(i for i in etat['joueurs'][1]['pos']))
    etatx.afficher()

if __name__ == "__main__":
    a = analyser_commande()
    b = a.idul
if a.automatique and a.graphique:
    partie_auto_graphique(b)
elif a.graphique:
    partie_graphique(b)
elif a.automatique:
    partie_automatique(b)
else:
    partie_ordinaire(b)

