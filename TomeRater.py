import re
import weakref
from operator import itemgetter

class DuplicateBookISBN(Exception):
    pass

class DuplicateUserEmail(Exception):
    pass

class InvalidUserEmail(Exception):
    pass

class User(object):

    _user_instances = set()

    def __init__(self, name, email):

        #save name and email in instance varables
        self.name = name
        self.email = email

        # dictionary of books and ratings
        # key is book object, value is the rating
        self.books = {}

        if not User.is_email_valid(self, email):
            raise InvalidUserEmail
        
        for user in User.getinstances():
            if user.get_email() == email:
                raise DuplicateUserEmail

        self._user_instances.add(weakref.ref(self))

    @classmethod
    def getinstances(cls):
        dead = set()
        for ref in cls._user_instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._user_instances -= dead

    # check email for validity.  return False if not valid and True if valid
    def is_email_valid(self, email):

        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        
        if match == None:
            return False
        last_four_chars = email[-4:]
        if not last_four_chars in [".com", ".edu", ".org"]:
            return False
        return True

    #return email of this this user
    def get_email(self):
        return self.email

    #change the email for this user
    def change_email(self, address):

        #first check if the new email is valid.  raise exception if not
        if not User.is_email_valid(self, address):
            raise InvalidUserEmail

        self.email = address
        output_str = "Updated email address for {name} user to {email}"
        print(output_str.format(name = self.name, \
                                email = self.email))

    #return representation of the user
    def __repr__(self):
        output_str = "User {name}, email: {email}, books read {number}"
        books_read = len(self.books)
        return output_str.format(name = self.name, email = self.email, \
                                 number = books_read)

    #method to test if self is equal to another user object
    def __eq__(self, other):
        if (self.name == other.name) and \
           (self.email == other.get_email()):
            return True
        else:
            return False

    #method to call when user has read a book.  takes optional rating
    def read_book(self, book, rating = None):
        self.books[book] = rating

    #return average rating of all books read and rated by this user
    def get_average_rating(self):
        total_of_rates = 0
        number_of_rates = 0

        #for every book read by this user total all their ratings
        for book, rating in self.books.items():
            if rating != None:
                total_of_rates += rating
                number_of_rates += 1

        #compute the average rating or set to 0 if no books rated
        if number_of_rates > 0:
            average_rating = total_of_rates / number_of_rates
        else:
            average_rating = 0

        return average_rating

    #return the number of books read by this user
    def get_number_of_books_read(self):
        return len(self.books)

    #returns the list of books read by this user
    def get_books_read(self):
        return list(self.books.keys())
    
    def __hash__(self):
        return hash((self.name, self.email))


class Book():

    _book_instances = set()
    
    def __init__(self, title, isbn, price = 0.0):
        self.title = title
        self.isbn = isbn
        self.ratings = []
        self.price = price
        
        for book in Book.getinstances():
            if book.get_isbn() == isbn:
                raise DuplicateBookISBN

        self._book_instances.add(weakref.ref(self))


    @classmethod
    def getinstances(cls):
        dead = set()
        for ref in cls._book_instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._book_instances -= dead

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def get_price(self):
        return self.price

    #set the isbn for the book.  raise exception if there already is a book
    #with the same isbn
    def set_isbn(self, isbn):
        for book in Book.getinstances():
            if book.get_isbn() == isbn:
                raise DuplicateBookISBN

        self.isbn = isbn
        output_str = "Updated ISBN for book \"{title}\" to {isbn}"
        print(output_str.format(title = self.title, \
                                isbn = self.isbn))

    #add a rating for a book.  rating must be integer between 0 and 5 inclusive
    def add_rating(self, rating):
        if rating in range(0,6):
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    #method to test if this book instance is the same as another book
    #books are the same if the title and isbn are the same
    def __eq__(self, other):
        if (self.title == other.get_title()) and \
           (self.isbn == other.get_isbn()):
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.title, self.isbn))

    #return the average ratings for this book.  If no rating yet receive
    #will return 0
    def get_average_rating(self):
        total_of_ratings = 0
        for rate in self.ratings:
            total_of_ratings += rate

        if total_of_ratings == 0:
            avg_rating = 0
        else:
            avg_rating = total_of_ratings / len(self.ratings)
        return avg_rating

    #return the string which represents this book
    def __repr__(self):
        ret_string = "{title} ISBN {isbn}"
        return ret_string.format(title = self.title, isbn = self.isbn)

#define a Fiction book which takes has an additional attribute called author
class Fiction(Book):
    def __init__(self, title, author, isbn, price = 0.0):
        super().__init__(title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        ret_string = "{title} by {author}"
        return ret_string.format(title = self.title, author = self.author)

#define a non fiction book which takes additional attributes subject and level
class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price = 0.0):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        ret_string = "{title}, a {level} manual on {subject}"
        return ret_string.format(title = self.title, level = self.level, \
                                 subject = self.subject)

class TomeRater():
    def __init__(self, name = "No Name"):
        self.users = {}
        self.books = {}
        self.name = name

    #define representation method which returns list of all users and books in
    #this instance of TomeRater
    def __repr__(self):

        if self.users:
            ret_str = "Users in " + self.name + " instance of TomeRater\r\n"
            for user in self.users.values():
                ret_str += str(user) + "\r\n"
        else:
            ret_str = "No users in " + self.name + " instance of  TomeRater\r\n"

        ret_str += "Books in " + self.name + " instance of TomeRater\r\n"

        if self.books:
            for book in self.books.keys():
                ret_str += str(book) + "\r\n"
        else:
            ret_str += "No books in " + self.name + " instance of TomeRater\r\n"

        return ret_str

    #compare this instance of TomeRater to another instance
    def __eq__(self, other):
        if self.users == other.users and \
           self.books == other.books and \
           self.name == other.name:
            return True
        else:
            return False

    #method to create a book.  returns the book instance
    def create_book(self, title, isbn, price = 0.0):
        book = Book(title, isbn, price = price)
        return book

    #method to create novel.  returns the novel instance
    def create_novel(self, title, author, isbn, price = 0.0):
        book = Fiction(title, author, isbn, price = price)
        return book

    #method to create a non fiction book.  returns the non fiction instance
    def create_non_fiction(self, title, subject, level, isbn, price = 0.0):
        book = Non_Fiction(title, subject, level, isbn, price = price)
        return book

    #method to a a book to a user with given email
    #inputs are book instance, email address of users, and optional rating
    def add_book_to_user(self, book, email, rating = None):
        if email in self.users.keys():
            self.users[email].read_book(book, rating)
            book.add_rating(rating)
            if book in self.books.keys():
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print("No user with email {email}".format(email=email))

    #method to add a user
    #inputs are the user name and email address as well a optional list of book
    #the user has read
    def add_user(self, name, email, user_books = None):

        try:
            user = User(name, email)
            self.users[email] = user
            if user_books != None:
                for book in user_books:
                    self.add_book_to_user(book, email)
        except DuplicateUserEmail:
            print("ERROR: user with email " + email + " already exists!")
        except InvalidUserEmail:
            print("ERROR invalid user email!")

    #method that prints all the books in this instance of TomeRater
    def print_catalog(self):

        for book in self.books:
            if isinstance(book, Book):
                print(book)
            else:
                print("NOT A BOOK!")


    #method that prints all the users in this instance of TomeRater
    def print_users(self):
        for email, user in self.users.items():
            if type(user) is User:
                print(user)
            else:
                print("NOT A USER!")

    #method to return the most read book in this instance of TomeRater
    def most_read_book(self):
        most_read_book = None
        number_of_reads = 0

        for book, reads in self.books.items():
            if reads > number_of_reads:
                number_of_reads = reads
                most_read_book = book

        return most_read_book

    #method to return the highest rated book in this instance of TomeRater
    #returns None if no books defined
    def highest_rated_book(self):

        highest_rating = 0
        highest_rated_book = None

        for book in self.books.keys():
            book_avg_rating = book.get_average_rating()
            if book_avg_rating > highest_rating:
                highest_rating = book_avg_rating
                highest_rated_book = book
        return highest_rated_book

    #return the user with the highest average rating
    #returns None if no users defined
    def most_positive_user(self):

        most_positive_rating = 0.0
        most_positive_user = None

        for user in self.users.values():
            user_average = user.get_average_rating()
            if user_average > most_positive_rating:
                most_positive_rating = user_average
                most_positive_user = user

        return most_positive_user

    #return the most read books in this instance of TomeRater
    #input is an integer that indicates how many most read books to return
    #returns list of book instances
    def get_n_most_read_books(self, n):
        most_read_books = []
        for book,reads in sorted(self.books.items(), key = itemgetter(1), \
                                 reverse = True):
            most_read_books.append(book)
        return most_read_books[:n]

    #return the most prolific readers in this instance of TomeRater
    #input is an integer that indicates how many users to return
    #returns list of user instances
    def get_n_most_prolific_readers(self, n):
        most_prolific_readers = []

        #form dictionary of users and number of books they have read
        users_to_books_read = {user: user.get_number_of_books_read() \
                               for user in self.users.values() }
        for user, reads in sorted(users_to_books_read.items(), \
                                  key = itemgetter(1), \
                                  reverse = True):
            most_prolific_readers.append(user)
            
        return most_prolific_readers[:n]

    #return list of most expensive books
    #input is an integer that indicates how many books to return
    #return list of book instances
    def get_n_most_expensive_books(self, n):
        books_prices = []

        #for dictionary of books and their prices
        book_prices = {book: book.get_price() \
                       for book in self.books.keys() \
                       if book.get_price() != None}

        print(book_prices)

        return sorted(book_prices.items(), \
                      key = itemgetter(1), \
                      reverse = True)[:n]

    #return value of books read by a particular user
    #input is the users email
    #returns total value of all books ready by this user
    #returns 0 if user with this email does not exist
    def get_worth_of_user(self, user_email):

        total_value = 0
        if user_email in self.users.keys():
            user = self.users[user_email]
            print(user)
            total_value = 0
            for book in user.get_books_read():
                total_value += book.get_price()
        else:
            print("No user with email {email}".format(email=user_email))
            total_value = 0

        return total_value

