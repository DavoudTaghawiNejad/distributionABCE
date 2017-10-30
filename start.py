""" This simulation simulates the distributional evolution of a society. In this simulation
a population of individuals endowed with human and capital endowment, sells their endowments
for a wage and profits to a representative firm. Wage is the marginal
productivity of labor and profit is the marginal productivity of capital.

The remuneration is in terms of a representative good, which can be either consumed or
cost free transformed into capital.


"""
from firm import Firm
from household import Household
from abce import Simulation, gui
import csv
import gini_coef
from plot_distributions import plot_distributions



simulation_parameters = {'name': 'name',
                         'rounds': 50,
                         'population_file': 'population.csv',
                         'cd_capital': 0.3,
                         'cd_labor': 0.7,
                         'depreciation': 0.05}

def main(simulation_parameters):
        simulation = Simulation()


        simulation.declare_round_endowment(resource='labor_endowment',
                                           units=1,
                                           product='labor')
        simulation.declare_perishable(good='labor')



        firms = simulation.build_agents(Firm, 'firm',
                       parameters=simulation_parameters,
                       number=1)

        with open(simulation_parameters['population_file'], 'rU') as f:
            population = [{k: float(v) for k, v in row.items() if k in ['capital', 'labor']}
                          for row in csv.DictReader(f, skipinitialspace=True)]

        households = simulation.build_agents(Household, 'household',
                       parameters=simulation_parameters,
                       agent_parameters=population)


        try:  # makes sure that graphs are displayed even when the simulation fails
            for r in range(simulation_parameters['rounds']):
                simulation.advance_round(r)
                households.send_labor_and_captial()
                firms.production()
                firms.pay_wage()
                households.receive_wage()
                firms.pay_profit()
                households.receive_profit()
                households.consume_and_save()
                households.panel_log(variables=['wage', 'profit', 'total_income'])
                firms.agg_log(variables=['mpl', 'mpc'])
                distributions = households.return_income()
                plot_distributions(distributions, r)



        except:
            raise
        finally:
            simulation.finalize()
            #gini_coef.transform_data_frame(simulation.path)
            simulation.graphs()










    # raise SystemExit()






if __name__ == '__main__':
    main(simulation_parameters)

