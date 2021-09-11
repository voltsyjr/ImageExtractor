from kivy.app import App
from kivy.core import text
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.properties import ObjectProperty

class PdfExtract(GridLayout):
    data = ObjectProperty(None)
    

    def logic(self,pdff):
        import fitz as ft
        # file=input('Enter Your Pdf Name (with .pdf): ')
        file = pdff[0]
        # print('this is file: ',file)
        # jj=input('Enter Your Pdf Name (with .pdf): ')
        # file=self.ids.data.text
        # file=self.txt.text
        substr=file[:-4]
        # print(substr)
        ext=file[-4:]
        if ext[:1]=='.':
            if ext!='.pdf':
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


        self.pop = Popup(
                title="Execution Result",
                size = (400,400),
                content=Label(
                    text=""
                ),
                size_hint=(0.4,0.4)
            )

        self.pop.content.text= 'Image extraction completed'
        self.pop.open()
    
    def selected(self,filename):
        try:
            pdff=filename[0]
        
        except:
            pass

class ExtractImageApp(App):
    def build(self):
        return PdfExtract()

ExtractImageApp().run()