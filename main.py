_J='Pxki Games'
_I='New World'
_H='True'
_G='savefile.tw'
_F='\n'
_E=','
_D='w'
_C='settings.dat'
_B=True
_A=False
from random import randint
from pygame.locals import*
import pygame,os,time,sys,asyncio,concurrent.futures
axe=0
gamename='TinyWorld'
gamever='2.1dev'
gameupdateurl='N/A'
print('Starting Game...')
upscale=1
limitfps=1000
sfps=0
debugmode=_B
if upscale<.9:print('Can not go down <=0.8');exit()
upscale=int(round(upscale))
introtiming=1/160
fullscreen=_A
musictime=0
def music():
	A='music.mp3';global musictime
	if os.path.isfile(A):
		if not'musictime'in globals():musictime=0
		if time.time()>musictime:musictime=time.time()+13;pygame.mixer.music.load(A);pygame.mixer.music.play()
pallete=0,0,0
forepallete=255,255,255
blue=0,0,255
green=0,255,0
red=255,0,0
voidcolor=0,0,0
modsloaded=0
texturepath='textures/'
if not os.path.isdir(texturepath):os.mkdir(texturepath)
if not os.path.isdir('mods'):os.mkdir('mods')
def mineblock(posx,posy):
	for b in blockcolor:
		if(posx,posy,b)in chunks:remove=_B;break
		else:remove=_A
	if remove:chunks.remove((posx,posy,b))
def placeblock(posx,posy,block):
	for b in blockcolor:
		if not(posx,posy,b)in chunks:place=_B
		else:place=_A;break
	if place:
		tmpchunks.append((posx,posy,block))
def keyboard(title):
	backgroundcolor1=100,100,100;backgroundcolor2=150,150,150;backgroundcolor3=100,100,100;backgroundcolor3focus=100,200,100;label='';x1=1;y1=2
	while _B:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:pygame.quit();sys.exit()
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_UP:
					if y1<2:y1=5
					else:y1-=1
				if event.key==pygame.K_DOWN:
					if y1>4:y1=1
					else:y1+=1
				if event.key==pygame.K_LEFT:
					if x1<2:x1=10
					else:x1-=1
				if event.key==pygame.K_RIGHT:
					if x1>9:x1=1
					else:x1+=1
				if event.key==pygame.K_RETURN:
					if not len(label)>=65:
						if y1==1:
							if x1==1:label+='0'
							elif x1==2:label+='1'
							elif x1==3:label+='2'
							elif x1==4:label+='3'
							elif x1==5:label+='4'
							elif x1==6:label+='5'
							elif x1==7:label+='6'
							elif x1==8:label+='7'
							elif x1==9:label+='8'
							elif x1==10:label+='9'
						elif y1==2:
							if x1==1:label+='q'
							elif x1==2:label+=_D
							elif x1==3:label+='e'
							elif x1==4:label+='r'
							elif x1==5:label+='t'
							elif x1==6:label+='y'
							elif x1==7:label+='u'
							elif x1==8:label+='i'
							elif x1==9:label+='o'
							elif x1==10:label+='p'
						elif y1==3:
							if x1==1:label+='a'
							elif x1==2:label+='s'
							elif x1==3:label+='d'
							elif x1==4:label+='f'
							elif x1==5:label+='g'
							elif x1==6:label+='h'
							elif x1==7:label+='j'
							elif x1==8:label+='k'
							elif x1==9:label+='l'
							elif x1==10:
								if len(label)>=1:label=label[:len(label)-1]
						elif y1==4:
							if x1==1:label+='z'
							elif x1==2:label+='x'
							elif x1==3:label+='c'
							elif x1==4:label+='v'
							elif x1==5:label+='b'
							elif x1==6:label+='n'
							elif x1==7:label+='m'
							elif x1==8:label+=_E
							elif x1==9:label+='.'
							elif x1==10:return label
						elif y1==5:
							if x1<=10:label+=' '
		pygame.draw.rect(screen,backgroundcolor2,pygame.Rect(w//2-400//2,h//2-200//2,400,230));pygame.draw.rect(screen,backgroundcolor3,pygame.Rect(w//2-400//2+10,h//2-200//2+30,380,20));write(label[:65],(w//2-400//2+14,h//2-200//2+35),15,forepallete);health=100
		if x1<100:
			if y1==5:pygame.draw.rect(screen,backgroundcolor3focus,pygame.Rect(w//2-400//2+10+40*(1-1),h//2-200//2+60+35*4,380,20))
			else:pygame.draw.rect(screen,backgroundcolor3,pygame.Rect(w//2-400//2+10+40*(1-1),h//2-200//2+60+35*4,380,20))
		else:pygame.draw.rect(screen,backgroundcolor3,pygame.Rect(w//2-400//2+10+40*(1-1),h//2-200//2+60+35*4,380,20))
		for b in range(1,2):
			for a in range(1,11):
				if x1==a:
					if y1==b:pygame.draw.rect(screen,backgroundcolor3focus,pygame.Rect(w//2-400//2+10+40*(a-1),h//2-200//2+60+35*(b-1),20,20))
					else:pygame.draw.rect(screen,backgroundcolor3,pygame.Rect(w//2-400//2+10+40*(a-1),h//2-200//2+60+35*(b-1),20,20))
				else:pygame.draw.rect(screen,backgroundcolor3,pygame.Rect(w//2-400//2+10+40*(a-1),h//2-200//2+60+35*(b-1),20,20))
				if b==1:
					if a==1:write('0',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==2:write('1',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==3:write('2',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==4:write('3',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==5:write('4',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==6:write('5',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==7:write('6',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==8:write('7',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==9:write('8',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==10:write('9',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
				elif b==3:
					if a==1:write('a',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==2:write('s',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==3:write('d',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==4:write('f',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==5:write('g',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==6:write('h',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==7:write('j',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==8:write('k',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==9:write('l',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==10:write('<-',(w//2-400//2+8+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
				elif b==2:
					if a==1:write('q',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==2:write(_D,(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==3:write('e',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==4:write('r',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==5:write('t',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==6:write('y',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==7:write('u',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==8:write('i',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==9:write('o',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==10:write('p',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
				elif b==4:
					if a==1:write('z',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==2:write('x',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==3:write('c',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==4:write('v',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==5:write('b',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==6:write('n',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==7:write('m',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==8:write(_E,(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==9:write('.',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==10:write('Go',(w//2-400//2+6+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
		write(title[:50]+' [Characters Left:'+str(65-len(label))+']',(w//2-190,h//2-90),20,forepallete);pygame.display.flip()
async def game():
			global playersize,tmpsize,health,sight,sprint,up,down,left,right,minemode,placemode,playerpos,renderdistancex,renderdistancey,blockid,debugmode,x,y,chunks,aix,aiy,aiblock,collide,activity,chat_box_visible,walking,aitime,axe,aitrigger,aipot,crontime,tmpchunks

			if not "crontime" in globals():
				crontime=time.time()
			if time.time()-crontime>1:
				if len(tmpchunks)==0:
					crontime=time.time()
				else:
				  chunks.extend(tmpchunks)
				  tmpchunks=[]
			if fps != 0:
				walking = (0.6 / fps) * 60
			elif fps < 20:
				walking = 0.6*fps
			crouching=(walking/2)
			sprinting=walking*2
			if not'worldtime'in globals():worldtime=0;wt=int(time.time())
			if int(time.time())>wt:wt=int(time.time());worldtime+=1
			if worldtime>=maxworldtime:worldtime=0
			renderdistancex=(w//(playersize*2))+2;renderdistancey=(h//(playersize*2))+2
			if tmpsize!=playersize:
				if tmpsize>playersize:x-=zoom;y-=zoom;playersize+=zoom
				elif tmpsize<playersize:x+=zoom;y+=zoom;playersize-=zoom
			playerpos=playercheck()
			if botmode:ais=[(aix,aiy)]
			else:ais=[]
			for a in ais:aipot=playersize*a[0]+playersize*x,playersize*a[1]+playersize*y
			if health>79:healthstatus=0,255,0
			elif health>30:healthstatus=255,255,0
			elif health<20:healthstatus=255,0,0
			if health<1:message='You have died';activity=1
			if optimize:
				if len(chunks)>2999:chunks=chunks[5:]
			if sight==_A:clear((0,150,0))
			else:clear((0,50,0))
			if botmode:
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
			if up:y+=movement
			if down:y-=movement
			if left:x+=movement
			if right:x-=movement
			if minemode:mineblock(playerpos[0],playerpos[1])
			if placemode:placeblock(playerpos[0],playerpos[1],blockcolor[blockid])
			for event in pygame.event.get():
				if event.type==pygame.QUIT:save();pygame.quit();sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:mouse_pos=pygame.mouse.get_pos()	
				if event.type==pygame.KEYUP:
					if event.key==pygame.K_LSHIFT:sprint=0
					if event.key==pygame.K_z:sprint=0
					if event.key==pygame.K_LCTRL:placemode=_A
					if event.key==pygame.K_LALT:minemode=_A
					if event.key==pygame.K_a:
						if health-10>-1:health-=10
					if event.key==pygame.K_UP:up=_A
					if event.key==pygame.K_DOWN:down=_A
					if event.key==pygame.K_LEFT:left=_A
					if event.key==pygame.K_RIGHT:right=_A
				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_t:
						chat_box_visible = not chat_box_visible
						if chat_box_visible:pygame.event.set_grab(True);pygame.mouse.set_visible(True)
						else:pygame.event.set_grab(False);pygame.mouse.set_visible(False)
					if event.key==pygame.K_F4:
						messagetime=time.time()+5
						if collide:message='Disabled Exact Value';collide=_A
						else:collide=_B;message='Enabled Exact Value'
					if event.key==pygame.K_F5:
						if debugmode:debugmode=_A
						else:debugmode=_B
					if event.key==pygame.K_LSHIFT:sprint=1
					if event.key==pygame.K_UP:
						if not y+movement>radius//1.5:up=_B
					if event.key==pygame.K_DOWN:
						if not y-movement<-radius//1.5:down=_B
					if event.key==pygame.K_LEFT:
						if not x+movement>radius//1.5:left=_B
					if event.key==pygame.K_RIGHT:
						if not x-movement<-radius//1.5:right=_B
					if event.key==pygame.K_q:save();activity=1;chunks=[]
					if event.key==pygame.K_s:
						if sight:sight=_A
						else:sight=_B
					if event.key==pygame.K_x:
						if blockid>=maxblock-1:blockid=0
						else:blockid+=1
					if event.key==pygame.K_MINUS:
						if tmpsize>5:tmpsize-=5
						else:tmpsize=20
					if event.key==pygame.K_LCTRL:placemode=_B
					if event.key==pygame.K_LALT:minemode=_B
					if event.key==pygame.K_z:sprint=2
					if event.key==pygame.K_r:save();foodcount=0;chunks=[];x=0;y=0;aix=0;aiy=0;reload()
#			loaded,colorstep=loadchunks()
			result = await load_chunks()
			loaded,colorstep = result
			pygame.draw.rect(screen,(255,0,0),pygame.Rect(playersize*(w//playersize//2-1),playersize*(h//playersize//2-1),playersize,playersize));pygame.draw.rect(screen,blockcolor[blockid],pygame.Rect(w//2-30,h-60,40,40));pygame.draw.rect(screen,(255,255,255),pygame.Rect(w//2-30,h-60,40,40),2)
			loaded_count = len(loaded)
			if debugmode:
				dsize=10
				write('('+str(int(x))+_E+str(int(y))+') '+str(len(chunks))+' Total Blocks ['+str(loaded_count)+' Loaded]', (20, 23), dsize, (255, 255, 255))
				write('Block ID: '+str(blockid)+'/'+str(len(blockcolor)-1), (20, 23*2), dsize, (255, 255, 255))
				write('Exact Value Mode: '+str(collide), (20, 23*3), dsize, (255, 255, 255))
				write('Size: '+str(playersize)+'/'+str(tmpsize), (20, 23*4), dsize, (255, 255, 255))
				write(str(walking),(20,23*5),20,(255,255,255))
			else:
				pygame.draw.circle(screen, (255,255,255), (20+50,20+50), 50)
				pygame.draw.circle(screen, (0,0,0), (20+50,20+50), 45)
			if gamemode==gamemodes[1]:write('Health Bar:'+str(health)+'%',(30,h-90),20,(255,255,255));pygame.draw.rect(screen,(150,150,150),pygame.Rect(30,h-72,100,2));pygame.draw.rect(screen,healthstatus,pygame.Rect(30,h-72,10*(health//10),2))

			pygame.draw.rect(screen, (255,255,255), pygame.Rect((playersize * playerpos[0] + playersize * x),playersize * playerpos[1] + playersize * y,playersize,playersize),2)
def settingspage():
  global button,optimize,botmode,fullscreen,activity,screen
  screen.fill((20,20,20))
  pygame.draw.rect(screen, (50,50,50), pygame.Rect(20,40,200,40),border_radius=20)
  write(gamename + ' - Settings', (40, 42), 60, (255, 255, 255))
  pygame.draw.rect(screen, (10,10,10), pygame.Rect(20,60,w-40,h-80))
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q:
        pygame.quit()
        sys.exit()
      if event.key == pygame.K_DOWN:
        button = (button % 4) + 1
      if event.key == pygame.K_UP:
        button = ((button-2) % 4)+1
      if event.key == pygame.K_RETURN:
        if button == 1:
          optimize = not optimize
        elif button == 2:
          botmode = not botmode
        elif button == 3:
          fullscreen = not fullscreen
          fullscreenchk()
          regen()
        elif button == 4:
          activity = 1
          button=2
  pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(20, h // 2 - 80, w - 40, 40))
  pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(20, h // 2 - 20, w - 40, 40))
  pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(20, h // 2 + 40, w - 40, 40))
  pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(20, h // 2 + 100, w - 40, 40))
  write('Optimize Mode: ' + ('Enabled' if optimize else 'Disabled'), (25, h // 2 - 68), 25, (255, 255, 255))
  write('Builder Bots: ' + ('Enabled' if botmode else 'Disabled'), (25, h // 2 - 8), 25, (255, 255, 255))
  write('Fullscreen: ' + ('Enabled' if fullscreen else 'Disabled'), (25, h // 2 + 52), 25, (255, 255, 255))
  write('Exit Menu', (25, h // 2 + 110), 25, (255, 255, 255))
  pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(20, h // 2 - 80 + 60 * (button - 1), w - 40, 40), 2)

def write(text, pos, size, color):
    screen.blit(font.render(text, True, color), pos)
def clear(color):screen.fill(color)
def crash(text):
	for b in range(1,h+1):pygame.draw.line(screen,(150,0,0),(0,b-1),(w,b-1))
	for a in range(1,35+1):pygame.draw.rect(screen,red,pygame.Rect(0,h//2-20,w,a-1))
	write(text[:int(60*upscale)],(20,h//2-10),20,forepallete);pygame.display.flip();time.sleep(3);exit()
def notify(text):
	pygame.display.flip();pygame.display.flip()
	for a in range(1,35+1):pygame.draw.rect(screen,(0,0,0),pygame.Rect(0,h//2-20,w,a-1));pygame.display.flip()
	write(text[:int(60*upscale)],(20,h//2-10),20,forepallete);pygame.display.flip();time.sleep(3)
fpstime=time.time()
fpstmp=0
fps=0
quickness=1
def pause(ms):
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
up=_A
down=_A
left=_A
right=_A
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
tmpchunks=[]
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
collide=_B
gamemodes=['God','Mortal']
blockid=0
maxblock=len(blockcolor)
x=0
y=0
def save():
    global messagetime, message
    f = open(_G, _D)
    f.write(
        '(' + str(int(round(x))) + _E +
        str(int(round(y))) + _E +
        str(health) + _E +
        str(radius) + _E +
        str(aix) + _E +
        str(aiy) + _E +
        str(aitrigger) + _E +
        str(collide) +
        '), ' +
        str(chunks).replace('[', '').replace(']', '')
    )
    f.close()
    messagetime = time.time() + 5
    message = 'Saved World'
foodpos=[]
sight=_A
def respawn():
	global foodpos;foodpos=[]
	for a in range(1,1000):place=_A;pos=randint(1,x+100)//2,randint(1,y+100)//2;foodpos.append((pos[0],pos[1],randint(1,2)))
def reload():
	global aix,aiy,aipos,foodcount,health,x,y,radius,playersize,foodpos,gamemode,aitrigger,collide,aitime,aipot
	try:
		x=0;y=0;aix=0;aiy=0;health=100;gamemode=gamemodes[0]
		if os.path.isfile(_G):
			clear((0, 0, 0))
			write('Preparing World...', (20, h // 2), 20, (255, 255, 255))
			pygame.display.flip()
			f = open(_G, 'r').read().replace(_F, '').replace('+', ', ')
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
			for c in tmp:
				if collide:chunks.append(c)
				else:chunks.append((int(round(c[0])),int(round(c[1])),c[2]))
		foodcount=0;t=time.time()+2;tok=0;xxx=time.time()+tok;fun=randint(1,len(messages))-1;fop=50
	except Exception as error:notify(str(error))
appear=_A
sight=_B
targetmode=_A
remove=_A
place=_A
aix=0
aiy=0
message=''
maxtime=5
aitrigger=1
up=_A
down=_A
left=_A
right=_A
placemode=_A
minemode=_A
optimize=_B
botmode=_A
worldtype=2
if not os.path.isfile('setup.dat'):
	x=open('setup.dat','w')
	x.write("""fullscreen=0
buildbots=0
optimize=1""")
def fullscreenchk():
	global w,h,screenw,screenh,screen,mmenu,button_size_width
	if fullscreen:w=0;h=0
	else:
		w=int(640*upscale)
		h=int(480*upscale)
	screenw=w
	screenh=h
	downscale=1
	if fullscreen:screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN,DOUBLEBUF);w=screen.get_width()//downscale;h=screen.get_height()//downscale;screenw=w;screenh=h
	else:screen=pygame.display.set_mode((screenw,screenh),DOUBLEBUF,pygame.RESIZABLE)
	button_size_width=w//2
	mmenu=pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)-(button_size_height+40), button_size_width, button_size_height),pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)+(button_size_height-80), (button_size_width//2)-5, button_size_height),pygame.Rect(((w - button_size_width) // 2)+(button_size_width//2)+5, ((h - button_size_height) // 2)+(button_size_height-80), (button_size_width//2)-5, button_size_height),pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)-(button_size_height-80), button_size_width, button_size_height)	
button_size_height=50
button_selected=(170,170,170)
button_idle=(150,150,150)
mtext='Play Game','Settings','Online','Exit'
fullscreenchk()
pygame.display.set_caption(gamename+' ('+str(gamever)+')')
pygame.mouse.set_visible(True)
screen.set_alpha(None)
#w=640
#h=480
button=1
sprint=_A
selection=0
movement=0
aiblock=2
aitimestep=1
hitbox=[]
x=True
"""
		if x:
		  x=False
		else:
		  x=True"""
splashsize=20
hideblocks=False
def shake(word,pos):
	wording=word
	write(wording, (pos[0]-randint(1,10), pos[1]-randint(1,10)), 60, (255, 0, 0))
	write(wording, (pos[0]-randint(1,10), pos[1]-randint(1,10)), 60, (0, 255, 0))
	write(wording, (pos[0]-randint(1,10), pos[1]-randint(1,10)), 60, (255, 255, 255))
	write(wording, (pos[0]+randint(1,10), pos[1]+randint(1,10)), 60, (0, 0, 255))
def worldmenu():
	global activity,button,axe,aitime
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_d:
				reload()
				activity=2
				axe = time.time()
				aitime = time.time()+aitimestep
			if event.key == pygame.K_q:
				activity=1
				button=1
	screen.fill((20,20,20))
	pygame.draw.rect(screen, (50,50,50), pygame.Rect(20,40,200,40),border_radius=20)
	write(gamename + ' - Worlds', (40, 42), 60, (255, 255, 255))
	pygame.draw.rect(screen, (10,10,10), pygame.Rect(20,60,w-40,h-80))
	shake('Press D for your Normal Gameplay',(40,100))
def regen():
	global blockmainmenu
	if not hideblocks:
		blockmainmenu=[]
		tmp=0
		x=True
		max=100*2
		madew=0
		madeh=0
		for b in range(1,(h//splashsize)+1):
			madeh+=1
			if madeh>=max:
				break
			for a in range(1,(w//splashsize)+1):
				madew+=1
				if madew>=max:
					break
				if randint(1,2)==2:
					blockmainmenu.append(((a-1)*splashsize,(b-1)*splashsize,tmp))
					tmp+=1
#10/randint(1,100)
regen()
async def blocksplash():
	global blockmainmenu
	if not hideblocks:
		border=10
		speed=1
		for a in blockmainmenu:
			if a[1]<=-25:
				blockmainmenu[a[2]]=(a[0],h+25,a[2])
			else:
				if speed==1:
					speed=0.8
				elif speed==0.8:
					speed=0.6
				elif speed==0.6:
					speed=1
				blockmainmenu[a[2]]=(a[0],a[1]-speed,a[2])
			pygame.draw.rect(screen, (0,0,0), pygame.Rect(a[0]-(border//2), a[1]-(border//2), splashsize+border, splashsize+border))
			pygame.draw.rect(screen, (50,50,50), pygame.Rect(a[0], a[1], splashsize, splashsize))
def click():
	global axe,aittime,activity
	if button == 1:
#		reload()
#		axe = time.time()
#		aitime = time.time()+aitimestep
		activity = 6
	elif button == 2:
		activity = 3
	elif button == 3:
		activity = 4
	elif button == 4:
		pygame.quit()
		sys.exit()
crazyness=0
def mainmenu():
	global debugmode,button,activity,crazyness
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			click()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_F5:
				if debugmode:
					debugmode = _A
				else:
					debugmode = _B
			if event.key == pygame.K_l:
				crazyness+=1
			if event.key == pygame.K_q:
				pygame.quit()
				sys.exit()
			if event.key == pygame.K_DOWN:
				if button > 3:
					button = 1
				else:
					button += 1
			if event.key == pygame.K_UP:
				if button < 2:
					button = 4
				else:
					button -= 1
			if event.key == pygame.K_RETURN:
				click()
	for a in range(1, len(mmenu)+1):
		if mmenu[a-1].collidepoint(pygame.mouse.get_pos()):
			if pygame.mouse.get_focused():
				button=a
		if a ==button:
			select = True
		else:
			select = False
		if select:
			buttcolour = button_selected
		else:
			buttcolour = button_idle
		pygame.draw.rect(screen, (buttcolour), mmenu[a-1])
		if select:
			pygame.draw.rect(screen, (200,200,200), mmenu[a-1],2)
		else:
			pygame.draw.rect(screen, (100,100,100), mmenu[a-1],2)
		tmp = font.render(mtext[a-1], True, (255, 255, 255))
		centertext = tmp.get_rect(center=mmenu[a-1].center)
		screen.blit(tmp, centertext)
	write('Press Return to Select     Up/Down To Navigate', (10,h-20), 20, (255,255,255))
	for a in range(1,crazyness+2):
		shake(gamename,(40+(a*5),60+(a*5)))
	write(gamename, (40, 60), 20, (255,255,255))
	if crazyness<4:
		if crazyness>0:
			write('You Found the Easter Egg Huh lol',(10,h-40),20,(255,255,255))
	elif crazyness<10:
			write('Ok you can stop now please...',(10,h-40),20,(255,255,255))
	elif crazyness<41:
		write('Actually Stop Now PLEASE',(10,h-40),20,(255,255,0))
	elif crazyness<51:
		shake('I SAID STOP',(10,h-40))
		write('I SAID STOP',(10,h-40),20,(255,0,0))
	elif crazyness<61:
		crash("You didn't stop so here is your reward")
async def main():
		global activity,screen,button,buttons,BUTTON_COLOR,SELECTED_BUTTON_BORDER_COLOR,SELECTED_BUTTON_BORDER_WIDTH,BUTTON_TEXT_OFFSET,BUTTON_TEXT_SIZE,BUTTON_TEXT_COLOR,debugmode,messagetime,aitime
		write('U can see me do you?', (10, h+2), 20, (255, 255, 255))
		if activity==1 or activity==3:
			if activity:
				clear((0, 150, 110))
			await blocksplash()
		if activity == 0:
			for a in range(1, 255):
				screen.fill((numlimit(a, 255), numlimit(a, 255), numlimit(a, 255)))
				if a >= 255//2:
					write(gamename, (20, h//2), 40, (255-a, 255-a, 255-a))
				pygame.display.flip()
				pygame.time.delay(introtiming)
			pygame.time.delay(1500)
			for a in range(255, 1, -1):
				screen.fill((255, 255, 255))
				write(gamename, (20, h//2), 40, (255-a, 255-a, 255-a))
				pygame.display.flip()
				pygame.time.delay(introtiming)
			for a in range(1, 255):
				screen.fill((255, 255, 255))
				write(_J, (20, h//2), 40, (255-a, 255-a, 255-a))
				write(_I, (22, h//2+23), 20, (255-a, 255-a, 255-a))
				pygame.display.flip()
				pygame.time.delay(introtiming)
			pygame.time.delay(3000)
			for a in range(255, 1, -1):
				color = a, numlimit(a, 150), numlimit(a, 110)
				screen.fill(color)
				if a >= 255//2:
					write(_J, (20, h//2), 40, (255-a, 255-a, 255-a))
					write(_I, (22, h//2+23), 20, (255-a, 255-a, 255-a))
			pygame.display.flip()
			pygame.time.delay(introtiming)
			activity = 1
		elif activity == 1:
			mainmenu()
		elif activity == 3:
			settingspage()
		elif activity == 2:
			await game()
		elif activity == 5:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					save()
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						activity = 2
			pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(20, 20, w-40, h-40))
			write('Arrow Keys - Move the Block', (30, 40), 20, (255, 255, 255))
			write('Z - Crouch', (30, 60), 20, (255, 255, 255))
			write('S - Sight Mode', (30, 80), 20, (255, 255, 255))
			write('Q - Save and Quits to menu', (30, 100), 20, (255, 255,255))
			write('SHIFT - Sprint', (30, 120), 20, (255,255,255))
			write('LControl - Places Block', (30, 140), 20,(255,255,255))
			write('LALT - Mines Block', (30, 160),20,(255,255,255))
			write('Press Return to Start Playing!', (25, h-45),20,(255,255,255))
		elif activity == 6:
			worldmenu()
		elif activity == 4:
			clear((0, 150, 150))
			write(gamename+' Online (Register Page)', (40, 60), 60, (255, 255, 255))
			pygame.draw.rect(screen, (255,255,255), pygame.Rect(40,80,w-80,h-160))
			write('Url Does not exist, Contact your Administrator',(45,85),20,(0,0,0))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
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
						0
		if debugmode:
			write('FPS:'+str(fps), (w-100, 23), 20, (255, 255, 255))
			pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, 0, w, 10))
			struct = ((fps)/limitfps)*w
			pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(0, 0, struct, 10))
		if len(message) > 0:
			if not 'messagetime' in globals():
				messagetime = time.time()+5
			elif not time.time() > messagetime:
				pygame.draw.rect(screen, (100, 100, 150), pygame.Rect(20, 20, w-40, 20))
				pygame.draw.rect(screen, (100, 100, 200), pygame.Rect(20, 20, w-40, 20),2)
				write(message[:50], (25, 23), 20, (255, 255, 255))
		pause(limitfps)
		pygame.display.flip()

def draw_rounded_rect(surface,rect,color,radius):pygame.draw.rect(surface,color,rect)
def draw_buttons():
	global hitbox
	hitbox=[]
	for(i,(text,pos))in enumerate(buttons,start=1):
		button_rect=pygame.Rect(pos[0],pos[1],w-40,40);draw_rounded_rect(screen,button_rect,BUTTON_COLOR,5)
		if button==i:pygame.draw.rect(screen,SELECTED_BUTTON_BORDER_COLOR,button_rect,SELECTED_BUTTON_BORDER_WIDTH)
		write(text,(pos[0]+BUTTON_TEXT_OFFSET[0],pos[1]+BUTTON_TEXT_OFFSET[1]),BUTTON_TEXT_SIZE,BUTTON_TEXT_COLOR)
def numlimit(cur,min):
	if cur>min:return cur
	else:return min
def playercheck():
    playerpos = -int(round(x)) + w // playersize // 2 - 1, -int(round(y)) + h // playersize // 2 - 1
    return playerpos
	
async def load_chunks():
	colorstep = 0
    # Create a list of visible chunks using a generator expression
	xmin = playerpos[0] - renderdistancex
	xmax = playerpos[0] + renderdistancex
	ymin = playerpos[1] - renderdistancey
	ymax = playerpos[1] + renderdistancey
	tmploaded=[tmp for tmp in tmpchunks if xmin <= tmp[0] <= xmax and ymin <= tmp[1] <= ymax]
	loaded = [tmp for tmp in chunks if xmin <= tmp[0] <= xmax and ymin <= tmp[1] <= ymax]
	# This is for Temporary Chunks (Not loaded to "Real" Chunks)
	for b in tmploaded:	
		chunk_x = playersize * b[0] + playersize * x
		chunk_y = playersize * b[1] + playersize * y
		rect = pygame.Rect(chunk_x, chunk_y, playersize + 1, playersize + 1)
		if sight == _A:
			pygame.draw.rect(screen, b[2], rect)
		else:
			color = (0,255,0)
			pygame.draw.rect(screen, color, rect, 1)
	# Iterate over visible chunks and draw them
	for b in loaded:	
		chunk_x = playersize * b[0] + playersize * x
		chunk_y = playersize * b[1] + playersize * y
		rect = pygame.Rect(chunk_x, chunk_y, playersize + 1, playersize + 1)
		if sight == _A:
			pygame.draw.rect(screen, b[2], rect)
		else:
			color = (255, 255, 0) if len(b) > 3 else (255, 255, 255)
			pygame.draw.rect(screen, color, rect, 1)
		if botmode:
			aipot_rect = pygame.Rect(aipot[0], aipot[1], playersize, playersize)
			pygame.draw.rect(screen, (0, 0, 255), aipot_rect)
			pygame.draw.rect(screen, (255, 255, 255), aipot_rect, 2)
        # Yield control to the event loop to maintain smooth FPS
	await asyncio.sleep(0)
	return loaded, colorstep
chat_messages = []
chat_box_width, chat_box_height = 600, 200
chat_box_x = (screenw - chat_box_width) // 2
chat_box_y = screenh - chat_box_height - 10
chat_box_rect = pygame.Rect(chat_box_x, chat_box_y, chat_box_width, chat_box_height)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
try:
	for a in os.listdir('mods/'):exec(open('mods/'+str(a)).read())
	while __name__ == "__main__":
		asyncio.run(main()) 
except Exception as error:print('Error had occurred!\n['+str(error)+']');crash(str(error))

