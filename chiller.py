from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
from math import *

def visBiquadratic(xr,yr,gsize,cL,xl,yl,ti,type=None,coef=1):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = np.arange(xr[0], xr[1], gsize)
    Y = np.arange(yr[0], yr[1], gsize)
    X, Y = np.meshgrid(X, Y)
    #Z = cL[0]+cL[1]*X+cL[2]*pow(X,2)+cL[3]*Y+cL[4]*pow(Y,2)+cL[5]
    Z =cL[0]+cL[1]*X+cL[2]*X**2+cL[3]*Y+cL[4]*Y**2+cL[5]*X*Y
    if type == "cap":
        Z=Z*coef
    if type == "cop":
        Z=Z/coef

    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet,
                           linewidth=0, antialiased=False)
    #ax.set_zlim(-1.01, 1.01)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    ax.set_xlabel(xl)
    ax.set_ylabel(yl)
    ax.set_title(ti)

    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

def visQuadratic(xr,gsize,cL,xl,yl,ti):
    fig = plt.figure()
    ax = fig.gca()
    X = np.arange(xr[0], xr[1], gsize)
    Y = cL[0]+cL[1]*X+cL[2]*X**2
    ax.plot(X,Y)
    ax.set_xlabel(xl)
    ax.set_ylabel(yl)
    ax.set_title(ti)
    plt.show()

if __name__ == '__main__':
    #xrange=[5,10]
    xrange=[0,1.1]
    yrange=[24,35]
    gsize=0.1
    cList=[0.227,0.313,0.464]
    #cList=[0.53,-0.04,0.0015,0.014,0,0]
    #cList=[1,0,0,0,0,0]
    xlabel="Part Load Ratio"
    ylabel="Electric Input Ratio"
    title="Electric Input to Cooling Output Ratio of Part Load Ratio"
    #visBiquadratic(xrange,yrange,gsize,cList,xlabel,ylabel,title)
    visQuadratic(xrange,gsize,cList,xlabel,ylabel,title)