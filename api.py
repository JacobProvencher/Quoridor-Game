"Importe le module requests qui permet de faire des requetes au serveur"
import requests

def débuter_partie(idulenchaine):
    "Permet au joueur de débuter une partie avec son idul"
    url_base = 'https://python.gel.ulaval.ca/quoridor/api/'
    rep = requests.post(url_base+'débuter/', data={'idul': idulenchaine})
    rep = rep.json()
    if rep.get('message'):
        raise RuntimeError(rep['message'])
    else:
        return (rep['id'], rep['état'])

def jouer_coup(id_p, type_c, pos):
    "permet au joueur de jouer un coup dans sa partie avec le type de coup et le point"
    url_base = 'https://python.gel.ulaval.ca/quoridor/api/'
    rep = requests.post(url_base+'jouer/', data={'id': id_p, 'type': type_c, 'pos': pos})
    a = rep.json()
    if a.get('message'):
        raise RuntimeError(a['message'])
    if a.get('gagnant'):
        raise StopIteration(a['gagnant'])
    else:
        return a['état']
