from tkinter import Tk
from view import VentanaPrincipal
from db import init_db

def main():
    init_db()
    root = Tk()
    app = VentanaPrincipal(root)
    root.mainloop()

if __name__ == '__main__':
    main()
