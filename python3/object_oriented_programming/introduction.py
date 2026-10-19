# Creation date: 2026-10-04 21:39 UTF

"""
Advantages of OOP
Provides a clear structure to programs
Makes code easier to maintain, reuse, and debug
Helps keep your code DRY (Don't Repeat Yourself)
Allows you to build reusable applications with less code
Tip: The DRY principle means you should avoid writing the same code more than once.
Move repeated code into functions or classes and reuse it.
"""

# in python almost everything is a object with its propereties and methods

# creation of class


class MyClass:
    x = 5


# creation of object from class MyClass
p1 = MyClass()
print(p1.x)
print(type(p1))

# del obj
del p1

# __init__ method is called every time new obj is created


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


p1 = Person("Filip", 30)
print(f"Obj prep 1:{p1.name} \nObj prep 2: {p1.age}")

"""
Creating class without __init__ not effisient
class Person:
  pass

p1 = Person()
p1.name = "Tobias"
p1.age = 25

print(p1.name)
print(p1.age)
"""

# You can also set default values for parameters in the __init__() method:


class Persona:
    def __init__(self, name="Guest", age=0):
        self.name = name
        self.age = age


p2 = Persona("Filip", 30)
default_persona = Persona()

print(default_persona.age, default_persona.name)

# self paramter:
# It does not have to be named self, you can call it whatever you like,
# but it has to be the first parameter of any method in the class:


class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print("Hello, my name is " + self.name)


p1 = Human("Filip", 32)

p1.greet()


class Person:
    def __init__(myobject, name, age):
        myobject.name = name
        myobject.age = age

    def greet(abc):
        print("Hello, my name is " + abc.name)


p1 = Person("Emil", 36)
p1.greet()

# i can declare as many arguments and methods within class with self as i want


class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def display_info(self):
        print(f"{self.year} {self.brand} {self.model}")


car1 = Car("Toyota", "Corolla", 2020)
car1.display_info()


class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello im {self.name}"

    def welcome(self):
        message = self.greet()
        print(message, "! Welcome to my website")


p1 = Person("Filip")
p1.welcome()

"""
Class Properties vs Object Properties
Properties defined inside __init__() belong to each object (instance properties).
Properties defined outside methods belong to the class itself (class properties) and are shared by all objects:
"""


class Person:
    species = "Human"  # Class property

    def __init__(self, name):
        self.name = name  # instance property


p1 = Person("Filip")
p2 = Person("Mark")

print(
    f"obj 1st: {p1.name} cl-prop: {p1.species}\nobj 2nd: {
        p2.name
    } cl-prop from 2nd obj: {p2.species}"
)

# When you modify a class property, it affects all objects:


class Person:
    lastname = ""

    def __init__(self, name):
        self.name = name


p1 = Person("Linus")
p2 = Person("Emil")

Person.lastname = "Refsnes"

print(p1.lastname)
print(p2.lastname)

# properities can be modified


class Person:
    def __init__(self, name):
        self.name = name


p1 = Person("Tobias")

p1.age = 25
p1.city = "Oslo"

print(p1.name)
print(p1.age)
print(p1.city)

# but lets try adding class property / it works too, but will make code hard to read
Person.new_prop = "some"
p2 = Person("John")
print(p2.new_prop)

# methods modifing properties


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name}, ({self.age})"

    def greet(self):
        return f"Hello im {self.name}"

    def welcome(self):
        message = self.greet()
        print(message, "! Welcome to my website")

    def celebrate_birthday(self, how_many_years):
        self.age += how_many_years
        print(f"Contratulations {self.name}, you became {self.age}")


p1 = Person("Filip", 30)
p1.celebrate_birthday(5)
print(p1.age)


# The __str__() method is a special method that controls what is returned when the object is printed:
print(p1)

# multiple methods


class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)
        print(f"Added: {song}")

    def remove_song(self, song):
        if song in self.songs:
            self.songs.remove(song)
            print(f"Removed: {song}")

    def show_songs(self):
        print(f"Playlist '{self.name}':")
        for song in self.songs:
            print(f"- {song}")


my_playlist = Playlist("Favorites")
my_playlist.add_song("Bohemian Rhapsody")
my_playlist.add_song("Stairway to Heaven")
my_playlist.show_songs()

# or i can delete methods from classes:
del Playlist.show_songs
