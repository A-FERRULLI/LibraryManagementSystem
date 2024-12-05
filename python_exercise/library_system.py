from unidecode import unidecode
import os

class Book:
    def __init__(self, title: str, author: str) -> None:
        self.title = title
        self.author = author
        self.is_available = True
    
    def __str__(self) -> str:
        return f'"{self.title}" by {self.author} is{" not " if not self.is_available else " "}available'


class Library:
    def __init__(self) -> None:
        self.books: list[Book] = []
    
    def add_book(self, title: str, author: str) -> None:
        self.books.append(Book(title, author))
    
    def list_books(self) -> list[Book]:
        return self.books
    
    def load_books(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                line = lines[i].replace('\n', '').replace('\r', '').strip()
                title = author = None
                try: title, author, *_ = line.split(',')
                except Exception as e:
                    if title is None or title == '':
                        raise Exception(f'Missing title at line {i+1}')
                    elif author is None or author == '':
                        raise Exception(f'Missing author at line {i+1}')
                    else: raise e
                self.add_book(title.strip(), author.strip())
    
    def lend_book(self, book_title: str, student: 'Student') -> bool:
        book = self.search_books(book_title)[0]
        if book.is_available and book not in student.borrowed_books:
            student.borrowed_books.append(book)
            book.is_available = False
            return True
        else: return False
    
    def accept_return(self, book_title: str, student: 'Student') -> None:
        book = self.search_books(book_title)[0]
        if not book.is_available and book in student.borrowed_books:
            book.is_available = True
    
    def search_books(self, query: str) -> list[Book]:
        results: list[Book] = []
        for book in self.books:
            # Normalize to Lowercase and no accents
            title = unidecode(book.title.lower())
            author = unidecode(book.author.lower())
            query = unidecode(query.lower())
            if query in title or query in author: results.append(book)
        return results
    
    def save_books(self, file_path: str) -> None:
        with open(file_path, 'w+') as f:
            for book in self.books:
                f.write(f'{book.title},{book.author}\n')


class Student:
    def __init__(self, name: str) -> None:
        self.name = name
        self.borrowed_books: list[Book] = []
    
    def borrow_book(self, book_title: str, library: Library) -> None:
        if not library.lend_book(book_title, self): raise Exception('Cannot lend specified book')
    
    def return_book(self, book_title: str, library: Library) -> None:
        library.accept_return(book_title, self)


def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def run_library_system():
    LIBRARY = Library()
    booksPath = input('Enter the books list file path (default: "library_data.txt"): ')
    if booksPath == '': booksPath = 'library_data.txt'
    LIBRARY.load_books(booksPath)
    name = input('Please enter your name: ')
    STUDENT = Student(name)
    
    running = True
    while running:
        clear()
        
        print('*********************************')
        print('*                               *')
        print('*   Library Management System   *')
        print('*                               *')
        print('*********************************')
        print('')
        print(f'Welcome {name}')
        print('')
        print('What would you like to do ?')
        print('1 - View all books')
        print('2 - Search for a book')
        print('3 - Add a new book')
        print('4 - Borrow a book')
        print('5 - Return a book')
        print('6 - View borrowed books')
        print('q - Quit the program')
        choice = input('>>> ').lower()
        clear()
        match choice:
            case '1':
                print('**********************')
                print('*                    *')
                print('*   View all books   *')
                print('*                    *')
                print('**********************')
                print('')
                books = LIBRARY.list_books()
                for book in books: print(book)
                print('')
                input('Press Enter to return...')
            case '2':
                print('*************************')
                print('*                       *')
                print('*   Search for a book   *')
                print('*                       *')
                print('*************************')
                print('')
                print('Enter a book title/author to search: ')
                query = input('>>> ')
                books = LIBRARY.search_books(query)
                print('')
                for book in books: print(book)
                print('')
                input('Press Enter to return...')
            case '3':
                print('**********************')
                print('*                    *')
                print('*   Add a new book   *')
                print('*                    *')
                print('**********************')
                print('')
                print('Please enter the book details:')
                title = input('Title: ')
                author = input('Author: ')
                LIBRARY.add_book(title, author)
                print('')
                input('Press Enter to return...')
            case '4':
                print('*********************')
                print('*                   *')
                print('*   Borrow a book   *')
                print('*                   *')
                print('*********************')
                print('')
                print('Enter the title/author of the book you want to borrow:')
                print('(borrows first result automatically)')
                query = input('>>> ')
                STUDENT.borrow_book(query, LIBRARY)
                print('')
                input('Press Enter to return...')
            case '5':
                print('*********************')
                print('*                   *')
                print('*   Return a book   *')
                print('*                   *')
                print('*********************')
                print('')
                print('Enter the title/author of the book you want to return:')
                print('(returns first result automatically)')
                query = input('>>> ')
                STUDENT.return_book(query, LIBRARY)
                print('')
                input('Press Enter to return...')
            case '6':
                print('***************************')
                print('*                         *')
                print('*   View borrowed books   *')
                print('*                         *')
                print('***************************')
                print('')
                books = STUDENT.borrowed_books
                for book in books: print(book)
                print('')
                input('Press Enter to return...')
            case '7':
                print('********************')
                print('*                  *')
                print('*   Save Library   *')
                print('*                  *')
                print('********************')
                print('')
                LIBRARY.save_books(booksPath)
                print(f'Books saved to {booksPath}')
                print('')
                input('Press Enter to return...')
            case 'q':
                print('***************')
                print('*             *')
                print('*   Goddbye   *')
                print('*             *')
                print('***************')
                running = False
            case _:
                raise Exception('Unknown option')


if __name__ == '__main__': run_library_system()
