import csv

i = 0
row_list = []
while i < 100:
 row_list = [["Hr", "Temperature", "Contribution"],
             [1, "Linus Torvalds", "Linux Kernel"],
             [2, "Tim Berners-Lee", "World Wide Web"],
             [3, "Guido van Rossum", "Python Programming"]]


with open('healt.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(row_list)