"""Ce module permet de joueur au jeu Quoridor"""
import random
import networkx as nx


def init_planche_mur(graphe, murs_horizontaux, murs_verticaux):
    '''initialise la planche de jeu avec les murs
    dans le graphe'''

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

     # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    return graphe

def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.

    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    graphe = init_planche_mur(graphe, murs_horizontaux, murs_verticaux)

    # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
    j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])

    # traiter le cas des joueurs adjacents
    if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

        # retirer les liens entre les joueurs
        graphe.remove_edge(j1, j2)
        graphe.remove_edge(j2, j1)

        def ajouter_lien_sauteur(noeud, voisin):
            """
            :param noeud: noeud de départ du lien.
            :param voisin: voisin par dessus lequel il faut sauter.
            """
            saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]

            if saut in graphe.successors(voisin):
                # ajouter le saut en ligne droite
                graphe.add_edge(noeud, saut)

            else:
                # ajouter les sauts en diagonale
                for saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)

        ajouter_lien_sauteur(j1, j2)
        ajouter_lien_sauteur(j2, j1)

    # ajouter les destinations finales des joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe

def coup(murs):
    """Retourne un dictionnaire contenant quatres clés auxquelles sont associés
    une liste ou un ensemble des coups valides ou invalides pour les positions
    horizontales ou verticales d'un mur pour l'état actuel.
    Accepte en argument le dictionnaire des murs."""
    # Toutes les positions valides pour le placement d'un mur horizontal ou vertical
    valid_h = {(x, y) for x in range(1, 9) for y in range(2, 10)}
    valid_v = {(x, y) for x in range(2, 10) for y in range(1, 9)}
    # Deux ensembles de positions invalides pour placement de mur horizontal et vertical
    invalid_h, invalid_v = set(), set()
    for x, y in murs['horizontaux']:
        invalid_h.add((x+1, y))
        invalid_h.add((x-1, y))
        invalid_v.add((x+1, y-1))
    for x, y in murs['verticaux']:
        invalid_v.add((x, y+1))
        invalid_v.add((x, y-1))
        invalid_h.add((x-1, y+1))
    invalid_h |= set(map(tuple, murs['horizontaux']))
    invalid_v |= set(map(tuple, murs['verticaux']))
    # La différence entre toutes les positions valides et
    # invalides retourne les positions valides restantes
    valid_h, valid_v = list(valid_h - invalid_h), list(valid_v - invalid_v)
    random.shuffle(valid_h)
    random.shuffle(valid_v)

    return {'valid_h':valid_h, 'valid_v':valid_v, 'invalid_h':invalid_h, 'invalid_v':invalid_v}

def shortest_path(graphe, positions, joueur):
    """Retourne un dictionnaire contenant le shortest_path pour les deux joueurs
    pour un état de jeu.
    Accepte en argument le graphe, leurs positions et un joueur"""
    player = nx.shortest_path(graphe, tuple(positions[joueur - 1]), 'B'+str(joueur))
    oppo = nx.shortest_path(graphe, tuple(positions[joueur % 2]), 'B'+str(joueur % 2 + 1))

    return {'player': player, 'oppo': oppo}


class QuoridorError(Exception):
    """Cette classe créer un nouveau type d'erreur, soit QuoridorError"""


class Quoridor:
    """Classe permettant d'afficher le damier
    ainsi que de jouer au jeu Quoridor tout en respectant les
    règles du jeu."""

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
        # si joueurs n'est pas itérable.
        if not hasattr(joueurs, '__iter__'):
            raise QuoridorError("L'argument 'joueurs' n'est pas un itérable.")

        # si l'itérable de joueurs en contient plus de deux.
        elif len(joueurs) != 2:
            message = "L'itérable de joueurs en contient un nombre différent de deux."
            raise QuoridorError(message)

        # Les deux joueurs sont des strings
        elif isinstance(joueurs[0], str) and isinstance(joueurs[1], str):
            self.etat = {"joueurs":[{"nom": joueurs[0], "murs": 10, "pos": [5, 1]},
                                    {"nom": joueurs[1], "murs": 10, "pos": [5, 9]}],
                         "murs": {"horizontaux": [], "verticaux": []}}

        # Les deux joueurs sont des dictionnaires
        elif isinstance(joueurs[0], dict) and isinstance(joueurs[1], dict):
            self.etat = {"joueurs":joueurs, "murs":murs}
            # Tests pour les infos de 'murs
            self.__tester_murs()
        else:
            raise QuoridorError("MESSAGE")

        # Tests pour les infos de 'joueurs'
        joueurs = [user['pos'] for user in self.etat['joueurs']]
        for user in self.etat['joueurs']:
            # si le nombre de murs qu'un joueur peut placer est >10, ou négatif.
            if not 0 <= user['murs'] <= 10:
                message = "Le nombre de murs qu'un joueur peut placer est >10, ou négatif."
                raise QuoridorError(message)
            # si la position d'un joueur est invalide.
            elif not 1 <= user['pos'][0] <= 9 or not 1 <= user['pos'][1] <= 9 or \
                joueurs[0] == joueurs[1]:
                raise QuoridorError("La position d'un joueur est invalide.")

    def __tester_murs(self):
        """
        Teste si les infos de 'murs' sont valides.
        """
        # si murs n'est pas un dictionnaire lorsque présent.
        if self.etat.get('murs'):
            if not isinstance(self.etat['murs'], dict):
                raise QuoridorError("L'argument 'murs' n'est pas un dictionnaire.")

        # si le total des murs placés et plaçables n'est pas égal à 20.
        murs_dispo = self.etat['joueurs'][0]['murs'] + self.etat['joueurs'][1]['murs']
        murs_on = len(self.etat['murs']['horizontaux']) + len(self.etat['murs']['verticaux'])
        if murs_dispo + murs_on != 20:
            raise QuoridorError("La somme des murs placés et plaçables n'est pas égale à 20.")

        # si la position d'un mur est invalide.
        walls_future = {'horizontaux':[], 'verticaux':[]}
        walls_now = {'horizontaux':[], 'verticaux':[]}
        joueurs = [user['pos'] for user in self.etat['joueurs']]

        for x, y in self.etat['murs']['horizontaux']:

            if not 1 <= x <= 8 or not 2 <= y <= 9:
                raise QuoridorError("La position d'un mur est invalide.")

            # la position d'un mur ne respecte pas les règles du jeu
            if (x, y) in coup(walls_now)['invalid_h']:
                raise QuoridorError("La position d'un mur est invalide.")

            # Un mur enferme un joueur
            walls_future['horizontaux'].append([x, y])
            graphe = construire_graphe(joueurs, walls_future['horizontaux'],
                                       walls_future['verticaux'])
            if self.__nopath(graphe):
                raise QuoridorError("La position d'un mur est invalide.")

            walls_now['horizontaux'].append([x, y])

        for x, y in self.etat['murs']['verticaux']:

            # la position d'un mur est invalide
            if not 2 <= x <= 9 or not 1 <= y <= 8:
                raise QuoridorError("La position d'un mur est invalide.")

            # la position d'un mur ne respecte pas les règles du jeu
            if (x, y) in coup(walls_now)['invalid_v']:
                raise QuoridorError("La position d'un mur est invalide.")

            # Un mur enferme un joueur
            walls_future['verticaux'].append([x, y])
            graphe = construire_graphe(joueurs, walls_future['horizontaux'],
                                       walls_future['verticaux'])
            if self.__nopath(graphe):
                raise QuoridorError("La position d'un mur est invalide.")

            walls_now['verticaux'].append([x, y])

    def __str__(self):
        """
        Produire la représentation en art ascii correspondant à l'état actuel de la partie.
        Cette représentation est la même que celle du TP précédent.

        :returns: la chaîne de caractères de la représentation.
        """
        # Construction du damier
        d1 = [[' ' for _ in range(39)] for _ in range(17)]
        for i, ligne in enumerate(d1[::2]):
            ligne[0] = str(9 - i)
            for n in range(4, 39, 4):
                ligne[n] = '.'
        d2 = []
        for ligne in d1:
            ligne[2] = ligne[38] = '|'
            d2 += ligne + ['\n']

        # Position des joueurs
        for i in range(2):
            x, y = self.etat['joueurs'][i]['pos']
            d2[40*(18-2*y)+4*x] = str(i+1)

        # Murs horizontaux
        for x, y in self.etat['murs']['horizontaux']:
            for i in range(7):
                d2[40*(19-2*y)+4*x-1 + i] = '-'

        # Murs verticaux
        for x, y in self.etat['murs']['verticaux']:
            index = 40*(18-2*y)+4*x-2
            d2[index] = d2[index - 40] = d2[index - 2*40] = '|'

        # Affiche du damier
        name1, name2 = self.etat['joueurs'][0]['nom'], self.etat['joueurs'][1]['nom']
        deb0 = ['Légende: ', f'1={name1}, ',
                f'2={name2}', '\n', '   ', '-'*35, '\n']
        end0 = ['--|', '-'*35, '\n', '  | ', '   '.join(str(n) for n in range(1, 10))]

        return ''.join(deb0 + d2 + end0)

    def déplacer_jeton(self, joueur, position: tuple):
        """
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).
        """
        users = [user['pos'] for user in self.etat['joueurs']]
        graphe = construire_graphe(users, self.etat['murs']['horizontaux'],
                                   self.etat['murs']['verticaux'])

        # Traitement des erreurs #
        # le numéro du joueur est autre que 1 ou 2.
        if joueur not in [1, 2]:
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")

        # la position est invalide (en dehors du damier).
        if not 1 <= position[0] <= 9 or not 1 <= position[1] <= 9:
            raise QuoridorError("La position est invalide.")

        # la position est invalide pour l'état actuel du jeu.
        if position not in list(graphe.successors(tuple((self.etat['joueurs'][joueur-1]['pos'])))):
            raise QuoridorError("La position est invalide pour l'état actuel du jeu.")

        self.etat['joueurs'][joueur-1]['pos'] = list(position)

    def état_partie(self):
        """
        Produire l'état actuel de la partie.

        :returns: une copie de l'état actuel du jeu sous la forme d'un dictionnaire:
        """
        return self.etat

    def jouer_coup(self, joueur):
        """
        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        """
        users = [user['pos'] for user in self.etat['joueurs']]
        mh, mv = self.etat['murs']['horizontaux'], self.etat['murs']['verticaux']
        graphe = construire_graphe(users, mh, mv)

        # Traitement des erreurs #
        # le numéro du joueur est autre que 1 ou 2.
        if joueur not in [1, 2]:
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")

        if not self.partie_terminée():

            path_now = shortest_path(graphe, users, joueur)
            # Si le joueur a un ou des coups d'avance sur son adverdsaire
            # ou qu'il ne lui reste aucun mur, se déplacer
            nb_murs = self.etat['joueurs'][joueur - 1]['murs']
            if len(path_now['player']) < len(path_now['oppo']) or nb_murs <= 0:
                self.déplacer_jeton(joueur, path_now['player'][1])
            # Autrement, place un mur ou avance en cas de doute
            else:
                besth = self.__meilleur_mur_h(joueur, path_now)
                bestv = self.__meilleur_mur_v(joueur, path_now)
                if besth[0] > bestv[0]:
                    self.placer_mur(joueur, besth[1], 'horizontal')
                elif besth[0] == bestv[0]:
                    self.déplacer_jeton(joueur, path_now['player'][1])
                else:
                    self.placer_mur(joueur, bestv[1], 'vertical')

        # la partie est déjà terminée.
        else:
            raise QuoridorError("La partie est déjà terminée")

    def partie_terminée(self):
        """
        Déterminer si la partie est terminée.

        :returns: le nom du gagnant si la partie est terminée; False autrement.
        """
        if self.etat['joueurs'][0]['pos'][1] == 9:
            return self.etat['joueurs'][0]['nom']
        if self.etat['joueurs'][1]['pos'][1] == 1:
            return self.etat['joueurs'][1]['nom']
        return False

    def placer_mur(self, joueur: int, position: tuple, orientation: str):
        """
        Pour le joueur spécifié, placer un mur à la position spécifiée.

        :param joueur: le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du mur.
        :param orientation: l'orientation du mur ('horizontal' ou 'vertical').
        """
        users = [user['pos'] for user in self.etat['joueurs']]
        mh, mv = self.etat['murs']['horizontaux'], self.etat['murs']['verticaux']

        # Traitement des erreurs #
        # le numéro du joueur est autre que 1 ou 2.
        if joueur not in [1, 2]:
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")

        # le joueur a déjà placé tous ses murs.
        if self.etat['joueurs'][joueur-1]['murs'] <= 0:
            raise QuoridorError("Le joueur a déjà placé tous ses murs.")

        if orientation == 'horizontal':

            # la position est invalide pour cette orientation.
            if not 1 <= position[0] <= 8 or not 2 <= position[1] <= 9:
                raise QuoridorError("La position est invalide pour cette orientation.")

            # un mur occupe déjà cette position.
            if position in coup(self.etat['murs'])['invalid_h']:
                raise QuoridorError("Un mur occupe déjà cette position.")

            mh.append(list(position))

            # il n'y pas de chemin jusqu'au target
            if self.__nopath(construire_graphe(users, mh, mv)):
                mh.pop()
                raise QuoridorError("La position est invalide pour cette orientation.")

            self.etat['joueurs'][joueur-1]['murs'] -= 1

        if orientation == 'vertical':

            # la position est invalide pour cette orientation.
            if not 2 <= position[0] <= 9 or not 1 <= position[1] <= 8:
                raise QuoridorError("La position est invalide pour cette orientation.")

            # un mur occupe déjà cette position.
            if position in coup(self.etat['murs'])['invalid_v']:
                raise QuoridorError("Un mur occupe déjà cette position.")

            mv.append(list(position))

            # il n'y pas de chemin jusqu'au target
            if self.__nopath(construire_graphe(users, mh, mv)):
                mv.pop()
                raise QuoridorError("La position est invalide pour cette orientation.")

            self.etat['joueurs'][joueur-1]['murs'] -= 1

    def __nopath(self, graphe):
        """"
        Détermine si il y a chemin pour les deux joueurs.
        Retourne True s'il n'y a pas de chemin, False autrement.
        """
        path = False
        for i in range(2):
            if not nx.has_path(graphe, tuple(self.etat['joueurs'][i]['pos']), 'B'+str(i+1)):
                path = True
                break
        return path

    def __meilleur_mur_h(self, joueur, path_now):
        """
        Détermine la meilleur position pour le placement d'un mur horizontal.
        Retourne un tuple contenant le nombre de coup de différence
        et la coordonnée de ce mur.
        Accepte en argument le numéro du joueur et les shortest_path de chaque joueur
        """
        users = [user['pos'] for user in self.etat['joueurs']]
        big_diff_h, tempoh, mur_optimal_h = 0, self.etat['murs']['horizontaux'], []

        # Optimisation du meilleur mur horizontal
        for coord in coup(self.etat['murs'])['valid_h']:
            tempoh.append(list(coord))
            graphe_tempo = construire_graphe(users, tempoh, self.etat['murs']['verticaux'])

            # Vérification que les deux joueurs ont des paths
            if self.__nopath(graphe_tempo):
                tempoh.pop()
                continue
            else:
                path_future = shortest_path(graphe_tempo, users, joueur)
                delta_oppo = len(path_future['oppo']) - len(path_now['oppo'])
                delta_player = len(path_future['player']) - len(path_now['player'])
                if delta_oppo - delta_player > big_diff_h:
                    big_diff_h = delta_oppo - delta_player
                    mur_optimal_h = coord
            tempoh.pop()

        return big_diff_h, mur_optimal_h

    def __meilleur_mur_v(self, joueur, path_now):
        """
        Détermine la meilleur position pour le placement d'un mur vertical.
        Retourne un tuple contenant le nombre de coup de différence
        et la coordonnée de ce mur.
        Accepte en argument le numéro du joueur et les shortest_path de chaque joueur
        """
        users = [user['pos'] for user in self.etat['joueurs']]
        big_diff_v, tempov, mur_optimal_v = 0, self.etat['murs']['verticaux'], []

        # Optimisation du meilleur mur vertical
        for coord in coup(self.etat['murs'])['valid_v']:
            tempov.append(list(coord))
            graphe_tempo = construire_graphe(users, self.etat['murs']['horizontaux'], tempov)

            # Vérification que les deux joueurs ont des paths
            if self.__nopath(graphe_tempo):
                tempov.pop()
                continue
            else:
                path_future = shortest_path(graphe_tempo, users, joueur)
                delta_oppo = len(path_future['oppo']) - len(path_now['oppo'])
                delta_player = len(path_future['player']) - len(path_now['player'])
                if delta_oppo - delta_player > big_diff_v:
                    big_diff_v = delta_oppo - delta_player
                    mur_optimal_v = coord
            tempov.pop()

        return big_diff_v, mur_optimal_v
