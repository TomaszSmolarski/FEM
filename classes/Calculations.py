from classes.Element import Element
from classes.UniversalElement import UniversalElement
import numpy as np
from classes.Grid import Grid


def local_to_global_point(elem: Element, ue: UniversalElement, e, n):
    X = ue.N1(e, n) * elem.nodes[0].x + ue.N2(e, n) * elem.nodes[1].x + ue.N3(e, n) * elem.nodes[
        2].x + ue.N4(e, n) * elem.nodes[3].x
    Y = ue.N1(e, n) * elem.nodes[0].y + ue.N2(e, n) * elem.nodes[1].y + ue.N3(e, n) * elem.nodes[
        2].y + ue.N4(e, n) * elem.nodes[3].y
    return [X, Y]


def local_to_global(elem: Element, ue: UniversalElement):
    point_array = []
    for row in ue.M_N:
        Xp, Yp = 0, 0
        for nr, Nnr in enumerate(row):
            Xp = Xp + Nnr * elem.nodes[nr].x
            Yp = Yp + Nnr * elem.nodes[nr].y
        point_array.append([Xp, Yp])
    return np.array(point_array)


def jakobian_matrix(elem: Element, ue: UniversalElement):
    point_array = []
    for point in range(len(ue.Pc)):
        dx_de, dx_dn, dy_de, dy_dn = 0, 0, 0, 0
        for value in range(len(ue.Pc)):
            dx_de = dx_de + ue.M_Ne[point][value] * elem.nodes[value].x
            dx_dn = dx_dn + ue.M_Nn[point][value] * elem.nodes[value].x
            dy_de = dy_de + ue.M_Ne[point][value] * elem.nodes[value].y
            dy_dn = dy_dn + ue.M_Nn[point][value] * elem.nodes[value].y
        point_array.append([[round(dx_de, 5), round(dy_de, 5)], [round(dx_dn, 5), round(dy_dn, 5)]])
    return np.array(point_array)


def h_matrix(elem: Element, ue: UniversalElement, cond: float, alpha: float):
    dNdxdNdxDJ = []
    dNdydNdyDJ = []
    detJ = np.linalg.det(jakobian_matrix(elem, ue))
    for nr, MforPoint in enumerate(dNdxdNdyM(elem, ue)):
        XasRow = []
        XasColumn = []
        YasRow = []
        YasColumn = []
        for column in range(len(MforPoint)):
            XasRow.append(MforPoint[column][0])
            XasColumn.append([MforPoint[column][0]])
            YasRow.append(MforPoint[column][1])
            YasColumn.append([MforPoint[column][1]])
        dNdxdNdxDJ.append(np.array(detJ[nr] * np.array(XasRow) * np.array(XasColumn)))
        dNdydNdyDJ.append(np.array(detJ[nr] * np.array(YasRow) * np.array(YasColumn)))
    HPointArray = []
    for point in range(len(dNdxdNdxDJ)):
        HPointArray.append(cond * (np.array(dNdxdNdxDJ[point]) + (np.array(dNdydNdyDJ[point]))))
    MH = np.zeros((len(HPointArray), len(HPointArray[0])))
    for m in HPointArray:
        b = np.add(MH, m)
        MH = b
    return MH


def c_matrix(elem: Element, ue: UniversalElement, cond: float, ro: float):
    NxN = []
    detJ = np.linalg.det(jakobian_matrix(elem, ue))
    for nr, row in enumerate(ue.M_N):

        as_row = []
        as_column = []
        for value in ue.M_N[nr]:
            # tworzenie i mnożęnie macierzy 1x4 i 4x1 z tych samych N
            as_row.append(value)
            as_column.append([value])
        NxN.append(np.array(as_row) * np.array(as_column) * detJ[nr] * cond * ro)
    MC = np.zeros((len(NxN), len(NxN[0])))
    for m in NxN:
        b = np.add(MC, m)
        MC = b
    return MC


def dNdxdNdyM(elem: Element, ue: UniversalElement):
    point_array = []
    M_J_R = np.linalg.inv(jakobian_matrix(elem, ue))
    for point in range(len(ue.Pc)):
        row_array = []
        for row in range(len(ue.Pc)):
            row_array.append(M_J_R[point].dot(np.array([ue.M_Ne[point][row], ue.M_Nn[point][row]])))
        point_array.append(row_array)
    return np.array(point_array)


def length_of_sizes(elem: Element, ue: UniversalElement):
    sides = []
    for point in range(len(elem.nodes)):
        xx = float((elem.nodes[point].x - elem.nodes[(point + 1) % len(ue.Pc)].x) ** 2)
        yy = float((elem.nodes[point].y - elem.nodes[(point + 1) % len(ue.Pc)].y) ** 2)
        sides.append(np.sqrt(xx + yy))
    return np.array(sides)


def h_bc_matrix_for_walls(elem: Element, ue: UniversalElement, alpha: float):
    # punkty całkowania na danej powierzchni
    pc = np.array([[[ue.Pc[0][0], -1], [ue.Pc[1][0], -1]],
                   [[1, ue.Pc[1][1]], [1, ue.Pc[2][1]]],
                   [[ue.Pc[2][0], 1], [ue.Pc[3][0], 1]],
                   [[-1, ue.Pc[3][1]], [-1, ue.Pc[0][1]]]])

    m_npc = []
    for nr, wallPoints in enumerate(pc):
        # wyliczenie N1234 dla danego punktu
        Npoint = []
        for point in wallPoints:
            Npoint.append([ue.N1(point[0], point[1]),
                           ue.N2(point[0], point[1]),
                           ue.N3(point[0], point[1]),
                           ue.N4(point[0], point[1])])
        m_npc.append(Npoint)  # macierz składająca się z 4 macierzy 4x2

    m_h_bc_side = []
    for side in m_npc:
        Arr = []
        for NforPoint in side:
            as_row = []
            as_column = []
            for value in NforPoint:
                # tworzenie i mnożęnie macierzy 1x4 i 4x1 z tych samych N
                as_row.append(value)
                as_column.append([value])
            # dla obu punktow calkowania
            Arr.append(np.array(as_row) * (np.array(as_column) * alpha))
        m_h_bc_side.append(np.array((Arr[0] + Arr[1]) * length_of_sizes(elem, ue) / 2))  # pisze detJ a jest długość/2?
    return np.array(m_h_bc_side)


def h_bc_matrix_2d(elem: Element, ue: UniversalElement, alpha: float):
    m_h_bc_side = h_bc_matrix_for_walls(elem, ue, alpha)
    mhbc = np.zeros((len(m_h_bc_side[0][0]), len(m_h_bc_side[0][0])))
    # pętla sprawdzająca i dodająca macierze na których krawędz jest graniczna
    for nr, MHbc in enumerate(m_h_bc_side):
        if nr + 1 in elem.wall_numbers:
            mhbc = mhbc + np.array(m_h_bc_side[nr])
    return mhbc


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


def p_matrix(elem: Element, ue: UniversalElement, alpha: float, ambient_temp: float):
    # boundary conditions for newton law
    edges_with_bc = {}
    for i in range(4):
        if elem.nodes[i].bc and elem.nodes[(i + 1) % 4].bc:
            edges_with_bc[i] = [elem.nodes[i], elem.nodes[(i + 1) % 4]]
    # calculating jacobians for each edge (half of edge length)
    edges_jacobians = {}
    for key, nodes in edges_with_bc.items():
        edges_jacobians[key] = length_of_sizes(elem, ue)[key] / 2.
    # creating form functions for 1d
    N = np.zeros(shape=(2, 1))
    for integral_point in [ue.PcM[1], ue.PcM[0]]:
        N += np.array([[ue.d1N1(integral_point), ue.d1N2(integral_point)]]).reshape(2, 1)
    # combining matrices
    P = np.zeros(shape=(4, 1))
    for bc_index in edges_with_bc:
        if bc_index != 3:  # in that case adding arrays is simple, just translation of N_dot_NT
            P[bc_index:bc_index + 2, 0:1] += N * edges_jacobians[bc_index]
        else:
            P[0:4:3, 0:1] += N * edges_jacobians[bc_index]
    alpha *= -1
    P *= alpha * ambient_temp
    return P
