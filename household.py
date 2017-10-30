import abce


class Household(abce.Agent, abce.Household, abce.Trade):
    def init(self, simulation_parameters, agent_parameters):
        self.create('capital', max(0, agent_parameters['capital']))
        self.create('labor_endowment', agent_parameters['labor'])

    def send_labor_and_captial(self):
        """ send all my labor and capital to the representative firm """
        self.rounds_initial_capital = self['capital']
        self.log('capital', self['capital'])

        self.sell(('firm', 0), good='capital', quantity=self['capital'], price=0)
        self.sell(('firm', 0), good='labor', quantity=self['labor'], price=0)

    def receive_wage(self):
        wage = self.get_offers('mana')[0]
        self.accept(wage)
        self.wage = wage.quantity

    def receive_profit(self):
        profit = self.get_offers('mana')[0]
        self.accept(profit)
        self.profit = profit.quantity

    def consume_and_save(self):
        self.log('total_income', self['mana'])
        self.destroy('mana', 0.5 * self['mana'])
        self.create('capital', self['mana'])
        self.destroy('mana', self['mana'])  # use proper transformation not create / destroy !
    def return_income(self):
        return {'income': self.total_income, 'wage': self.wage, 'profit': self.profit, 'consumption': self.consumption, 'saving': self.saving}


