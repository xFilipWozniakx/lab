# lets make litle script for interactive dir changing with python3 super simplyfied not sure if worth spending time on
import os
import sys


def explorer():
    while True:
        print(f"current: {os.getcwd()}\n {os.listdir(path='.')}")
        choice = input("Where to?\n")
        if choice == "exit":
            sys.exit()
        elif os.path.isdir(choice):
            os.chdir(choice)
        elif os.path.isfile(choice):
            return os.path.abspath(choice)
        else:
            print("Path doesnt exist")
