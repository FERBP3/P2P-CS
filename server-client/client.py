from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
import socket
import threading
import sys

class App:
    def __init__(self, server_port):
        self.server_port = server_port
        self.server_conn = None
        self.window = Tk()
        self.window.title("Diccionario")
        self.window.geometry('1500x900')

        self.labelword = Label(self.window, text="Palabra")
        self.labelword.pack()
        self.word = Entry(self.window, width=30)
        self.word.pack()

        self.labelmean = Label(self.window, text="Significado")
        self.labelmean.pack()

        self.meaning = Entry(self.window, width=50)
        self.meaning.pack()

        self.monitor = scrolledtext.ScrolledText(self.window, width=120, height=40)
        self.monitor.pack()

        self.buttonAdd = Button(self.window, text="add", width=25, command=self.add)
        self.buttonAdd.pack()

        self.buttonEdit = Button(self.window, text="edit", width=25, command=self.edit)
        self.buttonEdit.pack()

        self.buttonList = Button(self.window, text="list", width=25, command=self.list_words)
        self.buttonList.pack()

        self.buttonExit = Button(self.window, text="salir", width=25, command=self.exit)
        self.buttonExit.pack()

    def init(self):
        self.window.mainloop()

    def add(self):
        new_word = self.word.get()
        new_meaning = self.meaning.get()
        if len(new_word)== 0 or len(new_meaning) == 0:
            messagebox.showinfo("Agrega palabra", "Error: alguno de los campos está vacío")
        else:
            self.server_conn.sendall(f"@add {new_word} {new_meaning}".encode())

    def edit(self):
        new_word = self.word.get()
        new_meaning = self.meaning.get()
        if len(new_word)== 0 or len(new_meaning) == 0:
            messagebox.showinfo("Editar palabra", "Error: alguno de los campos está vacío")
        else:
            self.server_conn.sendall(f"@edit {new_word} {new_meaning}".encode())

    def list_words(self):
        self.server_conn.sendall("@list".encode())

    def exit(self):
        self.server_conn.sendall("@exit".encode())
        self.server_conn.close()
        self.window.destroy()
        sys.exit(0)

    def espera_como_client(self):
        self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_conn.connect(('localhost', self.server_port))
        except Exception as e:
            print(e)
            return
        print("Conectado con el servidor")
        while True:
            try:
                data = self.server_conn.recv(1024).decode("utf-8")
                #print(data)
                if data.startswith("@exit"):
                    break
                self.monitor.delete(1.0, END)
                self.monitor.insert(INSERT, data)
            except Exception as e:
                print("Error recibiendo:",e)
                break

port = int(sys.argv[1])
my_app = App(port)
threading.Thread(target=my_app.espera_como_client).start()
my_app.init()

