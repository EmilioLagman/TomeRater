class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("{name}'s e-mail address has been updated".format(name=self.name))

    def __repr__(self):
        return "User {name}, email: {email}, books read: {books_read}".format(name=self.name, email=self.email, books_read= self.books)

    def __eq__(self, other):
        if self.name == other.name and self.email == other.email:
            return True
        else:
            return False

    def read_book(self, book, rating=None):
        self.books[book] = rating
        
    def get_average_rating(self):
        total_rating = 0
        for book, rating in self.books.items():
            if rating != None:
                total_rating += rating
        return total_rating / len(self.books)

    def __hash__(self):
            return hash((self.name, self.email))

class Book:
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []
                    
    def get_title(self):
        return self.title
    
    def get_isbn(self):
        return self.isbn
    
    def set_isbn(self, new_isbn):
        self.isbn = new_isbn     
        print("{title} ISBN has been updated".format(title=self.title))

    def add_rating(self, rating):
        if rating >= 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def __eq__(self, other):
        if self.title == other_title and self.isbn == other.isbn:
            return True
        else:
            return False

    def get_average_rating(self):
        total_rating = 0
        for rating in self.ratings:
            total_rating += rating

        return total_rating / len(self.ratings)

    def __repr__(self):
        return "{title} and {isbn}".format(title= self.title, isbn= self.isbn)

    def __hash__(self):
        return hash((self.title, self.isbn))

class Fiction(Book):
    def __init__(self, title, isbn, author):
        super().__init__(title, isbn)
        self.author = author
    
    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author} ".format(title=self.title, author=self.author, isbn=self.isbn)

class Non_Fiction(Book):
    def __init__(self, title, isbn, subject, level):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level
    
    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)

class TomeRater:
    def __init__(self):
        self.users = {}
        self.books = {}
        self.created_isbns = []

    def create_book(self, title, isbn):
        if isbn in self.created_isbns:
            print("Book Already Exists!")
        else:
            self.created_isbns.append(isbn)
            return Book(title, isbn)
        
    def create_novel(self, title, author, isbn):
        if isbn in self.created_isbns:
            print("Book Already Exists!")
        else:
            self.created_isbns.append(isbn)
            return Fiction(title, isbn, author)

    def create_non_fiction(self, title, subject, level, isbn):
        if isbn in self.created_isbns:
            print("Book Already Exists!")
        else:
            self.created_isbns.append(isbn)
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        try:
            if email in self.users:
                self.users[email].read_book(book, rating)
                if rating != None:
                    book.add_rating(rating)
                if book not in self.books:
                    self.books[book] = 1
                else:
                    self.books[book] += 1
        except KeyError:
            print("No user with email {email}!".format(email= email))

    def add_user(self, name, email, user_books=None):
        valid_domains = [".com", ".edu", ".org"]
        if "@" not in email:
            print("Invalid Email!")
        elif not any(domain in email for domain in valid_domains):
            print("Invalid Domain!")
        elif email in self.users:
            print("User Already Exists!")
        else:
            self.users[email] = User(name, email)
            if user_books != None:
                for book in user_books:
                    TomeRater.add_book_to_user(self, book, email)

    def print_catalog(self):
        for book in self.books:
            print(book)
    
    def print_users(self):
        for user in self.users:
            print(user)
    
    def most_read_book(self):
        total_read = 0
        most_read_book = None
        for book, read in self.books.items():
             if read > total_read:
                total_read = read
                most_read_book = book
        return most_read_book
    
    def highest_rated_book(self):
        highest_rating = 0
        highest_rated_book = None
        for book in self.books:
           if book.get_average_rating() > highest_rating:
               highest_rating = book.get_average_rating()
               highest_rated_book = book
        return highest_rated_book

    def most_positive_user(self):
        highest_rating = 0
        most_positive_user = None
        for user in self.users.values():
           if user.get_average_rating() > highest_rating:
               highest_rating = user.get_average_rating()
               most_positive_user = user
        return most_positive_user

Tome_Rater = TomeRater()

#Create some books:
book1 = Tome_Rater.create_book("Society of Mind", 12345678)
book2 = Tome_Rater.create_book("Society of Mind", 12345678) #Book ISBN already exists Test
novel1 = Tome_Rater.create_novel("Alice In Wonderland", "Lewis Carroll", 12345)
novel1.set_isbn(9781536831139)
nonfiction1 = Tome_Rater.create_non_fiction("Automate the Boring Stuff", "Python", "beginner", 1929452)
nonfiction2 = Tome_Rater.create_non_fiction("Computing Machinery and Intelligence", "AI", "advanced", 11111938)
novel2 = Tome_Rater.create_novel("The Diamond Age", "Neal Stephenson", 10101010)
novel3 = Tome_Rater.create_novel("There Will Come Soft Rains", "Ray Bradbury", 10001000)

#Create users:
Tome_Rater.add_user("Alan Turing", "alan@turing.com")
Tome_Rater.add_user("David Marr", "david@computation.org")
Tome_Rater.add_user("Alan Turing", "alan@turing.com")  #User already exists Test

#Invalid user addition Test:
Tome_Rater.add_user("Lara Croft ", "lcroftcodeacademy.com") #Invalid email missing @
Tome_Rater.add_user("Emilio Lagman", "elagman@codeacademy.ca") #Invalid domain

#Add a user with three books already read:
Tome_Rater.add_user("Marvin Minsky", "marvin@mit.edu", user_books=[book1, novel1, nonfiction1])

#Add books to a user one by one, with ratings:
Tome_Rater.add_book_to_user(book1, "alan@turing.com", 1)
Tome_Rater.add_book_to_user(novel1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction2, "alan@turing.com", 2)
Tome_Rater.add_book_to_user(novel3, "alan@turing.com", 1)

Tome_Rater.add_book_to_user(novel2, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "david@computation.org", 4)

#Uncomment these to test your functions:
Tome_Rater.print_catalog()
Tome_Rater.print_users()
print(Tome_Rater.books)

print()
print("Most positive user:")
print(Tome_Rater.most_positive_user())
print()
print("Highest rated book:")
print(Tome_Rater.highest_rated_book())
print()
print("Most read book:")
print(Tome_Rater.most_read_book())