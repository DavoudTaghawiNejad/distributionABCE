from __future__ import division
import abce


class Firm(abce.Agent, abce.Firm, abce.Trade):
    def init(self, simulation_parameters, agent_parameters):
        """ the economy is a Cobb-Douglas economy """
        self.cd_labor = simulation_parameters["cd_labor"]
        self.cd_capital = simulation_parameters["cd_capital"]
        self.set_cobb_douglas("mana", 1, {"labor": self.cd_labor, "capital": self.cd_capital})

    def production(self):
        self.labor_offers = self.get_offers('labor')
        self.capital_offers = self.get_offers('capital')

        for offer in self.labor_offers + self.capital_offers:
            self.accept(offer)

        a = self.cd_labor
        b = self.cd_capital

        labor = self.possession('labor')
        capital = self.possession('capital')

        self.mpl = a * labor ** (a - 1) * capital ** b
        self.mpc = labor ** a * b * capital ** (b - 1)

        self.produce_use_everything()

    def distribution(self):
        for offer in self.labor_offers:
            self.give('household', offer.sender_id, good='mana', quantity=offer.quantity * self.mpl)

        for offer in self.capital_offers:
            self.give('household', offer.sender_id, good='mana', quantity=offer.quantity * self.mpc)

        assert self.possession('mana') < 0.0001


