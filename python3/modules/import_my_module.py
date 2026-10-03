
# import my_module_sample
import my_module_sample as mms
# You can create an alias when you import a module, by using the as keyword:

# to spare memory i can import module partaly 
# import person_1 from my_module_sample
# and use it by its name f.ex 
# print(person_1["age"])

mms.greeting("Filip")
# module.function/object/variable to call it 
a = mms.person_1
for i in a.items():
    print(i)

# theres a lot of mudules already included into py3 libraries like:
import platform
x = platform.system()
print(x)

print(dir(platform))

print(dir(mms))

# dir() is very usefull module that allows you inspect functions and object of given library

