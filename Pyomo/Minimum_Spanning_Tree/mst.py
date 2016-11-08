"""
Minimum Spanning Tree Code. This code is a general one and can be extended to a larger
MST problem that is being discussed here. This is a simple problem from the Minimum
Spanning Tree page from wikipedia.

In this implementation the row generation technique is not used.
"""

import pyomo
import pyomo.opt
import pyomo.environ as pe
import pandas
import networkx

class MST_Simple:
    def __init__(self,fname):
        self.df = pandas.read_csv(fname)
        self.createSimpleModel()


# Creating the Pyomo environment model and the sets
    def createSimpleModel(self):
        df = self.df
        node_set = set(list(df.startNode) + list(df.destNode))
        df.set_index(['startNode','destNode'], inplace = True)
        df.sort_index(inplace = True)

        m = pe.ConcreteModel()


        # Creating the edge_set
        edge_set = df.index.unique()
        m.edge_set = pe.Set(initialize = edge_set, dimen = 2)

        # Defining the Varibles

        m.Y = pe.Var(m.edge_set, domain = pe.Binary)

        # Defining the Objective Function

        def obj_rule(m):
            return sum(m.Y[e]*df.ix[e,'dist'] for e in m.edge_set)
        m.OBJ = pe.Objective(rule = obj_rule, sense = pe.minimize)


        # Add the n-1 constraint
        def simple_const_rule(m):
            return sum(m.Y[e] for e in m.edge_set) == len(node_set) - 1
        m.simpleConst = pe.Constraint(rule = simple_const_rule)

        self.m = m

    # Solving the pyomo model using the cplex solver

    def solve(self):
        solver = pyomo.opt.SolverFactory('cplex')
        results = solver.solve(self.m, tee = True, keepfiles = False, options_string = "")

        # To check for the errors that the solver throws in any.

        if (results.solver.status != pyomo.opt.SolverStatus.ok):
            logging.warning('Check solver not ok?')
        if (results.solver.termination_condition != pyomo.opt.TerminationCondition.optimal):
            logging.warning('Check solver optimality?')


if __name__ == "__main__":
    mst = MST_Simple('mst.csv')
    mst.solve()