# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 12:53:15 2025

@author: varunsharma
"""


import pandas as pd

from shapely import wkt

import math

import warnings
warnings.filterwarnings(action='ignore')



def wrap(deg):
    while deg < -180:
        deg += 360
    while deg > 180:
        deg -= 360
    return deg

def areaCalc(wkt):
    RE = 6378.137
    RAD = math.pi / 180
    FE = 1 / 298.257223563
    E2 = FE * (2 - FE)
    
    lat = wkt.centroid.y
    m = RAD * RE * 1000
    coslat = math.cos(lat * RAD)
    
    w2 = 1 / (1 - E2 * (1 - coslat * coslat))
    w = math.sqrt(w2)
    kx = m * w * coslat
    ky = m * w * w2 * (1 - E2)
    
    ring = wkt.exterior.coords

    sumVal = 0
    j = 0
    l = len(ring)
    k = l - 1
    while j < l:
        sumVal += wrap(ring[j][0] - ring[k][0]) * (ring[j][1] + ring[k][1])
        k = j
        j += 1

    return (abs(sumVal) / 2) * kx * ky/4048;

#%%
wkt_= "POLYGON ((86.4356307796207 20.8608445763909,86.4409765233617 20.8589461762285,86.4397675919149 20.8554232744345,86.4343935138432 20.8573972328124,86.4356307796207 20.8608445763909))"
wkt_poly = wkt.loads(wkt_)
a = round(areaCalc(wkt_poly),2)
print("Area of the given wkt polygon is (sqkm) :", a)
