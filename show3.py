# -*- coding: utf-8 -*-
# Advanced zoom example. Like in Google Maps.
# It zooms only a tile, but not the whole image. So the zoomed tile occupies
# constant memory and not crams it with a huge resized image for the large zooms.
import random, warnings
import tkinter as tk
from tkinter import ttk,Label
import subprocess
import sys
import numpy as np
import re
from PIL import Image, ImageTk

test = True
box = sys.argv[1]

Image.MAX_IMAGE_PIXELS = 1000000000
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

def images_to_load(box):
    m = [0,0,0,0]
    (x1_, y1_, xf_, yf_) = (box[0], box[1], box[2], box[3])

    if xf_ < 8192 and yf_ < 8192:
        m[0] = 1
    elif x1_ > 8192 and yf_ < 8192:
        m[1] = 1
    elif xf_ < 8192 and y1_ > 8192:
        m[2] = 1
    elif x1_ > 8192 and y1_ > 8192:
        m[3] = 1
    elif yf_ < 8192:
        m[0] = 1
        m[1] = 1
    elif y1_ > 8192:
        m[2] = 1
        m[3] = 1
    elif xf_ < 8192:
        m[0] = 1
        m[2] = 1
    elif x1_ > 8192:
        m[1] = 1
        m[3] = 1
    else:
        m = [1,1,1,1]

    return m

def create_im(m):
    haut = False
    bas = False
    if not ((m[0] == 0) and (m[1] == 0)):
        if (m[0] == 1) and (m[1] == 1):

            images = map(Image.open, [path1, path2])
            widths, heights = zip(*(i.size for i in images))

            total_width = sum(widths)
            max_height = max(heights)

            new_im = Image.new('RGB', (total_width, max_height), color = None)

            images = map(Image.open, [path1, path2])
            x_offset = 0
            for im in images:
                new_im.paste(im, (x_offset,0))
                x_offset += im.size[0]

            new_im.save('haut.png')
            haut = True
        elif (m[0] == 0) and (m[1] == 1):
            new_im = Image.open(path2)
            new_im.save('haut.png')
            haut = True

        elif (m[0] == 1) and (m[1] == 0):
            new_im = Image.open(path1)
            new_im.save('haut.png')
            haut = True

    if not ((m[2] == 0) and (m[3] == 0)):
        if (m[2] == 1) and (m[3] == 1):

            images = map(Image.open, [path3, path4])
            widths, heights = zip(*(i.size for i in images))

            total_width = sum(widths)
            max_height = max(heights)

            new_im = Image.new('RGB', (total_width, max_height), color = None)

            images = map(Image.open, [path3, path4])
            x_offset = 0
            for im in images:
                new_im.paste(im, (x_offset,0))
                x_offset += im.size[0]

            new_im.save('bas.png')
            bas = True

        elif (m[2] == 0) and (m[3] == 1):
            new_im = Image.open(path4)
            new_im.save('bas.png')
            bas = True

        elif (m[2] == 1) and (m[3] == 0):
            new_im = Image.open(path3)
            new_im.save('bas.png')
            bas = True

    if (bas == True and haut == True):
        images = map(Image.open, ['haut.png', 'bas.png'])
        widths, heights = zip(*(i.size for i in images))


        max_width = max(widths)
        total_height = sum(heights)

        new_im = Image.new('RGB', (max_width, total_height), color = None)

        images = map(Image.open, ['haut.png', 'bas.png'])
        y_offset = 0
        for im in images:
            new_im.paste(im, (0,y_offset))
            y_offset += im.size[1]

        new_im.save('image_final.png')

    elif bas == True:
        new_im = Image.open('bas.png')
        new_im.save('image_final.png')

    elif haut == True:
        new_im = Image.open('haut.png')
        new_im.save('image_final.png')


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
    def __init__(self, mainframe, path):

        global coeff1
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
        self.canvas.bind('<Configure>', self.show_image)  # canvas is resized
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>',     self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up
        self.image = Image.open(path)  # open image
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
"""


#path = 'C400/'+path_  # place path to your image here
#path = '1MFibres-32768_THD.png'  # place path to your image here
path1 = 'C400/C400-Mesh_16384_0_0.png'
path2 = 'C400/C400-Mesh_16384_1_0.png'
path3 = 'C400/C400-Mesh_16384_0_1.png'
path4 = 'C400/C400-Mesh_16384_1_1.png'

coeff1 = int("6000")/8192
#inputWindow = InputApp()
#inputWindow.start()
boxs = ([int(s) for s in box.split(",") if s.isdigit()])

# Création de l'image que l'on souhaite étudier
m = images_to_load(boxs)
create_im(m)

#Lancement de tkinter
root = tk.Tk()
root.geometry('600x600') # Size 200, 200
app = Zoom_Advanced(root, path='image_final.png')
root.mainloop()
