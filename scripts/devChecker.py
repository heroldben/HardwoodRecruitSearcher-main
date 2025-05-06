from bs4 import BeautifulSoup
import requests

player = "http://onlinecollegebasketball.org/player/214216"
response = requests.get(player)

html_content = response.content
soup2 = BeautifulSoup(html_content, "html.parser")
table = soup2.find("table", class_="stats-table-medium_font")

positions = [(1, 35), (2, 35), (3, 35)]#, (4, 35)]
values = []
rows = table.find_all('tr')
for row_idx, col_idx in positions:
    cell = rows[row_idx].find_all('td')[col_idx]
    values.append(int(cell.get_text(strip=True)))

# Print the extracted values
print(values)
print(values[2] - values[0])