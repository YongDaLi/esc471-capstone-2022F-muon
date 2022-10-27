"""
Yong Da Li
Monday, October 17, 2022

quick and dirty script to plot the peak data
"""

from matplotlib import pyplot as plt

data = []

with open("peak_typical.txt", "r") as file:
    for row in file:
        a = row.strip("\n").strip(" ").split(" ")
        for elem in a:
            if elem != "":
                data.append(int(elem))

plt.plot(data)
plt.show()
