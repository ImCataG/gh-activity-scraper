import requests
from bs4 import BeautifulSoup
import sys
import shapes

# look for username in args, if there is none, ask for it

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    username = input("Enter your GitHub username: ")

response = requests.get(f"https://github.com/{username}")

if response.status_code == 200:
    html_content = response.text

else:
    print(f"Check that username. Status code: {response.status_code}")
    exit()

# only keep table with class "ContributionCalendar-grid"
soup = BeautifulSoup(html_content, "html.parser")
table = soup.find_all("div", class_="ContributionCalendar")[0]

# get all td with class "ContributionCalendar-day" and put them in a matrix
days = table.find_all("td", class_="ContributionCalendar-day")

# go through them in order, when data-ix = 0 go to new line in the matrix
matrix = []
row = []
for day in days:
    if day["data-ix"] == "0":
        matrix.append(row)
        row = []
    # put the data-level in the matrix
    row.append(day["data-level"])

# remove the first empty row
matrix.pop(0)

# add the last row
matrix.append(row)

# get largest width and height for shape in shapes
max_width = max([len(shape[0]) for shape in shapes.shapes])
max_height = max([len(shape) for shape in shapes.shapes])
maxwh = max(max_width, max_height)

class activity_matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.max_length = max([len(row) for row in matrix])
        for row in self.matrix:
            row.extend(["0"] * (self.max_length - len(row)))

        self.highlightmatrix = [['_' for _ in range(len(row))] for row in matrix]
        self.xlimit = len(matrix)
        self.ylimit = self.max_length
    
    def getValue(self, x, y):
        if x < 0 or y < 0 or x >= self.xlimit or y >= self.ylimit:
            return False
        return self.matrix[x][y] != "0"
    
    def checkShape(self, x, y, shape):
        for i in range(x, x + len(shape)):
            for j in range(y, y + len(shape[0])):
                # if ?, continue
                if shape[i - x][j - y] == "?":
                    continue
                # else check for it to be the same
                if shape[i - x][j - y] == "0" and self.getValue(i, j) != False:
                    return False
                
                if shape[i - x][j - y] == "1" and self.getValue(i, j) != True:
                    return False
        return True
    
    def findOccurences(self, shape):
        occurences = 0
        for x in range(-maxwh, self.xlimit):
            for y in range(-maxwh, self.ylimit):
                if self.checkShape(x, y, shape):
                    occurences += 1
                    # highlight the shape
                    for i in range(x, x + len(shape)):
                        for j in range(y, y + len(shape[0])):
                            if shape[i - x][j - y] == "1":
                                self.highlightmatrix[i][j] = '#'
        return occurences


activity = activity_matrix(matrix)
total = 0
for shape in shapes.shapes:

    occ = activity.findOccurences(shape)
    if occ > 0:
        total += occ
        # print shape without bloat
        # for row in shape:
        #     print(*row)
        
        # print(f"occurences: {occ}\n")

print(f"Total occurences: {total}")

# print the matrix with the shapes highlighted
for i in range(len(activity.highlightmatrix)):
    for j in range(len(activity.highlightmatrix[0])):
        print(activity.highlightmatrix[i][j], end="")
    print()