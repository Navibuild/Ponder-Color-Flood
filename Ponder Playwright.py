#Arnav Bal
#Ponder Club Color Flood solver using various methods

#Imports:

import playwright
from time import sleep
from playwright.sync_api import sync_playwright
import cv2
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import os
from collections import Counter
from collections import deque

#Color Match iniialize:
COLORS = {
    'Teal':   (91, 191, 186),
    'Lavender': (201, 187, 222),
    'Blue':   (145, 178, 209),
    'Amber': (236, 176, 97),
    'Olive':  (184, 194, 108),
}
_NAMES = list(COLORS)
_REFS = np.array([COLORS[n] for n in _NAMES], dtype=np.int32)

#Initializing the color grid:
rows = 10
cols = 10
default_string = ""
cols_array = [[default_string for _ in range(cols)] for _ in range(rows)]
chain_arr = [(0,0)]
freq_color = ""
move_count = 0

#Main:
os.chdir('C:\\Users\\arnav\\OneDrive\\Desktop\\Projects\\Ponder Color Flood')

#Playwright inspector:
#python -m playwright codegen https://www.ponderclub.co/color-flood

#Initializing the page for the screenshot:
with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    page = browser.new_page(viewport={"height":1080, "width": 1720})
    page.goto("https://www.ponderclub.co/color-flood")
    sleep(0.5)
    page.get_by_role("button", name="Close").click()

    #Positional debugging to find the bounding box of the How to play button
    #htb_size = how_to_button.bounding_box()
    #height = htb_size['height']
    #width = htb_size["width"]
    #print (height)
    #print(width)

    #how_to_button.click()
    sleep(0.5)
    #how_to_button.click(position={"x": 200, "y": 200})


#Taking the screenshot:
    #page.wait_for_timeout(1000)
    page.locator("div.MuiBox-root.css-1qwe623").screenshot(path = "color_grid.png")
    page.wait_for_timeout(2000)
    
#Finding the size of the image
image = cv2.imread('color_grid.png')
dimensions = image.shape
height = dimensions[0]
width = dimensions[1]

#Editing the image down to size: i no longer need to crop the image down as the cssSelector for this exact class is availaible
#and isnt hidden
#cropped_img = image[168:(height-113),400:(width-400)]

#cv2.imwrite('cropped_grid.png',cropped_img)

#Finding the size of the cropped image
#cr_image = cv2.imread("cropped_grid.png")


cr_image = cv2.imread("color_grid.png")
dimensions = cr_image.shape\
#Old Css code from when I still needed to crop the image because the div was nested too deep.
#cr_height = dimensions[0]
#cr_width = dimensions[1]

#Extracting the Color of the cells and converting it into a 2x2 array

#Function to find the pixels of the squares in the grid for testing purposes:
def image_pix_text():
    #img = cv2.imread("cropped_grid.png")
    img = cv2.imread("color_grid.png")
    img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    plt.figure()
    plt.imshow(img_rgb)
    plt.show()

#Function that returns the color name given the rgb value:
def rgb_to_color(pixel):
    d = np.sum((_REFS - np.array(pixel, dtype=np.int32)) ** 2, axis=1)
    return _NAMES[int(np.argmin(d))]

#Takes the pixel coordinates of the middle of each square then uses return_rgb to convert it to rgb values then converts
#those values into colors using rgb_to_color. Lastly it stores this list of colors into an array from which we can use algorithms
#to find the optimal solution:
def grid_to_array(path="color_grid.png", rows=10, cols=10):
    img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
    h, w = img.shape[:2]
    ch, cw = h / rows, w / cols
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            y, x = int((r + 0.5) * ch), int((c + 0.5) * cw)
            patch = img[y-3:y+4, x-3:x+4].reshape(-1, 3)
            row.append(rgb_to_color(np.median(patch, axis=0)))
        grid.append(row)
    return grid

#Check if adjacent cells have the same color and if so adding the coordinates to the chain arr:
def adj_color_chain(array):
    for i in range(len(array)):
        if((cols_array[int((array[i])[0])][int((array[i])[1])]) == cols_array[0][0]):
            if((((array[i][0],array[i][1])) not in chain_arr) and (0 <= (array[i])[0] < len(cols_array)) and (0 <= (array[i])[1] < len(cols_array))):
                chain_arr.append((array[i][0],array[i][1]))
                #print(chain_arr)

#Forms the chain of similar colors
def chain_form():
    x = 0
    cal = 1
    while x < cal:
        adj_color_chain(adjacency(chain_arr[x][0],chain_arr[x][1]))
        cal = len(chain_arr)
        x+=1

#Return list of adjacent cells to the whole chain:
def adj_chain(array):
    cells_adj_chain = []
    for item in array:
        adjacent_to_current_cells = adjacency(item[0],item[1])
        for item in chain_arr:
            try:
                adjacent_to_current_cells.remove(item)
            except:
                pass
        for x in adjacent_to_current_cells:
            if ((x not in cells_adj_chain) and (0 <= x[0] < len(cols_array)) and (0 <= x[1] < len(cols_array))):
                cells_adj_chain.append(x)
    return cells_adj_chain

#Checking the color of each of the adjacent cells and finding the most common one or using random:
def popular_color():
    curr_color = cols_array[0][0]
    color_freq = []
    chain_form()
    adjacent_cells = adj_chain(chain_arr)
    colors_array = []
    for item in (adjacent_cells):
        colors_array.append(cols_array[item[0]][item[1]])
    color_counter = Counter(colors_array)
    for string, count in color_counter.items():
        color_freq.append([string,count])
    return (highest_freq_color(color_freq))

#Method to find the highest frequency number given a mixed 2d list:
def highest_freq_color(array):
    global freq_color
    global_max = float('-inf')
    for x in range(len(array)):
        for item in array[x]:
#            if isinstance(item, str):
#                freq_color = item
            if isinstance(item, int):
                if item > global_max:
                    global_max = item
                    freq_color = array[x][0]
    return ([global_max,freq_color])

#Code to replace all cells being refered by chain_arr to the color outputted by popular_color()
def color_shift():
    global freq_color
    #print(freq_color)
    freq_color = popular_color()[1]
    for item in (chain_arr):
        cols_array[item[0]][item[1]] = freq_color

#For loop to check if all squares are the same color:
def check(two_d_list):
    flattened_list = [s for sublist in two_d_list for s in sublist]
    return len(set(flattened_list)) == 1

#Grid format to test where the pixels line up for the middle of the square
#image_pix_text()

#Printing the array in a readable format for testing
#for row in cols_array:
    #print(row)

#Attempting to solve the flood it game using chain theory to choose the most populat color adjacent to the current chain of same color
def chain_theory():
    cols_array[:] = grid_to_array()
    global move_count
    while not (check(cols_array)):
        color_shift()
        move_count +=1
    print("Total moves used for popular chain algorithm: " + str(move_count))

#New adjacency check for region conversion
def adjacency(a, b, rows=10, cols=10):
    candidates = [(a-1, b), (a+1, b), (a, b-1), (a, b+1)]
    return [(r, c) for r, c in candidates if 0 <= r < rows and 0 <= c < cols]

def find_regions(grid):
    """
    Collapse a 2D grid of colors into connected regions.

    grid: list of lists, grid[row][col] = color string

    Returns: dict mapping region_index -> {'color': str, 'cells': set of (row, col)}
    """
    rows, cols = len(grid), len(grid[0])
    visited = set()
    regions = {}
    next_index = 0

    for r in range(rows):
        for c in range(cols):
            if (r, c) in visited:
                continue

            tempset = set()
            visited.add((r, c))
            tempset.add((r, c))
            search_list = deque([(r, c)])

            while search_list:
                current = search_list.popleft()
                for x in adjacency(current[0], current[1]):
                    if x not in visited:
                        if grid[current[0]][current[1]] == grid[x[0]][x[1]]:
                            tempset.add(x)
                            visited.add(x)
                            search_list.append(x)

            regions[next_index] = {'color': grid[r][c], 'cells': tempset}
            next_index += 1

    return regions

def build_region_graph(regions):
    """
    Given a list of regions (from find_regions), determine which
    regions are adjacent to each other.

    Returns: dict mapping region_index -> set of neighboring region_indices
    """
    cell_to_region = {}
    for i, region in regions.items():
        for cell in region['cells']:
            cell_to_region[cell] = i

    graph = {i: set() for i in range(len(regions))}

    for i, region in regions.items():
        for cell in region['cells']:
            for neighbor in adjacency(cell[0], cell[1]):
                j = cell_to_region[neighbor]
                if i != j:
                    graph[i].add(j)
                    graph[j].add(i)

    return graph

def bfs_distances(graph, start):
    """
    Given a region graph and a starting region index, compute the
    shortest-path distance (in hops) from `start` to every other
    reachable region.

    Returns: dict mapping region_index -> distance (number of hops from start)
    """
    distances = {start: 0}
    queue = deque([start])

    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    return distances

def heuristic(graph):
    return max(bfs_distances(graph, 0).values())

def make_move(graph, regions, root, color):
    """
    Simulate choosing `color` as the next move. Merges every region
    directly adjacent to `root` that has color `color` into `root`.

    graph: dict, region_index -> set of neighboring region_indices
    regions: dict, region_index -> {'color': str, 'cells': set}
    root: int, the region index currently representing the captured blob
    color: str, the color being chosen for this move

    Returns: (new_graph, new_regions) — fresh copies, inputs untouched.
    """
    to_absorb = set()
    for i in graph[root]:
        if regions[i]['color'] == color:
            to_absorb.add(i)

    new_graph = {i: set(neighbors) for i, neighbors in graph.items()}

    for i in to_absorb:
        for neighbor in graph[i]:
            if neighbor != root and neighbor not in to_absorb:
                new_graph[root].add(neighbor)
                new_graph[neighbor].discard(i)
                new_graph[neighbor].add(root)

    for i in to_absorb:
        new_graph[root].discard(i)

    new_regions = {
        i: {'color': r['color'], 'cells': set(r['cells'])}
        for i, r in regions.items()
    }

    for i in to_absorb:
        new_regions[root]['cells'].update(new_regions[i]['cells'])
        del new_regions[i]

    return new_graph, new_regions

FOUND = "FOUND"  # sentinel value, distinct from any number

def ida_search(graph, regions, root, g, threshold, path):
    """
    g: moves made so far to reach this state
    threshold: current IDA* cost limit

    Returns FOUND if solved within threshold, otherwise the smallest
    f-value that exceeded threshold (for the outer loop to use next).
    """
    f = g + heuristic(graph)
    if f > threshold:
        return f

    if len(regions) == 1:
        return FOUND

    min_exceeded = float('inf')
    candidate_colors = {regions[i]['color'] for i in graph[root]}

    for color in candidate_colors:
        new_graph, new_regions = make_move(graph, regions, root, color)
        result = ida_search(new_graph, new_regions, root, g + 1, threshold, path)

        if result == FOUND:
            path.append(color)
            return FOUND
        else:
            min_exceeded = min(min_exceeded, result)

    return min_exceeded

def ida_star(graph, regions, root=0):
    threshold = heuristic(graph)
    path = []

    while True:
        result = ida_search(graph, regions, root, 0, threshold, path)
        if result == FOUND:
            path.reverse()
            return threshold, path
        threshold = result
        path.clear() 

def solve_pipeline_check():
    grid = grid_to_array()
    regions = find_regions(grid)
    graph = build_region_graph(regions)
    h = heuristic(graph)

    print(f"Regions: {len(regions)}")
    print(f"Total edges: {sum(len(v) for v in graph.values()) // 2}")
    print(f"Heuristic lower bound (moves): {h}")

    return graph, regions

def test_regions():
    """
    grid = grid_to_array()
    regions = find_regions(grid)
    print(f"Board collapsed into {len(regions)} regions")
    total_cells = sum(len(r['cells']) for r in regions.values())
    print(f"Total cells across all regions: {total_cells} (should be 100)")

    graph = build_region_graph(regions)
    print(f"Region 0 is adjacent to: {graph[0]}")
    print(f"Total edges: {sum(len(v) for v in graph.values()) // 2}")

    distances = bfs_distances(graph, 0)
    print(distances)
    print("Eccentricity (heuristic lower bound):", max(distances.values()))

    regions_dict = {i: r for i, r in enumerate(regions)}  # convert your list to the dict form
    new_graph, new_regions = make_move(graph, regions, 0, "Teal")

    print("Regions before:", len(regions), "-> after:", len(new_regions))
    print("Root's cell count before:", len(regions[0]['cells']), "-> after:", len(new_regions[0]['cells']))
    print("Original untouched? root cells still:", len(regions[0]['cells']))
    """

    grid = grid_to_array()
    regions = find_regions(grid)
    graph = build_region_graph(regions)

    optimal, move_sequence = ida_star(graph, regions)
    print(f"Optimal move count: {optimal}")
    print(f"Move sequence: {move_sequence}")

def solver(method):
    if (method == "a*"):
        grid = grid_to_array()
        regions = find_regions(grid)
        graph = build_region_graph(regions)
    
        optimal, move_sequence = ida_star(graph, regions)
        print(f"Optimal move count: {optimal}")
        print(f"Move sequence: {move_sequence}")
    elif(method == "greedy"):
        chain_theory()


def main():
    solver("a*")
    

main()


#Brute force to find the optimal solution. Optimized however to prevent using colors that cannot be accessed.
#Prime box is top left since this is where it starts

#Conway game of life
