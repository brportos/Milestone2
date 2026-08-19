def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
    mtx =[]

    for m in matrix:
        mtx += [m[::-1]]
    return mtx


print(mirror_matrix([[-1,-2],[-3,-4]]))
