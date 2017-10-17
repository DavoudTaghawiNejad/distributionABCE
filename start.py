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
import pandas as pd
import holoviews as hv
renderer = hv.renderer('matplotlib').instance(fig='pdf', holomap='gif')


simulation_parameters = {'name': 'name',
                         'rounds': 50,
                         'population_file': 'population.csv',
                         'cd_capital': 0.3,
                         'cd_labor': 0.7}

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
            population = [{k: float(v) for k, v in row.items()}
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
        except:
            pass
        finally:
            simulation.graphs()


def plot_distributions(distributions, r):
    distributions = pd.DataFrame(distributions)
    distributions.sort_values(by='income', ascending=True, inplace=True)
    distributions.reset_index(drop=True, inplace=True)


    Y = sum(distributions['income'])
    ttl_profit = sum(distributions['profit'])
    ttl_wage = sum(distributions['wage'])
    ttl_consumption = sum(distributions['consumption'])
    ttl_saving = sum(distributions['saving'])

    income_dist = pd.DataFrame()
    income_dist['income'] = distributions['income'].cumsum() / Y
    income_dist['wage'] = distributions['wage'].cumsum() / Y
    income_dist['profit'] = distributions['profit'].cumsum() / Y
    income_dist['index'] = distributions.index
    income_dist['profit0polarization'] = ttl_profit / Y * income_dist['income']
    income_dist['wage0polarization'] = ttl_wage / Y * income_dist['income']
    income_dist = hv.Dataset(income_dist)

    spending_dist = pd.DataFrame()
    spending_dist['income'] = distributions['income'].cumsum() / Y
    spending_dist['consumption'] = distributions['consumption'].cumsum() / Y
    spending_dist['saving'] = distributions['saving'].cumsum() / Y
    spending_dist['index'] = distributions.index
    spending_dist['consumption0polarization'] = ttl_consumption / Y * income_dist['income']
    spending_dist['saving0polarization'] = ttl_saving / Y * income_dist['income']
    spending_dist = hv.Dataset(spending_dist)

    graph = ((hv.Curve(income_dist, kdims=['index'], vdims=['income'], label='Income') *
              hv.Curve(income_dist, kdims=['index'], vdims=['profit'], label='Profit') *
              hv.Curve(income_dist, kdims=['index'], vdims=['wage'], label='Wage') *
              hv.Curve(income_dist, kdims=['index'], vdims=['profit0polarization'], label='profit0polarization') *
              hv.Curve(income_dist, kdims=['index'], vdims=['wage0polarization'], label='wage0polarization')) +

             (hv.Curve(spending_dist, kdims=['index'], vdims=['income'], label='Income') *
              hv.Curve(spending_dist, kdims=['index'], vdims=['consumption'], label='Consumption') *
              hv.Curve(spending_dist, kdims=['index'], vdims=['saving'], label='Saving') *
              hv.Curve(spending_dist, kdims=['index'], vdims=['consumption0polarization'], label='consumption0polarization') *
              hv.Curve(spending_dist, kdims=['index'], vdims=['saving0polarization'], label='saving0polarization')))




    renderer.save(graph, '%05i' % r, style=dict(Image={'cmap':'jet'}))


    # raise SystemExit()






if __name__ == '__main__':
    main(simulation_parameters)

