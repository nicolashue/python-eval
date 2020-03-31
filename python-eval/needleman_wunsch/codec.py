import numpy as np
from typing import *

def couper(mot: str, dic_poids: dict, poids: int) -> Tuple[str, str, int, int]:
    '''
    Cette fonction permet de couper un mot en deux, de manière à minimiser la différence de poids entre les moitiés de gauche et de droite.
    '''
    gauche = ''
    poids_gauche = 0
    droite = mot
    poids_droite = poids
    for i in range(len(mot)):
        poids_lettre = dic_poids[mot[i]]
        nouv_poids_gauche = poids_gauche+poids_lettre
        nouv_poids_droite = poids_droite-poids_lettre
        if poids_droite-poids_gauche <= nouv_poids_gauche-nouv_poids_droite: # l'objectif est de minimiser l'écart G/D ; si à  l'étape suivante, l'écart est augmenté, on s'arrête
            return gauche, droite, poids_gauche, poids_droite
        else :
            gauche += mot[i]
            droite = droite[1:]
            poids_gauche = nouv_poids_gauche
            poids_droite = nouv_poids_droite


def creer_dic_poids(texte: str) -> dict:
    '''
    Cette fonction crée un dictionnaire, de la forme {lettre:poids} à partir du texte.
    '''
    dic_poids = {}
    for lettre in texte:
        if lettre in dic_poids:
            dic_poids[lettre] += 1
        else:
            dic_poids[lettre] = 1
    return dic_poids


def creer_lettres(dic_poids: dict) -> str:
    '''
    Cette fonction crée la suite de lettre, située au sommet de l'abre, à partir du dictionnaire {lettre:poids}.
    '''
    mot = ''
    for lettre in dic_poids:
        mot += lettre
    return mot


def calcul_poids(mot: str, dic_poids: dict) -> int:
    '''
    Cette fonction calcule le poids d'un mot
    '''
    poids = 0
    for lettre in mot :
        poids += dic_poids[lettre]
    return poids


def arbre_reccursif(mot: str, emplacement: int, poids: int, dic_poids: dict, dic_codage: dict, dic_decodage: dict):
    '''
    Cette fonction récursive permet de créer étape par étape l'arbre de Huffman. Elle permet de compléter un dictionnaire de type {lettre:lettre codée}, servant au codage, ainsi qu'un dictionnaire {lettre codée:lettre} pour le décodage.
    '''
    if len(mot) == 1: # lorsque l'on arrive à une feuille de l'arbre, on peut compléter le dictionnaire
        dic_codage[mot] = emplacement
        dic_decodage[emplacement] = mot
    else: # sinon, on coupe le mot en deux, on ajoute à la coordonnées des deux moitiés les chiffres 0 et 1, et on recommence
        gauche, droite, poids_gauche, poids_droite = couper(mot, dic_poids, poids)
        emplacement_gauche = emplacement + '0'
        emplacement_droite = emplacement + '1'
        arbre_reccursif(gauche, emplacement_gauche, poids_gauche, dic_poids, dic_codage, dic_decodage)
        arbre_reccursif(droite, emplacement_droite, poids_droite, dic_poids, dic_codage, dic_decodage)


def arbre(texte: str) -> Tuple[dict, dict]:
    '''
    Cette fonction se sert de toutes les fonctions précédentes. Elle prend en entrée le texte à coder, et renvoit les deux dictionnaires qui serviront au codage et au décodage.
    '''
    dic_poids = creer_dic_poids(texte)
    mot = creer_lettres(dic_poids)
    poids = calcul_poids(mot, dic_poids)
    dic_codage, dic_decodage = {}, {}
    arbre_reccursif(mot, '', poids, dic_poids, dic_codage, dic_decodage)
    return dic_codage, dic_decodage
    def __init__(self, text: str):
        self.text = text


def coder(dic_codage: dict, texte: str) -> str:
    '''
    Cette fonction code le texte en se servait du dictionnaire de codage. Elle remplace chaque lettre par sa version codée et retourne le mot codé.
    '''
    codage = ''
    for lettre in texte:
        codage += dic_codage[lettre]
    return codage


def decoder(dic_decodage: dict, code: str) -> str:
    '''
    Cette fonction décode le texte en se servant du dictionnaire de décodage. Pour cela, elle parcourt le texte, et dès qu'elle couvre une chaîne de bits reconnue comme correspondant à une lettre, elle décode cette séquence, et passe à une autre.
    Elle renvoit le texte décodé.
    '''
    mot = ''
    n = len(code)
    indice_gauche, indice_droite = 0, 0
    
    while indice_gauche < n:
        morceau_code = code[indice_gauche:indice_droite]
        if morceau_code in dic_decodage:
            lettre = dic_decodage[morceau_code]
            mot += lettre
            indice_gauche = indice_droite
        else:
            indice_droite += 1
    
    return mot


class TreeBuilder:
    '''
    Cette classe permet de construire, à partir d'un texte, les dictionnaires qui serviront à son codage et décodage.
    Cette construction se fait par la méthode tree.
    '''
    
    def __init__(self, text):
        self.text = text
    
    def tree(self):
        return arbre(self.text)


class Codec:
    '''
    Cette classe permet de coder et de décoder un texte à partir de son arbre binaire (ici deux dictionnaires).
    '''
    
    def __init__(self, tree):
        self.tree = tree
        
    def encode(self, text: str):
        return coder(self.tree[0], text)
    
    def decode(self, code: str):
        return decoder(self.tree[1], code)
