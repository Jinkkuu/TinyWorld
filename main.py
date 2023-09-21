#!/usr/bin/python3
import random
import pygame,os,time,sys,threading,urllib.request
nline='\n'
axe=0
gamename='TinyWorld'
gamever='3.0.0910.0dev'
gameverspl=gamever.split('.')
gameminserve=int(gameverspl[0])+((1+float(gameverspl[1]))*float(gameverspl[2]))

gameupdateurl='N/A'
gameauthor='Pxki Games'
print('Starting Game...')
upscale=1
limitfps=60
maxmem=1024*1024
sfps=0
debugmode=True
if upscale<.9:
    print('Can not go down <=0.8')
    exit()
upscale=int(round(upscale))
introtiming=1/160
musictime=0
gamemode='not in use'
stop=0
worldtype=0
def music():
    A='music.mp3'
    global musictime
    if os.path.isfile(A):
        if not'musictime'in globals():
            musictime=0
        if time.time()>musictime:
            musictime=time.time()+13
            pygame.mixer.music.load(A)
            pygame.mixer.music.play()
username='User'+str(random.randint(1111,9999))
pallete=0,0,0
forepallete=255,255,255
blue=0,0,255
green=0,255,0
red=255,0,0
voidcolor=0,0,0
modsloaded=0
istd=False
texturepath='textures/'
gamepath='saves/'
saves=[]
savename=str(random.randint(11111,12345))+'.tw'
netqueue=''
netresult=''
playerlist=False
datapath='./data/'
if not os.path.isdir(datapath):
    os.mkdir(datapath)
    print('Created',datapath.replace('./','').replace('/',''))
settingskeystore=[False,False,False]
if os.path.isfile(datapath+'settings.db'):
    if not len(open(datapath+'settings.db').read().rstrip("\n").split("\n"))<3:
        settingskeystore=open(datapath+'settings.db').read().rstrip("\n").split("\n")
        for a in range(len(settingskeystore)):
            if settingskeystore[a].isdigit() or settingskeystore[a]=='True' or settingskeystore[a]=='False':
              settingskeystore[a]=eval(settingskeystore[a])
        if len(settingskeystore)>=4 and str(settingskeystore[3]).isdigit():
            limitfps=int(settingskeystore[3])
else:
    for a in range(1,4):
        settingskeystore.append(False)
    settingskeystore.append(limitfps)
print('Setting Language...')
lang='en'
print('Set Lang to '+lang)
print('This will be Used Later in the coming Updates')
langpack=open(datapath+'languages/en.lang').read().rstrip("\n").split(';')
print('index '+str(len(langpack)-1))
if os.path.isdir('Saves'):
    os.rename('Saves',gamepath)
if not os.path.isdir(texturepath):
    os.mkdir(texturepath)
if not os.path.isdir(gamepath):
    os.mkdir(gamepath)
if not os.path.isdir('mods'):
    os.mkdir('mods')
def stopnow():
    global stop
    stop=1
    exit()
def mineblock(posx,posy):
    for b in blockcolor:
        if(posx,posy,b)in chunks:
            chunks.remove((posx,posy,b))
            break
def placeblock(posx,posy,block):
    if not(posx,posy,block)in chunks:
        chunks.append((posx,posy,block))
def cbytes(size):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0

    while size >= 1000 and unit_index < len(units) - 1:
        size /= 1000
        unit_index += 1

    converted_size = f"{size:.2f} {units[unit_index]}"
    return converted_size
def game():
    global up,left,down,right,x,y,placemode,minemode,blockid,playerlist,activity,chunks,multinames,multipos
    multinames[0]=username
    move=1
    pos=-int(x)+((w//playersize)//2),-int(y)+((h//playersize)//2)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            stopnow()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_q:
                chunks=[]
                loaded=[]
                activity=1
            if event.key==pygame.K_w:up=True
            if event.key==pygame.K_x:
                if blockid>=len(blockcolor)-1:
                    blockid=0
                else:
                    blockid+=1
            if event.key==pygame.K_a:left=True
            if event.key==pygame.K_s:down=True
            if event.key==pygame.K_d:right=True
            if event.key==pygame.K_RCTRL:placemode=True
            if event.key==pygame.K_RALT:minemode=True
            if event.key==pygame.K_TAB:playerlist=True
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_w:up=False
            if event.key==pygame.K_a:left=False
            if event.key==pygame.K_s:down=False
            if event.key==pygame.K_d:right=False
            if event.key==pygame.K_RCTRL:placemode=False
            if event.key==pygame.K_RALT:minemode=False
            if event.key==pygame.K_TAB:playerlist=False
    # Clears Screen
    render('clear',((0,150,0),))
    if placemode:placeblock(pos[0],pos[1],blockcolor[blockid])
    elif minemode:mineblock(pos[0],pos[1])
    #Moves the Character
    if up:y+=move
    if down:y-=move
    if left:x+=move
    if right:x-=move
    #Block Rendering
    renderdistancex=(w//(playersize))
    renderdistancey=(h//(playersize))
    load=0
    for a in (tmp for tmp in chunks if tmp[0] <= pos[0]+renderdistancex and tmp[0] >= pos[0]-renderdistancex and tmp[1] <= pos[1]+renderdistancey and tmp[1] >= pos[1]-renderdistancey):
        load+=1
        ax=((playersize*a[0])+(playersize*(x)),(playersize*a[1])+(playersize*(y)))
        #pygame.draw.line(screen,(255,0,0),(w//2-playersize,h//2-playersize),ax)
        render('rect',arg=((playersize * a[0] + playersize * x,playersize * a[1] + playersize * y,playersize,playersize),a[2],False))
    if playerlist:
#        render('rect',arg=((20,20,w-40,200),(50,50,50),False))
        o=0
        render('rect',arg=((30,20,160,270),(20,20,20),False))
        render('text',arg=((40,30),(255,255,255)),text=str(len(multipos))+' Players')
        for a in multinames[:8]:
            if o==0:
                coco=(20,50,20)
            else:
                coco=(50,20,20)
            render('rect',arg=((35,50+(o),150,25),coco,False))
            render('text',arg=((40,54+(o)),(255,255,255)),text=a[:10])
            o+=30

#    if debugmode:
#        render('text',arg=((30,50),forepallete),text=blockid)
#        render('text',arg=((30,70),forepallete),text=(x,y))
#        render('text',arg=((30,90),forepallete),text='Loaded '+str(load))
    render('rect',arg=((playersize * pos[0] + playersize * x,playersize * pos[1] + playersize * y,playersize,playersize),(255,0,0),False))
    for a in range(1,len(blockcolor)+1):
        if blockid+a-1>=len(blockcolor)-1:
            tmp=-1
        else:
            tmp=blockid+a
        if not tmp==-1:
            render('rect',arg=((w//2-40-(25*a),h-70,20,20),blockcolor[tmp],True),bordercolor=forepallete)
    render('rect',arg=((w//2-40,h-80,40,40),blockcolor[blockid],True),bordercolor=forepallete)
if os.path.isfile(datapath+'game-dev.py'):
    print('Using External Game File')
    exec(open(datapath+'game-dev.py').read())
    gmode=True
else:
    gmode=False
def settingspage():
  global button,settingskeystore,activity,screen,firstcom,change,limitfps
  if change:
    tmp=open(datapath+'settings.db','w')
    if not len(settingskeystore)>=4:
        settingskeystore.append(limitfps)
    for a in settingskeystore:
        tmp.write(str(a)+'\n')
    tmp.close()
    change=False
  #settingskeystore[2],settingskeystore[1],fullscreen
  render('header')
  render('rect',arg=((-5,titlepos[1]+40,w+10,h-120),(0,0,0),True),bordercolor=forepallete)
  render('text',text=gamename + ' - '+langpack[21],arg=(titlepos,forepallete))
  setbutton=menu_draw((pygame.Rect(titlepos[0], titlepos[1]+55, 220, button_size_height//1.5),pygame.Rect(titlepos[0], titlepos[1]+100, 220, button_size_height//1.5),pygame.Rect(titlepos[0], titlepos[1]+145, 220, button_size_height//1.5),pygame.Rect(titlepos[0], titlepos[1]+190, 220, button_size_height//1.5),pygame.Rect(titlepos[0], titlepos[1]+235, 220, button_size_height//1.5),pygame.Rect(10, h-45, w-20, button_size_height/1.5),),((langpack[23] if settingskeystore[2] else langpack[22])+' '+langpack[24],(langpack[23] if settingskeystore[1] else langpack[22])+' '+langpack[25],(langpack[23] if settingskeystore[0] else langpack[22]) + ' '+langpack[26],'Notification Test',langpack[41]+str(limitfps),'<--'))
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      stopnow()
    if event.type == pygame.MOUSEBUTTONDOWN: 
        if setbutton == 1:
          settingskeystore[2] = not settingskeystore[2]
          change=True
        elif setbutton == 2:
          settingskeystore[1] = not settingskeystore[1]
          change=True
        elif setbutton == 3:
          settingskeystore[0] = not settingskeystore[0]
          change=True
          firstcom=False
          regen()
        elif setbutton == 4:
          notify('Boop :>')
        elif setbutton == 5:
          if not limitfps-30<10:
            limitfps-=30
          else:
            limitfps=120
          if len(settingskeystore)>=4:
              settingskeystore[3] = limitfps
          change=True
        elif setbutton == 6:
          activity = 1

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q:
        activity=1
fpstime=time.time()
fpstmp=0
fps=0
quickness=1
#def limiter():
#	global fpstime,fpstmp,sfps,fps
#	if time.time()-fpstime>1/quickness:
#		fps=int(fpstmp)
#		fpstmp=0
#		fpstime=time.time()
#	else:
#		fpstmp+=1*quickness
pygame.init()
font = pygame.font.SysFont(None, 24)
clock=pygame.time.Clock()
power=1
if not os.path.isfile('disableintro'):activity=0
else:activity=1
up=False
down=False
left=False
right=False
playersize=20
zoom=.5
tmpsize=playersize
maxplayer=8
chunks=[]
aipos=(0,2),(0,2)
aicolor=(0,100,0),(141,78,133),(141,182,0),(27,24,17)
radius=2**32
fpstime=time.time()
fps=0
fpstmp=0
maxsprite=int(radius*5)
messages='Weewoo!','Likies','Yo Mum','Baka','idiot','nikonikoni~'
voidsize=500
foodcount=0
targetx=0
targety=0
maxworldtime=450
blockcolor=[(100,0,0),(0,0,100),(100,100,100),(200,0,0),(0,0,100),(0,100,200),(224, 187, 228),(149, 125, 173), (210, 145, 188),(254, 200, 216)]
foodcolor=0,255,0
collide=True
gamemodes=['God','Mortal']
blockid=0
maxblock=len(blockcolor)
select=False
def render(type,arg=(0,0) , text='N/A',bordercolor=forepallete,borderradius=0):
#	print(type,arg,text)
    try:
        if type=='text':
            screen.blit(font.render(str(text), True, arg[1]), arg[0])
        elif type=='rect':
#			print(arg[0][0],arg[0][1],arg[0][2],arg[0][3])
            pygame.draw.rect(screen,arg[1],pygame.Rect(arg[0][0],arg[0][1],arg[0][2],arg[0][3]),border_radius=borderradius)
            if arg[2]:
                pygame.draw.rect(screen,bordercolor,pygame.Rect(arg[0][0],arg[0][1],arg[0][2],arg[0][3]),2,border_radius=borderradius)
            ## This was for a "Wireframe" Like Square
            #pygame.draw.rect(screen,(0,255,0),pygame.Rect(arg[0][0],arg[0][1],arg[0][2],arg[0][3]),1)
        elif type=='header':
            render('rect',arg=((0,-40,w,100),(50,50,50),False),borderradius=20)
        elif type=='clear':
            screen.fill(arg[0])
        else:
            crash('Render unsupported Type')
    except Exception as error:
        crash(str(error)+' (renderer)')

def save():
    global messagetime, message,chunks,aipos
    f = open(gamepath+savename, 'w')
    f.write(
        '(' + str(int(round(x))) + ',' +
        str(int(round(y))) + ',' +
        str(health) + ',' +
        str(radius) + ',' +
        str(aix) + ',' +
        str(aiy) + ',' +
        str(aitrigger) + ',' +
        str(collide) + ',' +
        str(worldtype) +
        '), ' +
        str(chunks).replace('[', '').replace(']', '')
    )
    f.close()
    chunks=[]
    aipos=[]
    notify('Saved World')
sight=False
def notify(text):
    global message,messagetime
    messagetime = time.time() + 5
    message = text
def respawn():
    for a in range(1,1000):place=False;pos=random.randint(1,x+100)//2,random.randint(1,y+100)//2;foodpos.append((pos[0],pos[1],random.randint(1,2)))
def reload():
    global aix,aiy,aipos,foodcount,health,worldtype,seed,x,y,radius,playersize,foodpos,gamemode,aitrigger,collide,aitime,aipot,wmenu,chunks,multipos,multinames
    x=0
    y=0
    health=100
    gamemode=gamemodes[0]
    if os.path.isfile(gamepath+savename):
        clear((0, 0, 0))
        filesize=os.stat(gamepath+savename).st_size
        render('text',text='Preparing World... ('+str(cbytes(filesize))+')',arg=((w//2-250, h // 2-20),forepallete))
        render('rect',arg=((w//2-250, h // 2,500,5),(50,50,50),False))
#        for a in range(1,filesize):
#            render('rect',arg=((w//2-250, h // 2,int((a/filesize)*500),5),(50,150,50),False))
#            pygame.display.flip()
        f = open(gamepath+savename, 'r').read().replace(nline, '').replace('+', ', ')
        aipos = list(eval(f))
        tmp = aipos[1:]
        pos = aipos[0]
        x = pos[0]
        y = pos[1]
        multipos=[(x,y),]
        multinames=['Loading...','FakeUser']
        multitime=[]
        try:
            worldtype=pos[8]
        except Exception:
            worldtype=0
        try:
            seed=pos[9]
        except Exception:
            seed=0
        chunks=[]
        for c in tmp:
            chunks.append(c) 
            
    t=time.time()+2;tok=0;xxx=time.time()+tok;fun=random.randint(1,len(messages))-1;fop=50
appear=False
targetmode=False
minemode=False
placemode=False
selected_save=0
aix=0
aiy=0
message=''
maxtime=5
aitrigger=1
up=False
down=False
left=False
right=False
place=False
mine=False
worldtype=2
def gamesaves():
    global savespos,savestext
    saves=os.listdir(gamepath)
    savespos=[]
    savestext=[]
    tmp=0
    for a in saves[:100]:
        tmp+=1
        savespos.append(pygame.Rect((w - button_size_width) // 2,(55*tmp)+20, button_size_width, button_size_height))
        savestext.append(a.replace('.tw','').replace('_',' '))

firstcom=False
def fullscreenchk():
    global w,h,w,h,screen,mmenu,button_size_width,wmenu,wtext,menuoverlay,firstcom
    if not settingskeystore[0]:
        if not firstcom:
            w=640
            h=480
#		w=int(640*upscale)
#		h=int(480*upscale)
            w=w
            h=h
        else:
            w=screen.get_width()
            h=screen.get_height()

    downscale=1
    flags=pygame.DOUBLEBUF|pygame.RESIZABLE|pygame.HWSURFACE
    bit=24
    if settingskeystore[0]:
        if not firstcom:
            screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN|flags,bit)
    else:
        if not firstcom:
            screen=pygame.display.set_mode((w,h),flags,bit)
    if not firstcom:
        firstcom=True
    ins=1
    if w>=screen.get_width():
        if not w-1<=320:
            w-=ins
    else:
        w+=1
    if h>=screen.get_height():
        if not h-1<=240:
            h-=ins
    else:
        h+=1
    button_size_width=w//2
    mmenu=pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)-(button_size_height+40), button_size_width, button_size_height),pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)+(button_size_height-80), (button_size_width//2)-5, button_size_height),pygame.Rect(((w - button_size_width) // 2)+(button_size_width//2)+5, ((h - button_size_height) // 2)+(button_size_height-80), (button_size_width//2)-5, button_size_height),pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)-(button_size_height-80), button_size_width, button_size_height),pygame.Rect(-10,h-50, 200,50)
    wmenu=pygame.Rect((w - (button_size_width) -4)//2, (h-button_size_height)-4, button_size_width//4, button_size_height),pygame.Rect((w - (button_size_width)+((button_size_width//2))+4)//2, (h-button_size_height)-4, button_size_width//4, button_size_height),pygame.Rect((w - (button_size_width)+((button_size_width//2)*2)+12)//2, (h-button_size_height)-4, button_size_width//4, button_size_height),pygame.Rect((w - (button_size_width)+((button_size_width//2)*3)+20)//2, (h-button_size_height)-4, button_size_width//4, button_size_height)
    if w<768:
        wtext=langpack[31],langpack[32],langpack[33],langpack[30]
    else:
        wtext=langpack[31]+' '+langpack[34],langpack[32]+' '+langpack[34],langpack[33]+' '+langpack[34],langpack[30]
button_size_height=50
button_selected=(170,170,170)
button_idle=(150,150,150)
mtext=langpack[27],langpack[28],langpack[29],langpack[30],langpack[36]
todo=[('Progress of Menu (Except Game)','80%'),('Progress of Game Interface','1%'),('Transitioning to New Renderer','20%'),('Progress of Game Multiplayer','Next Up')]
fullscreenchk()
pygame.display.set_caption(gamename+' '+str(gamever))
pygame.mouse.set_visible(True)
screen.set_alpha(None)
#w=640
#h=480
button=1
crazyness=0
menubutton=0
sprint=False
ingame=False
selection=0
movement=0
aiblock=2
aitimestep=1
hitbox=[]
splashsize=20
hideblocks=False
intense=5*9
titlepos=20, 30
textbox_text=''
textbox_active=True
update=False
def createworld():
    global activity, button,textbox_active,textbox_text,savename,worldtype
    render('header')
    render('text',text=langpack[31]+' '+langpack[34],arg=(titlepos,forepallete))
    floorbuttons=menu_draw((pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)+(button_size_height+100), button_size_width//2-5, button_size_height),pygame.Rect((w - button_size_width) // 2+(button_size_width//2+5), ((h - button_size_height) // 2)+(button_size_height+100), button_size_width//2-5, button_size_height),pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)+(button_size_height+40), button_size_width, button_size_height),),text=(langpack[31],langpack[40],langpack[37]+' '+(langpack[38] if worldtype==0 else langpack[39])))
    render('rect',arg=(((w - button_size_width) // 2, ((h - button_size_height) // 2) + (button_size_height - 60),button_size_width, 60),(0,0,0),True),bordercolor=forepallete)
    maxtext=32
    if len(textbox_text)<maxtext:
        colortext=255,255,255
    else:
        colortext=255,0,0
    render('text',arg=(((w - button_size_width) // 2+10,((h - button_size_height) // 2) + (button_size_height//4)),colortext),text=textbox_text)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopnow()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                activity = 1
            if textbox_active:
                if event.key == pygame.K_BACKSPACE:
                    # Remove the last character when Backspace is pressed
                    textbox_text = textbox_text[:-1]
                else:
                    # Append the entered character to the textbox text
                    if not len(textbox_text)>maxtext-1:
                        textbox_text += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if floorbuttons == 1:
                savename=textbox_text.replace(' ','_')+'.tw'
                reload()
                activity=2
                axe = time.time()
                aitime = time.time()+aitimestep
                
            elif floorbuttons == 2:
                activity=6
            elif floorbuttons == 3:
                if worldtype>=1:
                    worldtype=0
                else:
                    worldtype+=1
def deleteworld():
    global activity, button,selected_save
    tmp = font.render(langpack[32]+' '+str(savestext[selected_save-1])+'?', True, (255, 255, 255))
    centertext = tmp.get_rect(center=pygame.Rect(0,((h - button_size_height) // 2)+(button_size_height-20),w,20).center)
    screen.blit(tmp, centertext)
    floorbuttons=menu_draw((pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)+(button_size_height+20), button_size_width, button_size_height),pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)+(button_size_height+100), button_size_width, button_size_height),),text=('Delete!','Nwooo'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopnow()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if floorbuttons == 1:
                os.remove(gamepath+str(savestext[selected_save-1].replace(' ','_')+'.tw'))
                activity=6
                gamesaves()
            elif floorbuttons == 2:
                activity=6
def menu_draw(instruction,text=None,istextbox=False,selected_button=0):
    button=0
    if istextbox:
        button_selected=0,0,0
        button_idle=0,0,0
        highlight=100,255,100
        highlight_idle=255,255,255
    else:
        button_selected=150,150,150
        button_idle=120,120,120
        highlight=200,200,200
        highlight_idle=100,100,100
    for a in range(1, len(instruction)+1):	
        if instruction[a-1].collidepoint(pygame.mouse.get_pos()):
            select=True
            buttcolour = button_selected
            if pygame.mouse.get_focused():
                button=a
        else:
            buttcolour = button_idle
            select=False
        if selected_button==a:
            render('rect',arg=((instruction[a-1]),buttcolour,True),bordercolor=(0,255,0))
        elif select:
            render('rect',arg=((instruction[a-1]),buttcolour,True),bordercolor=highlight)
        else:
            render('rect',arg=((instruction[a-1]),buttcolour,True),bordercolor=highlight_idle)
        if not text==None:
            tmp = font.render(text[a-1], True, (255, 255, 255))
            centertext = tmp.get_rect(center=instruction[a-1].center)
            screen.blit(tmp, centertext)
    return button
def worldmenu():
    global activity,button,axe,aitime,selected_save,savename
    gamesaves()
    #(w//4)-55,35,200,40
    render('header')
    render('text',text=gamename + ' '+langpack[18],arg=(titlepos,forepallete))
    render('rect',arg=(((w//4)-20,60,w-(w//2)+40,h-120),(10,10,10),True),bordercolor=forepallete)
    savebutton=menu_draw(savespos,text=savestext,selected_button=selected_save)
    worldbutton=menu_draw(wmenu,text=wtext)
    if worldbutton==1:
        if len(saves)>3:
            if w>767:
                render('text',text=langpack[15],arg=((25,h-85),(255,255,0)))
            else:
                render('text',text=langpack[16],arg=((25,h-85),(255,255,0)))
    elif worldbutton==2 or worldbutton==3:
        if selected_save==0:
            render('text',text=langpack[17],arg=((25,h-85),(255,255,0)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopnow()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if savebutton==0:
                if worldbutton == 1:
        #		reload()
        #		axe = time.time()
        #		aitime = time.time()+aitimestep
                    if len(saves)<4:
                        activity = 7
                elif worldbutton == 2:
                    if selected_save!=0:
                        activity = 8
                elif worldbutton == 3:
                    if selected_save!=0:
                        savename=savestext[selected_save-1].replace(' ','_')+'.tw'
                        reload()
                        activity=2
                        axe = time.time()
                        aitime = time.time()+aitimestep
                elif worldbutton == 4:
                    activity=1
                    selected_save=0
            else:
                selected_save=savebutton
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                activity=1
                button=0
def regen():
    global blockmainmenu,blocklen
    if not hideblocks:
        blockmainmenu=[]
        tmp=0
        x=True
        max=99999999
        madew=0
        madeh=0
#		maxh=(h//splashsize)+1
#		maxw=(w//splashsize)+1
        maxw=h//intense
        maxh=w//intense
        for b in range(1,maxh):
            madeh+=1
            if madeh>=max:
                break
            for a in range(1,maxw):
                madew+=1
                if madew>=max:
                    break
                if random.randint(1,2)==2:
                    #(a-1)*splashsize,(b-1)*splashsize
                    blockmainmenu.append((-100,-100,tmp))
                    tmp+=1
        blocklen=len(blockmainmenu)
#10/random.randint(1,100)
regen()
blocksplashid=0
border = 6
speed = 1
maxspeed = 3
def blocksplash():
    global blockmainmenu, blocksplashid,speed
    
    if not hideblocks:
        block_rect = pygame.Rect(0, 0, splashsize + border, splashsize + border)
        speed = min(speed + 1, maxspeed)
        w_div_splashsize = w // splashsize - 1
        inverse_speed=(1 / speed)
        for i, a in enumerate(blockmainmenu):
            if a[1] <= -25:
                random_x = random.randint(1, w_div_splashsize * splashsize)
                blockmainmenu[i] = (random_x, h + random.randint(100, h), a[2])
            else:
                new_y = a[1] - inverse_speed
                blockmainmenu[i] = (a[0], new_y, a[2])

            block_rect.topleft = (a[0] - (border // 2), a[1] - (border // 2))
            pygame.draw.rect(screen, (30, 30, 30), block_rect)
            pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(a[0], a[1], splashsize, splashsize))
def mainmenu():
    global debugmode,activity,crazyness
    menubutton=menu_draw(mmenu,text=mtext)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopnow()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menubutton == 1:
                activity = 6
            elif menubutton == 2:
                activity = 3
            elif menubutton == 5:
                activity = 9
            elif menubutton == 3:
                activity = 4
            elif menubutton == 4:
                stopnow()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F5:
                if debugmode:
                    debugmode = False
                else:
                    debugmode = True
            if event.key == pygame.K_l:
                crazyness+=1
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                stopnow()
#			if event.key == pygame.K_DOWN:
#				if button > 3:
#					button = 1
#				else:
#					button += 1
#			if event.key == pygame.K_UP:
#				if button < 2:
#					button = 4
#				else:
#					button -= 1
#			if event.key == pygame.K_RETURN:
#				click()
#	for a in range(1,crazyness+2):
#		shake(gamename,(40+(a*5),60+(a*5)))
    render('text',text=gamename,arg=(titlepos,forepallete))
    render('text',text=gamever,arg=((titlepos[0],titlepos[1]+25),forepallete))
    render('rect',arg=((140,30,32,32),(99,53,15),False),borderradius=10)
    render('rect',arg=((140,30,32,12),(34,155,19),False),borderradius=10)
    if update:
        render('text',text=langpack[44],arg=((182,30),forepallete))
        render('text',text=langpack[45],arg=((182,50),forepallete))
#    if debugmode:
#        render('text',text='(Server Use) MIN:'+str(int(gameminserve)),arg=((titlepos[0],titlepos[1]+50),forepallete))
    #render('text',text='BUTTON:'+str(menubutton),arg=((titlepos[0],titlepos[1]+30),forepallete))
    if crazyness<4:
        if crazyness>0:
            render('text',text=langpack[0],arg=((10,h-40),forepallete))
    elif crazyness<10:
            render('text',text=langpack[1],arg=((10,h-40),forepallete))
    elif crazyness<41:
        render('text',text=langpack[2],arg=((10,h-40),forepallete))
    elif crazyness<51:
        render('text',text=langpack[3],arg=((10,h-40),forepallete))
#		shake(langpack[3],(10,h-40))
    elif crazyness<61:
        crash(langpack[4])
def onlinemode():
    global activity, button,textbox_active,textbox_text,savename,worldtype
    render('header')
    render('text',text=gamename+' - '+langpack[5],arg=(titlepos,forepallete))
    floorbuttons=menu_draw((pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)+(button_size_height+80), button_size_width//2-5, button_size_height),pygame.Rect((w - button_size_width) // 2+(button_size_width//2+5), ((h - button_size_height) // 2)+(button_size_height+80), button_size_width//2-5, button_size_height),),text=(langpack[43],langpack[40],))
    render('rect',arg=(((w - button_size_width) // 2, ((h - button_size_height) // 2) + (button_size_height - 60),button_size_width, 60),(0,0,0),True),bordercolor=forepallete)
    maxtext=32
    if len(textbox_text)<maxtext:
        colortext=255,255,255
    else:
        colortext=255,0,0
    render('text',arg=(((w - button_size_width) // 2+10,((h - button_size_height) // 2) + (button_size_height//4)),colortext),text=textbox_text)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopnow()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                activity = 1
            if textbox_active:
                if event.key == pygame.K_BACKSPACE:
                    # Remove the last character when Backspace is pressed
                    textbox_text = textbox_text[:-1]
                else:
                    # Append the entered character to the textbox text
                    if not len(textbox_text)>maxtext-1:
                        textbox_text += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if floorbuttons == 1:
                savename=textbox_text.replace(' ','_')+'.tw'
                reload()
                activity=2
                axe = time.time()
                aitime = time.time()+aitimestep
                
            elif floorbuttons == 2:
                activity=1
            elif floorbuttons == 3:
                if worldtype>=1:
                    worldtype=0
                else:
                    worldtype+=1

def progressmenu():
    global activity
    tmp=0
    render('text',text=gamename+' '+langpack[19],arg=(titlepos,forepallete))
    render('rect',arg=((40,80,w-80,h-160),forepallete,False))
    for a in todo:
        render('text',text=a[0]+' ('+str(a[1])+')',arg=((45,90+(30*(tmp))),(0,0,0)))
        tmp+=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopnow()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                activity = 1
            if event.key == pygame.K_ESCAPE:
                activity = 1
            if event.key == pygame.K_DOWN:
                if button > 2:
                    button = 1
                else:
                    button += 1
            if event.key == pygame.K_UP:
                if button < 2:
                    button = 3
                else:
                    button -= 1
def tutorial():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save()
            stopnow()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                activity = 2
    
    render('rect',arg=((20, 20, w-40, h-40),(50, 50, 50),False))
    for a in range(1,9):
        render('text',text=langpack[6+a],arg=((30, 40+(20*(a-1))),forepallete))
#tmp!!!!
msgx=0
messagetime=0
change=False
colorstep = 0
loaded=[]
ama=0
def msgchk():
    global msgx,messagetime,message
    if not 'messagetime' in globals():
        messagetime = time.time()+5
    #mv=2*(fps//10)
    mv=1
    if not time.time()>=messagetime and not msgx>199:
        msgx+=mv
    elif time.time()>=messagetime and not msgx<=0:
        msgx-=mv
    for a in range(1,2):
        render('rect',arg=((w+1-msgx,20+(5*(a-1)), 220, 50),(100,100,100),True),bordercolor=(50,50,50),borderradius=10)
        if msgx>20:
            render('text',text=message[:50],arg=((w-msgx+20, 40+(5*(a-1))),forepallete))
def main():
    global activity,ingame,screen,settingskeystore,button,buttons,BUTTON_COLOR,SELECTED_BUTTON_BORDER_COLOR,SELECTED_BUTTON_BORDER_WIDTH,BUTTON_TEXT_OFFSET,BUTTON_TEXT_SIZE,BUTTON_TEXT_COLOR,debugmode,messagetime,aitime
    update=time.time()
    fps=int(clock.get_fps())-2
    allowed=[1,3,6,9,4,7,8]
    fullscreenchk()
    if activity==2:
        ingame=True
    else:
        ingame=False
    if activity in allowed:
        clear((20,20,20))
#			blocksplash()
    if gmode:
        render('rect',arg=((0,h-20,w,20),(255,255,0),False))
        render('rect',arg=((0,h-15,w,10),(255,0,0),False))
    if activity == 0:
        activity = 1
    elif activity == 1:
        mainmenu()
    elif activity == 2:
        game()
    elif activity == 3:
        settingspage()
    elif activity == 4:
        onlinemode()
    elif activity == 5:
        tutorial()
    elif activity == 6:
        worldmenu()
    elif activity == 7:
        createworld()
    elif activity == 8:
        deleteworld()
    elif activity == 9:
        progressmenu()
    msgchk()
    if debugmode:
        render('text',text='FPS:'+str(fps),arg=((w-100, 23),forepallete))
        render('text',text=str((time.time()-update)/0.001)[:4]+'ms',arg=((w-100, 43),forepallete))
#			render('text',text=str(cbytes(memspace()))+' Out of '+cbytes(maxmem),arg=((25, h-70),forepallete))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, 0, w, 10))
        struct = ((fps)/limitfps)*w
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(0, 0, struct, 10))
    if "-debug" in sys.argv:
        tmp=[pygame.Rect(w-130,30+(40),100,30),pygame.Rect(w-130,30+(40*2),100,30),pygame.Rect(w-130,30+(40*3),100,30),pygame.Rect(w-130,30+(40*4),100,30),pygame.Rect(w-130,30+(40*5),100,30),pygame.Rect(w-130,30+(40*6),100,30),pygame.Rect(w-130,30+(40*7),100,30),pygame.Rect(w-130,30+(40*8),100,30),pygame.Rect(w-130,30+(40*9),100,30),]
        button=menu_draw((tmp),text=('Home','Gameplay','Settings','Online','Tutorial','Worlds','CreateM','DeleteM','Progress'),selected_button=activity)
        if button!=0:
            activity=button
    pygame.display.update()
    clock.tick(limitfps)
def repaint():
    while True:
        pygame.display.flip()
#		print('x')
#		time.sleep(1/60)

def draw_rounded_rect(surface,rect,color,radius):pygame.draw.rect(surface,color,rect)
def draw_buttons():
    global hitbox
    hitbox=[]
    for(i,(text,pos)) in enumerate(buttons,start=1):
        button_rect=pygame.Rect(pos[0],pos[1],w-40,40)
        draw_rounded_rect(screen,button_rect,BUTTON_COLOR,5)
        if button==i:
            pygame.draw.rect(screen,SELECTED_BUTTON_BORDER_COLOR,button_rect,SELECTED_BUTTON_BORDER_WIDTH)
        render('text',text=text,arg=((pos[0]+BUTTON_TEXT_OFFSET[0],pos[1]+BUTTON_TEXT_OFFSET[1]),BUTTON_TEXT_COLOR))
def numlimit(cur,min):
    if cur>min:return cur
    else:return min
def clear(color):screen.fill(color)
def crash(text):
#	pygame.draw.rect(screen,red,pygame.Rect(0,h//2-20,w,35))
    #
    bypass=0
    while not bypass:
        fullscreenchk()
        buttonm=(pygame.Rect(w//4+10,h//4+h//2-40,w//4-20,30),pygame.Rect(w//4+w//2-w//4-5,h//4+h//2-40,w//4-5,30),)
        buttont=('Continue','Exit',)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stopnow()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button==1:
                    bypass=1
                elif button==2:
                    stopnow()
        render('rect',arg=((w//4,h//4,w//2,h//2),(40,40,40),False),borderradius=20)
        render('rect',arg=((w//4+3,h//4+33,w//2-6,h//2-36),(20,20,20),False),borderradius=20)
        button=menu_draw(buttonm,text=buttont)
        render('text',text=langpack[20],arg=((w//4+8,h//4+8),forepallete))
        render('text',text=text[:int(60*upscale)],arg=((w//4+15,h//4+48),forepallete))
        pygame.display.update()
def keychk():
    for a in pygame.event.get():
        if a.type==pygame.KEYDOWN or a.type==pygame.KEYUP:
            key=a.key
        else:
            key=None
        return a,a.type,key
    return None,None,None

def testmode():
    for a in range(1,10):
        clear((255,0,0))
        if a==1:
            mainmenu()
        elif a==2:
            game()
        elif a==3:
            settingspage()
        elif a==4:
            onlinemode()
        elif a==5:
            tutorial()
        elif a==6:
            worldmenu()
        elif a==7:
            createworld()
        elif a==8:
            deleteworld()
        elif a==9:
            progressmenu()
        render('text',text='Testing '+str(a)+' [!!Automated!!]',arg=((10,10),forepallete))
        pygame.display.flip()
        time.sleep(1)
    print('All Good!')
    stopnow()
def netcall(str):
    global netresult,netqueue
    netqueue=str
    if not netresult!='':
        netresult=''
    return netresult
def netthread():
    global netqueue,netresult
    print('Started NetThread')
    while True:
        try:
            if stop:
                break
            if len(netqueue)>0:
                print(netqueue)
                #netresult=urllib.request.urlopen(netqueue).read()
                netqueue=''
        except Exception as error:
            print(time.time(),': [NetThread]',error)
            netqueue=''
        time.sleep(1/60)
chat_messages = []
chat_box_width, chat_box_height = 600, 200
chat_box_x = (w - chat_box_width) // 2
chat_box_y = h - chat_box_height - 10
chat_box_rect = pygame.Rect(chat_box_x, chat_box_y, chat_box_width, chat_box_height)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
if __name__ == "__main__":
#	threading.Thread(target=repaint).start()
    try:
        for a in os.listdir('mods/'):
            exec(open('mods/'+str(a)).read())
        threading.Thread(target=netthread).start()
        #threading.Thread(target=load_chunks).start()
        while True:
            try:
                if "-testmode" in sys.argv:
                    testmode()
                else:
                    main()
            except Exception as error:
                crash(str(error))

    except Exception as error:
        crash(str(error))

