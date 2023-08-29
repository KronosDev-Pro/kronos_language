from os import path, listdir

LIST_VALID_GENERATOR: list[str] = [element for element in listdir(__path__[0]) if path.isdir(path.join(__path__[0], element)) and element[0] not in ('.', '_') and element != 'template']
