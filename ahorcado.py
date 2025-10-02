import os

palabra=input("Escribe una palabra: ")
lst_palabra=["_"]*len(palabra)

os.system("clear")

err = int(input("Escribe fallos: "))
lst_fal=["X"]*err

os.system("clear")
cyc=0;lts=[]
while True:
    try:
        print(lst_palabra)
        print(lst_fal)
        letra=input("Escribe una letra: ")
        if not letra in lts:
            pass
        else: os.system("clear");raise ValueError()
        lts.append(letra)
        k=0;idx=[]
        for i in palabra:
            if i == letra:
                idx.append(k)
            k=k+1
        if idx == []:
            lst_fal[cyc] = letra
            cyc=cyc+1
        else:
            for i in idx:
                lst_palabra[i] = letra.upper()
        if lst_palabra == list(palabra.upper()):
            os.system("clear")
            print("Has ganado")
            print(palabra)
            break
        elif cyc == err:
            os.system("clear")
            print(lst_fal)
            
            print("has perdido")
            print("la palabra era: {0}".format(palabra))
            break
        else:
            os.system("clear")
            continue
    except ValueError:
        print("Esa letra {0} ya está".format(letra))
        pass
        
        
            

