import sqlite3
from tkinter import ttk
from tkinter import *
from db import session
from models import Producto
import db
class VentanaPrincipal:
    db = 'database/productos.db'
    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1, 1)
        self.ventana.wm_iconbitmap('recursos/icon.ico')

        # Configuración de estilos:
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', background='#4CAF50', foreground='white', font=('Calibri', 13), borderwidth=1, focusthickness=3, focuscolor='none')
        style.map('TButton', background=[('active', '#45a049')])
        style.configure('TEntry', font=('Calibri', 13), padding=5)

        # Creación del contenedor Frame principal
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto", font=('Calibri', 16, 'bold'))
        frame.grid(row=0, column=0, columnspan=3, pady=20, padx=20, sticky=W + E)

        # Creación de mensaje de error:
        self.mensaje_error = Label(frame, text='', fg='red', bg='#f0f0f0')
        self.mensaje_error.grid(row=4, column=0, columnspan=2, sticky=W + E)

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=('Calibri', 13), bg='#f0f0f0')
        self.etiqueta_nombre.grid(row=1, column=0, padx=10, pady=5)

        # Entry Nombre
        self.nombre = Entry(frame, font=('Calibri', 13))
        self.nombre.focus()
        self.nombre.grid(row=1, column=1, padx=10, pady=5)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ", font=('Calibri', 13), bg='#f0f0f0')
        self.etiqueta_precio.grid(row=2, column=0, padx=10, pady=5)

        # Entry Precio
        self.precio = Entry(frame, font=('Calibri', 13))
        self.precio.grid(row=2, column=1, padx=10, pady=5)

        # Label Categoría
        self.etiqueta_categoria = Label(frame, text="Categoría: ", font=('Calibri', 13), bg='#f0f0f0')
        self.etiqueta_categoria.grid(row=3, column=0, padx=10, pady=5)

        # Combobox Categoría
        self.categorias = ["Electrónica", "Ropa", "Alimentos", "Hogar", "Libros", "Otros"]
        self.categoria = ttk.Combobox(frame, values=self.categorias, font=('Calibri', 13), state='readonly')
        self.categoria.grid(row=3, column=1, padx=10, pady=5)

        # Botón Agregar Producto
        self.boton_agregar = ttk.Button(frame, text="Guardar Producto", command=self.add_producto)
        self.boton_agregar.grid(row=4, columnspan=2, padx=10, pady=5, sticky=W + E)

        # Mensaje informativo para el usuario
        self.mensaje_confirmacion = Label(text='', fg='green', bg='#f0f0f0')
        self.mensaje_confirmacion.grid(row=5, column=0, columnspan=2, sticky=W + E)

        # Estilo de la tabla de Productos
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=("precio", "categoria"), style="mystyle.Treeview")
        self.tabla.grid(row=6, column=0, columnspan=2, padx=20, pady=20)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)
        self.tabla.heading('precio', text='Precio', anchor=CENTER)
        self.tabla.heading('categoria', text='Categoría', anchor=CENTER)
        self.get_productos()

        # Botones de Eliminar y Editar
        self.boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto)
        self.boton_eliminar.grid(row=7, column=0, padx=10, pady=10, sticky=W + E)
        self.boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto)
        self.boton_editar.grid(row=7, column=1, padx=10, pady=10, sticky=W + E)

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)
        query = 'SELECT * FROM producto ORDER BY nombre DESC'
        registros_db = self.db_consulta(query)

        for fila in registros_db:
            self.tabla.insert('', 0, text=fila[1], values=(fila[2], fila[3]))

    def validacion_nombre(self):
        return self.nombre.get().strip() != ""

    def validacion_precio(self):
        try:
            precio = float(self.precio.get())
            return precio > 0
        except ValueError:
            return False

    def validacion_categoria(self):
        return self.categoria.get() in self.categorias

    def add_producto(self):
        self.mensaje_error['text'] = ''
        if not self.validacion_nombre():
            self.mensaje_error.config(text='El nombre es obligatorio y no puede estar vacío')
            return
        if not self.validacion_precio():
            self.mensaje_error.config(text='El precio es obligatorio y debe ser un número válido mayor que 0')
            return
        if not self.validacion_categoria():
            self.mensaje_error.config(text='Debe seleccionar una categoría válida')
            return

        query = 'INSERT INTO producto (nombre, precio, categoria) VALUES (?, ?, ?)'
        parametros = (self.nombre.get(), self.precio.get(), self.categoria.get())
        self.db_consulta(query, parametros)
        self.mensaje_confirmacion['text'] = f'Producto {self.nombre.get()} añadido con éxito'
        self.nombre.delete(0, END)
        self.precio.delete(0, END)
        self.categoria.set('')

        self.get_productos()

    def del_producto(self):
        self.mensaje_confirmacion['text'] = ''
        self.mensaje_error['text'] = ''
        try:
            nombre = self.tabla.item(self.tabla.selection())['text']
        except IndexError:
            self.mensaje_error['text'] = 'Por favor, seleccione un producto'
            return

        query = 'DELETE FROM producto WHERE nombre = ?'
        self.db_consulta(query, (nombre,))
        self.mensaje_confirmacion['text'] = f'Producto {nombre} eliminado con éxito'
        self.get_productos()

    def edit_producto(self):
        self.mensaje_error['text'] = ''
        self.mensaje_confirmacion['text'] = ''
        try:
            nombre = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            categoria = self.tabla.item(self.tabla.selection())['values'][1]

            VentanaEditarProducto(self, nombre, precio, categoria)
        except IndexError:
            self.mensaje_error['text'] = 'Por favor, seleccione un producto'


class VentanaEditarProducto:
    def __init__(self, ventana_principal, nombre, precio, categoria):
        self.ventana_principal = ventana_principal
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Producto")

        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", font=('Calibri', 16, 'bold'), bg='#f0f0f0')
        frame_ep.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky=W + E)

        Label(frame_ep, text="Nombre antiguo: ", font=('Calibri', 13), bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=5)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly', font=('Calibri', 13)).grid(row=1, column=1, padx=10, pady=5)

        Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13), bg='#f0f0f0').grid(row=2, column=0, padx=10, pady=5)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=2, column=1, padx=10, pady=5)
        self.input_nombre_nuevo.focus()

        Label(frame_ep, text="Precio antiguo: ", font=('Calibri', 13), bg='#f0f0f0').grid(row=3, column=0, padx=10, pady=5)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=precio), state='readonly', font=('Calibri', 13)).grid(row=3, column=1, padx=10, pady=5)

        Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13), bg='#f0f0f0').grid(row=4, column=0, padx=10, pady=5)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=4, column=1, padx=10, pady=5)

        Label(frame_ep, text="Categoría antigua: ", font=('Calibri', 13), bg='#f0f0f0').grid(row=5, column=0, padx=10, pady=5)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=categoria), state='readonly', font=('Calibri', 13)).grid(row=5, column=1, padx=10, pady=5)

        Label(frame_ep, text="Categoría nueva: ", font=('Calibri', 13), bg='#f0f0f0').grid(row=6, column=0, padx=10, pady=5)
        self.input_categoria_nueva = ttk.Combobox(frame_ep, values=self.ventana_principal.categorias, font=('Calibri', 13), state='readonly')
        self.input_categoria_nueva.grid(row=6, column=1, padx=10, pady=5)

        ttk.Button(frame_ep, text="Actualizar Producto", command=self.actualizar).grid(row=7, columnspan=2, padx=10, pady=5, sticky=W + E)

    def actualizar(self):
        nuevo_nombre = self.input_nombre_nuevo.get() or self.nombre
        nuevo_precio = self.input_precio_nuevo.get() or self.precio
        nueva_categoria = self.input_categoria_nueva.get() or self.categoria

        if nuevo_nombre and nuevo_precio and nueva_categoria:
            query = 'UPDATE producto SET nombre = ?, precio = ?, categoria = ? WHERE nombre = ?'
            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, self.nombre)
            self.ventana_principal.db_consulta(query, parametros)
            self.ventana_principal.mensaje_confirmacion['text'] = f'El producto {self.nombre} ha sido actualizado con éxito'
        else:
            self.ventana_principal.mensaje_error['text'] = f'No se pudo actualizar el producto {self.nombre}'

        self.ventana_editar.destroy()
        self.ventana_principal.get_productos()



