import tkinter as tk
import perlin
import game


shape = (0.3,0.3)
res = (84,112)
perlin_noise = perlin.perlinGrid(-shape[0], -shape[1], shape[0], shape[1], res[0], res[1])


win = tk.Tk()

donnees=tk.Frame(win, width=1182, height=40, bg='gray')
canevas=tk.Canvas(win, width=982, height=737, bg='white')
panneau=tk.Frame(win, width=200, height=737, bg='gray')
panneau.pack_propagate(False)



taillecase = 35
carte = []

for i in range(len(perlin_noise)):
    carte.append([])
    for j in range(len(perlin_noise[i])):
        
        couleur = max(0, min(255, int((perlin_noise[i][j]+0.5)*255)))
        test = canevas.create_rectangle(i*taillecase, j*taillecase, i*taillecase+taillecase, j*taillecase+taillecase, fill='gray' if couleur < 32 else 'green' if couleur < 210 else 'blue', outline='black')
        terrain = 'roche' if couleur < 32 else 'herbe' if couleur < 210 else 'eau'
        if couleur < 32:
            canevas.itemconfig(test, tags=['roche'])
        elif couleur < 210:
            canevas.itemconfig(test, tags=['herbe'])
        else:
            canevas.itemconfig(test, tags=['eau'])
        tile=game.Case((i,j),test,terrain)
        carte[i].append(tile)



def on_enter(event, item):
    canevas.itemconfig(item.tkItem, outline='red', width = 2)
    canevas.tag_raise(item.tkItem, 'all')
    canevas.bind('<Button-1>', lambda event, item=item : on_click(item.coords))


def on_leave(event, item):
    canevas.itemconfig(item.tkItem, outline='black', width = 1)
    canevas.tag_lower(item.tkItem)
    
    canevas.unbind('<Button-1>')
    outlineontop()

def on_click(event):
    for child in panneau.winfo_children():
        child.destroy()
    x = event[0]
    y = event[1]
    player="lime"
    squareData=tk.Label(panneau, text='Case '+str(x)+', '+str(y), bg='gray')
    squareData.pack(side="top")
    showCaptureButton(x,y,player)
    
        
    
def outlineontop():
    pass
        
def capture(i,j,player):
    coul = canevas.itemcget(carte[i][j].tkItem, 'fill')
    if 'captured' in canevas.gettags(carte[i][j].tkItem):
        return
    color = tuple((c//256 for c in win.winfo_rgb(coul)))
    playcolor = tuple((c//256 for c in win.winfo_rgb(player)))
    final='#'
    for val in range(3):
        aadd=str(hex((color[val]+playcolor[val])//2))[-2:]
        if aadd.startswith('x'):
            aadd='0'+aadd[1:]
        final+=aadd
    canevas.itemconfig(carte[i][j].tkItem, fill=final, tags=list(canevas.gettags(carte[i][j].tkItem))+['captured', 'capturedby*'+player])
    updateCapturedOutline(player)
    




def captureButton(i,j,player):
    print("ll")
    bouton=tk.Button(panneau, text="Capture", command=lambda: capture(i,j,player))
    bouton.pack()

def showCaptureButton(i,j,player):
    if 'captured' not in canevas.gettags(carte[i][j].tkItem):
        if j == 0 and i == 0:
            if 'captured' in canevas.gettags(carte[i + 1][j].tkItem) or 'captured' in canevas.gettags(carte[i][j + 1].tkItem):
                captureButton(i, j, player)
        elif j == 0:
            if 'captured' in canevas.gettags(carte[i][j + 1].tkItem) or 'captured' in canevas.gettags(carte[i + 1][j].tkItem) or 'captured' in canevas.gettags(carte[i - 1][j].tkItem):
                captureButton(i, j, player)
        elif i == 0:
            if 'captured' in canevas.gettags(carte[i + 1][j].tkItem) or 'captured' in canevas.gettags(carte[i][j + 1].tkItem) or 'captured' in canevas.gettags(carte[i][j - 1].tkItem):
                captureButton(i, j, player)
        elif i == len(carte) - 1 and j == len(carte[i]) - 1:
            if 'captured' in canevas.gettags(carte[i - 1][j].tkItem) or 'captured' in canevas.gettags(carte[i][j - 1].tkItem):
                captureButton(i, j, player)
        elif i == len(carte) - 1:
            if 'captured' in canevas.gettags(carte[i - 1][j].tkItem) or 'captured' in canevas.gettags(carte[i][j + 1].tkItem) or 'captured' in canevas.gettags(carte[i][j - 1].tkItem):
                captureButton(i, j, player)
        elif j == len(carte[i]) - 1:
            if 'captured' in canevas.gettags(carte[i + 1][j].tkItem) or 'captured' in canevas.gettags(carte[i][j - 1].tkItem) or 'captured' in canevas.gettags(carte[i - 1][j].tkItem):
                captureButton(i, j, player)
        else:
            if 'captured' in canevas.gettags(carte[i + 1][j].tkItem) or 'captured' in canevas.gettags(carte[i][j + 1].tkItem) or 'captured' in canevas.gettags(carte[i][j - 1].tkItem) or 'captured' in canevas.gettags(carte[i - 1][j].tkItem):
                captureButton(i, j, player)


def updateCapturedOutline(player):
    for adelete in canevas.find_withtag('capturedoutline*'+player):
        canevas.delete(adelete)
    for i in range(len(carte)):
        for j in range(len(carte[i])):
            tile=carte[i][j].tkItem
            tilecos=canevas.coords(tile)
            if 'captured' in canevas.gettags(tile):
                if 'capturedby*'+player in canevas.gettags(tile):
                    if i==0:
                        canevas.create_line(tilecos[0],tilecos[1],tilecos[0],tilecos[3], fill=player, width=2, tags=['capturedoutline*'+player])
                    else:
                        if 'capturedby*'+player not in canevas.gettags(carte[i-1][j].tkItem):
                            canevas.create_line(tilecos[0],tilecos[1],tilecos[0],tilecos[3], fill=player, width=2, tags=['capturedoutline*'+player])
                    if j==0:
                        canevas.create_line(tilecos[0],tilecos[1],tilecos[2],tilecos[1], fill=player, width=2, tags=['capturedoutline*'+player])
                    else: 
                        if 'capturedby*'+player not in canevas.gettags(carte[i][j-1].tkItem):
                            canevas.create_line(tilecos[0],tilecos[1],tilecos[2],tilecos[1], fill=player, width=2, tags=['capturedoutline*'+player])
                    if i==len(carte)-1:
                        canevas.create_line(tilecos[2],tilecos[1],tilecos[2],tilecos[3], fill=player, width=2, tags=['capturedoutline*'+player])
                    else:
                        if 'capturedby*'+player not in canevas.gettags(carte[i+1][j].tkItem):
                            canevas.create_line(tilecos[2],tilecos[1],tilecos[2],tilecos[3], fill=player, width=2, tags=['capturedoutline*'+player])
                    if j==len(carte[i])-1:
                        canevas.create_line(tilecos[0],tilecos[3],tilecos[2],tilecos[3], fill=player, width=2, tags=['capturedoutline*'+player])
                    else:
                        if 'capturedby*'+player not in canevas.gettags(carte[i][j+1].tkItem):
                            canevas.create_line(tilecos[0],tilecos[3],tilecos[2],tilecos[3], fill=player, width=2, tags=['capturedoutline*'+player])

def do_zoom(event):
    x = canevas.canvasx(event.x)
    y = canevas.canvasy(event.y)
    factor = 1.001 ** event.delta
    canevas.scale(tk.ALL, x, y, factor, factor)

def do_zoom_in(event):
    global taillecase
    x = canevas.canvasx(event.x)
    y = canevas.canvasy(event.y)
    factor = 1.1
    taillecase=taillecase*factor
    canevas.config(scrollregion=(0,0,112*taillecase,84*taillecase))
    canevas.scale(tk.ALL, x, y, factor, factor) #https://stackoverflow.com/questions/48112492/canvas-scale-only-size-but-not-coordinates html
    

def do_zoom_out(event):
    global taillecase
    x = canevas.canvasx(event.x)
    y = canevas.canvasy(event.y)
    if taillecase>=8:
        factor = 0.9
        taillecase=taillecase*factor
        canevas.config(scrollregion=(0,0,112*taillecase,84*taillecase))
        canevas.scale(tk.ALL, x, y, factor, factor)

def test(event):
    print(canevas.canvasx(event.x),canevas.canvasy(event.y))

for i in range(len(carte)):
    for j in range(len(carte[i])):
        item = carte[i][j]
        canevas.tag_bind(item.tkItem, '<Enter>', lambda event, item=item: on_enter(event, item))
        canevas.tag_bind(item.tkItem, '<Leave>', lambda event, item=item: on_leave(event, item))

canevas.bind("<MouseWheel>", do_zoom) 

canevas.bind('<4>', do_zoom_in)
canevas.bind('<5>', do_zoom_out) 

canevas.bind('<ButtonPress-3>', test)
canevas.bind('<ButtonPress-2>', lambda event: canevas.scan_mark(event.x, event.y))
canevas.bind("<B2-Motion>", lambda event: canevas.scan_dragto(event.x, event.y, gain=1))


canevas.config(scrollregion=(0,0,112*taillecase,84*taillecase))




capture(10,10,"lime")

donnees.grid(column=0,row=0,columnspan=2)
canevas.grid(column=0,row=1)
panneau.grid(column=1,row=1)

win.resizable(False,False)
win.mainloop()
