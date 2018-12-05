# -*- coding: utf-8 -*-
# Advanced zoom example. Like in Google Maps.
# It zooms only a tile, but not the whole image. So the zoomed tile occupies
# constant memory and not crams it with a huge resized image for the large zooms.
#Voir problème de mise à jour de matrice

import random, warnings
import tkinter as tk
from tkinter import ttk,Label
import subprocess
import sys
import numpy as np
import re
from PIL import Image, ImageTk

test = True
zoom = sys.argv[1]
box = sys.argv[2]

Image.MAX_IMAGE_PIXELS = 1000000000
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

def images_to_load(box, level):
    global m
    if level == 32768:
        m = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        (x1_, y1_, xf_, yf_) = (box[0], box[1], box[2], box[3])

        case1_x = x1_//8192
        taille_x = xf_-x1_
        case1_y = y1_//8192
        taille_y = yf_-y1_

        if taille_x <= 8192 and taille_y <= 8192:
            m[case1_x][case1_y] = 1
        elif taille_x > 8192 and taille_y <= 8192:
            m[case1_x][case1_y] = 1
            m[case1_x + 1][case1_y] = 1
        elif taille_x <= 8192 and taille_y > 8192:
            m[case1_x][case1_y] = 1
            m[case1_x][case1_y + 1] = 1
        elif taille_x > 8192 and taille_y > 8192:
            m[case1_x][case1_y + 1] = 1
            m[case1_x][case1_y + 1] = 1

    elif level == 16384:
        m = [[0,0],[0,0]]
        (x1_, y1_, xf_, yf_) = (box[0], box[1], box[2], box[3])

        if xf_ < 8192 and yf_ < 8192:
            m[0][0] = 1
        elif x1_ > 8192 and yf_ < 8192:
            m[0][1] = 1
        elif xf_ < 8192 and y1_ > 8192:
            m[1][0] = 1
        elif x1_ > 8192 and y1_ > 8192:
            m[1][1] = 1
        elif yf_ < 8192:
            m[0][0] = 1
            m[0][1] = 1
        elif y1_ > 8192:
            m[1][0] = 1
            m[1][1] = 1
        elif xf_ < 8192:
            m[0][0] = 1
            m[1][0] = 1
        elif x1_ > 8192:
            m[0][1] = 1
            m[1][1] = 1
        else:
            m = [[1,1],[1,1]]

    return m

def create_im_haut(box, m, level):
    if level == 32768:
        (x1_, y1_, xf_, yf_) = (box[0], box[1], box[2], box[3])

        case1_x = x1_//8192
        taille_x = xf_-x1_
        case1_y = y1_//8192
        if taille_x < 8192:
            return(Image.open('C400/C400-Mesh_32768_' + str(case1_x) + '_' + str(case1_y) + '.png'), True)
        else:
            images = map(Image.open, ['C400/C400-Mesh_32768_' + str(case1_x) + '_' + str(case1_y) + '.png',
                                        'C400/C400-Mesh_32768_' + str(case1_x + 1) + '_' + str(case1_y) + '.png'])
            widths, heights = zip(*(i.size for i in images))

            total_width = sum(widths)
            max_height = max(heights)

            new_im_haut = Image.new('RGB', (total_width, max_height), color = None)

            images = map(Image.open, ['C400/C400-Mesh_32768_' + str(case1_x) + '_' + str(case1_y) + '.png',
                                        'C400/C400-Mesh_32768_' + str(case1_x + 1) + '_' + str(case1_y) + '.png'])
            x_offset = 0
            for im in images:
                new_im_haut.paste(im, (x_offset,0))
                x_offset += im.size[0]
            haut = True
            return(new_im_haut, haut)
    elif level == 16384:
        if not ((m[0][0] == 0) and (m[0][1] == 0)):
            if (m[0][0] == 1) and (m[0][1] == 1):

                images = map(Image.open, [path163841, path163842])
                widths, heights = zip(*(i.size for i in images))

                total_width = sum(widths)
                max_height = max(heights)

                new_im_haut = Image.new('RGB', (total_width, max_height), color = None)

                images = map(Image.open, [path163841, path163842])
                x_offset = 0
                for im in images:
                    new_im_haut.paste(im, (x_offset,0))
                    x_offset += im.size[0]
                haut = True
                return(new_im_haut, haut)
            elif (m[0][0] == 0) and (m[0][1] == 1):
                new_im_haut = Image.open(path163842)
                haut = True
                return(new_im_haut, haut)

            elif (m[0][0] == 1) and (m[0][1] == 0):
                new_im_haut = Image.open(path163841)
                haut = True
                return(new_im_haut, haut)
        else:
            return([], False)

def create_im_bas(box, m, level):
    if level == 32768:
        (x1_, y1_, xf_, yf_) = (box[0], box[1], box[2], box[3])

        case1_x = x1_//8192
        taille_x = xf_-x1_
        case1_y = y1_//8192
        taille_y = yf_-y1_

        if taille_y < 8192:
            return([], False)
        else:
            if taille_x < 8192:
                return(Image.open('C400/C400-Mesh_32768_' + str(case1_x) + '_' + str(case1_y + 1) + '.png'), True)
            else:
                images = map(Image.open, ['C400/C400-Mesh_32768_' + str(case1_x) + '_' + str(case1_y + 1) + '.png',
                                            'C400/C400-Mesh_32768_' + str(case1_x + 1) + '_' + str(case1_y + 1) + '.png'])
                widths, heights = zip(*(i.size for i in images))

                total_width = sum(widths)
                max_height = max(heights)

                new_im_haut = Image.new('RGB', (total_width, max_height), color = None)

                images = map(Image.open, ['C400/C400-Mesh_32768_' + str(case1_x) + '_' + str(case1_y + 1) + '.png',
                                            'C400/C400-Mesh_32768_' + str(case1_x + 1) + '_' + str(case1_y + 1) + '.png'])
                x_offset = 0
                for im in images:
                    new_im_haut.paste(im, (x_offset,0))
                    x_offset += im.size[0]
                haut = True
                return(new_im_haut, haut)
    elif level == 16384:
        if not ((m[1][0] == 0) and (m[1][1] == 0)):
            if (m[1][0] == 1) and (m[1][1] == 1):

                images = map(Image.open, [path163843, path163844])
                widths, heights = zip(*(i.size for i in images))

                total_width = sum(widths)
                max_height = max(heights)

                new_im_bas = Image.new('RGB', (total_width, max_height), color = None)

                images = map(Image.open, [path163843, path163844])
                x_offset = 0
                for im in images:
                    new_im_bas.paste(im, (x_offset,0))
                    x_offset += im.size[0]
                return(new_im_bas, True)


            elif (m[1][0] == 0) and (m[1][1] == 1):
                new_im_bas = Image.open(path163844)
                return(new_im_bas, True)

            elif (m[1][0] == 1) and (m[1][1] == 0):
                new_im_bas = Image.open(path163843)
                return(new_im_bas, True)
        else:
            return([], False)

def create_im(boxs, m, level):
    haut = False
    bas = False

    im_haut,haut = create_im_haut(boxs, m, level)
    im_bas, bas = create_im_bas(boxs, m, level)


    if (bas == True and haut == True):
        images = [im_haut,im_bas]
        widths, heights = zip(*(i.size for i in images))


        max_width = max(widths)
        total_height = sum(heights)

        new_im = Image.new('RGB', (max_width, total_height), color = None)

        images = [im_haut,im_bas]
        y_offset = 0
        for im in images:
            new_im.paste(im, (0,y_offset))
            y_offset += im.size[1]

        return(new_im)

    elif bas == True:
        new_im = im_bas
        return(new_im)

    elif haut == True:
        new_im = im_haut
        return(new_im)


class AutoScrollbar(ttk.Scrollbar):
    ''' A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager '''
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise tk.TclError('Cannot use place with this widget')

class Zoom_Advanced(ttk.Frame):
    ''' Advanced zoom of the image '''
    def __init__(self, mainframe):

        ''' Initialize the main Frame '''
        ttk.Frame.__init__(self, master=mainframe)
        self.master.title('Zoom with mouse wheel')
        # Vertical and horizontal scrollbars for canvas
        vbar = AutoScrollbar(self.master, orient='vertical')
        hbar = AutoScrollbar(self.master, orient='horizontal')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='we')
        # Create canvas and put image on it
        self.canvas = tk.Canvas(self.master, highlightthickness=0,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.canvas.update()  # wait till canvas is created
        vbar.configure(command=self.scroll_y)  # bind scrollbars to the canvas
        hbar.configure(command=self.scroll_x)
        # Make the canvas expandable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        # Bind events to the Canvas
        #self.canvas.scan_dragto()
        self.m = images_to_load(boxs, level)
        self.canvas.bind('<Configure>', self.show_image)  # canvas is resized
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>',     self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up
        # Création de l'image que l'on souhaite étudier
        self.image = create_im(boxs, self.m, level)  # open image

        self.width, self.height = self.image.size
        self.imscale = 1  # scale for the canvaas image
        self.delta = 2  # zoom magnitude
        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.canvas.create_rectangle(0, 0, self.width, self.height, width=0)
        # Plot some optional random rectangles for the test purposes
        '''
        minsize, maxsize, number = 5, 20, 10
        for n in range(number):
            x0 = random.randint(0, self.width - maxsize)
            y0 = random.randint(0, self.height - maxsize)
            x1 = x0 + random.randint(minsize, maxsize)
            y1 = y0 + random.randint(minsize, maxsize)
            color = ('red', 'orange', 'yellow', 'green', 'blue')[random.randint(0, 4)]
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, activefill='black')
        '''
        self.initial_show_image(boxs[0] ,boxs[1])

    def scroll_y(self, *args, **kwargs):
        ''' Scroll canvas vertically and redraw the image '''
        self.canvas.yview(*args, **kwargs)  # scroll vertically
        self.show_image()  # redraw the image

    def scroll_x(self, *args, **kwargs):
        ''' Scroll canvas horizontally and redraw the image '''
        self.canvas.xview(*args, **kwargs)  # scroll horizontally
        self.show_image()  # redraw the image

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.show_image()  # redraw the image

    def initial_show_image(self, xg, yg, event=None):

        self.canvas.update()
        print("chargement")
        if(xg > self.width - 600):
            xg = self.width - 600
        if(xg < 0):
            xg = 0
        if(yg > self.height - 600):
            yg = self.height - 600
        if(yg < 0):
            yg = 0

        self.canvas.scan_dragto(-xg,-yg, gain=1)
        self.show_image()

    def wheel(self, event):

        global test
        ''' Zoom with mouse wheel '''
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        bbox = self.canvas.bbox(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]: pass  # Ok! Inside the image
        else: return  # zoom only inside image area
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        print(event.delta,"event.delta",test)
        if event.num == 5 or event.delta == -120:  # scroll down
            i = min(self.width, self.height)
            if int(i * self.imscale) < 300: return  # image is less than 30 pixels
            self.imscale /= self.delta
            scale        /= self.delta
            print(scale,self.imscale)
        if event.num == 4 or event.delta == 120:  # scroll up
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
#            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            if int(i * self.imscale) > 15000: return
            self.imscale *= self.delta
            scale        *= self.delta
            test = False
#            process = subprocess.Popen("./darknet detect cfg/yolov3.cfg yolov3.weights " + path2 + name_pict +str(i) + '.png >> base.csv', shell=True, stdout=subprocess.PIPE)
#            print(scale,self.imscale)
        self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
        self.show_image()

    def show_image(self, event=None):

        ''' Show image on the Canvas '''
        test = True
        bbox1 = self.canvas.bbox(self.container)  # get image area
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        print(bbox1,"test1")
        bbox2 = (self.canvas.canvasx(0),  # get visible area of the canvas
                 self.canvas.canvasy(0),
                 self.canvas.canvasx(self.canvas.winfo_width()),
                 self.canvas.canvasy(self.canvas.winfo_height()))
        print(bbox2,"canva visible")
        print(bbox2[3] - self.canvas.canvasx(self.canvas.winfo_reqwidth()))
        bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
                max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
        print(bbox,"test3")
        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]
        self.canvas.configure(scrollregion=bbox)  # set scroll region
        x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(bbox2[1] - bbox1[1], 0)
        x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        #Insérer ici l'évolution de la matrice M
        print(self.m)
        self.m = self.update(x1,y1,x2,y2,level)
        print("This is m", self.m)
        print("aaa",x1,y1,x2,y2)
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            x = min(int(x2 / self.imscale), self.width)   # sometimes it is larger on 1 pixel...
            y = min(int(y2 / self.imscale), self.height)  # ...and sometimes not
            print(int(x1 / self.imscale), int(y1 / self.imscale),int(x2 / self.imscale),int(y2 / self.imscale),self.width,self.height)
            image = self.image.crop((int(x1 / self.imscale), int(y1 / self.imscale), x, y))
            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
            imageid = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
                                               anchor='nw', image=imagetk)
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

    def left_right_update(self, x1, y1, x2, y2, level):
        global thru, lim
        test = True
        lim_droite = level // 8192 - 1
        if (level == 16384):
            thru = 2
            lim = 8192
        elif (level == 32768):
            thru = 4
            lim = 16384
        if x1 == 0:
            if (self.m[0][0] == 1) or (self.m[1][0] == 1) or (self.m[2][0] == 1) or (self.m[3][0] == 1):
                print("Tout à gauche")
            else:
                for j in range(thru):
                    for i in range(thru):
                        if self.m[i][j] == 1:
                            if self.m[i][j+1] == 0:
                                self.m[i][j-1] = 1
                            else:
                                self.m[i][j-1] = 1
                                self.m[i][j+1] = 0

        elif x2 == lim:
            if (self.m[0][lim_droite] == 1) or (self.m[1][lim_droite] == 1) or (self.m[2][lim_droite] == 1) or (self.m[3][lim_droite] == 1):
                print("Tout à droite")
            else:
                for j in range(thru-1,0,-1):
                    for i in range(thru):
                        if self.m[i][j] == 1:
                            if self.m[i][j-1] == 0:
                                self.m[i][j+1] = 1
                            else:
                                self.m[i][j-1] = 0
                                self.m[i][j+1] = 1
        return(self.m)

    def update(self, x1, y1, x2, y2, level):
        global thru, lim
        lim_bas = level // 8192 - 1
        if (level == 16384):
            thru = 2
            lim = 8192
        elif (level == 32768):
            thru = 4
            lim = 16384

        if y1 == 0:
            if (self.m[0][0] == 1) or (self.m[0][1] == 1) or (self.m[0][2] == 1) or (self.m[0][3] == 1):
                #define new level
                print("Tout en haut")
            else:
                for i in range(thru):
                    for j in range(thru):
                        if self.m[i][j] == 1:
                            if self.m[i+1][j] == 0:
                                self.m[i-1][j] = 1
                            else:
                                self.m[i+1][j] = 0
                                self.m[i-1][j] = 1

        elif y2 == lim:
            if (self.m[lim_bas][0] == 1) or (self.m[lim_bas][1] == 1) or (self.m[lim_bas][2] == 1) or (self.m[lim_bas][3] == 1):
                #define new level
                print("Tout en bas")
            else:
                for i in range(thru):
                    for j in range(thru,0,-1):
                        if self.m[i][j] == 1:
                            if self.m[i-1][j] == 0:
                                self.m[i+1][j] = 1
                            else:
                                self.m[i+1][j] = 1
                                self.m[i-1][j] = 0

        self.m = self.left_right_update(x1, y1, x2, y2, level)
        return(self.m)
"""
    #def load_new_images(box, level, m):


"""
class InputApp(ttk.Frame):
	def __init__(self, master=None):
		ttk.Frame.__init__(self, master)

		self.root2 = tk.Toplevel()
		self.root2.title('Integration of label coordinates')
		self.root2.geometry('500x100')

		self.pack()
		self.output()

	def output(self):
		self.labelBox = Label(self.root2, text='Coordonnées:')
		self.labelBox.pack(side=tk.LEFT, padx=5, pady=5)

		self.inputBox = tk.Entry(self.root2, width=10)
		self.inputBox.pack(side=tk.LEFT ,padx=5, pady=5)

		self.submitButton = tk.Button(self.root2, text='Submit', command=self.saveLabel)
		self.submitButton.pack(side=tk.RIGHT, padx=5, pady=5)

		self.root2.bind("<Return>", self.saveLabel)

	def saveLabel(self, event=None):
		global label
		label = self.inputBox.get()

		self.root2.quit()
		self.root2.destroy()

	def start(self):
		self.root2.after(1, lambda: self.root2.focus_force())
		self.inputBox.focus()
		self.root2.mainloop()



#path = 'C400/'+path_  # place path to your image here
#path = '1MFibres-32768_THD.png'  # place path to your image here
path163841 = 'C400/C400-Mesh_16384_0_0.png'
path163842 = 'C400/C400-Mesh_16384_1_0.png'
path163843 = 'C400/C400-Mesh_16384_0_1.png'
path163844 = 'C400/C400-Mesh_16384_1_1.png'

path327681 = 'C400/C400-Mesh_32768_0_0.png'
path327682 = 'C400/C400-Mesh_32768_1_0.png'
path327683 = 'C400/C400-Mesh_32768_2_0.png'
path327684 = 'C400/C400-Mesh_32768_3_0.png'
path327685 = 'C400/C400-Mesh_32768_0_1.png'
path327686 = 'C400/C400-Mesh_32768_1_1.png'
path327687 = 'C400/C400-Mesh_32768_2_1.png'
path327688 = 'C400/C400-Mesh_32768_3_1.png'
path327689 = 'C400/C400-Mesh_32768_0_2.png'
path3276810 = 'C400/C400-Mesh_32768_1_2.png'
path3276811 = 'C400/C400-Mesh_32768_2_2.png'
path3276812 = 'C400/C400-Mesh_32768_3_2.png'
path3276813 = 'C400/C400-Mesh_32768_0_3.png'
path3276814 = 'C400/C400-Mesh_32768_1_3.png'
path3276815 = 'C400/C400-Mesh_32768_2_3.png'
path3276816 = 'C400/C400-Mesh_32768_3_3.png'

level = int(zoom)
coeff1 = int("6000")/8192
#inputWindow = InputApp()
#inputWindow.start()
boxs = ([int(s) for s in box.split(",") if s.isdigit()])
print(boxs)
#Lancement de tkinter
root = tk.Tk()
root.geometry('600x600') # Size 200, 200
app = Zoom_Advanced(root)
root.mainloop()
