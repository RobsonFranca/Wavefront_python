from tkinter import *
from threading import Thread
from time import sleep

LARGURA = 9
ALTURA = 9

tamanho_quadrado = 20

inicio = [1,1]
fim = [8,6]

def click(event):
    global lista
    item = event.widget
    x=(int(item.place_info()['x'])-1)/tamanho_quadrado
    y=(int(item.place_info()['y'])-1)/tamanho_quadrado
    try:
        i = lista.index([x,y])
        lista.remove([x,y])
    except Exception:
        lista.append([x,y])
    
    Thread(target = calcular).start()


def desenhar(pixel,l):
    for item in l:
        eita = int(item[0]+item[1]*LARGURA)
        pixel[eita]['label'].configure(bg = 'gray')
        pixel[eita]['valor'] = -1

def is_not_rep(value):
    try:
        return todaspropagacao.index(value)<0
    except Exception:
        return True

def montarrota():
    global pixel, propagacao, n
    p = propagacao[:]
    propagacao.clear()
    for l in p:
        c = [l[0], l[1]-1]
        b = [l[0], l[1]+1]
        d = [l[0]+1, l[1]]
        e = [l[0]-1, l[1]]
        pixel[l[0]+l[1]*LARGURA]['valor'] = n
        if l[0]+1<LARGURA and pixel[d[0]+d[1]*LARGURA]['valor'] == 0:
            propagacao.append(d)
        if l[1]+1<ALTURA and pixel[b[0]+b[1]*LARGURA]['valor'] == 0:
            propagacao.append(b)
        if l[0]-1>=0 and pixel[e[0]+e[1]*LARGURA]['valor'] == 0:
            propagacao.append(e)
        if l[1]-1>=0 and pixel[c[0]+c[1]*LARGURA]['valor'] == 0:
            propagacao.append(c)
    
    propagacao = list(filter(is_not_rep, propagacao))
    todaspropagacao.append(propagacao[:])
    n+=1
    if len(propagacao)>0:
        montarrota()

def fazerrota(valor):
    global pixel, anterior
    c = [valor['x'], valor['y']-1]
    b = [valor['x'], valor['y']+1]
    d = [valor['x']+1, valor['y']]
    e = [valor['x']-1, valor['y']]
    if valor['label'].config()['background'][4] != 'red' and valor['label'].config()['background'][4] != 'green':
        valor['label'].configure(bg = 'blue')
    n = valor['valor']
    #print(n, (valor['x'],valor['y']))
    if c[1]>=0 and 0 < pixel[c[0]+c[1]*LARGURA]['valor'] < n:
        valor['label'].configure(text = '↑')
        fazerrota(pixel[c[0]+c[1]*LARGURA])
    elif b[1]<ALTURA and 0 < pixel[b[0]+b[1]*LARGURA]['valor'] < n:
        valor['label'].configure(text = '↓')
        fazerrota(pixel[b[0]+b[1]*LARGURA])
    elif d[0]<LARGURA and 0 < pixel[d[0]+d[1]*LARGURA]['valor'] < n:
        valor['label'].configure(text = '→')
        fazerrota(pixel[d[0]+d[1]*LARGURA])
    elif e[0]>=0 and 0 < pixel[e[0]+e[1]*LARGURA]['valor'] < n:
        valor['label'].configure(text = '←')
        fazerrota(pixel[e[0]+e[1]*LARGURA])
            

def calcular():
    global c,lista,pixel,propagacao,todaspropagacao,n
    n=1
    for item in c.winfo_children():
        item.configure(bg = 'white', text='')
    for item in pixel:
        item['valor'] = 0;
    
    i = 1
    desenhar(pixel,lista)
    pixel[inicio[0]+inicio[1]*LARGURA]['label'].configure(bg = 'green')
    pixel[fim[0]+fim[1]*LARGURA]['valor'] = 1
    pixel[fim[0]+fim[1]*LARGURA]['label'].configure(bg = 'red')

    propagacao = [fim]
    todaspropagacao = [fim]
    t = Thread(target = montarrota)
    t.start()
    while t.is_alive():
        pass
    t = Thread(target = fazerrota, args = [pixel[inicio[0]+inicio[1]*LARGURA]])
    t.start()


j = Tk()
j.configure(bg = 'black')
lista = []
'''
for y in range(ALTURA):
    for x in range(LARGURA):
        if x==0 or x == LARGURA-1 or y==0 or y==ALTURA-1:
            lista.append([x,y])'''

lista.append([3,1])
lista.append([3,2])

lista.append([3,3])
lista.append([3,4])

propagacao = [fim]
todaspropagacao = [fim]
n = 1

pixel = []
c = Canvas(j,width=LARGURA*tamanho_quadrado,height=ALTURA*tamanho_quadrado, bg = 'black')
c.pack()

for y in range(ALTURA):
    for x in range(LARGURA):
        l = Label(c, bd=0, fg = 'white', font = 'Arial 10 bold')
        l.bind('<Button-1>',click)
        l.place(x=x*tamanho_quadrado+1,y=y*tamanho_quadrado+1,height = tamanho_quadrado-2, width = tamanho_quadrado-2)
        pixel.append({'label':l,'valor':0,'x':x,'y':y})

Thread(target = calcular).start()

j.mainloop()



