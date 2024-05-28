from tkinter import ttk
from tkinter import *
import sqlite3


class VentanaPrincipal:
    db = 'database/productos.db'
    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Produtos")
        self.ventana.resizable(1, 1)
        self.ventana.wm_iconbitmap('recursos/icon.ico')

        # Creacion del contenedor Frame principal
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto", font=('Calibri', 16, 'bold'))
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        #Creación de mensaje de error:
        self.mensaje = Label(frame, text='', fg='red')
        self.mensaje.grid(row=4, column=0, columnspan=2, sticky=W + E)

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=('Calibri', 13))
        self.etiqueta_nombre.grid(row=1, column=0)

        # Entry Nombre (caja de texto que recibira el nombre)
        self.nombre = Entry(frame, font=('Calibri', 13))
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ", font=('Calibri', 13))
        self.etiqueta_precio.grid(row=2, column=0)
        # Entry Precio (caja de texto que recibira el precio)
        self.precio = Entry(frame, font=('Calibri', 13))
        self.precio.grid(row=2, column=1)

        # Boton Agregar Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_agregar = ttk.Button(frame, text="Guardar Producto",
                                        command=self.add_producto, style='my.TButton')
        self.boton_agregar.grid(row=3, columnspan=2, sticky=W + E)

        # Mensaje informativo para el usuario
        self.mensaje = Label(text='', fg='red')
        self.mensaje.grid(row=3, column=0, columnspan=2, sticky=W + E)

        # Tabla de Productos
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabla.grid(row=4, column=0, columnspan=2)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)
        self.tabla.heading('#1', text='Precio', anchor=CENTER)
        self.get_productos()

        # Botones de Eliminar y Editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto, style='my.TButton')
        self.boton_eliminar.grid(row=5, column=0, sticky=W + E)
        self.boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto, style='my.TButton')
        self.boton_editar.grid(row=5, column=1, sticky=W + E)

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
            print(fila)
            self.tabla.insert('', 0, text=fila[1], values=fila[2])

    def validacion_nombre(self):
        return self.nombre.get().strip() != ""

    def validacion_precio(self):
        try:
            precio = float(self.precio.get())
            return precio > 0
        except ValueError:
            return False

    def add_producto(self):
        if not self.validacion_nombre():
            self.mensaje.config(text='El nombre es obligatorio y no puede estar vacío')
            return
        if not self.validacion_precio():
            self.mensaje.config(text='El precio es obligatorio y debe ser un número válido mayor que 0')
            return

        query = 'INSERT INTO producto VALUES(NULL, ?, ?)'
        parametros = (self.nombre.get(), self.precio.get())
        self.db_consulta(query, parametros)
        self.mensaje['text'] = 'Producto {} añadido con éxito'.format(self.nombre.get())
        self.nombre.delete(0, END)  # Borrar el campo nombre del formulario
        self.precio.delete(0, END)  # Borrar el campo precio del formulario

        self.get_productos()

    def del_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        # Comprobacion de que se seleccione un producto para poder eliminarlo
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        
        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?'  # Consulta SQL
        self.db_consulta(query, (nombre,))  # Ejecutar la consulta
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()  # Actualizar la tabla de productos

    def edit_producto(self):
        try:
            nombre = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            VentanaEditarProducto(self, nombre, precio, self.mensaje)
        except IndexError:
            self.mensaje['text'] = 'Por favor, seleccione un producto'

class VentanaEditarProducto:
    def __init__(self, ventana_principal, nombre, precio, mensaje):
        self.ventana_principal = ventana_principal
        self.nombre = nombre
        self.precio = precio
        self.mensaje = mensaje
        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Producto")

        # Creación del contenedor Frame para la edición del producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", font=('Calibri', 16, 'bold'))
        frame_ep.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Label y Entry para el Nombre antiguo (solo lectura)
        Label(frame_ep, text="Nombre antiguo: ", font=('Calibri', 13)).grid(row=1, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly', font=('Calibri', 13)).grid(row=1, column=1)

        # Label y Entry para el Nombre nuevo
        Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13)).grid(row=2, column=0)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=2, column=1)
        self.input_nombre_nuevo.focus()

        # Precio antiguo (solo lectura)
        Label(frame_ep, text="Precio antiguo: ", font=('Calibri', 13)).grid(row=3, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=precio), state='readonly', font=('Calibri', 13)).grid(row=3, column=1)

        # Precio nuevo
        Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13)).grid(row=4, column=0)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=4, column=1)

        # Botón Actualizar Producto
        ttk.Style().configure('my.TButton', font=('Calibri', 14, 'bold'))

        # Ejemplo de cómo creamos y configuramos el estilo en una sola línea
        ttk.Button(frame_ep, text="Actualizar Producto", style='my.TButton', command=self.actualizar).grid(row=5, columnspan=2, sticky=W + E)

    def actualizar(self):
        nuevo_nombre = self.input_nombre_nuevo.get() or self.nombre
        nuevo_precio = self.input_precio_nuevo.get() or self.precio
        if nuevo_nombre and nuevo_precio:
            query = 'UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ?'
            parametros = (nuevo_nombre, nuevo_precio, self.nombre)
            self.ventana_principal.db_consulta(query, parametros)
            self.mensaje['text'] = f'El producto {self.nombre} ha sido actualizado con éxito'
        else:
            self.mensaje['text'] = f'No se pudo actualizar el producto {self.nombre}'

        self.ventana_editar.destroy()
        self.ventana_principal.get_productos()

if __name__ == '__main__':
    root = Tk()
    app = VentanaPrincipal(root)
    root.mainloop()
