import pygame as gui
import sys
import torch
import speech_recognition as sr
from transformers import pipeline

classifier = pipeline("sentiment-analysis")

w,h = 1600,900
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)

class TomCounts_ARI:
	def __init__(self):
		gui.mixer.init()
		gui.init()
		gui.font.init()
		self.det = "SENTIMENT TOM"
		self.pred = None
		self.list = []
		self.font = gui.font.Font("./quake.TTF", 80)
		self.count = 0
		self.width = 1920
		self.height = 1080
		self.bgimg = gui.image.load('bg.png')
		self.logo = gui.image.load('logo.png')
		self.shinelogo = gui.image.load('bglogo.png')
		self.shinelogo = gui.transform.scale(self.shinelogo,(800,800))
		self.bgimg = gui.transform.scale(self.bgimg,(self.width//2-100,self.height))
		self.disp = gui.display.set_mode((self.width,self.height),0,0)
		gui.display.set_caption("SENTIMENT Tom")
		self.img = gui.image.load("Speak/0001.jpg")
		self.img = gui.transform.scale(self.img,(w+120,h+160))
		self.CAPTURE_ALL()
    
	def infer(self,text):
		return classifier(text)[0]['label']

	def recordAudio(self):
		r = sr.Recognizer()
		r.dynamic_energy_threshold = False
		r.energy_threshold = 480
		with sr.Microphone() as source:
		    r.adjust_for_ambient_noise(source=source)
		    print('Listening')
		    try:
			    audio = r.listen(source,timeout=4,phrase_time_limit=4)
			    data = r.recognize_google(audio)
			    return data
		    except:
		        return "ERROR"

	def blitForever(self,val=None):
		if(val!=None):
			if(val not in self.list):
				self.list = []
				self.list.append(val)
				self.playAudioARI(val)
		else:
			self.disp.blit(self.img,(560,0,0,0))
		self.disp.blit(self.bgimg,(0,0))
		self.disp.blit(self.shinelogo,(0,self.height//2-450))
		self.disp.blit(self.logo,(150,self.height//2-300))
		text1 = self.font.render(str(self.det), True, white)
		text1Rect = text1.get_rect()
		text1Rect.center = (w//2,h)
		self.blitText()
		self.blittext()
		gui.display.update()


	def blittext(self):
		if self.det=='POSITIVE':
		    color = green
		elif self.det == 'NEGATIVE':
		    color = red
		else:
		    color = white
		text1 = self.font.render(str(self.det), True, color)
		text1Rect = text1.get_rect()
		text1Rect.center = (w//2+600,h+40)
		self.disp.blit(text1,text1Rect)
 
	def blitText(self):
		text1 = self.font.render(self.pred, True, white)
		text1Rect = text1.get_rect()
		text1Rect.center = (w//2-400,h+20)
		self.disp.blit(text1,text1Rect)

	def playAudioARI(self,data):
		i = 1
		gui.mixer.music.load(f'SpeakAud/{self.det}.mp3')
		gui.mixer.music.play()
		while(True):
			img = gui.image.load("Speak/0"+str(i).zfill(3)+".jpg")
			img = gui.transform.scale(img,(w+120,h+160))
			self.disp.blit(img,(560,0,0,0))
			self.disp.blit(self.bgimg,(0,0))
			self.disp.blit(self.shinelogo,(0,self.height//2-450))
			self.disp.blit(self.logo,(150,self.height//2-300))
			i+=1
			if(i==10):
				return
			self.blittext()
			gui.display.update()


	def CAPTURE_ALL(self):
		RUN = True
		while RUN:
			self.blitForever()
			for	eve in gui.event.get():
				if eve.type==gui.KEYDOWN:
					if eve.key==gui.K_RETURN:
					    data = self.recordAudio()
					    self.pred = data
					    sentiment = self.infer(data)
					    self.det = sentiment
					    self.playAudioARI(data)
					elif eve.key==gui.K_ESCAPE:
						RUN = False
						gui.quit()
						return

TomCounts_ARI()
