from typing import ContextManager
from kivy.app import App 
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.layout import Layout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from random import randint
import json
import os
import re
ligne = 30
colonnes = 40

def verif(tab):
    liste_changement = []
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            vivante = 0

            # x o o
            # o o o
            # o o o
            if i - 1 >= 0 and j - 1 >= 0:
                if tab[i-1][j-1] == 1:
                    vivante = vivante + 1
                    
            # o x o
            # o o o
            # o o o
            if i - 1 >= 0:
                if tab[i-1][j] == 1:
                    vivante = vivante + 1

            # o o x
            # o o o
            # o o o
            if i - 1 >= 0 and j + 1 < len(tab[i]):
                if tab[i-1][j+1] == 1:
                    vivante = vivante + 1
                    
            # o o o
            # x o o
            # o o o
            if j - 1 >= 0:
                if tab[i][j-1] == 1:
                    vivante = vivante + 1
                    

            # o o o
            # o o x
            # o o o
            if j + 1 < len(tab[i]):
                if tab[i][j+1] == 1:
                    vivante = vivante + 1
                    
                    
            # o o o
            # o o o
            # x o o
            if i + 1 < len(tab) and j - 1 >= 0:
                if tab[i+1][j-1] == 1:
                    vivante = vivante + 1
                    
            # o o o
            # o o o
            # o x o
            if i + 1 < len(tab):
                if tab[i+1][j] == 1:
                    vivante = vivante + 1
                    
            # o o o
            # o o o
            # o o x
            if i + 1 < len(tab) and j + 1 < len(tab[i]):
                if tab[i+1][j+1] == 1:
                    vivante = vivante + 1

            
            celluletype = tab[i][j]
            if celluletype == 0 and vivante == 3:
                changement = []
                changement.append(1)
                changement.append(i)
                changement.append(j)
                liste_changement.append(changement)
                pass
            if celluletype == 1:
                if vivante == 2 or vivante == 3:
                    pass
                else:
                    changement = []
                    changement.append(0)
                    changement.append(i)
                    changement.append(j)
                    liste_changement.append(changement)

    for i in liste_changement:
        tab[i[1]][i[2]] = i[0]
    return tab



class Exemple(BoxLayout):
    def build(self):
        self.ligne = ligne
        self.colonnes = colonnes
        self.temps = 0.5
        self.box = BoxLayout(orientation='horizontal')

        self.Mes_Boutons()
        return self.box
    
    def loadBoutons(self, tab):
        if tab == 0:
            tableau = [[0 for j in range(self.colonnes)] for i in range(self.ligne)]
        else:
            tableau = tab
        self.Liste_Boutons=[]
        try:
            self.grid.clear_widgets()
            
        except:
            pass
        for i in range(len(tableau)):
            self.Liste_Boutons.append([])
            for j in range(len(tableau[i])):
                self.Liste_Boutons[i].append(Button())
                self.Liste_Boutons[i][j].text=str(tableau[i][j])
                self.Liste_Boutons[i][j].id=str(i)+"_"+str(j)
                self.Liste_Boutons[i][j].bind(on_press=self.Une_Fonction_Bouton)
                self.grid.add_widget(self.Liste_Boutons[i][j])
                if tableau[i][j] == 0:
                    self.Liste_Boutons[i][j].background_color=[0.5,0.5,0.5,1]
                else:
                    self.Liste_Boutons[i][j].background_color=[0,1,0,1]
        
    def Mes_Boutons(self, tab=0):
        self.grid = GridLayout(rows=self.ligne, cols=self.colonnes, size_hint=(.8,1))
        self.box.add_widget(self.grid)

        self.loadBoutons(tab)

        self.menu = BoxLayout(orientation='vertical', size_hint=(.2,1))
        self.btn_start = Button(text=str('START'))
        self.btn_start.bind(on_press=self.play)
        self.menu.add_widget(self.btn_start)
        self.btn_random = Button(text=str("RANDOM"))
        self.btn_random.bind(on_press=self.random)
        self.menu.add_widget(self.btn_random)
        self.box.add_widget(self.menu)
        self.btn_parms = Button(text=str("PARAMETRES"))
        self.btn_parms.bind(on_press=self.parms)
        self.menu.add_widget(self.btn_parms)


    def parms(self, instance):
        self.focus = False
        content = BoxLayout(orientation="vertical")
        self.popup = Popup(title="Parmètres", content=content)
        if self.btn_start.text == "STOP":
            self.function_interval.cancel()
        self.parmtab = self.Liste_Boutons.copy()
        BoxLigne = BoxLayout(orientation="horizontal")
        LabelLigne = Label(text="Ligne:", halign="right")
        BoxLigne.add_widget(LabelLigne)
        self.InputLigne = TextInput(text=str(self.ligne), multiline=False)
        self.InputLigne.bind(text=self.edit_text, on_text_validate=self.ligne_valide, focus=self.on_focus)
        BoxLigne.add_widget(self.InputLigne)
        content.add_widget(BoxLigne)

        BoxCol = BoxLayout(orientation="horizontal")
        LabelCol = Label(text="Colonnes:", halign="right")
        BoxCol.add_widget(LabelCol)
        self.InputCol = TextInput(text=str(self.colonnes), multiline=False)
        self.InputCol.bind(text=self.edit_text, on_text_validate=self.col_validate, focus=self.on_focus)
        BoxCol.add_widget(self.InputCol)
        content.add_widget(BoxCol)

        Sauvegarde_Load = BoxLayout(orientation="horizontal")
        Sauvegarde = Button(text="Sauvegarder")
        Sauvegarde.bind(on_press=self.sauvegarde)
        Sauvegarde_Load.add_widget(Sauvegarde)
        Load = Button(text="Load")
        Load.bind(on_press=self.load)
        Sauvegarde_Load.add_widget(Load)
        content.add_widget(Sauvegarde_Load)
        Btn_Retour = Button(text="RETOUR")
        Btn_Retour.bind(on_press=self.Fermer)
        content.add_widget(Btn_Retour)
        
        self.popup.open()
    def on_focus(self, instance, value):
        self.focus = True
    def Fermer(self,instance):
        if self.focus:
            self.col_validate(0)
            self.ligne_valide(0)
            self.focus=False
        self.popup.dismiss()
    def sauvegarde(self,instance):
        self.popop = Popup(title="Sauvegarde")
        self.FileChooserSauver = FileChooserListView(path=os.path.abspath(os.getcwd()), dirselect=False)
        Box = BoxLayout(orientation="horizontal")
        Box.add_widget(self.FileChooserSauver)
        Box_bas = BoxLayout(orientation="vertical")
        Box.add_widget(Box_bas)
        self.LabelfileSauver=TextInput(multiline=False)
        Box_bas.add_widget(self.LabelfileSauver)
        Sauver = Button(text="Sauvegarder")
        Retour = Button(text="Retour")
        
        Box_bas.add_widget(Sauver)
        Box_bas.add_widget(Retour)
        Retour.bind(on_press=self.popop.dismiss)
        self.popop.add_widget(Box)
        Sauver.bind(on_press=self.sauver)
        self.popop.open()

    def sauver(self, instance):
        if len(self.LabelfileSauver.text) <1:
            return
        else:
            liste=[[0 for j in range(self.colonnes)] for i in range(self.ligne)]
            for a in self.Liste_Boutons:
                for b in a:
                    i, j = b.id.split("_")
                    liste[int(i)][int(j)] = int(b.text) 
            with open(self.FileChooserSauver.path+"\\"+self.LabelfileSauver.text+".json", "w") as donnees:
                json.dump(liste,donnees)
            self.popop.dismiss()

    def load(self,instance):
        self.pop = Popup(title="Load Fichier")
        
        Box = BoxLayout(orientation="horizontal")
        self.loadfileLayout = Label(text="Aucun Fichier")

        FileChooser = FileChooserListView(path=os.path.abspath(os.getcwd()), dirselect=False)
        FileChooser.bind(selection=self.selected)

        Retour = Button(text="Retour")
        Retour.bind(on_press=self.pop.dismiss)
        LoadFile = Button(text="Lancer")
        LoadFile.bind(on_press=self.load_file)
        Box_Retour_Press = BoxLayout(orientation="vertical")
        Box_Retour_Press.add_widget(LoadFile)

        Box_Retour_Press.add_widget(Retour)
        Box.add_widget(self.loadfileLayout)
        Box.add_widget(Box_Retour_Press)

        content = BoxLayout(orientation="vertical")
        content.add_widget(FileChooser)
        content.add_widget(Box)

       
        self.pop.add_widget(content)
        self.pop.open()

    def load_file(self, instance):
        if self.loadfileLayout.text == "Aucun Fichier":
            return
        else:
            name, extansion = os.path.splitext(self.loadfileLayout.text)
            if extansion != ".json":
                return
            else:
                with open(self.loadfileLayout.text) as donnes:
                    data = json.load(donnes)
                self.ligne = len(data)
                self.colonnes = len(data[0])
                self.box.clear_widgets()
                self.Mes_Boutons(data)
                self.pop.dismiss()
                self.popup.dismiss()
    def selected(self, fc_instance, selection):
        try:
            self.loadfileLayout.text=str(selection[0])
        except:
            pass
    def ligne_valide(self, instance):
        if len(self.InputLigne.text)<1 or int(self.InputLigne.text)<1:
            self.InputLigne.text = "1"
        self.ligne = int(self.InputLigne.text)
        self.box.clear_widgets()
        self.Mes_Boutons()
    def col_validate(self, instance):
        if len(self.InputCol.text)<1 or int(self.InputCol.text)<1:
            self.InputCol.text = "1"
        self.colonnes = int(self.InputCol.text)
        self.box.clear_widgets()
        self.Mes_Boutons()
    def edit_text(self, instance, value):
        
        for i in value:
            try: 
                nbr=int(i)
            except:
                value = re.sub(i,"", value)
        instance.text = value
    
    def random(self,instance):
        liste=[[0 for j in range(self.colonnes)] for i in range(self.ligne)]
        for i in range(len(liste)):
            for j in range(len(liste[i])):
                self.Liste_Boutons[i][j].text = str(randint(0,1))
                if self.Liste_Boutons[i][j].text == "0":
                    self.Liste_Boutons[i][j].background_color=[0.5,0.5,0.5,1]
                else:
                    self.Liste_Boutons[i][j].background_color=[0,1,0,1]
        
    def Une_Fonction_Bouton(self,instance):
        if instance.text == "0":
            instance.text = "1"
            instance.background_color=[0,1,0,1]
        else:
            instance.text = "0"
            instance.background_color=[0.5,0.5,0.5,1]
            
    def play(self,instance):
        if instance.text == "START":
            instance.text = "STOP"
            self.function_interval = Clock.schedule_interval(self.launch, self.temps)
        elif instance.text == "STOP":
            instance.text = "START"
            self.function_interval.cancel()

    def launch(self, instance):
        liste=[[0 for j in range(self.colonnes)] for i in range(self.ligne)]
        for a in self.Liste_Boutons:
            for b in a:
                i, j = b.id.split("_")
                liste[int(i)][int(j)] = int(b.text)
           
        newmatrice=verif(liste)
        for i in range(len(newmatrice)):
            for j in range(len(newmatrice[i])):
                self.Liste_Boutons[i][j].text = str(newmatrice[i][j])
                if self.Liste_Boutons[i][j].text == "0":
                    self.Liste_Boutons[i][j].background_color=[0.5,0.5,0.5,1]
                else:
                    self.Liste_Boutons[i][j].background_color=[0,1,0,1]

class App(App):
    def build(self):
        
        root=Exemple().build()
        self.title = "Jeu de la Vie"
        
        return root

App().run()
