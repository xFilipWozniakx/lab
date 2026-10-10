main_dict = {}
secondary_dict = {
    "litle": {"name": "some", "lname": "somesome"},
    "litle_2": {"name": "some", "lname": "somesome"},
    "litle_3": {"name": "some", "lname": "somesome"},
}
third_dict = {
    "litle": {"name": "some", "lname": "somesome"},
    "litle_2": {"name": "some", "lname": "somesome"},
    "litle_3": {"name": "some", "lname": "somesome"},
    "litle_4": {"name": "some", "lname": "somesome"}
}

# for key,value in secondary_dict.items():
#     main_dict[key] = value
# print(main_dict)
to_request = {}

for key in third_dict:
    if key not in secondary_dict.keys():
        main_dict[key] = third_dict[key]

print(main_dict)

