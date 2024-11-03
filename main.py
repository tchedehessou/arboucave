import tkinter as tk
import perlin


shape = (0.5,0.5)
res = (21,28)
perlin_noise = perlin.perlinGrid(-shape[0], -shape[1], shape[0], shape[1], res[0], res[1])


win = tk.Tk()

donnees=tk.Frame(win, width=1182, height=40, bg='gray')
canevas=tk.Canvas(win, width=982, height=737, bg='white')
panneau=tk.Frame(win, width=200, height=737, bg='gray', relief='sunken')


taillecase = 35
carte = []

for i in range(len(perlin_noise)):
    carte.append([])
    for j in range(len(perlin_noise[i])):
        couleur = max(0, min(255, int((perlin_noise[i][j]+0.5)*255)))
        test = canevas.create_rectangle(2+i*taillecase, 2+j*taillecase, 2+i*taillecase+taillecase, 2+j*taillecase+taillecase, fill='gray' if couleur < 32 else 'green' if couleur < 210 else 'blue', outline='black')
        if couleur < 32:
            canevas.itemconfig(test, tags=['roche'])
        elif couleur < 210:
            canevas.itemconfig(test, tags=['herbe'])
        else:
            canevas.itemconfig(test, tags=['eau'])
        carte[i].append(test)

def on_enter(event, item):
    canevas.itemconfig(item, outline='red', width = 2)
    canevas.tag_raise(item, 'all')

def on_leave(event, item):
    """if 'captured' in canevas.gettags(item):
        if len(canevas.gettags(item)[2].split('*'))>1:
            color = canevas.gettags(item)[2].split('*')[1]
            canevas.itemconfig(item, outline=color, width = 2)
    else:
        canevas.itemconfig(item, outline='black', width = 1)
        canevas.tag_lower(item)"""


    canevas.itemconfig(item, outline='black', width = 1)
    canevas.tag_lower(item)


    outlineontop()

def on_click(event):
    x = event.x
    y = event.y
    i = x//taillecase
    j = y//taillecase
    player="light blue"
    capture(i,j,player)
    
def outlineontop():
    for i in carte:
        if 'captured' in canevas.gettags(i):
            canevas.tag_raise(i)
        
def capture(i,j,player):
    coul = canevas.itemcget(carte[i][j], 'fill')
    if 'captured' in canevas.gettags(carte[i][j]):
        return
    color = tuple((c//256 for c in win.winfo_rgb(coul)))
    playcolor = tuple((c//256 for c in win.winfo_rgb(player)))
    final='#'
    for val in range(3):
        aadd=str(hex((color[val]+playcolor[val])//2))[-2:]
        if aadd.startswith('x'):
            aadd='0'+aadd[1:]
        final+=aadd
    canevas.itemconfig(carte[i][j], fill=final, outline=player, tags=list(canevas.gettags(carte[i][j]))+['captured', 'capturedby*'+player])
    updateCapturedOutline(player)
    


def updateCapturedOutline(player):#i,j,player,checked = [], tocheck=[], cos=[]):
    for adelete in canevas.find_withtag('capturedoutline*'+player):
        canevas.delete(adelete)
    for i in range(1,len(carte)-1):
        for j in range(1,len(carte[i])-1):
            if 'captured' in canevas.gettags(carte[i][j]):
                if 'capturedby*'+player in canevas.gettags(carte[i][j]):
                    if 'capturedby*'+player in canevas.gettags(carte[i-1][j]):
                        canevas.create_line(






    """unfiltered=[]
    for i in range(len(carte)-1):
        for j in range(len(carte[i])-1):
            if 'capturedby*'+player in canevas.gettags(carte[i][j]):
                unfiltered.append([[i,j,i,j+1],[i,j+1,i+1,j+1],[i+1,j+1,i+1,j],[i+1,j,i,j]])
    flattened = []
    for item in unfiltered:
        for jtem in item:
            flattened.append(jtem)
    print(unfiltered)
    filtered=filtering(unfiltered, flattened)
    aflatten = tk._flatten(filtered)
    final=[point*taillecase+2 for point in aflatten]
    if canevas.find_withtag('capturedoutline*'+player):
        canevas.delete('capturedoutline*'+player)
    canevas.create_polygon(final, fill='', outline=player, width=2, tags=['capturedoutline*'+player])


def filtering(unfiltered, vecteurs, filtered=[]):
    for carre in range(len(unfiltered)):
        for vect in range(len(unfiltered[carre])):
            if unfiltered[carre][vect][2:4]+unfiltered[carre][vect][0:2] not in vecteurs:
                filtered.append(vect)
            else:
                filtered=filtering(unfiltered[carre+1:], vecteurs, filtered)
    
    return filtered"""


for i in range(len(carte)):
    for j in range(len(carte[i])):
        item = carte[i][j]
        canevas.tag_bind(item, '<Enter>', lambda event, item=item: on_enter(event, item))
        canevas.tag_bind(item, '<Leave>', lambda event, item=item: on_leave(event, item))

canevas.bind('<Button-1>', on_click)

donnees.pack(side='top')
canevas.pack(side='left')
panneau.pack(side='right')
win.resizable(False,False)
win.mainloop()
