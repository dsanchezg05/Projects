import random
import time
from datetime import datetime
import glob
import os
import requests



class Operador_ADN:
    def __init__(self, seq): #constructor definition with the sequence provided
        self.seq=seq

    nts=["A","C","G","T"] #different nucleotides definition

    def DNA_chain(self,x): #DNA chain creation definition
        nt=["A","C","T","G"];fc=[0.3,0.2,0.3,0.2];chn="" #fc means que different frequency for each nt. Empty chain string created
        selection=random.choices(nt,fc,k=x) # creation of a list with random nucleotides based on their frequency repeated x times
        chn="".join(selection) #conversion from list to string
        return chn

    def countX(self,i,ret=True): #nt count creation
        num=0
        for nt in self.seq.upper():
            if nt == i.upper(): #with counter = 0, for each nt in DNAseq, if nt equals nt provided, counter +1
                num=num+1
        if ret==True: return num
        else: return "Hay un total de {0} nucleótidos de {1}".format(num, i.upper()) #return simply the result,or the result iwth print (only result default)
    
    def loader(self): # load DNA seqs form disk creation
        cwd = os.getcwd() #obtain the path and create an empty list where the seqs will be stored
        final_seq=[]
        for i in glob.glob(cwd+"\\"+"*."+str(self.seq)): #for each file founded in the directory with the extension provided as input
            k=0;seqs="";cont=0 #variables initialation
            with open(i) as file: 
                readed_l = file.readlines() # read the lines and create a list for each file
                for i in range(len(readed_l)): #form 0 to the last line of each file
                    if readed_l[i][0] == ">": #if the line starts with ">", meaning the id of que seq
                        cont=cont+1
                        k=i
                        while True: #for the next lines from que line that starts with ">"
                            k=k+1
                            if readed_l[k][0] == ">" or readed_l[k] == "\n": # if the line starts with ">" again, meaning a new seq appear, add al the fragments of a seq to list of final_seq and break
                                final_seq.append(seqs.upper())
                                seqs=""
                                break
                            seqs=seqs+str(readed_l[k][:-1]) #else, this is a line containing a fragment os seq, add it to a temporal list
                            if k==len(readed_l)-1: #but, if the line is the last one, add all the framgents of the seq to list of final_seq and break
                                final_seq.append(seqs.upper())
                                seqs=""
                                break
                    elif cont==0 and readed_l[0][0] in ["A","C","G","T"]: #if file contains no id but a seq, add the seq to final_seq
                        for i in readed_l:
                            seqs=seqs+i.replace("\n","")
                            final_seq=seqs.upper()
                

        return final_seq
    
    def saver(self,name_f: str): #save a DNseq into disk creation
        t=time.time() #store the time at this step in a variable
        hora_actual = str(datetime.fromtimestamp(t)).split(".") #change time to human readable time
        h_fin=hora_actual[0].replace(" ","_") #delete the characters that aren't compatible with the name format of files
        with open (name_f+"_"+str(h_fin.replace(":","'")+".txt"),"w") as new_file: #create an empty file with unique name
            k=1
            if not ">" in self.seq: #if there`s only nt with no ">" ath beggining (only 1 seq), write the id and seq
                new_file.write("> Seq_"+str(1)+"\n")
                new_file.write(self.seq)
            else:
                sq_spl=self.seq.split(">") # if there are several seqs separated by ">", for eache seq, write id and seq (seqs have more then 3 characters)
                for i in sq_spl:
                    if len(i)>3:
                        new_file.write("> Seq_"+str(k)+"\n")
                        new_file.write(i+"\n")
                        new_file.write("\n")
                        k=k+1


    def palindrom(self) -> str: 
        def pares(c,d):
            a=c.upper()
            b=d.upper()
            if a == "A" and b == "T" or a == "T" and b == "A" or a == "C" and b == "G" or a == "G" and b == "C":
                return True
        mitad = len(self.seq)/2
        paso=0
        tot=0
        if len(self.seq) % 2 == 0:
            for k in self.seq.upper():
                if paso != mitad:
                    #print(self.seq[paso],self.seq[-(paso+1)])
                    if pares(self.seq[paso],self.seq[-(paso+1)]) == True:
                        tot=tot+1
                        paso=paso+1
        else: return "La secuencia tiene un número impar de nt, no es palindrómica"
        if tot == mitad:
            return "La secuencia es palindromica"
        else:return "la secuenica no es palindromica. Continuidad de {0}, en mitad de {1}".format(tot, mitad)

    def islas(self,i="ACGT",min=3): #nt island founding method creation
        self.seq=self.seq.upper()

        dict_islas={} #creation of empty dict
        alma=1
        lista_letra=[]
        lista_final=""
        acop="" #initialization of variables and strings
        for k in range(len(self.seq)): #for each position of the seq
            if k != len(self.seq)-1 and self.seq[k] in i.upper(): #if the position is not the end and cointains a nucleotide (nt)
                j=k+1
                if self.seq[k] == self.seq[j]: # if position is the same as position +1
                    alma=alma+1;acop=acop+self.seq[k] #counter goes foward, island_string (acop) adds the nt in position
                elif alma >= min: #if acop is higher then the minimun established length of island
                        fin=k
                        lista_nt=[self.seq[k]]*alma #creation of a list of lenght counter with the nt in position
                        lista_letra=self.seq[k]+"_"+str(fin-alma+2)+","+str(fin+1) #creation of a list with positions of beggining and end toh the island
                        dict_islas[lista_letra]=lista_nt # add info to dict
                        lista_final=lista_final +str(acop.lower())+str(self.seq[k].lower())
                        alma=1;acop="" #variables default
                else: lista_final=lista_final+acop+self.seq[k];acop="";alma=1 # if not minimunm ahieved

            else: #the same but the island arrives at the end of the seq
                if alma >= min:
                    fin=k
                    lista_nt=[self.seq[k]]*alma
                    lista_letra=self.seq[k]+"_"+str(fin-alma+2)+","+str(fin+1)
                    dict_islas[lista_letra]=lista_nt
                    lista_final=lista_final + str(acop.lower())+str(self.seq[k].lower())
                    alma=1;acop=""
                else: lista_final=lista_final+acop+self.seq[k];acop="";alma=1

        return dict_islas,lista_final
    
    def fragmentos(self, sbs): # subsequence (sbs) counter definition
        self.seq=self.seq.upper()

        frg=self.seq.split(sbs.upper()) #split the seq according to sbs
        appear=0;nueva_sec="" # variables initialization

        for i in frg: #then, add a fragment and then sbs again and counter goes foward
            nueva_sec=nueva_sec+i
            if i != frg[-1]:
                nueva_sec=nueva_sec + str(sbs.lower())
                appear=appear+1
                
        return appear, nueva_sec # return the number of appearances and the final seq
    

    def validate(self,nts=nts): #DNAseq validation creation
        self.seq=self.seq.upper()
        cont=0 #counter starts form 0
        for i in self.seq:
            if not i.upper() in nts: #for each nt in seq, if nt is not in nt_list, valisdation returns FALSE
                return False
            else : cont=cont+1
        if cont == len(self.seq): return True #if length of seq equals counter (all nt are correct) validation returns TRUE

        
    def percentGC(self): #CG% content creation
        self.seq=self.seq.upper()
        c=self.seq.count("C") #Cs count
        g=self.seq.count("G") #Gs count
        percent=round(((g+c)/len(self.seq))*100,2) # GC% calculation
        return percent  
      
    def count_freqs(self, nts=nts): #nts frequency calculation creation
        self.seq=self.seq.upper()
        dict_freq = {} #creation of emptry dict
        for i in nts:
            dict_freq[i] = self.seq.count(i) # count each frequ and add it to dict
        return dict_freq
    
    def mutate(self,p,nts=["A","C","G","T"]): #DNAseq mutation method definition
        self.seq=self.seq.upper()
        class bcolors: #creation of a class thar alllows 3 types of colors (not used in assignment)
            OK = '\033[92m' #GREEN
            WARNING = '\033[93m' #YELLOW
            FAIL = '\033[91m' #RED
            RESET = '\033[0m' #RESET COLOR
        pstn = random.sample(range(len(self.seq)-2),p) # as number_of_mutations equals p, pstn obtains p random index positions of seq
        mt_chain=list(self.seq);white=list(self.seq)
        nts=["A","C","G","T"]
        for i in pstn: #for each index position in seq
            nts.remove(self.seq[i].upper()) # eliminate nt in position i from the pool of possible nts that could replace it
            white[i] = white[i].replace(white[i],str(random.choice(nts).lower())) # replace the nt in position i with random nt from pool, lowercase
            mt_chain[i] = bcolors.OK + str(white[i]) + bcolors.RESET # the same but with different color insted of lowercase (not used in assignment)
            nts=["A","C","G","T"] #regenerate the nt pool
        mt_chain_fin="".join(mt_chain)
        white_fin="".join(white) #create string form list
        return  mt_chain_fin,white_fin
    
    def comp_and_rev(self,nts=nts): # DNAseq reverse and complementary method creation
        self.seq=self.seq.upper()
        d={}
        comp_seq="5'- " #creation of empty dict and 5' ending string
        nts_rev = [item for item in nts[::-1]] # nts_rev stores the inverse of nts pool
        for i in range(len(self.seq)): #for each position in seq
            comp_seq = comp_seq + nts_rev[nts.index(self.seq[i])] # each position in comp_rev is the complementary of each position in seq
        comp_seq = comp_seq + str(" -3'")
        rev_sq = str("5'- "+ self.seq[::-1] + " -3'")
        final_seq= str("5'- "+ self.seq + " -3'") #create strings of the normal seq, complementary, and reverse. Add endings
        d["DNA"] = final_seq
        d["complementary"] = comp_seq
        d["reverse"] = rev_sq #add the strings to dict

        return d
            
class DB_Parse():
    def __init__(self,id):
        self.id=id

    def Ensembl_info(self):
        id_ens=self.id.upper()
        server="https://rest.ensembl.org"
        extension="/lookup/id/"+id_ens+"?"
        r=requests.get(server+extension, headers={"Content-type":"application/json"})
        elements=[]
        if r.ok:
            dic=r.json()
            if dic["object_type"] == "Gene":
                elements=[dic["id"],dic["object_type"], dic["species"], dic["description"]]
                a=1
                return elements,a
            elif dic["object_type"] == "Transcript":
                elements=[dic["id"],dic["object_type"], dic["species"], dic["logic_name"], dic["Parent"]]
                a=2
                return elements,a
        else:
            raise NameError()
        
    def Ensembl_seq(self):
        id_ens_seq=self.id
        server="https://rest.ensembl.org"
        ext="/sequence/id/"+id_ens_seq+"?"
        r=requests.get(server+ext, headers={"Content-type":"application/json"})
        if r.ok:
            seq=r.json()["seq"]
            return seq    

    def UniProt_info(self):
        server= "https://www.ebi.ac.uk/proteins/api"
        id_uni=self.id
        location="/proteins"
        parameters={
            "offset":"0",
            "size":"100",
            "accession": id_uni
        }

        r=requests.get(server+location, params= parameters, headers={ "Accept" : "application/json"})
        if r.ok:
            a=r.json()
            dic=a[0]
            elements=[dic["accession"], dic["proteinExistence"],dic["organism"]["names"][0]["value"],dic["protein"]["recommendedName"]["fullName"]["value"],dic["sequence"]["sequence"]]
            return elements
        else:
            raise NameError()    

    




    def __str__(self):
        return "La secuencia elegida es {0}".format(self.seq)