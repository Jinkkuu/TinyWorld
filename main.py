#!/usr/bin/python3
import random
import pygame,os,time,sys,threading,urllib.request
nline='\n'
axe=0
gamename='TinyWorld'
gamever='2.5.0904.0.dev'
gameupdateurl='N/A'
gameauthor='Pxki Games'
print('Starting Game...')
upscale=1
limitfps=1000
maxmem=1024*1024
sfps=0
debugmode=True
if upscale<.9:
	print('Can not go down <=0.8')
	exit()
upscale=int(round(upscale))
introtiming=1/160
musictime=0
x=0
y=0
aix=0
aiy=0
health=100
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
datapath='./data/'
if not os.path.isdir(datapath):
    os.mkdir(datapath)
    print('Created',datapath.replace('./','').replace('/',''))
settingskeystore=[False,False,False]
if os.path.isfile(datapath+'settings.db'):
    if not len(open(datapath+'settings.db').read().rstrip("\n").split("\n"))<3:
        settingskeystore=open(datapath+'settings.db').read().rstrip("\n").split("\n")
        for a in range(len(settingskeystore)):
            settingskeystore[a]=eval(settingskeystore[a])
            	
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
		if(posx,posy,b)in chunks:remove=True;break
		else:remove=False
	if remove:chunks.remove((posx,posy,b))
def placeblock(posx,posy,block):
	for b in blockcolor:
		if not(posx,posy,b)in chunks:
			place=True
		else:
			place=False
			break
	if place:
		chunks.append((posx,posy,block))
#def memspace():
#  if len(str(globals())) >= maxmem:
#    print('Memory Overload !\nThis will be sent to the Developer! :)')
#    stopnow()
#  else:
#    return len(str(globals()))
def cbytes(size):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0

    while size >= 1000 and unit_index < len(units) - 1:
        size /= 1000
        unit_index += 1

    converted_size = f"{size:.2f} {units[unit_index]}"
    return converted_size
def game():
			global playersize,tmpsize,health,sight,sprint,up,down,left,right,minemode,placemode,playerpos,renderdistancex,renderdistancey,blockid,debugmode,x,y,chunks,aix,aiy,aiblock,collide,activity,chat_box_visible,walking,aitime,axe,aitrigger,aipot,crontime
			if not "crontime" in globals():
				crontime=time.time()
			if time.time()-crontime>1:
				pass
			if fps != 0:
				walking = 3 /(fps//10)
			else:
				walking = 3
			crouching=(walking/2)
			sprinting=walking*2
			if not'worldtime'in globals():
				worldtime=0
				wt=int(time.time())
			if int(time.time())>wt:
				wt=int(time.time())
				worldtime+=1
			if worldtime>=maxworldtime:
				worldtime=0
			renderdistancex=(w//(playersize*2))+2
			renderdistancey=(h//(playersize*2))+2
			if tmpsize!=playersize:
				if tmpsize>playersize:x-=zoom;y-=zoom;playersize+=zoom
				elif tmpsize<playersize:x+=zoom;y+=zoom;playersize-=zoom
			playerpos=playercheck()
			if settingskeystore[1]:ais=[(aix,aiy)]
			else:ais=[]
			for a in ais:aipot=playersize*a[0]+playersize*x,playersize*a[1]+playersize*y
			if health>79:healthstatus=0,255,0
			elif health>30:healthstatus=255,255,0
			elif health<20:healthstatus=255,0,0
			if health<1:message='You have died';activity=1
			if settingskeystore[2]:
				if len(chunks)>2999:chunks=chunks[5:]
			if settingskeystore[1]:
				if time.time()>aitime:
					aiblock=2;aitime=time.time()+aitimestep;aiy+=1
					if aitrigger>3:aitrigger=1
					else:aitrigger+=1
				elif time.time()>axe:
					placeblock(aix,aiy,blockcolor[aiblock])
					if aitrigger==1:aix+=1
					elif aitrigger==2:aiy+=1
					elif aitrigger==3:aix-=1
					elif aitrigger==4:aiy-=1
					axe=time.time()
			if sprint==1:movement=sprinting
			elif sprint==2:movement=crouching
			else:movement=walking
			if up:
				y+=movement
			if down:
				y-=movement
			if left:
				x+=movement
			if right:
				x-=movement
			if minemode:
				mineblock(playerpos[0],playerpos[1])
			if placemode:
				placeblock(playerpos[0],playerpos[1],blockcolor[blockid])
			result =load_chunks()
			screen.blit(buffer, (0, 0))
			ama,loaded,colorstep = result
			pygame.draw.rect(screen,(255,0,0),pygame.Rect(playersize*(w//playersize//2-1),playersize*(h//playersize//2-1),playersize,playersize));pygame.draw.rect(screen,blockcolor[blockid],pygame.Rect(w//2-30,h-60,40,40));pygame.draw.rect(screen,forepallete,pygame.Rect(w//2-30,h-60,40,40),2)
			loaded_count = ama
			if istd:
				controllerbutton=menu_draw((pygame.Rect(120,h-160,40,40),pygame.Rect(120,h-80,40,40),pygame.Rect(80,h-120,40,40),pygame.Rect(160,h-120,40,40),pygame.Rect(w-140,h-120,40,40),pygame.Rect(w-100,h-160,40,40),pygame.Rect(w-180,h-160,40,40),),('^','v','<','>','<o>','M','P',))
			else:
				controllerbutton=0
			for event in pygame.event.get():
				if event.type==pygame.QUIT:save();pygame.quit();sys.stopnow()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if controllerbutton==1:
						up=1	
					if controllerbutton==2:
						down=1	
					if controllerbutton==3:
						left=1	
					if controllerbutton==4:
						right=1	
					if controllerbutton==5:
						sight=(True if not sight else False)
					if controllerbutton==6:
						place=(True if not place else False)
				if event.type == pygame.MOUSEBUTTONUP:
					up=0
					down=0
					left=0
					right=0
				if event.type==pygame.KEYUP:
					if event.key==pygame.K_LSHIFT:sprint=0
					if event.key==pygame.K_z:sprint=0
					if event.key==pygame.K_LCTRL:placemode=False
					if event.key==pygame.K_LALT:minemode=False
					if event.key==pygame.K_a:
						if health-10>-1:health-=10
					if event.key==pygame.K_UP:up=False
					if event.key==pygame.K_DOWN:down=False
					if event.key==pygame.K_LEFT:left=False
					if event.key==pygame.K_RIGHT:right=False
				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_t:
						chat_box_visible = not chat_box_visible
						if chat_box_visible:
							pygame.event.set_grab(True)
							pygame.mouse.set_visible(True)
						else:
							pygame.event.set_grab(False)
							pygame.mouse.set_visible(False)
					if event.key==pygame.K_F4:
						messagetime=time.time()+5
						if collide:
							message='Disabled Exact Value'
							collide=False
						else:
							collide=True
							message='Enabled Exact Value'
					if event.key==pygame.K_F5:
						if debugmode:
							debugmode=False
						else:
							debugmode=True
					if event.key==pygame.K_LSHIFT:
						sprint=1
					if event.key==pygame.K_UP:
						if not y+movement>radius//1.5:
							up=True
					if event.key==pygame.K_DOWN:
						if not y-movement<-radius//1.5:
							down=True
					if event.key==pygame.K_LEFT:
						if not x+movement>radius//1.5:
							left=True
					if event.key==pygame.K_RIGHT:
						if not x-movement<-radius//1.5:
							right=True
					if event.key==pygame.K_q:
						save()
						activity=1
						chunks=[]
					if event.key==pygame.K_s:
						if sight:
							sight=False
						else:
							sight=True
					if event.key==pygame.K_x:
						if blockid>=maxblock-1:
							blockid=0
						else:
							blockid+=1
					if event.key==pygame.K_MINUS:
						if tmpsize>5:tmpsize-=5
						else:tmpsize=20
					if event.key==pygame.K_LCTRL:
						placemode=True
					if event.key==pygame.K_LALT:
						minemode=True
					if event.key==pygame.K_z:
						sprint=2
					if event.key==pygame.K_r:
						save()
						chunks=[]
						x=0
						y=0
						aix=0
						aiy=0
						reload()
#			loaded,colorstep=loadchunks()
			if debugmode:
				dsize=10
				render('text',text='('+str(int(x))+','+str(int(y))+') '+str(len(chunks))+' Total Blocks ['+str(loaded_count)+' Loaded]',arg=((20, 23),forepallete))
				render('text',text='Block ID: '+str(blockid)+'/'+str(len(blockcolor)-1),arg=((20, 23*2),forepallete))
				render('text',text='Exact Value Mode: '+str(collide),arg=((20, 23*3),forepallete))
				render('text',text='Size: '+str(playersize)+'/'+str(tmpsize),arg=((20, 23*4),forepallete))
#			if gamemode==gamemodes[1]:write('Health Bar:'+str(health)+'%',(30,h-90),20,forepallete);pygame.draw.rect(screen,(150,150,150),pygame.Rect(30,h-72,100,2));pygame.draw.rect(screen,healthstatus,pygame.Rect(30,h-72,10*(health//10),2))

			pygame.draw.rect(screen, forepallete, pygame.Rect((playersize * playerpos[0] + playersize * x),playersize * playerpos[1] + playersize * y,playersize,playersize),2)
			render('text',text='Note: This will be changed Later',arg=((30,h-40),forepallete))
if os.path.isfile(datapath+'game-dev.py'):
    print('Using External Game File')
    exec(open(datapath+'game-dev.py').read())
def settingspage():
  global button,settingskeystore,activity,screen,firstcom,change
  if change:
    tmp=open(datapath+'settings.db','w')
    for a in settingskeystore:
        tmp.write(str(a)+'\n')
    tmp.close()
    change=False
  #settingskeystore[2],settingskeystore[1],fullscreen
  render('header')
  render('rect',arg=((-5,titlepos[1]+40,w+10,h-120),(0,0,0),True),bordercolor=forepallete)
  render('text',text=gamename + ' - '+langpack[21],arg=(titlepos,forepallete))
  setbutton=menu_draw((pygame.Rect(titlepos[0], titlepos[1]+55, 220, button_size_height//1.5),pygame.Rect(titlepos[0], titlepos[1]+100, 220, button_size_height//1.5),pygame.Rect(titlepos[0], titlepos[1]+145, 220, button_size_height//1.5),pygame.Rect(titlepos[0], titlepos[1]+190, 220, button_size_height//1.5),pygame.Rect(10, h-45, w-20, button_size_height/1.5),),((langpack[23] if settingskeystore[2] else langpack[22])+' '+langpack[24],(langpack[23] if settingskeystore[1] else langpack[22])+' '+langpack[25],(langpack[23] if settingskeystore[0] else langpack[22]) + ' '+langpack[26],'Notification Test','<--'))
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
          global messagetime,message
          messagetime = time.time() + 5
          message='EXAMPPLE MESSAGE'
        elif setbutton == 5:
          activity = 1

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q:
        activity=1
#  pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(20, h // 2 - 80, w - 40, 40))
#  pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(20, h // 2 - 20, w - 40, 40))
#  pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(20, h // 2 + 40, w - 40, 40))
#  pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(20, h // 2 + 100, w - 40, 40))
#  write('settingskeystore[2] Mode: ' + ('Enabled' if settingskeystore[2] else 'Disabled'), (25, h // 2 - 68), 25, (255, 255, 255))
#  write('Builder Bots: ' + ('Enabled' if settingskeystore[1] else 'Disabled'), (25, h // 2 - 8), 25, (255, 255, 255))
#  write('Fullscreen: ' + ('Enabled' if fullscreen else 'Disabled'), (25, h // 2 + 52), 25, (255, 255, 255))
#  write('Exit Menu', (25, h // 2 + 110), 25, (255, 255, 255))
#  pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(20, h // 2 - 80 + 60 * (button - 1), w - 40, 40), 2)
def notify(text):
	pygame.display.flip();pygame.display.flip()
	for a in range(1,35+1):
		pygame.draw.rect(screen,(0,0,0),pygame.Rect(0,h//2-20,w,a-1))
		pygame.display.flip()
		render('text',text=text[:int(60*upscale)],arg=((20,h//2-10),forepallete))
		pygame.display.flip()
		time.sleep(3)
fpstime=time.time()
fpstmp=0
fps=0
quickness=1
def limiter():
	global fpstime,fpstmp,sfps,fps
	if time.time()-fpstime>1/quickness:
		fps=int(fpstmp)
		fpstmp=0
		fpstime=time.time()
	else:
		fpstmp+=1*quickness
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
x=0
y=0
helperx=0
helpery=0
aix=-1
aiy=-1
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
blockcolor=[(100,0,0),(0,0,100),(100,100,100),(200,0,0),(0,0,100),(0,100,200)]
foodcolor=0,255,0
collide=True
gamemodes=['God','Mortal']
blockid=0
maxblock=len(blockcolor)
x=0
y=0
select=False
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
    messagetime = time.time() + 5
    message = 'Saved World'
sight=False
def respawn():
	for a in range(1,1000):place=False;pos=random.randint(1,x+100)//2,random.randint(1,y+100)//2;foodpos.append((pos[0],pos[1],random.randint(1,2)))
def reload():
	global aix,aiy,aipos,foodcount,health,worldtype,seed,x,y,radius,playersize,foodpos,gamemode,aitrigger,collide,aitime,aipot,wmenu,chunks
	x=0;y=0;aix=0;aiy=0;health=100;gamemode=gamemodes[0]
	if os.path.isfile(gamepath+savename):
		clear((0, 0, 0))
		render('text',text='Preparing World...',arg=((20, h // 2),forepallete))
		pygame.display.flip()
		f = open(gamepath+savename, 'r').read().replace(nline, '').replace('+', ', ')
		aipos = list(eval(f))
		tmp = aipos[1:]
		pos = aipos[0]
		x = pos[0]
		y = pos[1]
		health = pos[2]
		radius = pos[3]
		aix = pos[4]
		aiy = pos[5]
		aitrigger = pos[6]
		collide = pos[7]
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
remove=False
place=False
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
placemode=False
minemode=False
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
	global w,h,screenw,screenh,screen,mmenu,button_size_width,wmenu,wtext,buffer,menuoverlay,firstcom
	if not settingskeystore[0]:
		if not firstcom:
			w=640
			h=480
#		w=int(640*upscale)
#		h=int(480*upscale)
			screenw=w
			screenh=h
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
			screen=pygame.display.set_mode((screenw,screenh),flags,bit)
	if not firstcom:
		firstcom=True
	w=screen.get_width()
	h=screen.get_height()
	if w<320:
		w=320
	if h<240:
		h=240
	
	screenw=w
	screenh=h
	button_size_width=w//2
	buffer = pygame.Surface((screenw, screenh))
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
todo=[('Progress of Menu (Except Game)','60%'),('Progress of Game Interface','0%')]
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
selection=0
movement=0
aiblock=2
aitimestep=1
hitbox=[]
splashsize=20
hideblocks=False
intense=5*9
titlepos=20, 30
#def shake(word,pos):
#	wording=word
#	write(wording, (pos[0]-random.randint(1,10), pos[1]-random.randint(1,10)), 60, (255, 0, 0))
#	write(wording, (pos[0]-random.randint(1,10), pos[1]-random.randint(1,10)), 60, (0, 255, 0))
#	write(wording, (pos[0]-random.randint(1,10), pos[1]-random.randint(1,10)), 60, (255, 255, 255))
#	write(wording, (pos[0]+random.randint(1,10), pos[1]+random.randint(1,10)), 60, (0, 0, 255))
#def debugmenu():
#	pygame.draw.rect(screen, (), rect)
textbox_text=''
textbox_active=True
def createworld():
	global activity, button,textbox_active,textbox_text,savename,worldtype
	render('header')
	render('text',text=langpack[31]+' '+langpack[34],arg=(titlepos,forepallete))
	floorbuttons=menu_draw((pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)+(button_size_height+100), button_size_width//2-5, button_size_height),pygame.Rect((w - button_size_width) // 2+(button_size_width//2+5), ((h - button_size_height) // 2)+(button_size_height+100), button_size_width//2-5, button_size_height),pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)+(button_size_height+40), button_size_width, button_size_height),),text=(langpack[31],langpack[40],langpack[37]+' '+(langpack[38] if worldtype==0 else langpack[39])))
	textbox_rect = pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2) + (button_size_height - 60),button_size_width, 60)
	pygame.draw.rect(screen,(0,0,0),pygame.Rect(textbox_rect))
	pygame.draw.rect(screen,forepallete,textbox_rect,2)
	maxtext=32
	if len(textbox_text)<maxtext:
		colortext=255,255,255
	else:
		colortext=255,0,0
	textofme=textbox_text
	textbox_surface = font.render(textofme, True, colortext)
	textbox_pos = textbox_rect.move(10, 50//2)
	screen.blit(textbox_surface, textbox_pos)
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

		pygame.draw.rect(screen, (buttcolour), instruction[a-1])
		if selected_button==a:
			pygame.draw.rect(screen, (0,255,0), instruction[a-1],2)
		elif select:
			pygame.draw.rect(screen, (highlight), instruction[a-1],2)
		else:
			pygame.draw.rect(screen, (highlight_idle), instruction[a-1],2)	
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
	pygame.draw.rect(screen, (10,10,10), pygame.Rect((w//4)-20,60,w-(w//2)+40,h-120))
	pygame.draw.rect(screen, forepallete, pygame.Rect((w//4)-20,60,w-(w//2)+40,h-120),2)
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
			#shake('Ha',(a[0],a[1]))
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
	global activity
	render('text',text=gamename+' '+langpack[5],arg=(titlepos,forepallete))
	pygame.draw.rect(screen, forepallete, pygame.Rect(40,80,w-80,h-160))
	render('text',text=netcall('localhost-\x20'),arg=((45,85),(0,0,0)))
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
			if event.key == pygame.K_RETURN:
				pass
def progressmenu():
	global activity
	tmp=0
	render('text',text=gamename+' '+langpack[19],arg=(titlepos,forepallete))
	pygame.draw.rect(screen, forepallete, pygame.Rect(40,80,w-80,h-160))
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
			pygame.quit()
			sys.stopnow()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				activity = 2
	pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(20, 20, w-40, h-40))
	for a in range(1,9):
		render('text',text=langpack[6+a],arg=((30, 40+(20*(a-1))),forepallete))
#tmp!!!!
msgx=0
messagetime=0
change=False
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
		pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(w-msgx,20+(5*(a-1)), 220, 50),border_radius=10)
		pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(w-msgx,20+(5*(a-1)), 420, 50),2,border_radius=10)
		if msgx>20:
			render('text',text=message[:50],arg=((w-msgx+20, 40+(5*(a-1))),forepallete))
def main():
	global activity,screen,settingskeystore,button,buttons,BUTTON_COLOR,SELECTED_BUTTON_BORDER_COLOR,SELECTED_BUTTON_BORDER_WIDTH,BUTTON_TEXT_OFFSET,BUTTON_TEXT_SIZE,BUTTON_TEXT_COLOR,debugmode,messagetime,aitime
	limiter()
	update=time.time()
	allowed=[1,3,6,9,4,7,8]
	fullscreenchk()
	if activity in allowed:
		clear((20,20,20))
#			blocksplash()
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
def playercheck():
    playerpos = -int(round(x)) + w // playersize // 2 - 1, -int(round(y)) + h // playersize // 2 - 1
    return playerpos
class Quadtree:
    def __init__(self, bounds):
        self.bounds = bounds
        self.chunks = []
        self.children = [None] * 4

    def insert(self, chunk):
        if not self._in_bounds(chunk):
            return

        if len(self.chunks) < 4:
            self.chunks.append(chunk)
        else:
            if self.children[0] is None:
                self._subdivide()
            for child in self.children:
                child.insert(chunk)

    def query_range(self, xmin, xmax, ymin, ymax):
        results = []
        if not self._intersects_range(xmin, xmax, ymin, ymax):
            return results

        for chunk in self.chunks:
            if xmin <= chunk[0] <= xmax and ymin <= chunk[1] <= ymax:
                results.append(chunk)

        if self.children[0] is not None:
            for child in self.children:
                results.extend(child.query_range(xmin, xmax, ymin, ymax))

        return results

    def _in_bounds(self, chunk):
        x, y = chunk
        xmin, ymin, xmax, ymax = self.bounds
        return xmin <= x <= xmax and ymin <= y <= ymax

    def _intersects_range(self, xmin, xmax, ymin, ymax):
        xmin_bound, ymin_bound, xmax_bound, ymax_bound = self.bounds
        return not (xmin > xmax_bound or xmax < xmin_bound or ymin > ymax_bound or ymax < ymin_bound)

    def _subdivide(self):
        xmin, ymin, xmax, ymax = self.bounds
        xmid = (xmin + xmax) // 2
        ymid = (ymin + ymax) // 2

        self.children[0] = Quadtree((xmin, ymin, xmid, ymid))
        self.children[1] = Quadtree((xmid, ymin, xmax, ymid))
        self.children[2] = Quadtree((xmin, ymid, xmid, ymax))
        self.children[3] = Quadtree((xmid, ymid, xmax, ymax))

def load_chunks():
	colorstep = 0
	ama=0
    # Create a list of visible chunks using a generator expression
	xmin = playerpos[0] - renderdistancex
	xmax = playerpos[0] + renderdistancex
	ymin = playerpos[1] - renderdistancey
	ymax = playerpos[1] + renderdistancey
	loaded = (tmp for tmp in chunks if xmin <= tmp[0] <= xmax and ymin <= tmp[1] <= ymax)
	# This is for Temporary Chunks (Not loaded to "Real" Chunks)
	if sight:
		buffer.fill((0,100,0))
	else:
		buffer.fill((0,150,0))
	# Iterate over visible chunks and draw them
	playerpos2=playercheck()
	if 0==1:
		for a in range(1,(w//int(playersize))+1):
			for b in range(1,(h//int(playersize))+1):
				random.seed(playerpos2[0]*playerpos2[1]*a*b)
				tmp=random.random()
				if tmp>=0.5:
					pygame.draw.rect(buffer, (blockcolor[5]), pygame.Rect((a-1)*playersize, (b-1)*playersize, playersize, playersize))			

	for b in loaded:	
		ama+=1
		
		chunk_x = playersize * b[0] + playersize * x
		chunk_y = playersize * b[1] + playersize * y
		rect = pygame.Rect(chunk_x, chunk_y, playersize + 1, playersize + 1)
		if sight == False:
			pygame.draw.rect(buffer, b[2], rect)
		else:
			color = (255, 255, 0) if len(b) > 3 else (255, 255, 255)
			pygame.draw.rect(buffer, color, rect, 1)
		if settingskeystore[1]:
			aipot_rect = pygame.Rect(aipot[0], aipot[1], playersize, playersize)
			pygame.draw.rect(screen, (0, 0, 255), aipot_rect)
			pygame.draw.rect(screen, (255, 255, 255), aipot_rect, 2)
        # Yield control to the event loop to maintain smooth FPS
	#await asyncio.sleep(0)
	return ama,loaded, colorstep
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
		pygame.draw.rect(screen,(40,40,40),pygame.Rect(w//4,h//4,w//2,h//2),border_radius=5)
		pygame.draw.rect(screen,(20,20,20),pygame.Rect(w//4+3,h//4+33,w//2-6,h//2-36))
		button=menu_draw(buttonm,text=buttont)
		render('text',text=langpack[20],arg=((w//4+8,h//4+8),forepallete))
		render('text',text=text[:int(60*upscale)],arg=((w//4+15,h//4+48),forepallete))
		pygame.display.update()
def render(type,arg=(0,0) , text='N/A',bordercolor=forepallete):
#	print(type,arg,text)
	try:
		if type=='text':
			screen.blit(font.render(text, True, arg[1]), arg[0])
		elif type=='rect':
#			print(arg[0][0],arg[0][1],arg[0][2],arg[0][3])
			pygame.draw.rect(screen,arg[1],pygame.Rect(arg[0][0],arg[0][1],arg[0][2],arg[0][3]))
			if arg[2]:
				pygame.draw.rect(screen,bordercolor,pygame.Rect(arg[0][0],arg[0][1],arg[0][2],arg[0][3]),2)
		elif type=='header':
			pygame.draw.rect(screen, (50,50,50), pygame.Rect(0,-40,w,100),border_radius=20)
		else:
			crash('Render unsupported Type')
	except Exception as error:
		crash(error)
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
				netresult=urllib.request.urlopen(netqueue).read()
				netqueue=''
		except Exception as error:
			print(time.time(),': [NetThread]',error)
			netqueue=''
		time.sleep(1/60)
chat_messages = []
chat_box_width, chat_box_height = 600, 200
chat_box_x = (screenw - chat_box_width) // 2
chat_box_y = screenh - chat_box_height - 10
chat_box_rect = pygame.Rect(chat_box_x, chat_box_y, chat_box_width, chat_box_height)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
if __name__ == "__main__":
#	threading.Thread(target=repaint).start()
	try:
		for a in os.listdir('mods/'):
			exec(open('mods/'+str(a)).read())
		threading.Thread(target=netthread).start()
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

