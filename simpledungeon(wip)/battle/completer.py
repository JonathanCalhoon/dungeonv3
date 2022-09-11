import sys, os
from fast_autocomplete import AutoComplete
from code import terminal, screen


try:
	from getkey import getkey, keys
except:
	import os
	os.system("pip install getkey")


screen = screen.Screen(colors=["\033[2m", "\033[3m", "\033[5m"])

class Completer():
	"""Autocomplete Sentences"""
	def __init__(self, sentences, prompt, player):
		"""Initate"""
		
		words = {}

		self.player = player

		self.sentences = sentences
		
		for word in sentences:
			words[word] = {}

		self.autocomplete = AutoComplete(words)
		
		self.prompt = prompt

		# add two extra lines
		self.prompt.append("")
		self.prompt.append("")
	
	def get_input(self):
		"""Do the thing"""
		
		reset = "\033[0m"
		color = "\033[2m\033[3m"
		blinking = "\033[5m"
		
		text = ""
		
		os.system('clear')

		result = ""
		
		while True:
			print("\033[H",end="")
			self.prompt[-2] = "-> " + text + blinking + "|" + reset
			self.prompt[-1] = result
			screen.display_card(self.player, self.prompt)
			key = getkey()
			try:
				if ord(key) == 127:
					if len(text) >= 0:
						text = text[:-1]
						key = ""
				elif ord(key) == 10:
					if text == "":
						return "attack 0"
					if text in self.sentences:
						return text
					else:
						result = color+"That command is not valid!"+reset
						key = ""
						text = ""
				elif ord(key) == 9:
					text = self.autocomplete.search(word=text, max_cost=3, size=3)[0][0]
				try:
					if ord(key) != 9:
						text += key
					
						values = self.autocomplete.search(word=text, max_cost=3, size=3)
						
						word = values[0][0]

						if text not in self.sentences and text:
							result = color+"do you mean? " + word+reset
						else:
							result = ""
				except Exception as e:
					pass
			except:
				pass
					
		
			
			
			
