from classes.Element import Element
from classes.UniversalElement import UniversalElement
import numpy as np
from classes.Grid import Grid


ue = UniversalElement()

'''
def local_to_global_point(elem: Element, e: float, n:float):
    X = ue.N1(e, n) * elem.nodes[0].x + ue.N2(e, n) * elem.nodes[1].x + ue.N3(e, n) * elem.nodes[
        2].x + ue.N4(e, n) * elem.nodes[3].x
    Y = ue.N1(e, n) * elem.nodes[0].y + ue.N2(e, n) * elem.nodes[1].y + ue.N3(e, n) * elem.nodes[
        2].y + ue.N4(e, n) * elem.nodes[3].y
    return [X, Y]


def local_to_global(elem: Element):
    point_array = []
    for row in ue.M_N:
        Xp, Yp = 0, 0
        for nr, Nnr in enumerate(row):
            Xp = Xp + Nnr * elem.nodes[nr].x
            Yp = Yp + Nnr * elem.nodes[nr].y
        point_array.append([Xp, Yp])

    return np.array(point_array)
'''

def jakobian_matrix(elem: Element):
    point_array = np.zeros(shape=(4, 2, 2))
    for point in range(len(ue.Pc)):
        dx_de, dx_dn, dy_de, dy_dn = 0, 0, 0, 0
        for value in range(len(ue.Pc)):
            dx_de = dx_de + ue.M_Ne[point][value] * elem.nodes[value].x
            dx_dn = dx_dn + ue.M_Nn[point][value] * elem.nodes[value].x
            dy_de = dy_de + ue.M_Ne[point][value] * elem.nodes[value].y
            dy_dn = dy_dn + ue.M_Nn[point][value] * elem.nodes[value].y
        point_array[point] = np.array([[dx_de, dy_de], [dx_dn, dy_dn]])
    return point_array


def h_matrix(elem: Element, cond: float, alpha: float):
    dNdxdNdxDJ = np.zeros(shape=(4, 4, 4))
    dNdydNdyDJ = np.zeros(shape=(4, 4, 4))
    detJ = np.linalg.det(jakobian_matrix(elem))
    dNdxdNdyM = np.zeros(shape=(4, 4, 2))
    M_J_R = np.linalg.inv(jakobian_matrix(elem))
    for point in range(len(ue.Pc)):
        for row in range(len(ue.Pc)):
            dNdxdNdyM[point][row] = M_J_R[point].dot(np.array([ue.M_Ne[point][row], ue.M_Nn[point][row]]))

    for nr, MforPoint in enumerate(dNdxdNdyM):
        XasRow = np.array([MforPoint[column][0] for column in range(len(MforPoint))])
        XasColumn = np.array([MforPoint[column][0] for column in range(len(MforPoint))]).reshape(4, 1)
        YasRow = np.array([MforPoint[column][1] for column in range(len(MforPoint))])
        YasColumn = np.array([MforPoint[column][1] for column in range(len(MforPoint))]).reshape(4, 1)
        dNdxdNdxDJ[nr] = (np.array(detJ[nr] * np.array(XasRow) * np.array(XasColumn)))
        dNdydNdyDJ[nr] = (np.array(detJ[nr] * np.array(YasRow) * np.array(YasColumn)))

    HPointArray = np.zeros(shape=(4, 4, 4))
    for point in range(len(dNdxdNdxDJ)):
        HPointArray[point] = cond * (np.array(dNdxdNdxDJ[point]) + (np.array(dNdydNdyDJ[point])))
    MH = np.zeros((len(HPointArray), len(HPointArray[0])))
    for m in HPointArray:
        b = np.add(MH, m)
        MH = b

    # h_bc_matrix_for_walls

    m_npc = np.zeros(shape=(4, 2, 4))
    for point_id, wallPoints in enumerate(ue.Pc_walls):
        for nr, point in enumerate(wallPoints):
            m_npc[point_id][nr] = np.array([ue.N1(point[0], point[1]),
                                            ue.N2(point[0], point[1]),
                                            ue.N3(point[0], point[1]),
                                            ue.N4(point[0], point[1])])
    m_h_bc_side = np.zeros(shape=(4, 4, 4))
    for point_nr, side in enumerate(m_npc):
        arr = np.zeros(shape=(4, 4, 4))
        for nr, n_for_point in enumerate(side):
            as_column = np.array([[value] for value in n_for_point]).reshape(4, 1)
            as_row = np.array([value for value in n_for_point])
            arr[nr] = as_row * (as_column * alpha)
        m_h_bc_side[point_nr] = ((arr[0] + arr[1] + arr[2] + arr[3]) * length_of_sizes(elem)[point_nr] / 2)

    mhbc = np.zeros((len(m_h_bc_side[0][0]), len(m_h_bc_side[0][0])))

    for nr, MHbc in enumerate(m_h_bc_side):

        if nr in elem.walls_with_bc.keys():
            mhbc += MHbc

    return MH + mhbc


def c_matrix(elem: Element, cond: float, ro: float):
    NxN = np.zeros(shape=(4, 4, 4))
    detJ = np.linalg.det(jakobian_matrix(elem))
    for nr, row in enumerate(ue.M_N):
        as_row = np.array([value for value in ue.M_N[nr]])
        as_column = np.array([value for value in ue.M_N[nr]]).reshape(4, 1)
        NxN[nr] = np.array(as_row) * np.array(as_column) * detJ[nr] * cond * ro
    MC = np.zeros((len(NxN), len(NxN[0])))
    for m in NxN:
        b = np.add(MC, m)
        MC = b
    return MC


def length_of_sizes(elem: Element):
    sides = np.zeros(shape=4)
    for point in range(len(elem.nodes)):
        xx = float((elem.nodes[point].x - elem.nodes[(point + 1) % len(ue.Pc)].x) ** 2)
        yy = float((elem.nodes[point].y - elem.nodes[(point + 1) % len(ue.Pc)].y) ** 2)
        sides[point] = np.sqrt(xx + yy)
    return sides


'''
def h_bc_matrix_1d(elem: Element, ue: UniversalElement, alpha: float):
    m_h_bc_side = h_bc_matrix_for_walls(elem, ue, alpha)
    MHBC1D = []
    for M in m_h_bc_side:
        no_zeros_matrix = []
        for row in M:
            new_row = []
            for value in row:
                if value != 0:
                    new_row.append(value)
            if new_row: no_zeros_matrix.append(new_row)
        MHBC1D.append(no_zeros_matrix)
    newMHBC1D = []
    for nr, M in enumerate(MHBC1D):
        if nr + 1 not in elem.wall_numbers:
            M = np.where(M != 0, 0, M)
        newMHBC1D.append(M)
    return np.array(newMHBC1D)
'''

def p_matrix(elem: Element, alpha: float, ambient_temp: float):

    p = np.zeros(shape=(4, 4, 1))
    for point_id, wallPoints in enumerate(ue.Pc_walls):
        for point in wallPoints:
            p[point_id] += np.array([[ue.N1(point[0], point[1])],
                                            [ue.N2(point[0], point[1])],
                                            [ue.N3(point[0], point[1])],
                                            [ue.N4(point[0], point[1])]])

        p[point_id]*=length_of_sizes(elem)[point_id]/2

    P = np.zeros(shape=(4,1))

    for nr, pp in enumerate(p):

        if nr in elem.walls_with_bc.keys():
            P += pp
    P*=alpha*ambient_temp*(-1)
    return P


def h_global(grid: Grid, conductivity: float, alpha: float):
    global_h = np.zeros(shape=(grid.ld.nN, grid.ld.nN))

    for i in range(grid.ld.nE):
        element = grid.elements[i]
        local_h = h_matrix(element, conductivity, alpha)
        indexes = [element.nodes[i].id - 1 for i in range(4)]
        for local_row_index, global_row_index in zip(range(4), indexes):
            for local_column_index, global_column_index in zip(range(4), indexes):
                global_h[global_row_index][global_column_index] += local_h[local_row_index][local_column_index]

    return global_h


def c_global(grid: Grid, density: float, specific_heat: float):
    global_c = np.zeros(shape=(grid.ld.nN, grid.ld.nN))

    for i in range(grid.ld.nE):
        element = grid.elements[i]
        local_c = c_matrix(element, density, specific_heat)
        indexes = [element.nodes[i].id - 1 for i in range(4)]

        for local_row_index, global_row_index in zip(range(4), indexes):
            for local_column_index, global_column_index in zip(range(4), indexes):
                global_c[global_row_index][global_column_index] += local_c[local_row_index][local_column_index]

    return global_c


def p_global(grid: Grid, alpha: float, specific_heat: float):
    global_p = np.zeros(shape=(grid.ld.nN, 1))

    for i in range(grid.ld.nE):
        element = grid.elements[i]
        local_p = p_matrix(element, alpha, specific_heat)

        indexes = [element.nodes[i].id - 1 for i in range(4)]

        for local_row_index, global_row_index in zip(range(4), indexes):
            global_p[global_row_index] += local_p[local_row_index]

    return global_p


def simulate_heat_transfer(grid: Grid, initial_temp: float, simulation_time: float, step_time: float,
                           ambient_temp: float,
                           alpha: float, specific_heat: float, conductivity: float, density: float):

    nodes_temp = np.array([[initial_temp for _ in range(grid.ld.nN)]]).reshape((grid.ld.nN, 1))
    steps = (int)(simulation_time / step_time)
    steps_times = [(step + 1) * step_time for step in range(steps)]

    for step in steps_times:
        global_h = h_global(grid, conductivity, alpha)
        global_c = c_global(grid, density, specific_heat)
        global_p = p_global(grid, alpha, ambient_temp)
        global_p *= -1
        global_c *= 1 / step_time
        global_h += global_c
        global_p += np.dot(global_c, nodes_temp)
        nodes_temp = np.dot(np.linalg.inv(global_h), global_p)
        print("Step time: {}\tMin temp: {}\tMax temp: {}".format(step, np.amin(nodes_temp), np.amax(nodes_temp)))
