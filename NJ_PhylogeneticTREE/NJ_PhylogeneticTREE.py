import numpy as np 
import pandas as pd
from itertools import combinations_with_replacement
import copy

blosum62=pd.read_csv("BLOSUM62.csv")
blosum62


def fill_matrix_NW(indice, columna, blosum):
    col=list(columna)
    idx=list(indice)
    col.insert(0,"0")
    idx.insert(0,"0")
    M=np.zeros([len(idx),len(col)], dtype=int)
    df_M=pd.DataFrame(M)
    df_M.columns = col
    df_M.index = idx
    for i in range(1,len(col)):
        df_M.iloc[0,i] = df_M.iloc[0,i-1] - 8
    for j in range(1,len(idx)):
        df_M.iloc[j,0] = df_M.iloc[j-1,0] - 8
    #df_M
    for i in range(1,len(idx)):
        for j in range(1,len(col)):
            let_col= col[j]
            let_idx=idx[i]
            val_MSM_M=df_M.iloc[i-1,j-1] + int(blosum.loc[let_col,let_idx])
            df_M.iloc[i,j] = max(val_MSM_M, df_M.iloc[i,j-1] -8, df_M.iloc[i-1,j] -8)
    score=(df_M.iloc[-1,-1])
    return df_M,score  


def obtain_alignment_NW(indice,columna,df_M,blosum):
    col=list(columna)
    idx=list(indice)
    col.insert(0,"0")
    idx.insert(0,"0")
    i=len(idx)-1
    j=len(col)-1
    rlt_idx=""
    rlt_col=""
    element = df_M.iloc[-1,-1]
    while True:
        if element == 0:
            break
        ver=df_M.iloc[i-1,j]
        diag=df_M.iloc[i-1,j-1]
        hor=df_M.iloc[i,j-1]
        opt=[ver,diag,hor]
        #print(diag - element + int(blosum.loc[idx[i-1],col[j-1]]))
        #print(int(blosum.loc[idx[i-1],col[j-1]]))
        try:
            if max(opt) == diag or ((diag - element + int(blosum.loc[idx[i],col[j]]) == 0) and (ver -8 != element) and (hor -8 != element)):
                element=diag;j=j-1;i=i-1
                rlt_idx = rlt_idx + idx[i+1]
                rlt_col = rlt_col + col[j+1]
            else:
                if max(opt) == ver:
                    element=ver;i=i-1
                    rlt_idx = rlt_idx + idx[i+1]
                    rlt_col = rlt_col + "-"
                elif max(opt) == hor:
                    element=hor;j=j-1
                    rlt_idx = rlt_idx + "-"
                    rlt_col = rlt_col + col[j+1]
        except:
            if max(opt) == ver:
                    element=ver;i=i-1
                    rlt_idx = rlt_idx + idx[i+1]
                    rlt_col = rlt_col + "-"
            elif max(opt) == hor:
                element=hor;j=j-1
                rlt_idx = rlt_idx + "-"
                rlt_col = rlt_col + col[j+1]
    return rlt_col[::-1],rlt_idx[::-1]

tot=int(input("Numero total de secuenicas en el MSA: "))
Input=[]
for i in range(0,tot):
    sq=str(input("Escribe la secuencia {0}: ".format(i+1)))
    Input.append(sq)
Input;r=2
opt=list(combinations_with_replacement(Input,r))


M=np.zeros([len(Input),len(Input)])
df_dst=pd.DataFrame(M)
df_dst.columns = Input
df_dst.index = Input


for i in opt:
    df,sc=fill_matrix_NW(i[0],i[1],blosum62)
    str1,str2=obtain_alignment_NW(i[0],i[1],df,blosum62)
    k=0;score=0
    for j in str1:
        if j == str2[k] and j != "-" and str2[k] != "-":
            score=score+1
            k=k+1
        else:k=k+1
    score_f=(score/(len(str1)))*100
    df_dst.loc[i[0],i[1]] = round(1-(score_f/100),2)
    df_dst.loc[i[1],i[0]] = round(1-(score_f/100),2)
df_dst

list_df=[df_dst]
while True:
    if len(Input) == 1:
        break
    min=100;I=0;J=0
    for i in range(0,df_dst.shape[0]):
        for j in range(0,df_dst.shape[1]):
            #print(round(df_dst.iloc[i,j],2))
            if df_dst.iloc[i,j] < min and round(df_dst.iloc[i,j],2) != 0.0:
                min=df_dst.iloc[i,j]
                I=i
                J=j
    #print(Input)
    print(I,J)
    print(min, Input[I],Input[J])
    word1=Input[I]
    word2=Input[J]
    Input.append("("+word1+"/"+word2+")");Input.remove(word1);Input.remove(word2)
    #print(Input)

    df_N=copy.copy(df_dst)
    df_N.drop([word1,word2],axis=1, inplace=True);df_N.drop([word1,word2],axis=0,inplace=True)
    df_N["("+word1+"/"+word2+")"] = 0.0
    new_aray=[0.0]*df_N.shape[1]
    df_N.loc[-1] = new_aray
    df_N.index = Input

    for i in range(0,df_N.shape[0]-1):
        df_N.iloc[i,-1] = (df_dst.loc[word1, Input[i]] + df_dst.loc[word2, Input[i]])/2
    for j in range(0,df_N.shape[1]-1):
        df_N.iloc[-1,j] = (df_dst.loc[word1, Input[j]] + df_dst.loc[word2, Input[j]])/2
    
    list_df.append(df_N)
    df_dst = df_N

result=Input[0].replace("/",",")
print("------")
print("El reusltado del arbol es: ")
print(result)
print("------")
escribir=str(input("Desea escribir el arbol en formato NEWICK en un .txt? (S/N): "))
if escribir.upper() == "S":
    nombre=str(input("Nombre del archivo: "))
    with open(nombre+".txt","w") as f:
        f.write(result)