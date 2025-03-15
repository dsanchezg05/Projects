#Test U de Mann-Withney, contrasrtas si dos muestras proceden de poblaciones equidistribiudas (En el caso de que 
#procedan de poblaciones equidistribiudas, las medianas seran iguales y Ho se areptará, queriendo decir que no hay diferencia entre las muestras,
#luego si se rechaza Ho, quiere deicr que las muestras no proceden de poblaciones equidstribiudas y son diferentes (es lo que se busca))
#claves para hacer el test:
    #es un test no paramétrico
    #no tiene porque serguir una distrubucion normal los resultados
    #la varianza entre los resultados de las distintas poblaciones debe ser parecida

muestra1=[1.1,3.4,4.3,2.1,7.0,2.5,2.2,3.0,2.9,3.5,4.0,9.0,10.0]
muestra2=[7.0,8.0,3.0,5.0,6.2,4.4,8.5,5.1,5.8,4.7,10.0]


#Ho: P(X>Y)=0.5 /// Ho: Mediana1 = Mediana2
#H1: P(X>Y)!=0.5 /// H1: Mediana1 != Mediana2

diccmue_rng={}
muestratotal=[]
for i in muestra1:
    muestratotal.append(i)
for i in muestra2:
    muestratotal.append(i)
#print(muestratotal)
muestratotalord=sorted(muestratotal)
i=0;j=1
endrange=[]
print(len(muestratotalord))
if muestra1[-1]!=muestra2[-1]:
    while i<len(muestratotalord):
        if muestratotalord[i]==muestratotalord[-1]:
            endrange.append(j)
            break
        if muestratotalord[i]==muestratotalord[i+1]:
            a=(j+(j+1))/2
            endrange.append(a)
            b=a
            endrange.append(b)
            i=i+1
            j=j+1
        else:endrange.append(j)
        i=i+1
        j=j+1
else:
    while i<len(muestratotalord):
        if muestratotalord[i]==muestratotalord[i+1]:
            a=(j+(j+1))/2
            endrange.append(a)
            b=a
            endrange.append(b)
            i=i+1
            j=j+1
        else:endrange.append(j)
        i=i+1
        j=j+1

#print(endrange)
#print(muestratotalord)
#print(len(muestratotalord))
#print(len(endrange))
endprueba=[]
for l in muestratotalord:
    endprueba.append(l)
    for k in muestra2:
        if l==k:
            endprueba.append("z"+str(k))
#print(endprueba)
endmuestra=[]
for acc in endprueba:
    if not acc in endmuestra:
        endmuestra.append(acc)

for i in endmuestra:
    a=str(i)
    if not i in muestra1 and a[0]!="z":
        endmuestra.remove(i)
#print(endmuestra)
#print(len(endrange))
#print(len(endmuestra))
m1j=1;m2j=1;i=0
while i<len(endmuestra):
    xx=str(endmuestra[i])
    if xx.startswith("z"):
        diccmue_rng["muestra2."+str(m2j)]=endrange[i]
        m2j=m2j+1
    else: 
        diccmue_rng["muestra1."+str(m1j)]=endrange[i]
        m1j=m1j+1
    i=i+1
#for key,value in diccmue_rng.items():
    #print(key,value)

#una vez obtenido el range separando por muestra 1 y 2 en diccionario se opera

print("La longitud de la muestra 1 es: ",len(muestra1))
print("La longitud de la muestra 2 es: ",len(muestra2))
sumRmuestra1=[];sumRmuestra2=[]
for i in range(1,m1j,1):
    sumRmuestra1.append(diccmue_rng["muestra1."+str(i)])
Rmuestra1=sum(sumRmuestra1)
for i in range(1,m2j,1):
    sumRmuestra2.append(diccmue_rng["muestra2."+str(i)])
Rmuestra2=sum(sumRmuestra2)
print("El rango de la muestra 1 es: ",Rmuestra1)
print("El rango de la muestra 2 es: ",Rmuestra2)

Umuestra1=len(muestra1)*len(muestra2)+(len(muestra1)*(len(muestra1)+1))/2-Rmuestra1;print("Umuestra1 es: ",Umuestra1)
Umuestra2=len(muestra1)*len(muestra2)+(len(muestra2)*(len(muestra2)+1))/2-Rmuestra2;print("Umuestra1 es: ",Umuestra2)

U=0
if Umuestra2<Umuestra1:
    U=Umuestra2
else:U=Umuestra1
print("U es: ",U)

if len(muestra1)>=10.0 and len(muestra2)>=10.0:
    Zcalculado=(U-(len(muestra1)*len(muestra2))/2)/pow(len(muestra1)*len(muestra2)*(len(muestra1)+len(muestra2)+1)/12,0.5)
    Zcalcfin=round(abs(Zcalculado),4)
    print("Zcalcfin es igual a: " + str(Zcalcfin))
    #suponiendo alfa como 0.05 y por tanto nivel de confianza de 95%, se calcula el valor crítico, el cual es siempre 1.96 para alfa =0.05
    Zcrítico=1.96; print("Z crítico es igual a: " + str(Zcrítico))
    if Zcalcfin>Zcrítico:
        print("Se rechaza la hipotesis nula (Ho) ya que Zcalcfin > Zcrítico")
    else:print("Se acepta la hipótesis nula (Ho) ya que Zcalcfin < Zcrítico")
else:print("Se mira en las tablas ya que alguna/s de las longitudes es menor a 10")

