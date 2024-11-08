import tkinter as tk
import perlin


shape = (0.5,0.5)
res = (21,28)
perlin_noise = perlin.perlinGrid(-shape[0], -shape[1], shape[0], shape[1], res[0], res[1])


win = tk.Tk()

donnees=tk.Frame(win, width=1182, height=40, bg='gray')
canevas=tk.Canvas(win, width=982, height=737, bg='white')
panneau=tk.Frame(win, width=200, height=737, bg='gray')


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
    canevas.itemconfig(item, outline='black', width = 1)
    canevas.tag_lower(item)


    outlineontop()

def on_click(event):
    for child in panneau.winfo_children():
        print(child)
        child.destroy()
    x = event.x
    y = event.y
    i = x//taillecase
    j = y//taillecase
    player="lime"
    squareData=tk.Label(panneau, text='Case '+str(i)+', '+str(j), bg='gray')
    squareData.pack(side="top")
    if 'captured' not in canevas.gettags(carte[i][j]):
        if j==0 and i==0:
            if 'captured' in canevas.gettags(carte[i+1][j]) or 'captured' in canevas.gettags(carte[i][j+1]):
                captureButton(i,j,player)
        elif j==0:
            if 'captured' in canevas.gettags(carte[i][j+1]) or 'captured' in canevas.gettags(carte[i+1][j]) or 'captured' in canevas.gettags(carte[i-1][j]):
                captureButton(i,j,player)
        elif i==0:
            if 'captured' in canevas.gettags(carte[i+1][j]) or 'captured' in canevas.gettags(carte[i][j+1]) or 'captured' in canevas.gettags(carte[i][j-1]):
                captureButton(i,j,player)
        elif i==len(carte)-1 and j==len(carte[i])-1:
            if 'captured' in canevas.gettags(carte[i-1][j]) or 'captured' in canevas.gettags(carte[i][j-1]):
                captureButton(i,j,player)
        elif i==len(carte)-1:
            if 'captured' in canevas.gettags(carte[i-1][j]) or 'captured' in canevas.gettags(carte[i][j+1]) or 'captured' in canevas.gettags(carte[i][j-1]):
                captureButton(i,j,player)
        elif j==len(carte[i])-1:
            if 'captured' in canevas.gettags(carte[i+1][j]) or 'captured' in canevas.gettags(carte[i][j-1]) or 'captured' in canevas.gettags(carte[i-1][j]):
                captureButton(i,j,player)
        else: 
            if 'captured' in canevas.gettags(carte[i+1][j]) or 'captured' in canevas.gettags(carte[i][j+1]) or 'captured' in canevas.gettags(carte[i][j-1]) or 'captured' in canevas.gettags(carte[i-1][j]):
                captureButton(i,j,player)
    
    
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
    canevas.itemconfig(carte[i][j], fill=final, outline='lime', tags=list(canevas.gettags(carte[i][j]))+['captured', 'capturedby*'+player])
    updateCapturedOutline(player)
    

def captureButton(i,j,player):
    print("lol")
    bouton=tk.Button(panneau, text="Capture", command=lambda: capture(i,j,player))
    bouton.pack()


def updateCapturedOutline(player):
    for adelete in canevas.find_withtag('capturedoutline*'+player):
        canevas.delete(adelete)
    for i in range(len(carte)):
        for j in range(len(carte[i])):
            if 'captured' in canevas.gettags(carte[i][j]):
                if 'capturedby*'+player in canevas.gettags(carte[i][j]):
                    if i==0:
                        canevas.create_line(i*taillecase+2,j*taillecase+2,i*taillecase+2,(j+1)*taillecase+2, fill=player, width=2, tags=['capturedoutline*'+player])
                    else:
                        if 'capturedby*'+player not in canevas.gettags(carte[i-1][j]):
                            canevas.create_line(i*taillecase+2,j*taillecase+2,i*taillecase+2,(j+1)*taillecase+2, fill=player, width=2, tags=['capturedoutline*'+player])
                    if j==0:
                        canevas.create_line(i*taillecase+2,j*taillecase+2,(i+1)*taillecase+2,j*taillecase+2, fill=player, width=2, tags=['capturedoutline*'+player])
                    else: 
                        if 'capturedby*'+player not in canevas.gettags(carte[i][j-1]):
                            canevas.create_line(i*taillecase+2,j*taillecase+2,(i+1)*taillecase+2,j*taillecase+2, fill=player, width=2, tags=['capturedoutline*'+player])
                    if i==len(carte)-1:
                        canevas.create_line((i+1)*taillecase+2,j*taillecase+2,(i+1)*taillecase+2,(j+1)*taillecase+2, fill=player, width=2, tags=['capturedoutline*'+player])
                    else:
                        if 'capturedby*'+player not in canevas.gettags(carte[i+1][j]):
                            canevas.create_line((i+1)*taillecase+2,j*taillecase+2,(i+1)*taillecase+2,(j+1)*taillecase+2, fill=player, width=2, tags=['capturedoutline*'+player])
                    if j==len(carte[i])-1:
                        canevas.create_line(i*taillecase+2,(j+1)*taillecase+2,(i+1)*taillecase+2,(j+1)*taillecase+2, fill=player, width=2, tags=['capturedoutline*'+player])
                    else:
                        if 'capturedby*'+player not in canevas.gettags(carte[i][j+1]):
                            canevas.create_line(i*taillecase+2,(j+1)*taillecase+2,(i+1)*taillecase+2,(j+1)*taillecase+2, fill=player, width=2, tags=['capturedoutline*'+player])




for i in range(len(carte)):
    for j in range(len(carte[i])):
        item = carte[i][j]
        canevas.tag_bind(item, '<Enter>', lambda event, item=item: on_enter(event, item))
        canevas.tag_bind(item, '<Leave>', lambda event, item=item: on_leave(event, item))



canevas.bind('<Button-1>', on_click)


capture(10,10,"lime")

donnees.pack(side='top')
canevas.pack(side='left')
panneau.pack(side='right')
win.resizable(False,False)
win.mainloop()
