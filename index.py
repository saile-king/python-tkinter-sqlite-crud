from tkinter import ttk
from tkinter import *

import sqlite3

class Aplicacion:
    # connection dir property
    db_name = 'database.db'

    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.title('Registro de Aplicaciones')

        # Creating a Frame Container 
        frame = LabelFrame(self.wind, text = 'Registrar nueva App')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Nombre Input
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # Propietario Input
        Label(frame, text = 'Propietario: ').grid(row = 2, column = 0)
        self.propietario = Entry(frame)
        self.propietario.grid(row = 2, column = 1)

        # Descripcion Input
        Label(frame, text = 'Descripcion: ').grid(row = 3, column = 0)
        self.descripcion = Entry(frame)
        self.descripcion.grid(row = 3, column = 1)

        # Plataforma Input
        Label(frame, text = 'Plataforma: ').grid(row = 4, column = 0)
        self.plataforma = Entry(frame)
        self.plataforma.grid(row = 4, column = 1)

        # URL Input
        Label(frame, text = 'URL: ').grid(row = 5, column = 0)
        self.url = Entry(frame)
        self.url.grid(row = 5, column = 1)

        # Button Add Product 
        ttk.Button(frame, text = 'Guardar App', command = self.add_app).grid(row = 6, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 6, column = 0, columnspan = 5, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(height = 10, columns = 5)
        self.tree["columns"]=("#0","#1","#2","#3","#4")
        self.tree.column("#0", width=40, minwidth=40)
        self.tree.column("#1", width=100, minwidth=100)
        self.tree.column("#2", width=150, minwidth=150)
        self.tree.column("#3", width=270, minwidth=270)
        self.tree.column("#4", width=150, minwidth=200)
        self.tree.column("#5", width=200, minwidth=120)

        self.tree.grid(row = 7, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Id', anchor = CENTER)
        self.tree.heading('#1', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#2', text = 'Propietario', anchor = CENTER)
        self.tree.heading('#3', text = 'Descripcion', anchor = CENTER)
        self.tree.heading('#4', text = 'Plataforma', anchor = CENTER)
        self.tree.heading('#5', text = 'URL', anchor = CENTER)

        # Buttons
        ttk.Button(text = 'BORRAR', command = self.delete_app).grid(row = 8, column = 0, sticky = W + E)
        ttk.Button(text = 'EDITAR', command = self.edit_app).grid(row = 8, column = 1, sticky = W + E)
        
        
        # Filling the Rows
        self.get_apps()

    # Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get Products from Database
    def get_apps(self):
        # cleaning Table 
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM app ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[0], values = (row[1],row[2],row[3],row[4],row[5]))

    # User Input Validation
    def validation(self):
        return len(self.name.get()) != 0 and len(self.propietario.get()) != 0 and len(self.descripcion.get()) != 0 and len(self.plataforma.get()) != 0 and len(self.url.get()) != 0

    def add_app(self):
        if self.validation():
            query = 'INSERT INTO app VALUES(NULL, ?, ?, ?, ?, ?)'
            parameters =  (self.name.get(), self.propietario.get(), self.descripcion.get(), self.plataforma.get(), self.url.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Apps {} Añadida Exitosamente'.format(self.name.get())
            self.name.delete(0, END)
            self.propietario.delete(0, END)
            self.descripcion.delete(0, END)
            self.plataforma.delete(0, END)
            self.url.delete(0, END)
        else:
            self.message['text'] = 'Todos los campos son requeridos'
        self.get_apps()

    def delete_app(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor, seleccionar un Registro'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['values'][0]
        query = 'DELETE FROM app WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Registro {} borrado Exitosamente'.format(name)
        self.get_apps()


    def edit_app(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor, seleccionar Registro'
            return 
        ide =  self.tree.item(self.tree.selection())['text']
        name = self.tree.item(self.tree.selection())['values'][0]
        old_propietario = self.tree.item(self.tree.selection())['values'][1]
        old_descripcion = self.tree.item(self.tree.selection())['values'][2]
        old_plataforma = self.tree.item(self.tree.selection())['values'][3]
        old_url = self.tree.item(self.tree.selection())['values'][4]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar App'
        # Id
        Label(self.edit_wind, text = 'ID:').grid(row = 0, column = 1)
        old_id = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = ide), state = 'readonly')
        old_id.grid(row = 0, column = 2)
        # New Name
        Label(self.edit_wind, text = 'New Nombre:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name))
        new_name.grid(row = 1, column = 2)
        # New Propietario
        Label(self.edit_wind, text = 'New Propietario:').grid(row = 2, column = 1)
        new_propietario= Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_propietario))
        new_propietario.grid(row = 2, column = 2)
        # New Descripcion
        Label(self.edit_wind, text = 'New Descripcion:').grid(row = 3, column = 1)
        new_descripcion= Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_descripcion))
        new_descripcion.grid(row = 3, column = 2)
        # New plataforma
        Label(self.edit_wind, text = 'New Plataforma:').grid(row = 4, column = 1)
        new_plataforma= Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_plataforma))
        new_plataforma.grid(row = 4, column = 2)
        # New url
        Label(self.edit_wind, text = 'New URL:').grid(row = 5, column = 1)
        new_url= Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_url))
        new_url.grid(row = 5, column = 2)

        Button(self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records(new_name.get(), new_propietario.get(), new_descripcion.get(), new_plataforma.get(), new_url.get(), ide)).grid(row = 6, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, new_propietario, new_descripcion, new_plataforma, new_url, ide):
        query = 'UPDATE app SET name = ?, propietario = ?, descripcion = ?, plataforma = ?, url = ? WHERE id = ?'
        #parameters = (new_name, new_propietario, new_descripcion, new_plataforma, new_url, ide)
        self.run_query(query, (new_name, new_propietario, new_descripcion, new_plataforma, new_url, ide ))
        #self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Registro {} actualizado exito'.format(new_name)
        self.get_apps()

    
if __name__ == '__main__':
    window = Tk()
    application = Aplicacion(window)
    window.mainloop()