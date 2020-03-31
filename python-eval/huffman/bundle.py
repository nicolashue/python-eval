import numpy as np
from colorama import Fore, Style
from typing import *

from ruler import Ruler


fichier = open('DATASET', 'r')
Lignes = fichier.readlines()
fichier.close()
nombre_couples = len(lignes)//2
for i in range(nombre_couple):
    mot_1, mot_2 = Lignes[2*i], Lignes[2*i+1]
    ruler = Ruler(mot_1, mot_2)
    ruler.compute()
    corrige_1, corrige2 = ruler.report
    print(f" =========== Example {i+1}: distance = {ruler.distance} \n {corrige1} \n {corrige2}")