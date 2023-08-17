from random import randint
from pygame.locals import *
import pygame,os,time,sys,asyncio,concurrent.futures,threading
nline='\n'
axe=0
gamename='TinyWorld'
gamever='2.5.0816.1.dev'
gameupdateurl='N/A'
gameauthor='Pxki Games'
print('Starting Game...')
upscale=1
limitfps=1000
maxmem=1024*64
sfps=0
debugmode=True
if upscale<.9:
	print('Can not go down <=0.8')
	exit()
upscale=int(round(upscale))
introtiming=1/160
fullscreen=False
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
istd=False
texturepath='textures/'
gamepath='Saves/'
saves=[]
if not os.path.isdir(texturepath):os.mkdir(texturepath)
if not os.path.isdir(gamepath):os.mkdir(gamepath)
if not os.path.isdir('mods'):os.mkdir('mods')
def mineblock(posx,posy):
	for b in blockcolor:
		if(posx,posy,b)in chunks:remove=True;break
		else:remove=False
	if remove:chunks.remove((posx,posy,b))
def placeblock(posx,posy,block):
	for b in blockcolor:
		if not(posx,posy,b)in chunks:place=True
		else:place=False;break
	if place:
		chunks.append((posx,posy,block))
def keyboard(title):
	backgroundcolor1=100,100,100;backgroundcolor2=150,150,150;backgroundcolor3=100,100,100;backgroundcolor3focus=100,200,100;label='';x1=1;y1=2
	while True:
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
							elif x1==2:label+='w'
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
							elif x1==8:label+=','
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
					elif a==2:write('w',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
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
					elif a==8:write(',',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==9:write('.',(w//2-400//2+10+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
					elif a==10:write('Go',(w//2-400//2+6+40*(a-1)+7,h//2-200//2+60+35*(b-1)+5),15,forepallete)
		write(title[:50]+' [Characters Left:'+str(65-len(label))+']',(w//2-190,h//2-90),20,forepallete);pygame.display.flip()
def memspace():
  if len(str(globals())) >= maxmem:
    print('Memory Overload !\nThis will be sent to the Developer! :)')
    exit()
  else:
    return len(str(globals()))
def cbytes(size):
    """
    Convert bytes to the appropriate unit (KB, MB, GB, TB) based on the size.

    Args:
        size (int): Size in bytes.

    Returns:
        str: Converted size with the appropriate unit.
    """
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
			pygame.draw.rect(screen,(255,0,0),pygame.Rect(playersize*(w//playersize//2-1),playersize*(h//playersize//2-1),playersize,playersize));pygame.draw.rect(screen,blockcolor[blockid],pygame.Rect(w//2-30,h-60,40,40));pygame.draw.rect(screen,(255,255,255),pygame.Rect(w//2-30,h-60,40,40),2)
			loaded_count = ama
			if istd:
				controllerbutton=menu_draw((pygame.Rect(120,h-160,40,40),pygame.Rect(120,h-80,40,40),pygame.Rect(80,h-120,40,40),pygame.Rect(160,h-120,40,40),pygame.Rect(w-140,h-120,40,40),pygame.Rect(w-100,h-160,40,40),pygame.Rect(w-180,h-160,40,40),),('^','v','<','>','<o>','M','P',))
			else:
				controllerbutton=0
			for event in pygame.event.get():
				if event.type==pygame.QUIT:save();pygame.quit();sys.exit()
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
					if event.key==pygame.K_F6:
						dump()
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
						dump()
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
				write('('+str(int(x))+','+str(int(y))+') '+str(len(chunks))+' Total Blocks ['+str(loaded_count)+' Loaded]', (20, 23), dsize, (255, 255, 255))
				write('Block ID: '+str(blockid)+'/'+str(len(blockcolor)-1), (20, 23*2), dsize, (255, 255, 255))
				write('Exact Value Mode: '+str(collide), (20, 23*3), dsize, (255, 255, 255))
				write('Size: '+str(playersize)+'/'+str(tmpsize), (20, 23*4), dsize, (255, 255, 255))
			if gamemode==gamemodes[1]:write('Health Bar:'+str(health)+'%',(30,h-90),20,(255,255,255));pygame.draw.rect(screen,(150,150,150),pygame.Rect(30,h-72,100,2));pygame.draw.rect(screen,healthstatus,pygame.Rect(30,h-72,10*(health//10),2))

			pygame.draw.rect(screen, (255,255,255), pygame.Rect((playersize * playerpos[0] + playersize * x),playersize * playerpos[1] + playersize * y,playersize,playersize),2)
			write('Note: This will be changed Later',(30,h-40),0,(255,255,255))
def settingspage():
  global button,optimize,botmode,fullscreen,activity,screen,firstcom	
  write(gamename + ' - Settings', (40, 42), 60, (255, 255, 255))
  setbutton=menu_draw((pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)-(button_size_height+40), button_size_width, button_size_height),pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)-(button_size_height-20), button_size_width, button_size_height),pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)-(button_size_height-80), button_size_width, button_size_height),pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)-(button_size_height-140), button_size_width, button_size_height),),('Optimize Mode: ' + ('Enabled' if optimize else 'Disabled'),'Builder Bots: ' + ('Enabled' if botmode else 'Disabled'),'Fullscreen: ' + ('Enabled' if fullscreen else 'Disabled'),'Main Menu'))
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN: 
        if setbutton == 1:
          optimize = not optimize
        elif setbutton == 2:
          botmode = not botmode
        elif setbutton == 3:
          fullscreen = not fullscreen
          firstcom=True
          fullscreenchk()
          regen()
        elif setbutton == 4:
          activity = 1

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q:
        pygame.quit()
        sys.exit()  
#  pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(20, h // 2 - 80, w - 40, 40))
#  pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(20, h // 2 - 20, w - 40, 40))
#  pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(20, h // 2 + 40, w - 40, 40))
#  pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(20, h // 2 + 100, w - 40, 40))
#  write('Optimize Mode: ' + ('Enabled' if optimize else 'Disabled'), (25, h // 2 - 68), 25, (255, 255, 255))
#  write('Builder Bots: ' + ('Enabled' if botmode else 'Disabled'), (25, h // 2 - 8), 25, (255, 255, 255))
#  write('Fullscreen: ' + ('Enabled' if fullscreen else 'Disabled'), (25, h // 2 + 52), 25, (255, 255, 255))
#  write('Exit Menu', (25, h // 2 + 110), 25, (255, 255, 255))
#  pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(20, h // 2 - 80 + 60 * (button - 1), w - 40, 40), 2)

def write(text, pos, size, color):
    screen.blit(font.render(text, True, color), pos)
def clear(color):screen.fill(color)
def crash(text):
#	pygame.draw.rect(screen,red,pygame.Rect(0,h//2-20,w,35))
	#
	button=0
	while True:
		fullscreenchk()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
		pygame.draw.rect(screen,(40,40,40),pygame.Rect(w//2//2,h//2//2,w//2,h//2),border_radius=5)
		pygame.draw.rect(screen,(20,20,20),pygame.Rect(w//2//2+3,h//2//2+33,w//2-6,h//2-36))
		write('Sorry! ('+str((w,h))+')',(w//2//2+8,h//2//2+8),20,forepallete)
		write(text[:int(60*upscale)],(w//2//2+8,h//2//2+38),20,forepallete)
		pygame.display.update()
#	xa=w//2
#	max=2**16
#	for a in range(1,max):		
#		pygame.draw.rect(screen,(10,10,10),pygame.Rect(xa//2,h//4-20,xa,20))
#		pygame.draw.rect(screen,(10,255,10),pygame.Rect(xa//2,h//4-20,(a/max)*xa,20))
#		write('Development',(xa//2+20,h//4-17),20,forepallete)
#		pygame.display.update()
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
	#return None
	if time.time()-fpstime>1/quickness:
		fps=int(fpstmp)
		fpstmp=0
		fpstime=time.time()
	else:
		fpstmp+=1*quickness
#	time.sleep(1/ms)
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
        str(collide) +
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
	for a in range(1,1000):place=False;pos=randint(1,x+100)//2,randint(1,y+100)//2;foodpos.append((pos[0],pos[1],randint(1,2)))
def reload():
	global aix,aiy,aipos,foodcount,health,x,y,radius,playersize,foodpos,gamemode,aitrigger,collide,aitime,aipot,wmenu,chunks
	x=0;y=0;aix=0;aiy=0;health=100;gamemode=gamemodes[0]
	if os.path.isfile(gamepath+savename):
		clear((0, 0, 0))
		write('Preparing World...', (20, h // 2), 20, (255, 255, 255))
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
		chunks=[]
		for c in tmp:
			chunks.append(c) 
			
	t=time.time()+2;tok=0;xxx=time.time()+tok;fun=randint(1,len(messages))-1;fop=50
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
optimize=False
botmode=False
worldtype=2
if not os.path.isfile('setup.dat'):
	x=open('setup.dat','w')
	x.write("""fullscreen=0
buildbots=0
optimize=1""")
def gamesaves():
	global savespos,savestext
	saves=os.listdir(gamepath)
	savespos=[]
	savestext=[]
	tmp=0
	for a in saves[:4]:
		tmp+=1
		savespos.append(pygame.Rect((w - button_size_width) // 2,(55*tmp)+20, button_size_width, button_size_height))
		savestext.append(a.replace('.tw','').replace('_',' '))

firstcom=False
def fullscreenchk():
	global w,h,screenw,screenh,screen,mmenu,button_size_width,wmenu,wtext,buffer,menuoverlay,firstcom
	if not fullscreen:
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
			screenw=w
			screenh=h

	downscale=1
	flags=DOUBLEBUF|pygame.RESIZABLE|pygame.HWSURFACE
	if fullscreen:
		if not firstcom:
			screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN|flags)
		w=screen.get_width()
		h=screen.get_height()
		screenw=w
		screenh=h
	else:
		if not firstcom:
			screen=pygame.display.set_mode((screenw,screenh),flags)
	if not firstcom:
		firstcom=True
	button_size_width=w//2
	buffer = pygame.Surface((screenw, screenh))
	mmenu=pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)-(button_size_height+40), button_size_width, button_size_height),pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)+(button_size_height-80), (button_size_width//2)-5, button_size_height),pygame.Rect(((w - button_size_width) // 2)+(button_size_width//2)+5, ((h - button_size_height) // 2)+(button_size_height-80), (button_size_width//2)-5, button_size_height),pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)-(button_size_height-80), button_size_width, button_size_height)	
	wmenu=pygame.Rect((w - (button_size_width) -4)//2, (h-button_size_height)-4, button_size_width//4, button_size_height),pygame.Rect((w - (button_size_width)+((button_size_width//2))+4)//2, (h-button_size_height)-4, button_size_width//4, button_size_height),pygame.Rect((w - (button_size_width)+((button_size_width//2)*2)+12)//2, (h-button_size_height)-4, button_size_width//4, button_size_height),pygame.Rect((w - (button_size_width)+((button_size_width//2)*3)+20)//2, (h-button_size_height)-4, button_size_width//4, button_size_height)
	if w<768:
		wtext='Create','Delete','Warp!','Exit'
	else:
		wtext='Create World','Delete World','Warp! World','Exit'
button_size_height=50
button_selected=(170,170,170)
button_idle=(150,150,150)
mtext='Play Game','Settings','View Progress','Exit'
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
x=True
"""
		if x:
		  x=False
		else:
		  x=True"""
splashsize=20
hideblocks=False
intense=5*9
def shake(word,pos):
	wording=word
	write(wording, (pos[0]-randint(1,10), pos[1]-randint(1,10)), 60, (255, 0, 0))
	write(wording, (pos[0]-randint(1,10), pos[1]-randint(1,10)), 60, (0, 255, 0))
	write(wording, (pos[0]-randint(1,10), pos[1]-randint(1,10)), 60, (255, 255, 255))
	write(wording, (pos[0]+randint(1,10), pos[1]+randint(1,10)), 60, (0, 0, 255))
def debugmenu():
	pygame.draw.rect(screen, (), rect)
textbox_text=''
textbox_active=True
def createworld():
	global activity, button,textbox_active,textbox_text,savename
	floorbuttons=menu_draw((pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)+(button_size_height+20), button_size_width, button_size_height),pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)+(button_size_height+100), button_size_width, button_size_height),),text=('Create','Back'))
	textbox_rect = pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2) + (button_size_height - 60),button_size_width, 60)
	pygame.draw.rect(screen,(0,0,0),pygame.Rect(textbox_rect))
	pygame.draw.rect(screen,(255,255,255),textbox_rect,2)
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
			exit()
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
				savename=textbox_text.replace(' ','_')+'.tw3'
				reload()
				activity=2
				axe = time.time()
				aitime = time.time()+aitimestep
				
			elif floorbuttons == 2:
				activity=6
def deleteworld():
	global activity, button,selected_save
	tmp = font.render('U wanna Delete '+str(savestext[selected_save-1])+'?', True, (255, 255, 255))
	centertext = tmp.get_rect(center=pygame.Rect(0,((h - button_size_height) // 2)+(button_size_height-20),w,20).center)
	screen.blit(tmp, centertext)
	floorbuttons=menu_draw((pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)+(button_size_height+20), button_size_width, button_size_height),pygame.Rect((w - button_size_width) // 2, ((h - button_size_height) // 2)+(button_size_height+100), button_size_width, button_size_height),),text=('Delete!','Nwooo'))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if floorbuttons == 1:
				os.remove(gamepath+str(savestext[selected_save-1].replace(' ','_')))
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
	pygame.draw.rect(screen, (50,50,50), pygame.Rect((w//4)-55,35,200,40),border_radius=20)
	write(gamename + ' - Worlds', ((w//4)-40, 42), 60, (255, 255, 255))
	pygame.draw.rect(screen, (10,10,10), pygame.Rect((w//4)-20,60,w-(w//2)+40,h-120))
	pygame.draw.rect(screen, (255,255,255), pygame.Rect((w//4)-20,60,w-(w//2)+40,h-120),2)
	savebutton=menu_draw(savespos,text=savestext,selected_button=selected_save)
	worldbutton=menu_draw(wmenu,text=wtext)
	if worldbutton==1:
		if len(saves)>3:
			if w>767:
				write('Unfortunately, I cannot save any more changes as I have already hit the limit of 4 saves /o\\',(25,h-85),20,(255,255,0))
			else:
				write("I've reached the dreaded 4-save limit! ;n;",(25,h-85),20,(255,255,0))
	elif worldbutton==2 or worldbutton==3:
		if selected_save==0:
			write("No World Selected",(25,h-85),20,(255,255,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
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
				if randint(1,2)==2:
					#(a-1)*splashsize,(b-1)*splashsize
					blockmainmenu.append((-100,-100,tmp))
					tmp+=1
		blocklen=len(blockmainmenu)
#10/randint(1,100)
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
				random_x = randint(1, w_div_splashsize * splashsize)
				blockmainmenu[i] = (random_x, h + randint(100, h*2), a[2])
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
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if menubutton == 1:
#		reload()
#		axe = time.time()
#		aitime = time.time()+aitimestep
				activity = 6
				gamesaves()
			elif menubutton == 2:
				activity = 3
			elif menubutton == 3:
				activity = 9
				#activity = 4
			elif menubutton == 4:
				exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_F5:
				if debugmode:
					debugmode = False
				else:
					debugmode = True
#			if event.key == pygame.K_l:
#				crazyness+=1
			if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
				exit()
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
def dump():
	return None
	print('Dumping RAM...')
	f=open('dump'+str(randint(1111,9999))+'.txt','w')
	f.write(str(globals()))
	f.close()
	print('Dumped!')
def main():
		global activity,screen,button,buttons,BUTTON_COLOR,SELECTED_BUTTON_BORDER_COLOR,SELECTED_BUTTON_BORDER_WIDTH,BUTTON_TEXT_OFFSET,BUTTON_TEXT_SIZE,BUTTON_TEXT_COLOR,debugmode,messagetime,aitime
		write('U can see me do you?', (10, h+2), 20, (255, 255, 255))
		allowed=[1,3,6,9]
		if activity in allowed:
			clear((20,20,20))
			blocksplash()
		if activity == 0:
			activity = 1
		elif activity == 1:
			mainmenu()
		elif activity == 2:
			game()
		elif activity == 3:
			settingspage()
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
		elif activity == 7:
			createworld()
		elif activity == 8:
			deleteworld()
		elif activity == 9:
#			clear((10, 10, 10))
			tmp=0
			write(gamename+' Progress', (40, 60), 60, (255, 255, 255))
			pygame.draw.rect(screen, (255,255,255), pygame.Rect(40,80,w-80,h-160))
			for a in todo:
			  write(a[0]+' ('+str(a[1])+')',(45,90+(30*(tmp))),20,(0,0,0))
			  tmp+=1
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
#			write(str(cbytes(memspace()))+' Out of '+cbytes(maxmem),(20,h-40),20,(255,255,255))
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
	for(i,(text,pos)) in enumerate(buttons,start=1):
		button_rect=pygame.Rect(pos[0],pos[1],w-40,40)
		draw_rounded_rect(screen,button_rect,BUTTON_COLOR,5)
		if button==i:
			pygame.draw.rect(screen,SELECTED_BUTTON_BORDER_COLOR,button_rect,SELECTED_BUTTON_BORDER_WIDTH)
		write(text,(pos[0]+BUTTON_TEXT_OFFSET[0],pos[1]+BUTTON_TEXT_OFFSET[1]),BUTTON_TEXT_SIZE,BUTTON_TEXT_COLOR)
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
		if botmode:
			aipot_rect = pygame.Rect(aipot[0], aipot[1], playersize, playersize)
			pygame.draw.rect(screen, (0, 0, 255), aipot_rect)
			pygame.draw.rect(screen, (255, 255, 255), aipot_rect, 2)
        # Yield control to the event loop to maintain smooth FPS
	#await asyncio.sleep(0)
	return ama,loaded, colorstep
chat_messages = []
chat_box_width, chat_box_height = 600, 200
chat_box_x = (screenw - chat_box_width) // 2
chat_box_y = screenh - chat_box_height - 10
chat_box_rect = pygame.Rect(chat_box_x, chat_box_y, chat_box_width, chat_box_height)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
#crash('Example Of Menu')
while True:
  main()
exit()
try:
	for a in os.listdir('mods/'):exec(open('mods/'+str(a)).read())
	while __name__ == "__main__":
		pass
		#asyncio.run(main()) 
		#thegame=threading.Thread(target=main)
		#thegame.start()
		#thegame.join()
except Exception as error:
    print('Error had occurred!\n['+str(error)+']')
    crash(str(error))

