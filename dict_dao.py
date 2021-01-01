import re
import json

class DICT_DAO:
    def __init__(self, rango):
        self.palabras = {}
        self.rango = rango

    def exec_command(self, command):
        if command.startswith("@add") or command.startswith("@edit"):
            command = command.split(" ", 2)
            word = command[1]
            meaning = command[2]
            if command[0].startswith("@add"):
                return self.add(word, meaning)
            else:
                return self.edit(word, meaning)
        elif command.startswith("@list"):
            return self.list()
        return "Comando no valido"

    def add(self, word, meaning):
        if not self.word_in_range(word):
            return "RangeError"
        if self.palabras.get(word, None) is None:
            self.palabras[word] = meaning
            return "Éxito"
        else:
            return "Error: la palabra ya existe"

    def list(self):
        return json.dumps(self.palabras)

    def edit(self, word, new_meaning):
        if not self.word_in_range(word):
            return "RangeError"
        if self.palabras.get(word, None) is None:
            return "Error: No se puede editar, la palabra no existe"
        else:
            self.palabras[word] = new_meaning
            return "Éxito"

    def word_in_range(self, word):
        if re.search(self.rango, word) is None:
            return False
        return True

