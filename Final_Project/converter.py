from lexer import Lexer
from parser import SyntaxAnalyzer


# The Converter class uses the results of the lexer and syntax analyzer. After the input string has passed the syntax analysis, it gets processed by converter. In this case, it takes the condition of the token type to determine how to convert the emmet input into HTML.

class Converter(object):

	# The converter first initializes the input text, the lexer (from the Lexer class), the syntax analyzer (from the SyntaxAnalyzer class), a stack to store HTML closing tags, and an output string where all the conversions will be concatenated to before being printed. All of the new lines and tabs for the html styling are made by trial and error

	def __init__(self, text):
		self.text = text
		self.lexer = Lexer
		self.lex = self.lexer(text)
		self.currentToken = self.lex.getNextToken()
		self.syntaxanalyzer = SyntaxAnalyzer
		self.syntax = self.syntaxanalyzer(text)
		self.check_syntax = self.syntax.check_syntax()
		self.stack = []
		self.output = ""
# 
	def convertTags(self):
		# Store the opening tag without the right angle bracket in a variable
		temporary =  "<" + self.currentToken.value

		# Create the closing tag and push into a stack
		closingtag = '</' + self.currentToken.value + '>'
		self.stack.append(closingtag)

		self.currentToken = self.lex.getNextToken()

		# If the following token is either a class or an id, add the attributes to the variable.
		while self.currentToken.type == 'CLASS' or self.currentToken.type == 'ID':
			if self.currentToken.type == 'ID':
				temporary += ' id=\"' + self.currentToken.value[1:] + '\"'
			elif self.currentToken.type == 'CLASS':
				temporary += ' class=\"' + self.currentToken.value[1:] + '\"'
			self.currentToken = self.lex.getNextToken()

		# Add the right angle bracket to the variable
		temporary += '>'

		# If the next token has type 'TIMES'
		if self.currentToken.type == 'TIMES':
			# Pop the closing tag from the stack
			self.stack.pop()
			# Get the next token to know the digit to multiply
			self.currentToken = self.lex.getNextToken()

			# Change the variable to contain a new line, tabs, the current variable and the closing tag multiplied by the digit in the token.
			temporary = ('\n' + '\t' * len(self.stack) + temporary + closingtag) * int(self.currentToken.value) + '\n' + ('\t' * (len(self.stack)-1))

			# Slices the front part of the variable to get rid of extra new lines and tabs
			temporary = temporary[len(self.stack)+1:]
			self.currentToken = self.lex.getNextToken()

		# Add the variable to the output string
		self.output += temporary	

	def convertChild(self):
		# Prints new line and tabs. The tabs are based on the number of items in the stack.
		self.output += '\n'+('\t'*len(self.stack))
		self.currentToken = self.lex.getNextToken()

	def convertSibling(self):
		if len(self.stack) > 0:
			# Pops from the stack so that the closing tag comes before the sibling tag
			self.output += self.stack.pop()
		# Adds a new line and tabs so that the next tag is positioned appropriately
		self.output += '\n'+('\t'*len(self.stack))		
		self.currentToken = self.lex.getNextToken()

	def convertPow(self):
		# (^) aligns the next tag with the parent of the current tag. It pops from the stack twice so that the current tag is closed, the parent tag is closed, and the next tag is aligned with the parent.
		self.output += self.stack.pop()
		self.output += '\n' + ('\t'*(len(self.stack)-1)) + self.stack.pop()
		# Adds a new line and tabs so that the next tag is positioned appropriately
		self.output += '\n'+('\t'*len(self.stack))
		self.currentToken = self.lex.getNextToken()

	def convertGroup(self):
		# First the function keeps count of the tags in the group so that it knows how many closing tags to pop from the stack later.
		tagCount = 0
		# Gets the first token inside the parentheses
		self.currentToken = self.lex.getNextToken()

		# The while loop goes through all the tokens as long as it is not a right parentheses. For each of the possible token types, it calls the corresponding function to convert them. For type TAGS, it also increments the tag count by 1.
		while self.currentToken.type != 'RPAREN':
			if self.currentToken.type == 'TAGS':
				self.convertTags()
				tagCount += 1
			elif self.currentToken.type == 'CHILD':
				self.convertChild()
			elif self.currentToken.type == 'SIBLING':
				self.convertSibling()
			elif self.currentToken.type == 'POW':
				self.convertPow()
			elif self.currentToken.type == 'LPAREN':
				self.convertGroup()
		# When the group is closed, the tags inside the group needs to have their closing tags. Pop the most recent one and decrement the tag count by 1.
		self.output += self.stack.pop()
		tagCount -= 1
		# For as long as the tag count is more than 1, the closing tags get popped from the stack. The condition is not set to while tag count is more than 0, because the next operator after the closing parentheses will also pop from the stack. Setting it to 0 here will lead to double popping.
		while tagCount > 1:
			# groupTags = self.stack.pop()
			# Add new line, tabs, and the closing tags to the output string, and decrement the tag count by 1
			self.output += '\n' + ('\t'*(len(self.stack)-1)) + self.stack.pop()
			tagCount -= 1
		# Add new line and tabs so that the next tag is positioned appropriately
		self.output += '\n' + ('\t' * (len(self.stack)-1))
		self.currentToken = self.lex.getNextToken()

	def convertText(self):
		self.currentToken = self.lex.getNextToken()
		# The while loop will accept all tokens as a text as long as they are inside the left and right brace.
		while self.currentToken.type != 'RBRACE':
			self.output += self.currentToken.value
			self.currentToken = self.lex.getNextToken()

		# Because texts appear in between opening and closing tags, after the converter meets a token of type RBRACE, it pops from the stack to close the tag.
		self.output += self.stack.pop()
		self.currentToken = self.lex.getNextToken()

	def convert(self):
		# The following portion is only done with the condition of successful parsing.
		if self.check_syntax == 1:
			# While the token type is not EOF, each condition calls their corresponding converter function.
			while self.currentToken.type != 'EOF':

				if self.currentToken.type == 'TAGS':
					self.convertTags()

				elif self.currentToken.type == 'CHILD':
					self.convertChild()

				elif self.currentToken.type == 'SIBLING':
					self.convertSibling()

				elif self.currentToken.type == 'POW':
					self.convertPow()

				elif self.currentToken.type == 'LPAREN':
					self.convertGroup()

				elif self.currentToken.type == 'LBRACE':
					self.convertText()

			# Now that everything has been looked at, all of the tags need to have their closing tags. Since all the closing tags were stored in a stack, first check if the stack is empty. If it is not empty, pop the closing tags.
			if len(self.stack) != 0:
				closingtags = self.stack.pop()
				# While there are still closing tags in the stack, pop the closing tag and add newline and tabs.
				while len(self.stack) != 0:
					tabs = '\t'*(len(self.stack)-1)
					closingtags += '\n' + tabs + self.stack.pop()
				# Add the closing tags to the output
				self.output += closingtags + '\n\n\n'

			print(self.output)

			# Writes into html and txt file
			f_html = open('output.html','a')
			f_txt = open('output.txt', 'a')
			f_html.write(self.output)
			f_txt.write(self.output)
			f_html.close()
			f_txt.close()

def main():
	while True:
		try:
			text = input("something > ")
		except EOFError:
			break
		if text:
			syntax = Converter(text)
			parse = syntax.convert()

if __name__ == '__main__':
    main()
