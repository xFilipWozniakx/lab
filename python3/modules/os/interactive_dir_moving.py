# lets make litle script for interactive dir changing with python3 super simplyfied not sure if worth spending time on
import os

while True:
    print(f"current: {os.getcwd()}\n {os.listdir(path='.')}")
    choice = input("Where to?")
    if choice == "exit":
        quit()
    else:
        os.chdir(choice)
