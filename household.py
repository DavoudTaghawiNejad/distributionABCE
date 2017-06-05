from __future__ import division
import abce


class Household(abce.Agent, abce.Household, abce.Trade):
    def init(self, simulation_parameters, agent_parameters):
        self.create('capital', agent_parameters['capital'])
        self.create('labor_endowment', agent_parameters['labor'])

    def send_labor_and_captial(self):
        """ send all my labor and captial to the representative firm """
        self.log('initial_capital', self.possession('capital'))
        self.log('initial_labor', self.possession('labor'))

        self.sell('firm', 0, good='capital', quantity=self.possession('capital'), price=0)
        self.sell('firm', 0, good='labor', quantity=self.possession('labor'), price=0)

    def consume_and_save(self):
        self.log('total_income', self.possession('mana'))
        self.destroy('mana', 0.5 * self.possession('mana'))
        self.create('capital', self.possession('mana'))
        self.destroy('mana', self.possession('mana'))  # use proper transformation not destroy/create !
        self.log('capital', self.possession('capital'))



