#!/usr/bin/python


def create_hades_matrix(data, startingpoint):
    # startingpoint = '24251'
    keepon = True
    hades_matrix = []
    hades_matrix.append([])
    hades_matrix[0].append(str(startingpoint))
    row = 0
    col = 0
    while keepon:
        hades_cell = data[str(startingpoint)]
        if 'LO' in hades_cell and 'pd' in hades_cell['LO']:
            dest_list = hades_cell['LO']['pd']
            if dest_list[2] != '0':
                if col == 0:
                    if dest_list[2] != hades_matrix[0][0]:
                        hades_matrix.append([])
                    else:
                        keepon = False
                        break
                hades_matrix[row + 1].append(dest_list[2])
            if dest_list[1] != '0':
                if dest_list[1] != hades_matrix[row][0]:
                    if row == 0:
                        hades_matrix[row].append(dest_list[1])
                    startingpoint = dest_list[1]
                    col = col + 1
                else:
                    row = row + 1
                    col = 0
                    startingpoint = hades_matrix[row][col]
            else:
                if dest_list[2] == '0':
                    keepon = False
                    break
                else:
                    row = row + 1
                    col = 0
                    startingpoint = hades_matrix[row][col]
    return hades_matrix
