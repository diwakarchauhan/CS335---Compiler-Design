#------------------------------------
#modula_lexer1.1.py
#has to be run like this :

#   $python modula_lexer1.1.py directory/

#	This commands takes all the files in 
#	the test directory and executes the 
#	tokenizer for these files one by one

#	Output : 
#	A part of the output is on an sample run:
#	
#	LexToken(ID,'WriteSm',19,414)
#	
#	Here,
#		ID is the token type
#		WriteSm is the token lexeme	
#		19 is the line no. of the
#		414 is the position of the token from the start of the file 
#------------------------------------

import sys
import os
import glob
import ply.lex as lex

# List of token names.   This is always required
reserved = (
    'ARRAY','BEGIN','BY','CASE','CONST',
    'DEFINITION','DO','ELSE','ELSIF','END',
    'EXIT','EXCEPT','EXPORT','FINALLY','FOR','FORWARD',
    'FROM','IF','IMPLEMENTATION','IMPORT','LOOP',
    'MODULE','OF','PACKEDSET','POINTER',
    'PROCEDURE','QUALIFIED','RECORD','RETRY','REPEAT',
    'RETURN','SET','THEN','TO','TYPE','UNTIL','VAR','WHILE',
    'WITH',
    'ABS','BITSET','BOOLEAN','CARDINAL','CAP','CHR','CHAR',
    'COMPLEX','CMPLX','DEC','DISPOSE','EXCL','FALSE','FLOAT',
    'HALT','HIGH','IM','INC','INCL','INT','INTERRUPTIBLE',
    'INTEGER','LENGTH','LFLOAT','LONGCOMPLEX','LONGREAL','MAX',
    'MIN','NEW','NIL','ODD','ORD','PROC','PROTECTION','RE','REAL',
    'SIZE','TRUE','TRUNC','UNINTERRUPTIBLE','VAL','DIV',
    'MOD','REM','OR',
)
tokens = reserved + (
    'ID',		        #identifier
    'COLON',			#:
    'NUMBER',   
    'COMMA',	 		# ,
    'ELLIPSIS',			# ..
    'EQUALS',			# = ; can be part of type declaration
    'PERIOD',			# .
    'SEMICOLON',		# ;
    'LPAREN',			# (
    'RPAREN',			# )
    'LBRACKETS',   		# [ or (!
    'RBRACKETS',	
    'LBRACES',			# { or (:
    'RBRACES',		
    'BAR',			# |
    'PRAGMA',  			# pragma
    #'COMMENT',			# (* *) neglect comment

    'ASSIGN',
    'PLUS',			# plus (identity) and set union operator, string concatenation symbol
    'MINUS',
    'TIMES',
    'DIVIDE',
    'AND',
    'NOT',
    'NOT_EQUALS',
    'LESS',
    'GREATER',
    'LESS_EQUAL',
    'GREATER_EQUAL',
    'IN',
    'DEREFERENCE',
    'STRING',
    'CONST_CHAR',  		# we are not sure wether " ' " is used in any other context or not
                   		#for the time being we are capturing the semantics constant cahracters 'a' and 'z' in the statement A : ['a'..'z']
)

# Regular expression rules for simple tokens
t_COMMA     		= r','
t_ELLIPSIS  		= r'\.\.'
t_EQUALS    		= r'='
t_PERIOD    		= r'\.'
t_SEMICOLON 		= r';'
t_LPAREN    		= r'\('
t_RPAREN    		= r'\)'
t_LBRACES   		= r'\{'
t_RBRACES   		= r'\}'
t_LBRACKETS 		= r'\['
t_RBRACKETS 		= r'\]'
t_BAR	    		= r'\|'
t_PRAGMA	 	= r'<\*.*\*>'
#t_COMMENT		= r'\(\*(.|\n)*\*\)'

t_ASSIGN 		= r':='
t_PLUS 			= r'\+'
t_MINUS 		= r'-'
#t_OR 			= r'OR'
t_TIMES 		= r'\*'
t_DIVIDE 		= r'/'
#t_DIV 			= r'(DIV)'
#t_MOD 			= r'MOD'
#t_REM 			= r'REM'
t_AND 			= r'AND|&'
t_NOT 			= r'NOT|~'
t_NOT_EQUALS 		= r'\#|<>'
t_LESS 			= r'<'
t_GREATER 		= r'>'
t_LESS_EQUAL 		= r'<='
t_GREATER_EQUAL 	= r'>='
t_IN 			= r'IN'
t_DEREFERENCE 		= r'\^|\@'
t_STRING                = r'".*"|\'.*\''
t_COLON			= r':'
t_CONST_CHAR	        = r'\'[a-zA-Z]\''


# Identifiers and reserved words

reserved_map = { }
for r in reserved:
    reserved_map[r] = r
    
def t_ID(t):
    r'[A-Za-z][A-Za-z0-9]*'
    t.type = reserved_map.get(t.value,"ID")
    return t

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_comment(t):
	r'\(\*(.|\n)*?\*\)'
	t.lexer.lineno += t.value.count('\n')
	#print t.value
	
# Define a rule so we can track line numbers
def t_newline(t):
    r'\n'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t \r'

# Error handling rule
def t_error(t):
    print "Illegal character '%s' " % t.value[0]
    t.lexer.skip(1)

def raw_string(s):
    if isinstance(s, str):
        s = s.encode('string-escape')
    elif isinstance(s, unicode):
        s = s.encode('unicode-escape')
    return s

# Build the lexer
lexer = lex.lex()
directory = sys.argv[1]
listing = os.listdir(directory)
for filename in listing:
	print filename,"*******************************************"
	filename = directory + filename 
	a = open(filename,"r")
	p = a.read()
	data = p
	lexer.input(data)
	while True:
		tok = lexer.token()
		if not tok: 
			lexer.lineno = 1
			break      # No more input
		print tok
	a.close()
