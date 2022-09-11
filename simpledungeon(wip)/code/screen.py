import os
from code import util, terminal
from getkey import getkey, keys
import copy
import cursor




class ScreenError():
	pass


class Screen():
	def __init__(self, colors=[]):
		"""Initiate the screen Object"""
		self.width = 0
		self.height = 0
		if colors:
			self.colors = [*set(["\033[0m","\033[30m","\033[40m","\033[31m","\033[41m","\033[32m","\033[42m","\033[33m","\033[43m","\033[34m","\033[44m","\033[35m","\033[45m","\033[36m","\033[46m","\033[37m","\033[47m"] + colors)]
		else:
			self.colors = ["\033[0m","\033[30m","\033[40m","\033[31m","\033[41m","\033[32m","\033[42m","\033[33m","\033[43m","\033[34m","\033[44m","\033[35m","\033[45m","\033[36m","\033[46m","\033[37m","\033[47m"]


	def countchars(self, string):
		"""Works similar to len() but disregards color symbols in count"""
		
		original_length = len(string)

		for color in self.colors:
			occurances = string.count(color)
			original_length -= (len(color)*occurances) if occurances else 0

		return original_length

	@staticmethod
	def hide_cursor():
		"""Hide the Cursor"""
		cursor.hide()

	@staticmethod
	def show_cursor():
		"""Show the cursor"""
		cursor.show()

	def balance_strings(self, strings):
		"""Return a list of strings with equal length"""

		longest = self.countchars(max(strings, key=self.countchars))

		balanced_strings = []

		for string in strings:
			balanced_strings.append(string+(" "*(longest-self.countchars(string))))

		return balanced_strings

	def build_padded_string(self, string):
		"""Return a string built to the correct length"""

		padding = int((60-self.countchars(string))/2)

		_str = "| " + (" "*padding) + string + (" "*padding)

		if self.countchars(_str) == 62:
			_str += "  |"
		elif self.countchars(_str) == 61:
			_str += "   |"
		else:
			_str += " |"

		return _str

	def center(self, string, width=61):
		"""Return a centered string"""

		length_of_string = self.countchars(string)

		padding = int((width-length_of_string)/2)

		return (" "*padding)+string+(" "*padding)


	def update_size(self):
		"""Update the screen size"""
		size = os.get_terminal_size()

		if size.columns != self.width or size.lines != self.height:
			terminal.clear()

		self.width = size.columns
		self.height = size.lines


	def display_out(self, strings, auto_print=True):
		"""Display a list of strings in the center of the screen"""

		self.update_size()

		if type(strings) != list:
			strings = strings.split("\n")

		length_of_string = self.countchars(strings[0])
		height_of_string = self.countchars(strings)

		padding_width = int((self.width - length_of_string) / 2)
		padding_height = int((self.height - height_of_string) / 2)

		

		if auto_print:
			print("\n"*padding_height)

			for string in strings:
					print((" "*padding_width)+string)

		else:
			out_strings = ["\n"*padding_height]

			for string in strings:
				out_strings.append((" "*padding_width)+string)

			return out_strings


	def display_table(self, table):
		"""Display a table"""

		# Balance the strings in each column

		# First we convert everything to strings
		new_table = []

		for row in table:
			new_table.append([str(item) for item in row])


		table = new_table

		# We continue by finding the longest the table

		columns = []

		for i in range(len(table[0])):
			columns.append(0)

		for row in table:
			for i in range(len(table[0])):
				length = self.countchars(row[i])
				if length > columns[i]:
					columns[i] = length

		# convert the lists of data into one string

		new_table = []

		for row in table:
			new_table.append("".join(string+(" "*((columns[row.index(string)]-self.countchars(string))+3)) for string in row))

		# Should now have a balanced table I can display using display out

		self.display_out(new_table)






	def display_card(self, player=None, content=["No content"]):
		"""Show a card from a line of content"""

		content = self.balance_strings(content)

		terminal.clear()

		length_of_content = self.countchars(content)

		if length_of_content > 60:
			raise ScreenError("Single Strings longer then 60 characters are not supported") # Throw error for now

		else:
			spacing = int((60-length_of_content) /  2)

			out = []

			if player:
				out.append("---"*21+"--") # it works, don't question it.

				for stat in [player.get_stats()]:
					out.append(self.build_padded_string(stat))

			out.append("---"*21+"--")

			for line in content:
				out.append(self.build_padded_string(line))


			for i in range(23-self.countchars(out)):
				out.append("|"+(" "*63)+"|")


			out.append("-"*65)
			out.append("\n")
			out.append("\n")

		self.display_out(out)



	def get_input(self, player=None, question="", raw_prompts=[]):
		"""Display a question with multiple options to choose from, return result"""

		terminal.clear()

		prompts = []
		return_values = []

		for i in raw_prompts:
			prompts.append(i[0])
			return_values.append(i[1])

		prompts = self.balance_strings(prompts)

		if type(question) != list:
			question = question.split("\n")

		index = 0

		question.append("")
		question.insert(0, "")

		while True:
			content = copy.deepcopy(question)
			for i in prompts:
				if prompts.index(i) == index:
					content.append(self.center(">  " + i, 42))
				else:
					content.append(self.center("   " + i, 42))

			self.display_card(
				player,
				content,
			)

			key = getkey()

			new_index = index

			if key == 'w' or key == keys.UP:
				new_index -= 1
			elif key == 's' or key == keys.DOWN:
				new_index += 1
			elif key == ' ' or key == '' or key == '\n':
				return return_values[index]

			# check valid

			if new_index >= 0 and new_index < self.countchars(prompts):
				index = new_index




			

