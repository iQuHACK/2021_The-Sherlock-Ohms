#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Painter for Qubo

@author: johannesseelig
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator

def paintbox(shape):

    xx=np.reshape(np.zeros(shape[0]*shape[1]), newshape=(shape[1],shape[0]))
    plt.imshow(xx)

    minor_locator1 = FixedLocator(np.arange(0.5,shape[0]+0.5,1))#AutoMinorLocator(2)
    minor_locator2 = FixedLocator(np.arange(0.5,shape[1]+0.5,1))
    plt.xlim(-0.5,shape[0]-0.5)
    plt.ylim(-0.5,shape[1]-0.5)
    plt.gca().xaxis.set_minor_locator(minor_locator1)
    plt.gca().yaxis.set_minor_locator(minor_locator2)
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.gca().xaxis.set_major_formatter(plt.NullFormatter())
    plt.grid(which='minor',color="black")

    plt.vlines(-0.5,-0.5,shape[1]-0.5,color="red",linewidth=10)
    plt.hlines(-0.5,-0.5,shape[0]-0.5,color="red",linewidth=10)

    plt.hlines(shape[1]-0.5,-0.5,shape[0]-0.5,color="red",linewidth=10)
    plt.vlines(shape[0]-0.5,-0.5,shape[1]-0.5,color="red",linewidth=10)


    plt.vlines(1.5,-0.5,0.5,color="red",linewidth=5)
    plt.vlines(0.5,0.5,2.5,color="red",linewidth=5)

    plt.hlines(0.5,0.5,1.5,color="red",linewidth=5)
    plt.hlines(2.5,-0.5,0.5,color="red",linewidth=5)

    plt.hlines(1.5,0.5,3.5,color="red",linewidth=5)
    plt.vlines(1.5,-0.5,0.5,color="red",linewidth=5)

    plt.vlines(1.5,1.5,3.5,color="red",linewidth=5)
    plt.plot(1,1,"*",markersize=15 )

    plt.show()