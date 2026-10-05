from pypdf import PdfReader
import os
import re

chapter_list_path = (
    "/data/lab-python3/lab/projects/text_to_speach/tts/chapters_list.txt"
)

phoenix_project = PdfReader(
    "/data/lab-python3/lab/projects/text_to_speach/tts/The_Phoenix_Project00.pdf"
)

# pages 384
# from 15 untill 338
page = phoenix_project.pages


class Chapter:
    def __init__(self, chap=0):
        self.chap = chap

    def __call__(self):
        self.chap += 1
        return f"Chapter {self.chap}"


chaptering = Chapter()


def find_actual_text():
    chapters_list_index = []

    i = 0
    while i < len(phoenix_project.pages):
        extracted = page[i].extract_text()
        if "CHAPTER" in extracted:
            chapters_list_index.append(f"{chaptering.__call__()}: {i}")
        i += 1

    for i in chapters_list_index:
        with open("chapters_list.txt", "a") as cha:
            cha.write(f"{i}\n")
    print("Finished saving chapter list")


# make tuple from chapters_list.txt create a index from-to and pass it to extraction()
# so it would know where to begin and stop at
def indexes():
    indexes_l = []
    with open("chapters_list.txt", "r") as file:
        for line in file:
            s = line.split(":")
            page_nr = int(s[1].lstrip())
            indexes_l.append(page_nr)
        return indexes_l


def extract_text_into_file(beg, end, file_name):
    with open(file_name, "w") as chapterx:
        for i in range(beg, end):
            page_text = page[i].extract_text()
            chapterx.write(page_text)


ind_l = indexes()

for i in range(len(ind_l) - 1):
    a = ind_l[i]
    b = ind_l[i + 1]
    chap_num = i + 1
    file_name = f"Chapter_{chap_num}"

    print(f"Creating {file_name}: pages {a} to {b - 1}")
    extract_text_into_file(int(a), int(b), file_name)
