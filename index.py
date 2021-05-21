from sqlite3.dbapi2 import Row, connect
from tkinter import ttk
from tkinter import *
import sqlite3

class Product:

    db_name = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Products Application')

        # Creating a Frame Container
        frame = LabelFrame(self.wind, text = 'Register A new Product')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Name Input
        Label(frame, text='Name: ').grid(row=1,column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1,column=1)

        # Price Input
        Label(frame, text='Price: ').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2,column=1)

        # Buttom Add Product
        ttk.Button(frame, text='Save product', command=self.add_product).grid(row=3,columnspan=2,sticky= W + E)

        # Output Messages
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=2, sticky= W+ E)

        # Table
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0,columnspan=2)
        self.tree.heading('#0', text = 'Name', anchor=CENTER)
        self.tree.heading('#1', text='Price', anchor=CENTER )

        # Buttoms
        ttk.Button(text = 'DELETE', command=self.delete_product).grid(row = 5, column=0, sticky=W+E)
        ttk.Button(text = 'EDIT', command=self.edit_product).grid(row = 5, column=1, sticky=W+E)

        # Filling the Row
        self.get_products()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def get_products(self):
        # Cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Quering Data
        query = 'SELECT * FROM Product ORDER BY Name DESC'
        db_rows = self.run_query(query)
        # Filling Data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values=row[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO Product VALUES(NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Product {} Added Successfully'.format(self.name.get())
            self.name.delete(0,END)
            self.price.delete(0,END)
        else:
            self.message['text'] = 'Name and Price are Required'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please Select a Record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM Product WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} Deleted Successfully'.format(name)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please Select a Record'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit.wind.title = 'Edit Product'

        #Old Name
        Label(self.edit_wind, text = 'Old Name: ').grid(row = 0, column=1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=name), state='readonly').grid(row=0,column=2)
        #New Name
        Label(self.edit_wind, [text = 'New Name']).grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1,column=2)

if __name__ == '__main__':
    window = Tk()   
    application = Product(window)
    window.mainloop()