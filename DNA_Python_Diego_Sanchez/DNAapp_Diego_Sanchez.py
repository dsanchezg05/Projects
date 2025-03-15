from textual import on
from textual.app import App
from textual.reactive import reactive
from textual.containers import ScrollableContainer, Horizontal, Grid, Container
from textual.widgets import Footer, Header, Button, Static, Input, Label
from textual.widget import Widget
import random
import time
from datetime import datetime
from textual.screen import ModalScreen
from DNA_ToolKit import DB_Parse
from DNA_ToolKit import Operador_ADN #import modules
import colorama
colorama.init()

from pathlib import Path

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR # class to add color

#CSS es un lenguaje dentro de textual que permite dar un estilo a las interfaces dentro de la aplicacion. Normalmente se define en un archivo aparte .css
# se denfine como:
# CSS = """
# Interfaz {
#   layout:   ;
#   background:   ;
#   margin:   ;
#   padding:   ;
#   height:   ;
#}
# #iddelboton o Button {
#   dock:   ;
#   height:    ;
#   display:    ;
#   position:    ;
#   top:   ;
#   left:    ;
#}
# Input_Display{
#   content-align:    ;
#   text-opacity:    ;
#}
# """

# En el caos de que se escriba CSS como un archivo aparte, se le llama usando CSS_PATH = "numbre.css"
#Static sirve apra crear una clase donde se pueden guardr widgets, luego a esa clase se le lllama en la clase principal y aparece


class Saving(Static): #creation of a static widget (python class) for text display
    Save=reactive("[[No new seq]]") #definition of reactive variable
    def to_react(self):
        new_save=self.Save # when something added to self.Save, variable Save reacts and reset itself to new string
        self.update(str(new_save))
    def string(self): #method to obtain the string that is stores in the reactive variable
        return self.Save
    
#Same aspect with the rest of Static widgets, although they are named different
class Hid(Static):
    Hid=reactive("[[No initial chain loaded]]")
    new=reactive("Empty")
    def to_react(self):
        new_hid = self.Hid
        self.update(str(new_hid))
    def to_react(self):
        new_seq = self.new
        self.update(str(new_seq))
    def string(self):
        return self.Hid
    def string_new(self):
        return self.new


class Seq_Display(Static):
    seq=reactive("[[No initial chain loaded]]")
    def watch_seq(self):
        dsp_seq=self.seq
        self.update(dsp_seq)
    def string(self):
        return self.seq
    
class Result_Display(Static):
    rlt=reactive("No result")
    def watch_rlt(self):
        new_rlt=self.rlt
        self.update(str(new_rlt))
    def string(self):
        return self.rlt

class Interfaz_1(Static): # Creation of a new static Widget, but this time with buttons and inputs inside it
                            # Buttons and Inputs appear and disappear according to functions in this script, and senences in CSS script


    def compose(self): #Function that allows button and input creation
        # yield command allows to create elements such as buttos or inputs
        # Each element has its name, color (variant) and unique id
        # Also, previous widgets defined before are incorporated into this widget
        # Elements defined before, appear before in the display
        yield Button("1 - Create new DNA chain", variant="success",id="one") #creation of a button with name "1 - Create new DNA chain", color green (success) and id "one", and so on
        yield Button("2 - Save DNA chain", variant="warning", id="two")
        yield Button("3 - Select DNA from disk", variant="warning", id="three")
        yield Button("4 - List all DNA info", variant="warning", id="four")
        yield Button("5 - Delete DNA info", variant="error", id="five")
        yield Button("6 - Operations with DNA",id="six")
        yield Button("2.1 - Re-generate DNA chain", variant="success", id="two_one")
        yield Button("2.2 - Validate DNA chain", variant="warning",id="two_two")
        yield Button("2.3 - Mutate DNA chain", variant="warning",id="two_three")
        yield Button("2.4 - Measure frequencies", variant="warning",id="two_four")
        yield Button("2.5 - Count subsecuences",variant="warning",id="two_five")
        yield Button("2.6 - Synthesize and complement DNA chain",variant="warning",id="two_six")
        yield Button("2.7 - Measure %GC’s",variant="warning",id="two_seven")
        yield Button("2.8 - Back", variant="error",id="two_eight")
        yield Button("Search in DB", variant="success", id="db1")
        yield Button("Search in Ensembl by id", variant="warning", id="ens")
        yield Button("Seacrh in UniProt by id", variant="warning", id="uni")
        yield Button("Exit DB", variant="error", id="exitdb")
        yield Input(placeholder="Write a number for DNA length: ",id="Seq_input")
        yield Input(placeholder="[number for DNA mutations, chain number (Default 0)if more than 1 chain provided]: ",id="Mut_input")
        yield Seq_Display()
        yield Result_Display()
        yield Hid()
        yield Saving()
        yield Input(placeholder="Write the name of the file: ",id="n_file") #when creating and input, placeholder means the text that appears on the background and indicates what to write
        yield Input(placeholder="Write numbers of chains separated by comma. Type ALL to select all sequences: ",id="num_chain")
        yield Input(placeholder="Select the id of the chains to delete, separated by comma: ", id="num_delete")
        yield Input(placeholder="Wish to know sub-fragments (type SB) or nulceotide islands (type NI)?: ", id="sb_ni")
        yield Input(placeholder="Write sub-sequence and sequence number (Default 0), separated by comma: ", id="sb")
        yield Input(placeholder="Writhe minimun length of the island, nucleotides and sequence number (Default 0), separated by comma: ", id="ni")
        yield Input(placeholder="Write the id of Ensembl", id="ipt_ens")
        yield Input(placeholder="Write the id of UniProt", id="ipt_uni")
        yield Button("Save and Use Mutated DNA", variant="success", id="Usemut")
        yield Button("Save seq and return to menu", variant="success",id="db_seq")
        yield Button("Back to operations menu", variant="error",id="volver")
        yield Button("Back to main",variant="error",id="back_menu")

    #once elements have been created, @on if a rective function that allows to execute lines of code, when an action has been done (Pressing a Button, Sumbmitting an Input...)
    # the lines of code to exectue must be inside a function with unique name

    @on(Button.Pressed, "#one") #when button with id = one has been pressed
    def display_seq(self): #execute function "display_seq", that contains some code
        # when function display_one has been executed, in this case, some calsses have been removed, and other have been added
        # what classes do, is defined inside CSS script. At this assignment, the basis is that classes allow elements of thw widget to appear and dissapear (changing menus)
        self.add_class("ops_menu") # A this time "ops_menu" class is added, meaning some buttons or static widgets inside Interfaz_1 will appear or dissapear, and so on 
        self.add_class("app_Seq_input")
        self.add_class("app_menu")
        self.remove_class("show_result")
        self.remove_class("app_n_file")
        self.remove_class("app_num_chain")
        self.remove_class("app_num_delete")
        #Sometimes, when pressing a button allows another button to apear (coded in classes), and this new button can also be pressed too
    @on(Input.Submitted, "#Seq_input") # When the input that has id = Seq_input has been submited...
    def accept_seq(self):# ...execute this unique function
        # Inside a fucntion, code can be created in order to query whar reactive variables (inside static widgets defined at the beggining) contain
        input=self.query_one("#Seq_input") # line of code that stores in input an object with information from what has been submitted in input with id = Seq_input
        final_num= input.value # final_num stores the string that was contained in the object...
        input.value = "" #... and restores the value of the string
        self.remove_class("show_result")
        self.remove_class("show_result_and_seq")
        init_seq = self.query_one(Seq_Display)
        save_str=self.query_one(Saving)
        hid_str=self.query_one(Hid) #static widgets can also be queried, in order to know the string that reactive variables contain(.string()) or in order to change its value

        try:
            int(final_num)#assert that final_num is int type
            chn=Operador_ADN("DNAseq").DNA_chain(int(final_num)) #objects from other files (DNA_ToolKit) can be used
            init_seq.seq = str(">"+chn) #update the value of the reactive value contained in Seq_Display static widget
            save_str.Save = str(">"+chn)#update the value of the reactive value contained in Saving static widget
            hid_str.Hid=str("[[No initial chain loaded]]")#update the value of the reactive value contained in Hid static widget
        except: 
            res_err=self.query_one(Result_Display) #In case funal_num is not int, update the value of the reactive value contained in Result_Display...
            res_err.rlt = str(bcolors.FAIL + "Query is equal to -" + str(final_num) + "-, retry" + bcolors.RESET) #...with this string of red (FAIL) color...
            self.add_class("show_result_and_seq") #... and show it with the content of the widget Seq_Display
            pass
    
    

    @on(Button.Pressed, "#two")
    def save_DNA(self):  # when button with id = two has been presed, function "save_DNA" is exectued 
        seq_dsp=self.query_one(Seq_Display).string()#Obtain the string characters of the reactive variable stored in Seq_Display
        res_dsp=self.query_one(Result_Display) #Prepare to chenge the value of the reactve variable stored in Result_Display
        if seq_dsp.startswith(">"): # if the string character begins with ">", meaning a sequence has been selected, add some buttons and inputs
            self.add_class("app_n_file")
            self.remove_class("show_result")
            self.remove_class("app_num_chain")
            self.remove_class("app_num_delete")
        else: #if not, raise an error and a string explaining it
            res_dsp.rlt = str(bcolors.FAIL+"No chains selected, list and Select them"+bcolors.RESET)
            self.add_class("show_result")
            pass
    @on(Input.Submitted,"#n_file") # if input with id = n_file has been submitted, meaning input appeared, so string character began with ">"...
    def ipt_file(self): #...execute function to create a file of seqs
        try: 
            file=self.query_one("#n_file")
            seq_dsp=self.query_one(Seq_Display).string()
            res_dsp= self.query_one(Result_Display)
            file_n=file.value
            if file_n == "": #obtain the name of the file stored in a reactive variable, but if name is empty, raise an error
                raise ValueError("Name empty")
            file.value="" #restore the reactive variable value
            Operador_ADN(seq_dsp).saver(file_n) #execute method from DNA_Toolkit to create a file with the sequences 
            res_dsp.rlt= str(bcolors.OK + "Result saved succesfully in program folder!" + bcolors.RESET) #if method success, print success message
            self.remove_class("app_n_file")
            self.add_class("show_result_and_seq")
            save=self.query_one(Saving)
            save.Save = str("[[No new seq]]") # if saved, no need to pop up a window asking to save
        except:
            res_dsp.rlt = str(bcolors.FAIL + "No valid archive name for saving provided" + bcolors.RESET) #error raised returns string explaining the error
            self.add_class("show_result")
            self.remove_class("app_n_file")
            pass


    
    @on(Button.Pressed, "#three")
    def load(self): #when button with id = three is pressed, execute function "load"
        seq_dsp=self.query_one(Seq_Display).string()
        hid_dsp=self.query_one(Hid).string() #obtain values from reactive variables in order to use them as input
        res_dsp=self.query_one(Result_Display) #prepare reactive variable to be changed and/or displayed
        if seq_dsp.startswith(">"): #if some sequences have been selected
            res_dsp.rlt = str(bcolors.WARNING+"Chains already selected, you can delete them"+bcolors.RESET)
            self.add_class("show_result_and_seq")
            pass
        elif seq_dsp != hid_dsp: # check if to strings of different reactive variables from different widgets differ, meaning sequences have been listed from disk
            #once checked, add or remove different buttons and inputs
            self.add_class("app_num_chain")
            self.remove_class("show_result")
            self.remove_class("app_n_file")
            self.remove_class("app_num_delete")
        else:
            #if no seqs have been listed or selected, rise the following statement (no error)
            res_dsp.rlt = str(bcolors.FAIL+"No chains imported, please list them"+bcolors.RESET)
            self.add_class("show_result")
            pass
    # after checking, an input appeared, with id = num_chain. Once input with this id was submitted, the following procedure will be executed
    @on(Input.Submitted,"#num_chain")
    def load_seq(self):
        N_chain=self.query_one("#num_chain")
        num_chain=N_chain.value 
        N_chain.value ="" #obtain the value of the input and restores it
        seq_str=self.query_one(Seq_Display).string()
        seq_result=self.query_one(Seq_Display)
        seq_result.seq =""
        res_dsp=self.query_one(Result_Display) # queries some widgets
        try:             
            numbers=[];final_seqs=[] #initialize variables
            seqs_splt=seq_str.split("\n") # if there are more than one sequence conforming the stirng of the reactive variable of the widget Seq_Display, split them
            if num_chain=="ALL" or num_chain == "all": 
                for i in seqs_splt:
                    sq=i.split(",")[-1] # if the value of the input is all, for each line, obtain the sequence and put ">" before each
                    final_seqs.append(sq.replace(" ",">"))
                for i in final_seqs:
                    if i != final_seqs[-1]: #sore the sequences in the reactive value of Seq_Display, makeing them the new string
                        seq_result.seq = seq_result.seq + str(i+"\n")
                    else: seq_result.seq=seq_result.seq + str(i)
                self.remove_class("app_num_chain") #line of code that removes the input
            else: # if the input value is not all...
                for i in num_chain.split(","):
                    numbers.append(int(i)) #...but is a number....
                    assert(int(i)<len(seqs_splt)) #... an the number is less than the number of sequences
                assert(len(numbers)<=len(seqs_splt)) 
                for i in seqs_splt:
                    if int(i[0]) in numbers: 
                        sq=i.split(",")[-1] # obtain the sequence that has the same id as the number provided, and store it in a list, adding ">" at the beggining
                        final_seqs.append(sq.replace(" ",">"))
                for i in final_seqs:
                    if i != final_seqs[-1]: #sore the sequences in the reactive value of Seq_Display, makeing them the new string
                        seq_result.seq = seq_result.seq + str(i+"\n")
                    else: seq_result.seq=seq_result.seq + str(i)
                self.remove_class("app_num_chain") #line of code that removes the input
        except:
            res_dsp.rlt = str(bcolors.FAIL + str("No correct number selected") + bcolors.RESET) #in case no number or incorrect number is provided, raise an error
            self.add_class("show_result") # and show the string that tells the error
            self.remove_class("app_num_chain")
            pass



    @on(Button.Pressed,"#four")
    def list(self): # if button with id = four has been pressed, execute "list" function
        self.remove_class("show_result")
        self.remove_class("show_result_and_seq")
        self.remove_class("app_n_file")
        self.remove_class("app_num_chain")
        self.remove_class("app_num_delete")
        try: #after adding or removing buttons and inputs, try the following procedure
            seq_dsp=self.query_one(Seq_Display)
            seq_dsp.seq = "" # reset the vlaue of the reactive variable in Seq_Display widget
            res_dsp=self.query_one(Result_Display)
            save=self.query_one(Saving) # prepare widgets to change the value of their reactive variable, or display it
            save.Save = "[[No new seq]]" # value of reative variable contained in widget "Save" equals [[No new seq]] beacuse sequences listed already are in the computer
            res= Operador_ADN("dna").loader() #load seqs contained in files with "dna" extension in the directory of the srcipt
            p=0
            if len(res) == 0: # if number of seqs equals 0, return that no seqs where found
                res_dsp.rlt=str(bcolors.WARNING + "No files found" + bcolors.RESET)
                self.add_class("show_result") # and display it
                pass
            else:
                self.remove_class("show_result")
                for i in range(len(res)): # if seqs were found...
                    if i != len(res)-1:
                        # display the seqs following the format: id - length, seq
                        seq_dsp.seq= seq_dsp.seq + str("{0} - {1}, {2}\n".format(p, len(res[i]),res[i]))
                        p=p+1
                    else:
                        seq_dsp.seq= seq_dsp.seq + str("{0} - {1}, {2}".format(p, len(res[i]),res[i]))
        except:
            res_dsp.rlt = str(bcolors.FAIL + str("No .dna files found in directory") + bcolors.RESET) #in case no files found, rise an error
            self.add_class("show_result") # and show the string that tells the error
            pass



    @on(Button.Pressed,"#five")
    def delete(self):# if button with id = five has been pressed, execute "delete" function
        seq_dsp=self.query_one(Seq_Display).string()
        hid_dsp=self.query_one(Hid).string()
        res_dsp=self.query_one(Result_Display)
        if seq_dsp != hid_dsp or seq_dsp.startswith(">"): #after queries to obtain values from reative variables have been done, test if sequences have been listed or selected
            #if correct, add and delete some buttons or inputs
            self.add_class("app_num_delete")
            self.remove_class("show_result")
            self.remove_class("show_result_and_seq")
            self.remove_class("app_n_file")
            self.remove_class("app_num_chain")
        else: # if not sequs have been listed or selected, program asks to at least list them form disk, or create a new one
            res_dsp.rlt = str(bcolors.FAIL+"No chains imported, please list them or create a new random one"+bcolors.RESET)
            self.add_class("show_result")
            pass
    @on(Input.Submitted,"#num_delete") 
    def delete_seq(self): #if sequences where listed or selected, and input with id = num_delete was submited, execute the following procedure
        N_chain=self.query_one("#num_delete")
        num_chain=N_chain.value
        N_chain.value ="" #obtain the value of the inout and restore it 
        seq_str=self.query_one(Seq_Display).string() #obtain value of reactive variable to use as input
        seq_result=self.query_one(Seq_Display)
        seq_result.seq ="" #once obtained the value of the string, reset it to ""
        hid_result=self.query_one(Hid)
        res_dsp=self.query_one(Result_Display)
        try:
            numbers=[]
            seqs_splt=seq_str.split("\n")
            for i in num_chain.split(","): #split tyhe different sequences
                numbers.append(int(i)) # make sure the nummber is an integer and is less than the number of sequs
                assert(int(i)<len(seqs_splt))
            assert(len(numbers)<=len(seqs_splt)) # in case that more than one seuqence wants to be eliminated, the total numbers provided are less than the total sequences
            if seq_str.startswith(">"): # if sequences starts with ">" (have been listed and selected)
                for i in seqs_splt:
                    if seqs_splt.index(i) not in numbers:
                        seq_result.seq = seq_result.seq + str(i+"\n") # eliminate the sequences that their index equals the number provided
                seq_result.seq = seq_result.seq[:-1]
                self.remove_class("app_num_delete") #remove the input
            else: # if sequences doont start with ">" (have been listed but not selected)
                p=0
                for i in seqs_splt:
                    if int(i[0]) not in numbers:
                        seq_result.seq = seq_result.seq + str("{0}{1}\n".format(p,i[1:]))  # eliminate the sequences that their index equals the number provided
                        p=p+1
                seq_result.seq=seq_result.seq[:-1]
                self.remove_class("app_num_delete")
            seq_str_f=self.query_one(Seq_Display).string()
            if seq_str_f == "": #in case all seqs have been eliminated, restore values of reactive variables involved to the original value
                seq_result.seq = str("[[No initial chain loaded]]")
                hid_result.Hid = str("[[No initial chain loaded]]")
        except:
            res_dsp.rlt = str(bcolors.FAIL + str("No correct number selected") + bcolors.RESET) # if not number or incorrect number provided, rise an error and display it
            self.add_class("show_result")
            self.remove_class("app_num_delete")
        


    @on(Button.Pressed, "#six")
    def menu_method(self): #if button that allows to change from initial menu to operations menu have been pressed..
        cstl_seq=self.query_one(Seq_Display).string()
        cstl_res=self.query_one(Result_Display)
        #.. check if sequences have been uploaded
        if cstl_seq == "[[No initial chain loaded]]":
            cstl_res.rlt = str(bcolors.FAIL+"No chain loaded"+bcolors.RESET) #negative case, raise an error
            self.add_class("show_result")
            pass
        elif cstl_seq[0] != ">": # chek if seqs have been listed and selected
            cstl_res.rlt = str(bcolors.FAIL+"No chains selected"+bcolors.RESET) # negative case, raise an error
            self.add_class("show_result")
            pass
        else: #if seqs have been listed and selected, go to operations menu
            self.remove_class("initial")
            self.add_class("ops_menu")
            self.remove_class("show_result")
            self.remove_class("show_result_and_seq")
            self.remove_class("app_n_file")
            self.remove_class("app_num_chain")
            self.remove_class("app_num_delete")
    
    # CHange to ops_menu

    @on(Button.Pressed, "#two_one")
    def reg_seq(self): # if button with id= two_one has been pressed, execute the same procedure to create a new random seq, as done pressing id = one button
        self.add_class("initial")
        self.add_class("app_Seq_input")
        self.add_class("app_volver")
        self.add_class("app_menu")
        self.remove_class("app_sb_ni")



    @on(Button.Pressed, "#two_two")
    def validation(self): #if button with id= two_two has been pressed, execute function "validation"
        self.add_class("initial")
        self.add_class("ops_menu")
        self.add_class("app_volver")
        self.add_class("app_menu")
        self.remove_class("app_sb_ni")
        self.remove_class("show_result_and_seq")
        secuencia=self.query_one(Seq_Display).string()
        udt_sec=self.query_one(Result_Display)
        udt_sec.rlt = str("You have selected option 2\n\n") #do queries to obtain input strings (seqs) and add or remove the buttons and input as needed
        seq_split=secuencia[1:].split(">");records=[]
        for sec in seq_split: records.append(sec.strip()) #obtain clean seqs from string contained in the reactive value 
        final_seq=self.query_one(Seq_Display)
        final_seq.seq =""
        for sec in records: #for each clear sequence
            if Operador_ADN(sec).validate() == True: # do vlaidation
                udt_sec.rlt = udt_sec.rlt + str("The chain " +str(sec)+ " is " + bcolors.WARNING + str("valid")+ bcolors.RESET+"\n")
                final_seq.seq = final_seq.seq + str(">"+sec+"\n") #if valid, add the following string next to the sequence and display it
            else: 
                # if sequence is not valid, remove it and display a message
                udt_sec.rlt = udt_sec.rlt + str("The chain " +str(sec) + " is " + bcolors.FAIL + str("not valid, eliminated")+ bcolors.RESET+"\n")
        final_seq.seq = final_seq.seq[:-1] # eliminate \n at the end of the string containing the result
        hid_res=self.query_one(Hid)
        hid_res.Hid = "Validated" # add Validated to a reactive value in Hid, in order to access to operations in operations menu
        self.add_class("show_result")



    @on(Button.Pressed, "#two_three")
    def mutacion(self): # if button with id = two_three is pressed, execute the following function
        hid_qry=self.query_one(Hid).string()
        res_dsp=self.query_one(Result_Display)
        if hid_qry == "Validated": # only if sequence has been validated (random sequences are validated since creation)
            self.add_class("initial")
            self.add_class("app_Mut_input")
            self.add_class("app_volver")
            self.add_class("app_menu")
            self.remove_class("app_sb_ni")
        else:
            res_dsp.rlt = str(bcolors.WARNING+"No chains validated, please validate them"+bcolors.RESET) # program tells to validate the sequence if not done
            self.add_class("show_result_and_seq")
            pass
    @on(Input.Submitted, "#Mut_input")
    #in case seq was validated, input asking for mutations should have appeared, and once submitted, the following command should execute
    def mutacion_2(self):
        self.remove_class("show_result")
        self.remove_class("show_result_and_seq")
        int_read=self.query_one("#Mut_input")
        res_read=self.query_one(Result_Display)
        res_read.rlt = str("You have selected option 3")
        seq_read=self.query_one(Seq_Display).string()
        hid_str=self.query_one(Hid)
        valor_num=int_read.value
        int_read.value = ""
        try: # after obtaining inputs and doing queries, try the following
            n=valor_num.split(",");numbers=[]
            for i in n:
                numbers.append(int(i))  # obtain the number corresponding to the number of mutations and the number corresponding to the id of the seq that will by mutated
            seq_split=seq_read[1:].split(">");records=[]
            for sec in seq_split: records.append(sec.strip())
            if len(numbers)==1:
                numbers.append(0) # in case no id was provided, id seq = 0 will be used as default 
            assert(len(numbers) == 2) # make sure there are two numbers
            if int(numbers[0]) < len(records[numbers[1]]) and int(numbers[0]) > 0:
                #in case number of mutations > 0 and this number < than the length of the sequence...
                self.add_class("App_butmut")
                res_read.rlt = res_read.rlt + str(", number of mutations (lowcase): "+bcolors.WARNING+str(numbers[0])+bcolors.RESET+"\n\n")
                mt_chain,w_chain=Operador_ADN(records[numbers[1]]).mutate(int(numbers[0])) #execute mutation method form DNA_ToolKit
                res_read.rlt = res_read.rlt + str("Previous DNA chain: {0} \n Mutated DNA chain: {1}".format(records[numbers[1]],w_chain))
                hid_str.new = str(w_chain.upper()) #also, store the chain mutated. It can be used as default chain if the user wants to
                self.add_class("show_result") # display the result
            elif int(numbers[0]) > len(records[numbers[1]]) or int(numbers[0]) < 0: 
                # if even the number of mutation exced the length of the sequence, or is a negative number, raise an error
                res_read.rlt = str(bcolors.FAIL + "Number provided excess secuence length or is negative, retry" + bcolors.RESET)
                self.add_class("show_result_and_seq")
                pass
            elif int(numbers[1]) > len(records) or int(numbers[1]) < 0:
                # if even the id number exced number of seqs or is negative, raise an error
                res_read.rlt = str(bcolors.FAIL + "chain number not valid, retry" + bcolors.RESET)
                self.add_class("show_result_and_seq")
                pass          
        except: 
            res_read.rlt = str(bcolors.FAIL + "No correct numbers provided, retry" + bcolors.RESET) # if no correct number type provided (stirng character) raise an error
            self.add_class("show_result_and_seq")
            pass
    @on(Button.Pressed, "#Usemut")
    def use_mutated(self):
        #once X seq has been mutated, if button with id = Usemut is pressed, mutated chain will be used as default. Also, this chain is validated
        hid_str=self.query_one(Hid).string_new()
        save=self.query_one(Saving)
        read_seq=self.query_one(Seq_Display)
        read_seq.seq = str(">"+hid_str)
        save.Save =str(">"+hid_str)
        self.remove_class("show_result")



    @on(Button.Pressed, "#two_four")
    def frq(self): #when button with id = two_four is pressed, "frq" function will be executed
        hid_qry=self.query_one(Hid).string()
        res_dsp=self.query_one(Result_Display)
        if hid_qry == "Validated": #only is seqs are validated
            self.add_class("initial")
            self.add_class("app_volver")
            self.add_class("app_menu")
            self.remove_class("app_sb_ni")
            seq_query=self.query_one(Seq_Display).string()
            res_query=self.query_one(Result_Display) # input and button or input display selection
            res_query.rlt = str("You have selected option 4\n\n")
            seq_split=seq_query[1:].split(">");records=[]
            for sec in seq_split: records.append(sec.strip()) #obtain clean sequences from input string 
            p=0
            for sec in records: #for each clean sequence... 
                dict_frs=Operador_ADN(sec).count_freqs() # count nt freqs...
                res_query.rlt=res_query.rlt + str("Sequence number {0}\n".format(p))
                for k,v in dict_frs.items():
                    # ... and display the frequency of each nt for each sequence following the next format: Nt X has the following total appearances: Y
                    res_query.rlt = res_query.rlt + str("Nucleotide: "+ bcolors.OK+str(k)+bcolors.RESET+" has the following total appearances: {0}\n".format(v))
                res_query.rlt = res_query.rlt + "\n"
                p=p+1
            self.add_class("show_result") # and display the result
        else:
            res_dsp.rlt = str(bcolors.WARNING+"No chains validated, please validate them"+bcolors.RESET) #if seqs arent validated, program tells you to do it
            self.add_class("show_result_and_seq")            
            pass

    

    @on(Button.Pressed,"#two_five")
    def two_five(self): # if button with id = two_five is pressed, then function two_five is executed
        hid_qry=self.query_one(Hid).string()
        res_dsp=self.query_one(Result_Display)
        if hid_qry == "Validated": # after obtaining strings from reactive variables, if Validated existes, then contninue the execution
            self.add_class("app_sb_ni")
            self.remove_class("show_result")
        else: # if not Validated, program tells to validate
            res_dsp.rlt = str(bcolors.WARNING+"No chains validated, please validate them"+bcolors.RESET)
            self.add_class("show_result_and_seq")
            pass
    # if Validation section was aproved, then an input with id = sb_ni appeared...
    @on(Input.Submitted,"#sb_ni") # ... and when submitted, function "select_class" executes
    def select_class(self):
        res=self.query_one(Result_Display)
        self.remove_class("show_result")
        query=self.query_one("#sb_ni")
        selection=query.value # the value of input wich id = sb_ni is obtained, and whether the result is, two ways are possible:
        query.value=""
        if selection.upper() == "SB":
            # if the value of input wich id = sb_ni equals sb, then execute the following lines, for neccesary buttons and inputr to appear
            self.add_class("app_sb")
            self.add_class("initial")
            self.remove_class("app_sb_ni")
            self.add_class("app_volver")
            self.add_class("app_menu")
        elif selection.upper() == "NI":
            # if the value of input wich id = sb_ni equals ni, then execute the following lines, for neccesary buttons and inputr to appear
            self.add_class("app_ni")
            self.add_class("initial")
            self.remove_class("app_sb_ni")
            self.add_class("app_volver")
            self.add_class("app_menu")
        else: res.rlt = str(bcolors.FAIL + "No correct input submitted, retry" + bcolors.RESET);self.add_class("show_result")
    @on(Input.Submitted,"#sb")
    # when input equals sb, then a new input which id = sb appears. When submitted, function "fragments" executes 
    def fragments(self):
        self.remove_class("show_result_and_seq")
        self.remove_class("show_result")
        try: # after removing the classes thar show results, try the following
            seq_query=self.query_one(Seq_Display).string()
            res_query=self.query_one(Result_Display)
            ipt_query=self.query_one("#sb")
            ipt_val=ipt_query.value
            ipt_query.value="" #obtain the value of the input that has id = sb
            res_query.rlt=str("You have selected option 5, fragments option\n\n")
            seq_split=seq_query[1:].split(">");records=[]
            for sec in seq_split: records.append(sec.strip()) # obtain clean sequences from the input of sequences stored in the reactive variable os Seq_Display
            ipt=ipt_val.split(",") # split the input value obtained from input id = sb before
            if len(ipt)==1:
                ipt.append(0)
            assert(len(ipt)==2) # if after split, only one value has been provided, then add 0 as default for the seocnd value (sequence selection)
            int(ipt[1]) 
            if int(ipt[1]) > len(records)-1: #otherwise, assert the second value is numeric and less than the total number of seuqences
                raise ValueError("num")#if not, raise an error
            for i in ipt[0]:
                if i.upper() not in "ACGT":
                    raise NameError("sub") #if the first value is not composed of A,C,G o T then raise another error
            # if asserts above are correct, then use a method from DNA_Toolkit to obtain number of fragments X form seq Y
            appearances,new_list=Operador_ADN(records[int(ipt[1])]).fragmentos(ipt[0].upper())
            res_query.rlt=res_query.rlt+str("{0} appears {1} times\n".format(ipt[0],appearances)) #display the result with this format
            res_query.rlt=res_query.rlt + str("\n"+new_list)
            self.add_class("show_result")
        #depending the type of the error, raise the correct information stirng
        except ValueError: # error corresponding to the second value of input, incorrect number
            res_query.rlt = str(bcolors.FAIL + "No correct number provided, retry" + bcolors.RESET)
            self.add_class("show_result_and_seq")
            pass
        except NameError: # error corresponding to the first value of the input, incorrect substring
            res_query.rlt = str(bcolors.FAIL + "No correct sub_sequence provided, retry" + bcolors.RESET)
            self.add_class("show_result_and_seq")
            pass
        except AssertionError: #incorret assert
            res_query.rlt = str(bcolors.FAIL + "No correct integer or comma separated elements provided, retry" + bcolors.RESET)
            self.add_class("show_result_and_seq")
            pass
    @on(Input.Submitted,"#ni")
    # when input equals ni, then a new input which id = ni appears. When submitted, function "island" executes 
    def island(self):
        self.remove_class("show_result_and_seq")
        self.remove_class("show_result")
        try: #when exectuted, try the following without errors
            seq_query=self.query_one(Seq_Display).string()
            res_query=self.query_one(Result_Display) # do queries to obtain values and prepare reactive variables to change or for display
            ipt_query=self.query_one("#ni")
            ipt_val=ipt_query.value
            ipt_query.value="" #obtain the value from input it = ni and reset it
            res_query.rlt=str("You have selected option 5, islands option\n\n")
            seq_split=seq_query[1:].split(">");records=[]
            for sec in seq_split: records.append(sec.strip()) #obtain clean sequs from the string obtained from reactive value
            ipt=ipt_val.split(",")
            if len(ipt)==2:
                ipt.append(0) # if the value from the input, after split by ",", has only two values, then add 0 value for seq selection as default
            assert(len(ipt)==3) # after, check that there are 3 values from the input after the split
            int(ipt[0]) #check the first one is a number ...
            assert(int(ipt[0])>1) #... and is above one
            int(ipt[2]) #also check the third value is a number
            if int(ipt[2]) > len(records)-1 or int(ipt[0]) > len(records[int(ipt[2])]):
            # also, if the first number tat specifies the minimum lenght of the island is higher tan length of seq
            # of if number two (third element) that specifies the seq selecter, is higher than total number os seqs
            #then rise an error (Value error)
                raise ValueError("num") 
            for i in ipt[1]:
                if i.upper() not in "ACGT": #if the second element is not composed of A,C,G or T, then rise anotcher error (name error)
                    raise NameError("nt")
            dic, ls= Operador_ADN(records[int(ipt[2])]).islas(ipt[1].upper(),int(ipt[0])) #if no error raised, then execture function from DNA_Toolkit
            # oobtain a dict with the initial and end positions of island, , the lenght and the island 
            #also obtain a new seq with the island as lowercase letters
            cont=0
            for k,v in dic.items():
                string="".join(v)
                long=len(v)# for each element in the dict, display it as follows
                res_query.rlt = res_query.rlt + str("{0}: {1} - {2} repetitions\n".format(k,string,long))
                cont=cont+1
            if cont==0: # y no island has been detected with ths parameters specified, display the following label
                res_query.rlt = str("No matches found, retry. Seq selected:")
            res_query.rlt = res_query.rlt + str("\n"+ls)
            self.add_class("show_result")

        except ValueError: # error corresponding to the second value of input, incorrect number
            res_query.rlt = str(bcolors.FAIL + "No correct number provided, retry" + bcolors.RESET)
            self.add_class("show_result_and_seq")
            pass
        except NameError:# error corresponding to the second value of the input, incorrect substring
            res_query.rlt = str(bcolors.FAIL + "No correct sub_sequence provided, retry" + bcolors.RESET)
            self.add_class("show_result_and_seq")
            pass
        except AssertionError:#incorret assert
            res_query.rlt = str(bcolors.FAIL + "No correct integer or comma separated elements provided, retry" + bcolors.RESET)
            self.add_class("show_result_and_seq")
            pass



    @on(Button.Pressed,"#two_six")
    def complementary_reverse(self): # if button with id = two_six is pressed, execute function "complementary_reverse"
        hid_qry=self.query_one(Hid).string()
        res_dsp=self.query_one(Result_Display)
        if hid_qry == "Validated": # if seqs are validated, continue with the execution 
            self.add_class("initial")
            self.add_class("app_volver")
            self.add_class("app_menu")
            self.remove_class("app_sb_ni") # display all buttons and inputs necessary
            seq_dsp = self.query_one(Seq_Display).string()
            res_dsp = self.query_one(Result_Display) # obtain string inputs form reactive variables and prepare others  
            res_dsp.rlt = str("You have selected option 6\n\n")
            seq_split=seq_dsp[1:].split(">");records=[]
            for sec in seq_split: records.append(sec.strip()) #obtain clean seqs from string input
            p=0
            for sec in records: # and for each clean sequence
                chain_dic=Operador_ADN(sec).comp_and_rev() # obtain a dict containing the normal, seq, reverse and complementary
                res_dsp.rlt=res_dsp.rlt + str("Sequence number {0}\n".format(p))            
                for k,v in chain_dic.items(): #display each sequence with the format in the following line
                    res_dsp.rlt = res_dsp.rlt + str("The {0} chain is: {1}\n".format(k,v))
                res_dsp.rlt = res_dsp.rlt + "\n"
                p=p+1
            self.add_class("show_result") #display the result
        else:
            res_dsp.rlt = str(bcolors.WARNING+"No chains validated, please validate them"+bcolors.RESET) # if no seq validated, program tells to do it
            self.add_class("show_result_and_seq")
            pass


    
    @on(Button.Pressed, "#two_seven")
    def islas_CG(self): # if button with id = two_seven is pressed, execute function "islas_CG"
        hid_qry=self.query_one(Hid).string()
        res_dsp=self.query_one(Result_Display)
        if hid_qry == "Validated":# if seqs are validated, continue with the execution 
            self.add_class("initial")
            self.add_class("app_volver")
            self.add_class("app_menu")
            self.remove_class("app_sb_ni")# display all buttons and inputs necessary
            seq_read=self.query_one(Seq_Display).string()
            res_read=self.query_one(Result_Display)# obtain string inputs form reactive variables and prepare others
            res_read.rlt = str("You have selected option 7\n\n")
            seq_split=seq_read[1:].split(">");records=[]
            for sec in seq_split: records.append(sec.strip())#obtain clean seqs from string input
            p=0
            for sec in records:# and for each clean sequence
                islas=Operador_ADN(sec).percentGC() #obtain the corresponding %CG, and display it followinf the format: "CpG percentage in Sequence "P" is: "X"%
                res_read.rlt = res_read.rlt + str("CpG percentage in Sequence "+str(p)+" is: "+bcolors.OK + str(islas)+ bcolors.RESET+ " %\n")
                p=p+1
            self.add_class("show_result")
        else:
            res_dsp.rlt = str(bcolors.WARNING+"No chains validated, please validate them"+bcolors.RESET) # if no seq validated, program tells to do it
            self.add_class("show_result_and_seq")
            pass


    @on(Button.Pressed, "#db1")
    def acceso_db(self):
        self.add_class("ops_menu")
        self.add_class("db_menu")
        self.add_class("app_menu")
    
    @on(Button.Pressed, "#ens")
    def ensembl(self):
        self.add_class("app_ipt_ens")
    @on(Input.Submitted, "#ipt_ens")
    def ens_ipt(self):
        self.remove_class("db_menu")
        self.remove_class("app_menu")
        self.add_class("app_exitdb")
        try:
            ipt=self.query_one("#ipt_ens")
            ens_value=ipt.value
            ipt.value=""
            rlt_dsp=self.query_one(Result_Display)
            rlt_dsp.rlt=""
            elements,a=DB_Parse(ens_value).Ensembl_info()
            if a==1:
                col=["ID","object_type","species", "description"]
            elif a == 2:
                col=["ID","object_type","species", "logic_name", "Parent"]
            x = 0
            for i in col:
                rlt_dsp.rlt = rlt_dsp.rlt + str(i+": "+elements[x]+"\n")
                x=x+1
            if elements != []:
                try:
                    seq=DB_Parse(ens_value).Ensembl_seq()
                    rlt_dsp.rlt = rlt_dsp.rlt + str("Seq: "+seq[0:50]+"..."+"["+str(len(seq))+"]")
                    self.add_class("app_db_seq")
                    sq=self.query_one(Seq_Display)
                    sq.seq = str(">"+seq)
                except:
                    raise ValueError()
            else: rlt_dsp.rlt = "No info aviable"
            self.add_class("show_result")
        except ValueError:
            rlt_dsp.rlt = rlt_dsp.rlt + str(colorama.Fore.YELLOW + "No seq aviable in Ensembl" + colorama. Style.RESET_ALL)
            self.add_class("show_result")
        except NameError:
            rlt_dsp.rlt = str(colorama.Fore.YELLOW + "No id aviable in Ensembl" + colorama. Style.RESET_ALL)
            self.add_class("show_result")
        except:
            rlt_dsp.rlt = str(colorama.Fore.RED + "Cant connect to Ensembl" + colorama. Style.RESET_ALL)
            self.add_class("show_result")


    @on(Button.Pressed, "#uni")
    def uniprot(self):
        self.add_class("app_ipt_uni")
    @on(Input.Submitted, "#ipt_uni")
    def uni_ipt(self):
        self.remove_class("db_menu")
        self.remove_class("app_menu")
        self.add_class("app_exitdb")
        try:
            val=self.query_one("#ipt_uni")
            Uniref=val.value
            val.value=""
            rlt_dsp=self.query_one(Result_Display)
            rlt_dsp.rlt=""
            response=DB_Parse(Uniref).UniProt_info()
            col=["Accession","Evidence","organism","name","Seq"]
            x=0
            for i in col:
                if i != col[-1]:
                    rlt_dsp.rlt = rlt_dsp.rlt + str(i+": "+ response[x]+"\n")
                    x=x+1
                else: 
                    if len(response[x]) >= 50:
                        rlt_dsp.rlt = rlt_dsp.rlt + str(i+": "+ response[x][0:50]+"...")
                    else: rlt_dsp.rlt = rlt_dsp.rlt + str(i+": "+ response[x])
            self.add_class("show_result")
        except NameError:
            rlt_dsp.rlt = str(colorama.Fore.YELLOW + "No id aviable in Uniprot" + colorama. Style.RESET_ALL)
            self.add_class("show_result")
        except:
            rlt_dsp.rlt = str(colorama.Fore.RED + "Cant connect to Uniprot" + colorama. Style.RESET_ALL)
            self.add_class("show_result")
            
    @on(Button.Pressed, "#db_seq")
    def guarda_seq_menu(self):
        self.remove_class("ops_menu")
        self.add_class("initial")
        self.remove_class("show_result")
        self.remove_class("app_volver")
        self.remove_class("app_menu")
        self.remove_class("app_Seq_input")
        self.remove_class("app_Mut_input")
        self.remove_class("App_butmut")
        self.remove_class("app_n_file")
        self.remove_class("app_num_chain")
        self.remove_class("app_sb_ni")
        self.remove_class("app_sb")
        self.remove_class("app_ni")
        self.remove_class("show_result_and_seq")
        self.remove_class("db_menu")
        self.remove_class("app_db_seq")
        self.remove_class("app_ipt_ens")
        self.remove_class("app_exitdb")






    @on(Button.Pressed, "#two_eight")
     # if button with id = two_eight is pressed, execute function "back_menu"
    def back_menu(self):
        #this function allows to display only the widgets that appear in the main menu, as initial, with the seqs user have been working with 
        self.remove_class("ops_menu")
        self.add_class("initial")
        self.remove_class("show_result")
        self.remove_class("app_volver")
        self.remove_class("app_menu")
        self.remove_class("app_Seq_input")
        self.remove_class("app_Mut_input")
        self.remove_class("App_butmut")
        self.remove_class("app_n_file")
        self.remove_class("app_num_chain")
        self.remove_class("app_sb_ni")
        self.remove_class("app_sb")
        self.remove_class("app_ni")
        self.remove_class("show_result_and_seq")




    @on (Button.Pressed, "#volver")
    # if button with id = volver is pressed, execute function "vuelta"
    def vuelta(self):
        # this button appears when inside an operation in ops_menu, an allows user to go back to ops_menu, with all the widgets that should appear
        # and also mantaining seqs validated, and with the seqs user have been working with
        self.add_class("ops_menu")
        self.remove_class("initial")
        self.remove_class("show_result")
        self.remove_class("app_volver")
        self.remove_class("app_menu")
        self.remove_class("app_Seq_input")
        self.remove_class("app_Mut_input")
        self.remove_class("App_butmut")
        self.remove_class("app_n_file")
        self.remove_class("app_num_chain")
        self.remove_class("app_sb_ni")
        self.remove_class("app_sb")
        self.remove_class("app_ni")
        self.remove_class("show_result_and_seq")



    @on (Button.Pressed, "#back_menu")
    # if button with id = back_menu is pressed, execute function "vuelta_menu"
    def vuelta_menu(self):
        # this button appears when inside an operation in ops_menu, an allows user to go back to main menu, with all the widgets that should appear
        # and also mantaining seqs validated, and with the seqs user have been working with
        self.remove_class("ops_menu")
        self.add_class("initial")
        self.remove_class("show_result")
        self.remove_class("app_volver")
        self.remove_class("app_menu")
        self.remove_class("app_Seq_input")
        self.remove_class("app_Mut_input")
        self.remove_class("App_butmut")
        self.remove_class("app_n_file")
        self.remove_class("app_num_chain")
        self.remove_class("app_sb_ni")
        self.remove_class("app_sb")
        self.remove_class("app_ni")
        self.remove_class("show_result_and_seq")
        self.remove_class("db_menu")
    

    @on(Button.Pressed, "#exitdb")
    def return_from_db(self):
        self.add_class("db_menu")
        self.add_class("app_menu")
        self.remove_class("app_exitdb")
        self.remove_class("app_ipt_uni")
        self.remove_class("app_ipt_ens")
        rst=self.query_one(Result_Display)
        rst.rlt = str("No result")
        self.remove_class("show_result")
        sq=self.query_one(Seq_Display)
        sq.seq = str("[[No initial chain loaded]]")




class Exit_save(ModalScreen): # creation of a new widget. This time, this widget is a pop-up window that appears when new seq has been created
    # it allows to save this new sew when exiting the program, if it hasnt been saved yet manually 
    # theis caracteristics are stored in CSS file
    def __init__(self, chain):
        self.chain = chain # to do that, Exit_save widget need to have the new seq as argument, so constructor is needed to obtain this new seq
        super().__init__()
    def compose(self): # this function allows the creation of buttons, input and labels (elements) inside this new widget
        with Container():
            yield Label("Exit saving new seq?: "+str(self.chain[0:5])+"...", id="up_label")
            with Horizontal(): # buttons are displayed horizontally
                yield Button("Yes",variant="success", id="Exitsaving")
                yield Button("No",variant="error", id="Exitprogram")
                yield Button("Quit", variant="warning", id="quit")
            yield Input(placeholder="Write the name of the file: ",id="save_file")
            yield Label(str(bcolors.OK + "Result saved succesfully in program folder!" + bcolors.RESET), id="label_fin")
            yield Label(str(bcolors.FAIL + "No correct string provided" + bcolors.RESET), id="label_fail")

    @on(Button.Pressed, "#Exitprogram") # when pop-up appears, if button with id = Exitprogram is pressed, no seq is saved and program is closed
    def leave(self):
        DNA_Toolkit.exit(self)

    @on(Button.Pressed, "#Exitsaving") # when pop-up appears, if button with id = Esxitsaving is pressed, procedure to save the sequence is initialized
    def exit_save(self):
        self.add_class("app_save_file") # a label to write the name of the fiule containing the seq appears...
    @on(Input.Submitted, "#save_file") #...and when submitted, exit_save_2 function is executed
    def exit_save_2(self):
        try:
            file=self.query_one("#save_file")
            file_n=file.value #file name is obtained
            if file_n == "":
                raise ValueError("Name empty") #if file name is empty, raise an error
            file.value=""
            Operador_ADN(self.chain).saver(file_n) # file is created and seq stored using procedure explained in button id = two
            self.remove_class("app_label_fail")
            self.remove_class("app_save_file")
            self.add_class("app_label_fin")
        except:
            self.add_class("app_label_fail")
            
    @on(Button.Pressed, "#quit")
    def exit_total(self): # when stored, a button with id = quit appears, allowing to close the program
        DNA_Toolkit.exit(self)

        

class DNA_Toolkit(App): #creation of the app itself, when widgets and elements are stored and displayed
    #Also, in the App, bindings can be created. Bindings are buttons at the bottom part of the App. that bind to a specific letter of the keyboard 
    # Bindings can call functions or widgets inside the app
    # Bindings are defined as below, and called with "action_" prefix, that define what that binding do
    BINDINGS=[
        ("d","dark_mode","dark_mode"),
        ("7","exit","exit"),
    ]
    CSS_PATH = "DNA_Toolkit_Scrollable.css" #allows to obtain the instructions stored in CSS file to run the program correctly 
    def compose(self): #Definition of app composition#Se ponen los widgets de los que se va a compner la app
        yield Header(show_clock=True) # Clock establishment in the header 
        yield Footer() #Allows bindings to appear

        with ScrollableContainer(): # allows to appear widgets inside the app, and allows scrolling
            #This time, widget Interfaz_1 with class initial will appear when app starts
            yield Interfaz_1(classes="initial")


    def action_dark_mode(self): #definition of what "dark_mode" binding do (alternate between dark mode)
        self.dark = not self.dark
    def action_exit(self):
        save_str=self.query_one(Saving).string()
        if save_str != "[[No new seq]]":
            #definition of what "exit" or number 7 binding do
            # when new seq is created, this binding allows pop-up saving window to apear, else, exits program
            self.push_screen(Exit_save(chain=save_str)) 
        else: DNA_Toolkit.exit(self)




        
if __name__ == "__main__": #execute program
    DNA_Toolkit().run()