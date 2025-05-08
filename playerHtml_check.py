from bs4 import BeautifulSoup

# Open and read the HTML file
with open("player.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, "html.parser")  # or "lxml" if you prefer

# Find all <td> elements
infoList = soup.find_all("tr")[1:]

# Print contents of each <td>

for i in range(len(infoList)):
    print(int(infoList[i].find_all("td")[7].text))