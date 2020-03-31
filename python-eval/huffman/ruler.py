import numpy as np
from colorama import Fore, Style
from typing import *


dic = {'a':0,'A':0,'g':1,'G':1,'c':2,'C':2,'t':3,'T':3} # ce dictionnaire servira à faire fonctionner la fonction correspondance_adn


def red_text(text: str) -> str: # cette fonction permet de faciliter l'écriture en rouge
    return f"{Fore.RED}{text}{Style.RESET_ALL}"



def correspondance(A: str, B: str, s: int = 1, d: int = 1) -> Tuple[str, str, int]:
    '''
    Cette fonction établit la meilleure correspondance entre A et B en suivant l'algorithme de Needleman.
    On peut la paramétrer en choisissant le coût des opérations de substitutions et d'ajout (s et d).
    Elle renvoit les deux mots corrigés (avec les corrections en rouge) aisni que la distance entre les deux mots
    '''
    n, m = len(A), len(B)
    F = np.vectorize(int)(np.zeros((n+1, m+1))) # le but de cette matrice est qu'à la fin, F[i,j] représente la distance entre a[:i+1] et B[:j+1]
    for i in range(n+1):
        F[i, 0] = d*i
    for j in range(m+1):
        F[0, j] = d*j
    
    for i in range(1,n+1): # pour cela, on calcule les termes par récurrence, en choisissant à chaque fos l'opération la moins coûteuse
        for j in range(1,m+1):
            if A[i-1] == B[j-1]:
                choix1 = F[i-1,j-1]
            else:
                choix1 = F[i-1,j-1] + s
            choix2 = F[i-1, j] + d
            choix3 = F[i, j-1] + d
            F[i, j] = min(choix1, choix2, choix3)
    AlignementA = ""
    AlignementB = ""
    i = len(A)
    j = len(B)
    while i > 0 or j > 0: # on memonte ensuite cette matrice jusqu'à la case (0,0), et en déterminant par quelle case nous sommes passés. Cela nous permet de savoir quelles opérations nous avons rélisé, et donc de reconstruire les meilleures correspondances
        print(i,j)
        Score = F[(i, j)]
        ScoreDiag = F[i - 1, j - 1]
        ScoreHaut = F[i, j - 1]
        ScoreGauche = F[i - 1, j]
        if Score == ScoreDiag and A[i-1] == B[j-1]:
            AlignementA = A[i-1] + AlignementA
            AlignementB = B[j-1] + AlignementB
            i -= 1
            j -= 1
        elif Score == ScoreDiag + s and A[i-1] != B[j-1]:
            AlignementA = red_text(A[i-1]) + AlignementA
            AlignementB = red_text(B[j-1]) + AlignementB
            i -= 1
            j -= 1
        
        elif Score == ScoreGauche + d:
            AlignementA = A[i-1] + AlignementA
            AlignementB = red_text("-") + AlignementB
            i = i - 1
        else:
            AlignementA = red_text("-") + AlignementA
            AlignementB = B[j-1] + AlignementB
            j = j - 1

    return AlignementA, AlignementB, F[n,m]

def correspondance_adn(A: str, B: str, S: np.ndarray = np.vectorize(int)(np.ones((4,4))-np.eye(4)), d: int = 1) -> Tuple[str, str, int]:
    '''
    Cette fonction a le même principe de fonctionnement que correspondance, mais est applicaple pour calculer la distance entre deux séquences ADN.
    Elle peut être paramétrée afin de pouvoir appliquer différents coûts de substitututions pour différentes lettres.
    Ces coûts sont à renseigner dans la matrice S.
    '''
    n, m = len(A), len(B)
    F = np.vectorize(int)(np.zeros((n+1, m+1)))
    for i in range(n+1):
        F[i, 0] = d*i
    for j in range(m+1):
        F[0, j] = d*j
    
    for i in range(1,n+1):
        for j in range(1,m+1):
            coord = dic[A[i-1]],dic[B[j-1]]
            choix1 = F[i-1,j-1] + S[coord]
            choix2 = F[i-1, j] + d
            choix3 = F[i, j-1] + d
            F[i, j] = min(choix1, choix2, choix3)
    AlignementA = ""
    AlignementB = ""
    i = len(A)
    j = len(B)
    while i > 0 or j > 0:
        Score = F[(i, j)]
        ScoreDiag = F[i - 1, j - 1]
        ScoreHaut = F[i, j - 1]
        ScoreGauche = F[i - 1, j]
        coord = dic[A[i-1]], dic[B[j-1]]
        if Score == ScoreDiag + S[coord]:
            if A[i-1] == B[j-1]:
                AlignementA = A[i-1] + AlignementA
                AlignementB = B[j-1] + AlignementB
            else :
                AlignementA = red_text(A[i-1]) + AlignementA
                AlignementB = red_text(B[j-1]) + AlignementB
            i = i - 1
            j = j - 1
        
        elif Score == ScoreGauche + d:
            AlignementA = A[i-1] + AlignementA
            AlignementB = red_text("-") + AlignementB
            i = i - 1
        else:
            AlignementA = red_text("-") + AlignementA
            AlignementB = B[j-1] + AlignementB
            j = j - 1

    return AlignementA, AlignementB, F[n, m]


class Ruler:
    '''
    Classe permettant d'appliquer l'algorithme de Needleman.
    Un élément est d'abord constitué des deux mots à comparer.
    En lui applicant la méthode compute, il gagne un nouvel argument, report, qui contient les deux mots corrigés ainsi que la distance entre les mots.
    '''
    
    def __init__(self, mot_1: str, mot_2: str):
        self.mot_1 = mot_1
        self.mot_2 = mot_2
    
    def compute(self):
        mot_1, mot_2 = self.mot_1, self.mot_2
        report_1, report_2, self.distance = correspondance(mot_1, mot_2)
        self.report=(report_1, report_2)