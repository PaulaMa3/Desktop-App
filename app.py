from tkinter import ttk
from tkinter import *
import sqlite3


class VentanaPrincipal:
    db = 'database/productos.db'

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1, 1)
        self.ventana.wm_iconbitmap('recursos/icon.ico')

        #Configuración de estilos:
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', background='#4CAF50', foreground='white', font=('Calibri', 13), borderwidth=1, focusthickness=3, focuscolor='none')
        style.map('TButton', background=[('active', '#45a049')])

        # Estilo para los botones
        style.configure('TButton', background='#4CAF50', foreground='white', font=('Calibri', 13), borderwidth=1,focusthickness=3, focuscolor='none')
        style.map('TButton', background=[('active', '#45a049')])

        # Estilo para las entradas
        style.configure('TEntry', font=('Calibri', 13), padding=5)

        # Creación del contenedor Frame principal
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto", font=('Calibri', 16, 'bold'), bg='#f0f0f0')
        frame.grid(row=0, column=0, columnspan=3, pady=20, padx=20, sticky=W+E)

        # Creación de mensaje de error:
        self.mensaje_error = Label(frame, text='', fg='red', bg='#f0f0f0')
        self.mensaje_error.grid(row=4, column=0, columnspan=2, sticky=W + E)

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=('Calibri', 13), bg='#f0f0f0')
        self.etiqueta_nombre.grid(row=1, column=0, padx=10, pady=5)

        # Entry Nombre (caja de texto que recibirá el nombre)
        self.nombre = Entry(frame, font=('Calibri', 13))
        self.nombre.focus()
        self.nombre.grid(row=1, column=1, padx=10, pady=5)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ", font=('Calibri', 13), bg='#f0f0f0')
        self.etiqueta_precio.grid(row=2, column=0, padx=10, pady=5)

        # Entry Precio (caja de texto que recibirá el precio)
        self.precio = Entry(frame, font=('Calibri', 13))
        self.precio.grid(row=2, column=1, padx=10, pady=5)

        # Botón Agregar Producto
        self.boton_agregar = ttk.Button(frame, text="Guardar Producto", command=self.add_producto, style='my.TButton')
        self.boton_agregar.grid(row=3, columnspan=2, padx=10, pady=5, sticky=W + E)

        # Mensaje informativo para el usuario
        self.mensaje_confirmacion = Label(text='', fg='green', bg='#f0f0f0')
        self.mensaje_confirmacion.grid(row=3, column=0, columnspan=2, sticky=W + E)

        # Estilo de la tabla de Productos
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabla.grid(row=4, column=0, columnspan=2, padx=20, pady=20)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)
        self.tabla.heading('#1', text='Precio', anchor=CENTER)
        self.get_productos()

        # Botones de Eliminar y Editar
        self.boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto, style='my.TButton')
        self.boton_eliminar.grid(row=5, column=0, padx=10, pady=10, sticky=W + E)
        self.boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto, style='my.TButton')
        self.boton_editar.grid(row=5, column=1, padx=10, pady=10, sticky=W + E)

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
            self.mensaje_error.config(text='El nombre es obligatorio y no puede estar vacío')
            return
        if not self.validacion_precio():
            self.mensaje_error.config(text='El precio es obligatorio y debe ser un número válido mayor que 0')
            return

        query = 'INSERT INTO producto VALUES(NULL, ?, ?)'
        parametros = (self.nombre.get(), self.precio.get())
        self.db_consulta(query, parametros)
        self.mensaje_confirmacion['text'] = 'Producto {} añadido con éxito'.format(self.nombre.get())
        self.nombre.delete(0, END)  # Borrar el campo nombre del formulario
        self.precio.delete(0, END)  # Borrar el campo precio del formulario

        self.get_productos()

    def del_producto(self):
        self.mensaje_confirmacion['text'] = ''  # Mensaje inicialmente vacío
        # Comprobación de que se seleccione un producto para poder eliminarlo
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje_error['text'] = 'Por favor, seleccione un producto'
            return

        self.mensaje_confirmacion['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?'  # Consulta SQL
        self.db_consulta(query, (nombre,))  # Ejecutar la consulta
        self.mensaje_confirmacion['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()  # Actualizar la tabla de productos

    def edit_producto(self):
        try:
            nombre = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            VentanaEditarProducto(self, nombre, precio, self.mensaje_confirmacion)
        except IndexError:
            self.mensaje_error['text'] = 'Por favor, seleccione un producto'


class VentanaEditarProducto:
    def __init__(self, ventana_principal, nombre, precio, mensaje):
        self.ventana_principal = ventana_principal
        self.nombre = nombre
        self.precio = precio
        self.mensaje = mensaje
        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Producto")

        # Creación del contenedor Frame para la edición del producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", font=('Calibri', 16, 'bold'), bg='#f0f0f0')
        frame_ep.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky=W+E)

        # Label y Entry para el Nombre antiguo (solo lectura)
        Label(frame_ep, text="Nombre antiguo: ", font=('Calibri', 13), bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=5)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly', font=('Calibri', 13)).grid(row=1, column=1, padx=10, pady=5)

        # Label y Entry para el Nombre nuevo
        Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13), bg='#f0f0f0').grid(row=2, column=0, padx=10, pady=5)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=2, column=1, padx=10, pady=5)
        self.input_nombre_nuevo.focus()

        # Precio antiguo (solo lectura)
        Label(frame_ep, text="Precio antiguo: ", font=('Calibri', 13), bg='#f0f0f0').grid(row=3, column=0, padx=10, pady=5)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=precio), state='readonly', font=('Calibri', 13)).grid(row=3, column=1, padx=10, pady=5)

        # Precio nuevo
        Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13), bg='#f0f0f0').grid(row=4, column=0, padx=10, pady=5)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=4, column=1, padx=10, pady=5)

        # Botón Actualizar Producto
        ttk.Button(frame_ep, text="Actualizar Producto", command=self.actualizar).grid(row=5, columnspan=2, padx=10, pady=5, sticky=W + E)

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
