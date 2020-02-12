from classes.GlobalData import GlobalData
from classes import Grid
from classes.Calculations import *

import json
import sys


def main(file=None):
    if file is None:
        with open("data_file.json", "r") as read_file:
            data = json.load(read_file)
    else:
        try:
            with open(file, "r") as read_file:
                data = json.load(read_file)
        except:
            print("Cannot open json file")
            return -1
    try:
        gd = GlobalData(data['H'], data['W'], data['nH'], data['nW'])
        grid = Grid(gd)
        result = simulate_heat_transfer(grid, data['initial_temp'], data['simulation_time'],
                                        data['simulation_step_time'],
                                        data['ambient_temp'], data['alpha'], data['specific_heat'],
                                        data['conductivity'],
                                        data['density'])
        with open("result.txt", "w") as write_file:
            for nr, temp in enumerate(result):
                if nr % int(data['nH']) == 0:
                    write_file.write("\n")
                write_file.write(str(temp) + ";")
            write_file.close()
    except:
        print("Wrong json file")
        return -1


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
