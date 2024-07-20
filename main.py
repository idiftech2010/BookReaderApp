import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import sqlite3
import fitz  # PyMuPDF
from PIL import Image
import io

class BookReaderApp(App):
    def build(self):
        self.title = "Book Reader"
        self.conn = sqlite3.connect('books.db')
        self.create_db()
        return MainLayout()

    def create_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT,
                file_path TEXT
            )
        ''')
        self.conn.commit()

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Button(text="Add Book", on_press=self.add_book))
        self.add_widget(Button(text="View Books", on_press=self.view_books))

    def add_book(self, instance):
        add_layout = AddBookLayout()
        self.clear_widgets()
        self.add_widget(add_layout)

    def view_books(self, instance):
        books_layout = ViewBooksLayout()
        self.clear_widgets()
        self.add_widget(books_layout)

class AddBookLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(AddBookLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.title_input = TextInput(hint_text="Title")
        self.content_input = TextInput(hint_text="Content (Leave empty if uploading a file)")
        self.filechooser = FileChooserIconView()
        self.add_widget(self.title_input)
        self.add_widget(self.content_input)
        self.add_widget(self.filechooser)
        self.add_widget(Button(text="Save", on_press=self.save_book))

    def save_book(self, instance):
        title = self.title_input.text
        content = self.content_input.text
        file_path = self.filechooser.selection[0] if self.filechooser.selection else None

        if title and (content or file_path):
            conn = sqlite3.connect('books.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO books (title, content, file_path) VALUES (?, ?, ?)', (title, content, file_path))
            conn.commit()
            conn.close()
            App.get_running_app().root.clear_widgets()
            App.get_running_app().root.add_widget(MainLayout())
        else:
            # Handle error
            pass

class ViewBooksLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ViewBooksLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, title FROM books')
        books = cursor.fetchall()
        conn.close()
        for book in books:
            self.add_widget(Button(text=book[1], on_press=lambda instance, b=book: self.read_book(b)))

    def read_book(self, book):
        book_id = book[0]
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        cursor.execute('SELECT content, file_path FROM books WHERE id = ?', (book_id,))
        book = cursor.fetchone()
        conn.close()
        read_layout = ReadBookLayout(book[1], book[0])
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(read_layout)

class ReadBookLayout(BoxLayout):
    def __init__(self, file_path, content, **kwargs):
        super(ReadBookLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text=content))
        self.add_widget(Button(text="Previous Page", on_press=self.prev_page))
        self.add_widget(Button(text="Next Page", on_press=self.next_page))
        self.add_widget(Button(text="Zoom In", on_press=self.zoom_in))
        self.add_widget(Button(text="Zoom Out", on_press=self.zoom_out))

    def prev_page(self, instance):
        pass

    def next_page(self, instance):
        pass

    def zoom_in(self, instance):
        pass

    def zoom_out(self, instance):
        pass

if __name__ == '__main__':
    BookReaderApp().run()
