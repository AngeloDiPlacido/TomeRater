from TomeRater import *

Tome_Rater = TomeRater()

#Create some books:
book1 = Tome_Rater.create_book("Society of Mind", 12345678)
novel1 = Tome_Rater.create_novel("Alice In Wonderland", "Lewis Carroll", 12345)
novel1.set_isbn(9781536831139)
book1.set_isbn(978153683113)

nonfiction1 = Tome_Rater.create_non_fiction("Automate the Boring Stuff", "Python", "beginner", 1929452)
nonfiction2 = Tome_Rater.create_non_fiction("Computing Machinery and Intelligence", "AI", "advanced", 11111938)
novel2 = Tome_Rater.create_novel("The Diamond Age", "Neal Stephenson", 10101010)
novel3 = Tome_Rater.create_novel("There Will Come Soft Rains", "Ray Bradbury", 10001000)

#Create users:
print("Create Users")
Tome_Rater.add_user("Alan Turing", "alan@turing.com")
Tome_Rater.add_user("David Marr", "david@computation.org")

#Add a user with three books already read:
Tome_Rater.add_user("Marvin Minsky", "marvin@mit.edu", user_books=[book1, novel1, nonfiction1])

#Add books to a user one by one, with ratings:
print("Add book to user")
Tome_Rater.add_book_to_user(book1, "alan@turing.com", 1)
Tome_Rater.add_book_to_user(novel1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction2, "alan@turing.com", 4)
Tome_Rater.add_book_to_user(novel3, "alan@turing.com", 1)

Tome_Rater.add_book_to_user(novel2, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "david@computation.org", 4)


#Uncomment these to test your functions:
Tome_Rater.print_catalog()
Tome_Rater.print_users()

print("Most positive user:")
print(Tome_Rater.most_positive_user())
print("Highest rated book:")
print(Tome_Rater.highest_rated_book())
print("Most read book:")
print(Tome_Rater.most_read_book())

"""
angelo = User("Angelo", "angelo@test.com")
kass = User("Kassandra", "kass@test.com")
print(angelo)
print(kass)
print(angelo.get_email())
print(kass.get_email())

angelo2 = User("Angelo", "angelo2@test.com")
print(angelo == angelo)
print(angelo == angelo2)

angelo2.change_email("angelo2@test.com")

print(angelo == angelo2)

book1 = Book("title1", "isbn1")
book2 = Book("title2", "isbn2", price=30.00)

print(book1 == book1)
print(book1 == book2)

print(book1.get_title())
print(book1.get_isbn())
print(book1.set_isbn("new_isbn1"))
print(book1.get_isbn())
print(book1.add_rating(None))
print(book1.add_rating(-1))
print(book1.add_rating(5))
print(book1.add_rating(1))
print(book1.ratings)
print(book1.add_rating(2))
print(book1.ratings)
print(book1.get_average_rating())

fiction1 = Fiction("fiction1", "fic1_auth", "fic_isbn1", price = 20.00)

print(fiction1)
print(fiction1.get_author())

nonfict1 = Non_Fiction("nonfict1", "nonfic1_subject1", "nonfict1 level", \
                       "nonfict_isbn1")
nonfict2 = Non_Fiction("nonfict2", "nonfic2_subject2", "nonfict2 level2", \
                       "nonfict_isbn2")

print(nonfict1)
print(nonfict1.get_subject())
print(nonfict1.get_level())
print(nonfict1 == nonfict2)
print(nonfict1 == nonfict1)

#ratings tests
kass.read_book(nonfict1)
kass.read_book(nonfict2, 1)
kass.get_average_rating()
kass.read_book(fiction1, 2)
kass.get_average_rating()

"""
# test TomeRater class

tomerater = TomeRater()

book1 = tomerater.create_book("book1", "isbn1", price = 40.00)
try:
    book1_dup = tomerater.create_book("book1_dup", "isbn2", price = 45.00)
except DuplicateBookISBN:
    print("ERROR: Book with ISBN isbn1 already exists!")

novel1 = tomerater.create_novel("Novel 1", "Author 1", "novel1 isbn")
nonfict1 = tomerater.create_non_fiction("Non-Fiction 1", "Math 1", "Level 1", \
                                        "non-fiction1 ibsn")
for book in Book.getinstances():
    print(book)

tomerater.add_book_to_user(book1, "angelo@test.com")

tomerater.add_user("Angelo", "angelo@test.com", \
                   [book1, novel1, nonfict1, book1_dup])
tomerater.add_user("Angelo DP", "angelodp@test.com", [novel1])
tomerater.add_user("test user 1", "angelo@test.edu", [book1])
tomerater.add_user("Angelo DP", "angelo@test.org", [book1])
tomerater.add_user("Dino", "dino@test.org", [book1, novel1])

tomerater.add_user("Kassandra", "kass@test.com")

tomerater.add_book_to_user(book1, "kass@test.com", 0)
tomerater.add_book_to_user(novel1, "kass@test.com", 1)
tomerater.add_book_to_user(nonfict1, "kass@test.com", 1)
tomerater.add_book_to_user(nonfict1, "angelo@test.com", 5)

tomerater.print_catalog()

tomerater.print_users()

print("Most read book: " + str(tomerater.most_read_book()))

print("\r\n***** Highest rated bool: " + str(tomerater.highest_rated_book()))

print("\r\n***** Testing most positive user")
print("Most positive user: " + str(tomerater.most_positive_user()))

print("\r\n***** Testing TomeRater __repr__ method")
print(tomerater)


print("\r\n***** Testing TomeRater get_n_most_read_books method")
print(tomerater.get_n_most_read_books(1))
print(tomerater.get_n_most_read_books(2))
print(tomerater.get_n_most_read_books(4))
print(tomerater.get_n_most_read_books(10))

print("\r\n***** Testing TomeRater get_n_most_prolific_readers method")
print(tomerater.get_n_most_prolific_readers(1))
print(tomerater.get_n_most_prolific_readers(2))
print(tomerater.get_n_most_prolific_readers(3))

print("\r\n***** Testing TomeRater get_n_most_expensive_books method")
print(tomerater.get_n_most_expensive_books(1))
print(tomerater.get_n_most_expensive_books(2))
print(tomerater.get_n_most_expensive_books(3))

print("\r\n***** Testing TomeRater get_worth_of_user method")
print(tomerater.get_worth_of_user("angelo@test.com"))
print(tomerater.get_worth_of_user("angelo2@test.com"))
print(tomerater.get_worth_of_user("kass@test.com"))


