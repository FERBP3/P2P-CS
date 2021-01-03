import re
import json
import mariadb
import sys

class DICT_DAO:
    def __init__(self, rango):
        self.palabras = {}
        self.rango = rango
        self.cursor = None
        self.conn = None
        self.tabla = ""
        if re.search(rango, "a") is None:
            self.tabla = "palabras2"
        else:
            self.tabla = "palabras1"
        self.conect_to_db()

    def conect_to_db(self):
        try:
            self.conn = mariadb.connect(
            user="ferbpp",
            password="1234",
            host="localhost",
            port=3306,
            database="diccionario"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.cursor = self.conn.cursor()

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
        if self.exists_word(word):
            return "Error: la palabra ya existe"

        try:
            query = "INSERT INTO {} (palabra, significado) VALUES('{}','{}')".format(self.tabla, word, meaning)
            self.cursor.execute(query)
            self.conn.commit()
            return "Éxito"
        except mariadb.Error as e:
            print(f"Error: {e}")
            return "Error: Fallo en la base de datos"

    def list(self):
        try:
            query = f"SELECT * FROM {self.tabla}"
            self.cursor.execute(query)
            palabras = ""
            for palabra, significado in self.cursor:
                palabras += f"{palabra} : {significado}\n"
            return palabras
        except mariadb.Error as e:
            print(f"Error: {e}")
            return "Error: Fallo en la base de datos"

    def edit(self, word, new_meaning):
        if not self.word_in_range(word):
            return "RangeError"
        if not self.exists_word(word):
            return "Error: la palabra no existe"

        try:
            query = f"UPDATE {self.tabla} SET significado='{new_meaning}' WHERE palabra='{word}'"
            self.cursor.execute(query)
            self.conn.commit()
            return "Éxito"
        except mariadb.Error as e:
            print(f"Error: {e}")
            return "Error: Fallo en la base de datos"

    def exists_word(self, word):
        try:
            query = f"SELECT * FROM {self.tabla} WHERE palabra='{word}'"
            self.cursor.execute(query)
        except mariadb.Error as e:
            print(f"Error al buscar la palabra en la base de datos {e}")
            return True
        res = ""
        for palabra, significado in self.cursor:
            res += palabra

        if len(res) != 0:
            return True
        return False

    def word_in_range(self, word):
        if re.search(self.rango, word) is None:
            return False
        return True
