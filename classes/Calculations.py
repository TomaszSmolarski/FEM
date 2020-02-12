from classes.Element import Element
from classes.UniversalElement import UniversalElement
import numpy as np
from classes.Grid import Grid

ue = UniversalElement()


def jacobian_matrix(elem: Element):
    point_array = np.zeros(shape=(4, 2, 2))
    for point in range(len(ue.Pc)):
        dx_de, dx_dn, dy_de, dy_dn = 0, 0, 0, 0
        for value in range(len(ue.Pc)):
            dx_de += ue.M_Ne[point][value] * elem.nodes[value].x
            dx_dn += ue.M_Nn[point][value] * elem.nodes[value].x
            dy_de += ue.M_Ne[point][value] * elem.nodes[value].y
            dy_dn += ue.M_Nn[point][value] * elem.nodes[value].y
        point_array[point] = np.array([[dx_de, dy_de], [dx_dn, dy_dn]])
    return point_array


def h_matrix(elem: Element, conductivity: float, alpha: float):
    dNdx_dNdxT = np.zeros(shape=(4, 4, 4))
    dNdy_dNdyT = np.zeros(shape=(4, 4, 4))
    detJ = np.linalg.det(jacobian_matrix(elem))
    dNdxdNdyM = np.zeros(shape=(4, 4, 2))
    M_J_R = np.linalg.inv(jacobian_matrix(elem))
    # obliczanie wektorów dN/dx i dN/dy
    for point_id in range(len(ue.Pc)):
        for row in range(len(ue.Pc)):
            dNdxdNdyM[point_id][row] = M_J_R[point_id].dot(np.array([ue.M_Ne[point_id][row], ue.M_Nn[point_id][row]]))
    for nr, M_for_point in enumerate(dNdxdNdyM):
        dNdxT = np.array([M_for_point[row][0] for row in range(len(M_for_point))])
        dNdx = np.array([M_for_point[row][0] for row in range(len(M_for_point))]).reshape(4, 1)
        dNdyT = np.array([M_for_point[row][1] for row in range(len(M_for_point))])
        dNdy = np.array([M_for_point[row][1] for row in range(len(M_for_point))]).reshape(4, 1)
        dNdx_dNdxT[nr] = dNdxT * dNdx
        dNdy_dNdyT[nr] = dNdyT * dNdy
    MH = np.zeros(shape=(4, 4))
    for point_id in range(len(dNdx_dNdxT)):
        # całkowanie numeryczne
        MH += detJ[point_id] * conductivity * (dNdx_dNdxT[point_id] + dNdy_dNdyT[point_id]) * ue.w[0] * ue.w[1]

    # Hbc
    m_npc = np.zeros(shape=(4, 2, 4))
    for point_id, wallPoints in enumerate(ue.Pc_walls):
        for nr, point in enumerate(wallPoints):
            m_npc[point_id][nr] = np.array([ue.N1(point[0], point[1]),
                                            ue.N2(point[0], point[1]),
                                            ue.N3(point[0], point[1]),
                                            ue.N4(point[0], point[1])])
    mhbc = np.zeros(shape=(4, 4))
    for wall_id, side in enumerate(m_npc):
        arr = np.zeros(shape=(2, 4, 4))
        for point_id, n_for_point in enumerate(side):
            N = np.array([[value] for value in n_for_point]).reshape(4, 1)
            N_T = np.array([value for value in n_for_point])
            arr[point_id] = N_T * N

        if wall_id in elem.walls_with_bc.keys():
            mhbc += ((arr[0] + arr[1]) * length_of_sizes(elem)[wall_id] / 2) * alpha * ue.w[0]

    return MH + mhbc


def c_matrix(elem: Element, density: float, specific_heat: float):
    NxN = np.zeros(shape=(4, 4, 4))
    detJ = np.linalg.det(jacobian_matrix(elem))
    MC = np.zeros((len(NxN), len(NxN[0])))
    for pc_id in range(4):
        N_T = np.array([value for value in ue.M_N[pc_id]])
        N = np.array([value for value in ue.M_N[pc_id]]).reshape(4, 1)
        MC += N_T * N * detJ[pc_id] * density * specific_heat * ue.w[0] * ue.w[1]
    return MC


def length_of_sizes(elem: Element):
    sides = np.zeros(shape=4)
    for node in range(len(elem.nodes)):
        xx = float((elem.nodes[node].x - elem.nodes[(node + 1) % len(ue.Pc)].x) ** 2)
        yy = float((elem.nodes[node].y - elem.nodes[(node + 1) % len(ue.Pc)].y) ** 2)
        sides[node] = np.sqrt(xx + yy)
    return sides


def p_matrix(elem: Element, alpha: float, ambient_temp: float):
    N = np.zeros(shape=(4, 4, 1))
    P = np.zeros(shape=(4, 1))
    for wall_id, wallPoints in enumerate(ue.Pc_walls):
        for point in wallPoints:
            N[wall_id] += np.array([[ue.N1(point[0], point[1])],
                                    [ue.N2(point[0], point[1])],
                                    [ue.N3(point[0], point[1])],
                                    [ue.N4(point[0], point[1])]])
        if wall_id in elem.walls_with_bc.keys():
            P += (-1) * alpha * ambient_temp * N[wall_id] * length_of_sizes(elem)[wall_id] / 2 * ue.w[0]
    return P


def h_global(grid: Grid, conductivity: float, alpha: float):
    global_h = np.zeros(shape=(grid.ld.nN, grid.ld.nN))
    for i in range(grid.ld.nE):
        element = grid.elements[i]
        local_h = h_matrix(element, conductivity, alpha)
        for local_row_index in range(4):
            for local_column_index in range(4):
                global_row_index = element.nodes[local_row_index].id - 1
                global_column_index = element.nodes[local_column_index].id - 1
                global_h[global_row_index][global_column_index] += local_h[local_row_index][local_column_index]
    return global_h


def c_global(grid: Grid, density: float, specific_heat: float):
    global_c = np.zeros(shape=(grid.ld.nN, grid.ld.nN))
    for i in range(grid.ld.nE):
        element = grid.elements[i]
        local_c = c_matrix(element, density, specific_heat)
        for local_row_index in range(4):
            for local_column_index in range(4):
                global_row_index = element.nodes[local_row_index].id - 1
                global_column_index = element.nodes[local_column_index].id - 1
                global_c[global_row_index][global_column_index] += local_c[local_row_index][local_column_index]
    return global_c


def p_global(grid: Grid, alpha: float, specific_heat: float):
    global_p = np.zeros(shape=(grid.ld.nN, 1))
    for i in range(grid.ld.nE):
        element = grid.elements[i]
        local_p = p_matrix(element, alpha, specific_heat)
        for local_row_index in range(4):
            global_row_index = element.nodes[local_row_index].id - 1
            global_p[global_row_index] += local_p[local_row_index]
    return global_p


def simulate_heat_transfer(grid: Grid, initial_temp: float, simulation_time: float, simulation_step_time: float,
                           ambient_temp: float,
                           alpha: float, specific_heat: float, conductivity: float, density: float):
    vector_temp_0 = np.array([[initial_temp for _ in range(grid.ld.nN)]]).reshape((grid.ld.nN, 1))
    steps = (int)(simulation_time / simulation_step_time)
    steps_times = [(step + 1) * simulation_step_time for step in range(steps)]
    global_h = h_global(grid, conductivity, alpha)
    global_c = c_global(grid, density, specific_heat)
    global_p = p_global(grid, alpha, ambient_temp)
    for step in steps_times:
        GP = global_p * (-1)
        GC = global_c * (1 / simulation_step_time)
        GH = global_h + GC
        GP += np.dot(GC, vector_temp_0)
        vector_temp_1 = np.linalg.solve(GH, GP)
        print("Step time: {}\tMin temp: {}\tMax temp: {}".format(step, np.amin(vector_temp_1), np.amax(vector_temp_1)))
        vector_temp_0 = vector_temp_1
    for node_id, temp in enumerate(vector_temp_0):
        grid.nodes[node_id].temp = float(temp)
    return vector_temp_0