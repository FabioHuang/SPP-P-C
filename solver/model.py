from pyscipopt import Model, quicksum, SCIP_PARAMEMPHASIS
from math import ceil
import numpy as np

from typing import Optional, Tuple

class SCIPSolver():
    ''' Position and Covering solver with SCIP model '''
    def __init__(self, items: dict, strip_width: int, init_height: Optional[int] = None):
        self.items = items
        self.W = strip_width

        if init_height:
            self.H = init_height
        else:
            self.H = ceil(sum(i["w"] * i["h"] for i in items) / self.W)

        self.model = None
        self.reset()

    def set_positions(self) -> dict:
        ''' Maps all the valid positions for each item '''
        placements = []
        pid = 0
    
        for item in self.items:
            w = item["w"]
            h = item["h"]

            # ignoring items that dont fit in the curently strip
            if(self.W <= w or self.H <= h):
                continue

            for x in range(self.W - w + 1):
                for y in range(h, self.H - h + 1):
                    cells = [(x + dx, y + dy)
                             for dx in range(w)
                             for dy in range(h)]
                    
                    placements.append({"pid": pid,
                                       "item_id": item["id"],
                                       "position": (x, y),
                                       "cells": cells})
                    pid += 1

        return placements

    def is_feasible(self, placements: dict) -> Tuple[bool, dict]:
        x = {p["pid"]: self.model.addVar(vtype='B', name = f"x_{p["pid"]}")
             for p in placements}

        # Constraint (1): Avoid overlapping assigning at most one item at each tile of the strip    
        all_cells = set(cell for p in placements for cell in p["cells"])

        for cell in all_cells:
            self.model.addCons(quicksum(x[p["pid"]] for p in placements if cell in p["cells"]) <= 1,
                          name = "Overlapping Constraint")

        # Constraint (2): Guarantee that all items will be packed into the strip
        for item in items:
            i = item["id"]
            self.model.addCons(quicksum(x[p["pid"]] for p in placements if p["item_id"] == i) == 1,
                          name = "All items into strip Constraint")
    
        # Constraint (3): Determines that the capacity of the strip should not be exceeded.
        self.model.addCons(quicksum(len(p["cells"]) * x[p["pid"]] for p in placements) <= self.W * self.H)

        # Feasibility
        self.model.setObjective(0)

        # Solve
        self.model.optimize()

        return (True if self.model.getStatus() == "optimal" else False, x)

    def solve(self) -> dict:
        feasible = False
        while(not feasible):
            self.reset()

            placements = self.set_positions()
            feasible, x = self.is_feasible(placements)

            self.H += 1

        optimal_results = {}
        for p in placements:
            if self.model.getVal(x[p["pid"]]) == 1:
                optimal_results[p["item_id"]] = p["position"]

        return optimal_results

    def reset(self) -> None:
        if self.model:
            self.model.freeProb()
        
        self.model = Model("CoveringModel")
        self.model.setEmphasis(SCIP_PARAMEMPHASIS.FEASIBILITY)
        self.model.hideOutput()

if __name__ == "__main__":
    items = [
        {"id": 0, "w": 6, "h": 5},
        {"id": 1, "w": 5, "h": 4},
        {"id": 2, "w": 4, "h": 6},
        {"id": 3, "w": 7, "h": 4},
        {"id": 4, "w": 3, "h": 7},
        {"id": 5, "w": 8, "h": 3},
        {"id": 6, "w": 4, "h": 5},
        {"id": 7, "w": 6, "h": 4},
        {"id": 8, "w": 5, "h": 5},
        {"id": 9, "w": 2, "h": 8},
        {"id": 10, "w": 6, "h": 5},
        {"id": 11, "w": 5, "h": 4},
        {"id": 12, "w": 4, "h": 6},
        {"id": 13, "w": 7, "h": 4},
        {"id": 14, "w": 3, "h": 7},
        {"id": 15, "w": 8, "h": 3},
        {"id": 16, "w": 4, "h": 5},
        {"id": 17, "w": 6, "h": 4},
        {"id": 18, "w": 5, "h": 5},
        {"id": 19, "w": 2, "h": 8},
       ]

    solver = SCIPSolver(items, strip_width = 30)

    print(solver.solve())
