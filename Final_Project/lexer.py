import re

#LEXICAL ANALYSER

CHILD, TIMES, SIBLING, NUMBERING, POW = 'CHILD', 'TIMES', 'SIBLING', 'NUMBERING', 'POW'
LPAREN, RPAREN, LBRACE, RBRACE, TAGS = 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'TAGS'
ID, CLASS, TEXT, DIGIT, LETTER = 'ID', 'CLASS', 'TEXT', 'DIGIT', 'LETTER'
WHITESPACE, COMMENT, EOF = 'WHITESPACE', 'COMMENT', 'EOF'


# The following section defines regular expressions that will be used to analyze the input text. If the input text matches any of the following regular expressions, they will be assigned to one of the token types declared above.

t_CHILD = r'\>'
t_TIMES = r'\*'
t_SIBLING = r'\+'
t_POW = r'\^'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_TAGS = r'(html|header|head|body|footer|foot|title|section|div|nav|ol|ul|li|table|tr|th|td|h[1-6]|p|a|span|em)'
t_ID = r'\#[a-zA-Z_-]+[0-9]*'
t_CLASS = r'\.[a-zA-Z_-]+[0-9]*'
t_DIGIT = r'[0-9]+'
t_LETTER = r'[a-zA-Z]'
t_TEXT = r'[a-zA-Z0-9_-]+'
t_WHITESPACE = r'\s'
t_EOF = r'þ'


# The token class is used to generate the tokens. It formats the token information as type and value.

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()
            

# The lexer class analyzes the input text and looks for tokens as defined by the regular expressions. It then uses the Token class to create a token object.

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.currentToken = None

    def error(self):
        raise Exception('Error parsing input')

    def getNextToken(self):
        text = self.text

        if self.pos > len(text) - 1:
            return Token(EOF, None)

        
        # Each individual character in the input string gets checked using self.pos as the index. It uses the match() function from the 're' library to check whether or not the current character matches a regular expression. It then creates a token by assigning a type and value.
        
        currentChar = text[self.pos]

        if re.match(t_CHILD, currentChar):
            token = Token(CHILD, currentChar)

        elif re.match(t_TIMES, currentChar):
            token = Token(TIMES, currentChar)

        elif re.match(t_SIBLING, currentChar):
            token = Token(SIBLING, currentChar)

        elif re.match(t_POW, currentChar):
            token = Token(POW, currentChar) 
            
        elif re.match(t_LPAREN, currentChar):
            token = Token(LPAREN, currentChar)

        elif re.match(t_RPAREN, currentChar):
            token = Token(RPAREN, currentChar)

        elif re.match(t_LBRACE, currentChar):
            token = Token(LBRACE, currentChar)

        elif re.match(t_RBRACE, currentChar):
            token = Token(RBRACE, currentChar)

        elif re.match(t_DIGIT, currentChar):
            token = Token(DIGIT, currentChar)

        # For the next 3 conditions, currentChar gets stored in a variable 'val'. This is because it will check for the next character to see if it is anything other than an operator. If it is not an operator, that character value will be concatenated to the 'val' variable. When it finds that the next character is an operator, it checks 'val' to see if it matches the t_TAGS regex. If it does, then the type is 'TAGS'. If not, then it is a plain text/ID/Class.

        elif re.match(t_LETTER, currentChar):
            val = currentChar
            while self.pos+1 <= len(text) - 1:
                if re.match(t_TEXT, text[self.pos+1]) or re.match(t_WHITESPACE, text[self.pos+1]):
                    self.pos += 1
                    currentChar = text[self.pos]
                    val = val + currentChar
                else:
                    break
            if re.match(t_TAGS, val):
                token = Token(TAGS, val)
            else:
                token = Token(TEXT, val)

        elif currentChar == "#":
            val = currentChar
            while self.pos+1 <= len(text) - 1:
                if re.match(t_TEXT, text[self.pos+1]):
                    self.pos += 1
                    currentChar = text[self.pos]
                    val = val + currentChar
                else:
                    break
            token = Token(ID, val) 

        elif currentChar == ".":
            val = currentChar
            while self.pos+1 <= len(text) - 1:
                if re.match(t_TEXT, text[self.pos+1]):
                    self.pos += 1
                    currentChar = text[self.pos]
                    val = val + currentChar
                else:
                    break 
            token = Token(CLASS, val)

        # If the current character matches the symbol in t_EOF, then it is the end of the input string.
        elif re.match(t_EOF, currentChar):
            token = Token(EOF, currentChar)


        # After creating a token object, self.pos gets incremented so that the next time the function gets called, it checks the next position.

        # print("current token = " + token.type + ": " + token.value)
        self.pos += 1
        return token