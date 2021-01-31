#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QUBO Two-Not-Touch
@author: johannesseelig
"""
import sympy
import numpy as np

from painter import paintbox
def main():

    """setup"""
    star_max  = 1
    gamma     = 1
    shape     = [4,4]
    nr_blocks = 4

    x,i,n,k,p = sympy.symbols("x i n k p")

    poly_lin  = 0
    poly_col  = 0

    """ Setup Poly for Lines """
    for i in range(shape[0]):
        a         = sympy.Sum(sympy.Sum(sympy.Indexed('x',(k,p)),(k,0,shape[0]-1)),(p,i,i))
        poly_lin += (a.doit()-star_max)**2

    """ Setup Poly for Cols """
    for j in range(shape[1]):
        b         = sympy.Sum(sympy.Sum(sympy.Indexed('x',(k,p)),(k,j,j)),(p,0,shape[1]-1))
        poly_col += (b.doit()-star_max)**2

    """ Hardcoded Blocks for a 4x4 two-not-touch """
    box_ids   = np.array(([0,0,1,1],[2,0,1,1],[2,3,3,3],[2,2,3,3]))

    """ Setup Poly for Blocks """
    c_arr = []
    for k in range(nr_blocks):
        d_arr = []
        for i in range(shape[0]):
            for j in range(shape[1]):
                if box_ids[i,j] == k:
                    d_arr.append(sympy.Indexed('x',(i,j)))
        c_arr.append(d_arr)

    poly_box = 0
    for i in range(len(c_arr)):
        sumer     = (sum(c_arr[i][j] for j in range(len(c_arr[i])))-star_max)**2
        poly_box += sumer.doit()

    neighbors = lambda x, y : [(x2, y2) for x2 in range(x-1, x+2)
                                   for y2 in range(y-1, y+2)
                                   if (-1 < x <= shape[0] and
                                       -1 < y <= shape[1] and
                                       (x != x2 or y != y2) and
                                       (0 <= x2 <= shape[0]) and
                                       (0 <= y2 <= shape[1]))]
    dd_arr = []
    for i in range(shape[0]):
        for j in range(shape[1]):
            ee_arr = []
            for pair in neighbors(i,j):
                ee_arr.append(sympy.Indexed('x',(pair[0],pair[1])))
            dd_arr.append(ee_arr)
    poly_neighbor = 0
    for i in range(len(dd_arr)):
        sumer = sum(dd_arr[i][j] for j in range(len(dd_arr[i])))
        poly_neighbor+=sumer.doit()

    print("Lin_poly\n",poly_lin,"\n")
    print("Col_Poly\n",poly_col,"\n")
    print("Box_Poly\n",poly_box,"\n")
    print("Nei_Poly\n",poly_neighbor)
    print()

    po     = sympy.Poly(gamma*(poly_lin+poly_col+poly_box+poly_neighbor))
    coeffs = po.coeffs()
    mono   = po.monoms()

    """
    Shift x^2 to x vals
    """
    coeffs_new = coeffs.copy()
    for i in range(len(coeffs)):
        for j in range(len(mono[i])):
            assert mono[i][j] < 3
            if mono[i][j] == 2:
                for k in range(len(coeffs)):
                    if mono[k][j] == 1 and k != i and np.sum(mono[k])==1:
                        coeffs_new[i] = 0
                        coeffs_new[k] = coeffs[i]+coeffs[k]



    """
    Pop out zero coeffs - there where x^2 was
    """
    leng = len(coeffs)
    i    = 0
    while i < leng:
        if coeffs_new[i] == 0:
            coeffs_new.pop(i)
            mono.pop(i)
        i   += 1
        leng = len(coeffs_new)

    #print("\nCoeffs:",coeffs_new)
    #print("\nVars  :",mono)

    index_n_val=[]

    """Reform indexes to Q Dict-format"""
    for i in range(len(mono)):
        indexes=np.where(mono[i])[0]

        if len(indexes) == 0:
            continue
        elif len(indexes) == 1:
            indexes = [indexes[0],indexes[0]]
        else:
            indexes = [indexes[0],indexes[1]]

        index_n_val.append((indexes,coeffs_new[i]))
    dict1={}
    for i in range(len(index_n_val)):
        dict1[(index_n_val[i][0][0],index_n_val[i][0][1])]=index_n_val[i][1]
    print("\nDICT\n",dict1)

    paintbox(shape)


if __name__ is "__main__":
    main()