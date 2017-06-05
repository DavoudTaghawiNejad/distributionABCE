from __future__ import division
from firm import Firm
from household import Household
from abce import Simulation, gui
import csv

simulation_parameters = {'name': 'name',
                         'rounds': 50,
                         'population_file': 'population.csv',
                         'cd_capital': 0.3,
                         'cd_labor': 0.7}

                             # commend out simulation.graphs() and uncomment
                             # this line to run the simulation with a Graphical
#@gui(simulation_parameters) # User Interface
def main(simulation_parameters):
        simulation = Simulation(rounds=simulation_parameters['rounds'])


        simulation.declare_round_endowment(resource='labor_endowment',
                                           units=1,
                                           product='labor'
        )
        simulation.declare_perishable(good='labor')



        firms = simulation.build_agents(Firm, 'firm',
                       parameters=simulation_parameters,
                       number=1)


        with open(simulation_parameters['population_file'], 'rU') as f:
            population = [{k: int(v) for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]

        households = simulation.build_agents(Household, 'household',
                       parameters=simulation_parameters,
                       agent_parameters=population)


        try:  # makes sure that graphs are displayed even when the simulation fails
            for round in simulation.next_round():
                households.do('send_labor_and_captial')
                firms.do('production')
                firms.do('distribution')
                households.do('consume_and_save')

        except:
            pass
        finally:
            simulation.graphs()

if __name__ == '__main__':
    main(simulation_parameters)

