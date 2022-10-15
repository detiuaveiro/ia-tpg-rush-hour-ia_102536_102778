import ctypes
import sys
import time

grid_str = "IBBxooIooLDDJAALooJoKEEMFFKooMGGHHHM"
# grid_str = "ABCDEFGHIJKLMNKOPQRSTUVWXYZooooooooo"
size = (6, 6)

def get_grid(str):
    """
    Get the grid from a string
    """
    letters = { 'o':0, 'x': 0xFF, 'A': 1}
    n_letters = 1
    for i in range(len(str)):
        if str[i] not in letters:
            n_letters += 1
            letters[str[i]] = n_letters
    grid = 0
    for i in range(len(str)):
        grid = grid << 8 | letters[str[i]]
    return letters, grid

def get_matrix(grid, letters, size):
    """
    Get the grid from a string
    """
    letters2 = {v: k for k, v in letters.items()}
    size_t = size[0]*size[1]
    str = ""
    for i in range(size_t):
        str += letters2[grid >> ((size_t - i -1) << 3 ) & 0xFF]
    return [[*str[i*size[0]:i*size[0]+size[0]]] for i in range(size[1])]

def print_matrix(matrix):
    print()
    for i in matrix:
        for j in i:
            print(j, end=' ')
        print()
    print()
            
def get_byte(grid, size_t, pos):
    return grid >> ((size_t - pos -1) << 3 ) & 0xFF

def get_coords(size, pos):
    return (pos % size[0], pos // size[0])

def get_pos(size, coords):
    return coords[1]*size[0] + coords[0]

def matrix_hash(matrix):
    hash_=0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            hash_ << 8 | ord(matrix[i][j])
    return hash_


letters, grid = get_grid(grid_str)

letters2 = {v: k for k, v in letters.items()}

print(f"String :{grid_str}")
print(f"Grid :{hex(grid)}")
print(letters)

coords = [3, 1]

size_t= len(grid_str)

pos = get_pos(size, coords)
byte_ = get_byte(grid, size_t, pos)

print(f"Coords :{coords}")
print(f"Pos :{pos}")
print(f"Byte :{hex(byte_)}, {letters2[byte_]}")

matrix = get_matrix(grid, letters, size)
print_matrix(matrix)

arr= [*grid_str]
pos = get_pos(size, coords)

def get_nums():
    for i in range(10):
        yield i

def get_nums2():
    lst = []
    for i in range(10):
        lst.append(i)
    return lst

start = time.time()
for i in range(100000):
    for j in get_nums():
        pass
end= time.time()
print(f"Time :{end-start}")

start = time.time()
for i in range(100000):
    for j in get_nums2():
        pass
end= time.time()
print(f"Time :{end-start}")

# matrix_cp = [i.copy() for i in matrix]

# print(hash(str(matrix_cp)))
# print(hash(str(matrix)))

