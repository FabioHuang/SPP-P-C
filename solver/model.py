from pyscipopt import Model, quicksum, SCIP_PARAMEMPHASIS
from math import ceil

from typing import Optional, Tuple

class SCIPSolver():
    ''' Position and Covering solver with SCIP model '''
    def __init__(self, init_height: Optional[int] = None):
        self.model = None
        self.reset()

    def set_positions(self, items: dict, W: int, H: int) -> dict:
        ''' Maps all the valid positions for each item '''
        placements = []
        pid = 0
    
        for i in items:
            w = items[i]["w"]
            h = items[i]["h"]

            # ignoring items that dont fit in the curently strip
            if(W < w or H < h):
                continue

            for x in range(W - w):
                for y in range(H - h):
                    cells = [(x + dx, y + dy)
                             for dx in range(w)
                             for dy in range(h)]
                    
                    placements.append({"pid": pid,
                                       "item_id": i,
                                       "position": (x, y),
                                       "cells": cells})
                    pid += 1

        return placements

    def is_feasible(self, items: dict, placements: dict, W: int, H: int) -> Tuple[bool, dict]:
        x = {p["pid"]: self.model.addVar(vtype='B', name = f"x_{p["pid"]}")
             for p in placements}

        # Constraint (1): Avoid overlapping assigning at most one item at each tile of the strip    
        all_cells = set(cell for p in placements for cell in p["cells"])

        for cell in all_cells:
            self.model.addCons(quicksum(x[p["pid"]] for p in placements if cell in p["cells"]) <= 1,
                          name = "Overlapping Constraint")

        # Constraint (2): Guarantee that all items will be packed into the strip
        for id in items:
            self.model.addCons(quicksum(x[p["pid"]] for p in placements if p["item_id"] == id) == 1,
                          name = "All items into strip Constraint")
    
        # Constraint (3): Determines that the capacity of the strip should not be exceeded.
        self.model.addCons(quicksum(len(p["cells"]) * x[p["pid"]] for p in placements) <= W * H)

        # Feasibility
        self.model.setObjective(0)

        # Solve
        self.model.optimize()

        return (True if self.model.getStatus() == "optimal" else False, x)

    def solve(self, items: dict, strip_width: int) -> dict:
        W = strip_width
        H = ceil(sum(items[i]['w'] * items[i]['h'] for i in items) / W)

        feasible = False
        while(not feasible):
            print(H)
            self.reset()

            placements = self.set_positions(items, W, H)
            feasible, x = self.is_feasible(items, placements, W, H)
            
            H += 1 if not feasible else 0

        optimal_results = {}
        for p in placements:
            if self.model.getVal(x[p["pid"]]) == 1:
                optimal_results[p["item_id"]] = p["position"]

        return optimal_results, H

    def reset(self) -> None:
        if self.model:
            self.model.freeProb()
        
        self.model = Model("CoveringModel")
        self.model.setEmphasis(SCIP_PARAMEMPHASIS.FEASIBILITY)
        self.model.hideOutput()

if __name__ == "__main__":
    items = {
        "1": {"w": 6, "h": 5},
        "2": {"w": 5, "h": 4}}

    solver = SCIPSolver()

    print(solver.solve(items, 8))
