

def find_degeneracy(combinations: list) -> int:
    length = 0
    for i in combinations:
        if i[0] == i[1] == i[2]:
            length += 1
        elif i[0] == i[1] or i[0] == i[2] or i[1] == i[2]:
            length += 3
        elif i[0] != i[1] and i[0] != i[2] and i[1] != i[2]:
            length += 6
    return length