import random

class Employer():
    def __init__(self, uid, N: int=3):

        # metadata
        self.uid  = uid
        self.n_vacances = N
        self.n_offers_per_vacancy = 3

        # in-cycle data
        self.n_currently_working = 0
        self.candidates = []

        # historical data
        self.n_working_history = []
        

    def new_cycle(self):
        '''Method used by World to drop state between iterations'''
        self.n_working_history.append(self.n_currently_working)
        self.n_currently_working = 0
        self.candidates = []

    def create_candidates_list(self, network):
        for _ in range(self.n_vacances):
            candidates = []
            for __ in range(self.n_offers_per_vacancy):
                candidates.append(random.choice(list(network.nodes())))
            self.candidates.append(candidates)

    def choose_workers(self, network):
        for vac in self.candidates:
            workers = [ network.nodes[v]['worker'] for v in vac ]
            min(workers).recieve_offer(self)

    def offer_candidates(self, network):
        '''Method used by World to cover stage 2'''
        self.create_candidates_list(network)
        self.choose_workers(network)

    def close_vacancy(self):
        '''Method used by Worker to agree for job'''
        self.n_currently_working += 1



