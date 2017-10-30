import abce


class Firm(abce.Agent, abce.Firm, abce.Trade):
    def init(self, simulation_parameters, agent_parameters):
        """ the economy is a Cobb-Douglas economy """
        self.cd_labor = simulation_parameters["cd_labor"]
        self.cd_capital = simulation_parameters["cd_capital"]

        def production_function(goods):
            return goods['labor'] ** self.cd_labor * goods['capital'] ** self.cd_capital

        use = {'labor': 1, 'capital': 0.05}

        self.set_production_function(production_function, output='mana', use=use)

        self.Y_1 = 0

    def production(self):
        self.labor_offers = self.get_offers('labor')
        self.capital_offers = self.get_offers('capital')

        for offer in self.labor_offers + self.capital_offers:
            self.accept(offer)

        a = self.cd_labor
        b = self.cd_capital

        labor = self['labor']
        capital = self['capital']

        self.mpl = a * labor ** (a - 1) * capital ** b
        self.mpc = labor ** a * b * capital ** (b - 1)

        self.log('r', self.mpc)

        Y = self.produce_use_everything()['mana']
        self.log('g', Y - self.Y_1)
        self.Y_1 = Y

    def pay_wage(self):
        for offer in self.labor_offers:
            self.sell(offer.sender, good='mana', quantity=offer.quantity * self.mpl, price=0)

    def pay_profit(self):
        remaining_cap =  self['capital'] / sum([o.quantity for o in self.capital_offers])
        print(remaining_cap)
        for offer in self.capital_offers:
            self.sell(offer.sender, good='mana', quantity=offer.quantity * self.mpc, price=0)
            self.give(offer.sender, good='capital', quantity=offer.quantity * remaining_cap, epsilon=0.0001)

        assert self.not_reserved('mana') < 0.0001


