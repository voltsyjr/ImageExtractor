from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from random import randint
from kivy.lang import Builder
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from plyer import filechooser
from kivy.properties import ListProperty
from kivy.uix.button import Button
import fitz as ft
from kivy.core.window import Window
Window.clearcolor = (0, 0.5, 0.3, 0.5)

class Main(GridLayout):

    selection = ListProperty([])

    def choose(self):
        '''
        Call plyer filechooser API to run a filechooser Activity.
        '''
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        '''
        Callback function for handling the selection response from Activity.
        '''
        self.selection = selection
        #print(str(selection))


    def logic(self,pdff):
            self.pop = Popup(
                    title="Execution Result",
                    size = (400,400),
                    content=Label(
                        text=""
                    ),
                    size_hint=(0.4,0.4)
                )

            # file=input('Enter Your Pdf Name (with .pdf): ')
            file = pdff
            # print('this is file: ',file)
            # jj=input('Enter Your Pdf Name (with .pdf): ')
            # file=self.ids.data.text
            # file=self.txt.text
            substr=file[:-4]
            # print(substr)
            ext=file[-4:]
            if ext[:1]=='.':
                if ext!='.pdf':
                    self.pop.content.text= 'Invalid Formate Please Choose pdf File'
                    self.pop.open()
                    return
            else:
                file=file + '.pdf'
            substr=file[:-4]

            pdf=ft.open(file)
            # print(len(pdf))
            # image_list=set()
            totalImage=0
            for i in range(len(pdf)):
                image_list=(pdf.getPageImageList(i))
                # print(f'{image_list} {i}')
            # i=1
                for image in image_list:   
                    xref =  image[0]
                    pix = ft.Pixmap(pdf, xref)
                    if pix.n<5:   
                        pix.writePNG("%s_%s.png" % (substr,totalImage+1))
                        totalImage=totalImage+1
                    else:   
                        pix1= ft.Pixmap(ft.csRGB, pix)
                        pix1.writePNG("%s_%s.png" % (substr,totalImage+1))
                        totalImage=totalImage+1
                        pix1=None
                    pix=None 


            
            self.pop.content.text= 'Image extraction completed'
            self.pop.open()
    


    def on_selection(self, *a, **k):
        '''
        Update TextInput.text after FileChoose.selection is changed
        via FileChoose.handle_selection.
        '''
        pdff=self.selection[0]
        print(pdff)
        self.logic(pdff)
        # self.b_t.ii = self.selection[0]
        # self.box.ii = self.selection[0]
        




class RunApp(App):
    def build(self):
        game = Main()
        return game

if __name__ == '__main__':
    RunApp().run()