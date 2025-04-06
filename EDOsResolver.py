import scipy as sp 
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd


var=str(input("Escribir las variables (separadas por coma): "))
var_list=var.split(",")
n_eq=int(input("Number of equations: "))
eqs=[];k=1
for i in range(0,n_eq):
    eqs.append(input("escibre la ecuacion {0}: ".format(k)))
    k=k+1
tmax=int(input("Tiempo maximo?: "))
Ci=[]
for i in range(0, len(var_list)):
    Ci.append(float(input("Condicion inicial para {0}: ".format(var_list[i]))))

print("-----")
print("INICIO")
print("-----")
from scipy.integrate import odeint
import copy
import string

timestamp=range(0,tmax,1)
new_eqs=[]
for i in eqs:
    for j in i:
        for ele in var_list:
            if j == ele:
                i=i.replace(j,str("var_list["+str(var_list.index(ele))+"]"))
    print(i)
    new_eqs.append(i)
#print(new_eqs)
def EDO(var_list,timestamp):
    k=0
    rlt=range(0,len(var_list))
    let=list(string.ascii_lowercase[0:len(var_list)])
    for i in rlt:
        let[i] = eval(new_eqs[k])
        k=k+1
    return let


result=odeint(EDO,Ci,timestamp)
df_result=pd.DataFrame(result)
df_result.columns = var_list
print("-----")
print("DF result:")
print(df_result)



k=0
for i in range(0,len(var_list)):
    plt.plot(timestamp, result[:,k],label=var_list[k])
    k=k+1
plt.xlabel("Time")
plt.ylabel("Quantity")
plt.legend(loc="best")
plt.show()