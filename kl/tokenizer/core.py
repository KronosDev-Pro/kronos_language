from re import Pattern, compile


# ----- NUMERIC FORMAT -----
# Authorized char: 0 - 9
# "num_value" or 'num_value' or num_value
# --------------------------
NUMERIC_VALUE: Pattern = compile(r'(\"|\'|)[0-9]*(\"|\'|)')

# ----- ALPHA FORMAT -----
# Authorized char: a - Z 0 - 9 -_[]() space
# "num_value" or 'num_value' or num_value
# ------------------------
ALPHA_VALUE: Pattern = compile(r'(\"|\')[^\{\[\(][a-zA-Z0-9 \-\_\[\]\(\)]*[^\)\]\}](\"|\')')


# ----- VAR FORMAT -----
# Authorized char: a - Z 0 - 9 -_[]() space
# Contrainst: first char is between a - Z (inclusive)
# "num_value" or 'num_value' or num_value
# ------------------------
VAR_PATTERN: Pattern = compile(r'[a-zA-Z\_][a-zA-Z0-9\_]*[^\)\]\}](\:|\=|)')

TYPE_PARTTERN: Pattern = compile(r'((string|((char|c)|(\*char|\*c))|s)|(number|(int|integer|i)|(float|decimal|f))|(bytes|b)|((list|\[.*\])|(tuple|\(.*\))))')
