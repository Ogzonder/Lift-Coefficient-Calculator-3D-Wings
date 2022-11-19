# coding: utf-8
__author__ = "Oguzhan Onder"

import numpy as np  
import math
global y_s
global CL1
global AR

N = 9
def LLT1(b,Croot,Ctip,i_w,root_twist,tip_twist,a_2d,alpha_0):
    S = b*(Croot+Ctip)/2
    AR = b**2/S
    taper = Ctip/Croot
    theta = np.linspace((math.pi / (2 * N)), (math.pi / 2), N, endpoint=True)
  
    alpha = np.linspace(i_w + tip_twist ,i_w + root_twist,N)
    
    z = (b / 2) * np.cos(theta)
    c = Croot * (1 - (1 - taper) * np.cos(theta))  # Mean Aerodynamics
    mu = c * a_2d / (4 * b)
    
    LHS = mu * (np.array(alpha) - alpha_0) / 57.3  
    # print(LHS)
    RHS = []
    for i in range(1, 2 * N + 1, 2):
        RHS_iter = np.sin(i * theta) * (
            1 + (mu * i) / (np.sin(list(theta)))
        )  
        RHS.append(RHS_iter)
    
    test = np.asarray(RHS)
    x = np.transpose(test)
    inv_RHS = np.linalg.inv(x)
    
    ans = np.matmul(inv_RHS, LHS)
    # print(ans)
    mynum = np.divide((4 * b), c)
    # print(ans[0])
    test = (np.sin((1) * theta)) * ans[0] * mynum
    test1 = (np.sin((3) * theta)) * ans[1] * mynum
    test2 = (np.sin((5) * theta)) * ans[2] * mynum
    test3 = (np.sin((7) * theta)) * ans[3] * mynum
    test4 = (np.sin((9) * theta)) * ans[4] * mynum
    test5 = (np.sin((11) * theta)) * ans[5] * mynum
    test6 = (np.sin((13) * theta)) * ans[6] * mynum
    test7 = (np.sin((15) * theta)) * ans[7] * mynum
    test8 = (np.sin((17) * theta)) * ans[8] * mynum
    # print(ans[0])
    CL = test + test1 + test2 + test3 + test4 + test5 + test6 + test7 + test8
    CL1 = np.append(0, CL)
    # print(CL1)
    y_s = [b / 2, z[0], z[1], z[2], z[3], z[4], z[5], z[6], z[7], z[8]]
    
    # print(CL1)
    # print(y_s)
    CL_wing = (math.pi * AR * ans[0]) 
    return y_s,CL1,CL_wing,AR
   


