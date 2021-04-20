import random
import math

import networkx as nx

from employer import Employer
from worker import Worker


NETWORK_REPRESENATION_TEMPLATE = """Social Network simulation
Iteration   {}
Mean wage   {}

Initial parameters:
Percent of low self esteemed people {}
Probability of giving information {}
Number of "friends" per worker {}
"""


class World():
    
    def __init__(self, beta=1, alpha=1, N_workers=10, N_companies=3, n_conn=2):
        self.beta = beta
        self.alpha = alpha
        self.N_workers = N_workers
        self.iteration = 0
        self.mean_wage_history = [0]
        self.n_connections_per_worker = n_conn

        self.social_network = nx.Graph()

        #creating Empoyers
        self.employers = []
        for i in range(N_companies):
            self.employers.append(Employer(i, N=5) )

        #creating workers
        n_low = math.ceil(self.N_workers * (1-self.beta))
        n_norm = math.floor(self.N_workers * self.beta)

        low = [(i, {'worker': self._init_worker(tpe='imposter')}) for i in range(n_low)]
        norm = [(n_low + i, {'worker': self._init_worker(tpe='normal')}) for i in range(n_norm)]

        self.social_network.add_nodes_from(low)
        self.social_network.add_nodes_from(norm)
        
        #creating connections between them, for now - fixed and getting as a param when init
        all_workers = list(range(self.N_workers))
        for i in all_workers:
            connections = random.choices(all_workers, k=self.n_connections_per_worker)
            if i in connections:
                connections.remove(i)
            self.social_network.add_edges_from([ (i, c) for c in connections ])
        

    def _init_worker(self, tpe):
        return Worker(utype=tpe, current_wage=100)


    def _all_workers_employed(self):
        print([not self.social_network.nodes[w]['worker'].is_employed for w in self.social_network.nodes])
        return all(
                [self.social_network.nodes[w]['worker'].is_employed for w in self.social_network.nodes]
                )

    def get_filtered_network(self, filter):
        #TODO
        raise NotImplementedError


    def __repr__(self):

        return NETWORK_REPRESENATION_TEMPLATE.format(
            self.iteration,
            self.get_mean_wage(),
            1-self.beta,
            self.alpha,
            self.n_connections_per_worker,
            )

    def get_mean_wage(self):
        return self.mean_wage_history[-1]

    def first_stage(self):
        for node in self.social_network.nodes:
            wages = []
            for neighbor in self.social_network.neighbors(node):
                wages.append(self.social_network.nodes[neighbor]['worker'].give_wage())
            self.social_network.nodes[node]['worker'].stage_wage_recearch(wages)


    def second_stage(self):
        for emp in self.employers:
            emp.offer_candidates(self.social_network)

    def third_stage(self):
        for node in list(self.social_network.nodes):
            self.social_network.nodes[node]['worker'].stage_choose_employer()
            # if  node > 10:
            #     exit(0)

    def can_finish_cycle(self):
        if self._all_workers_employed():
            print('here')
            return True
        for emp in self.employers:
            if emp.get_open_vacancies():
                return False
                
        return True


    def new_cycle(self):
        '''
        This method 
        - calculates World statistics for finisched iteration 
        - prepares employers and workers for new cycle
        '''
        self.iteration += 1

        for emp in self.employers:
            emp.new_cycle()

        wages = []
        for node in self.social_network.nodes:
            wages.append(self.social_network.nodes[node]['worker'].give_employer_wage())
            self.social_network.nodes[node]['worker'].new_cycle()
        
        self.mean_wage_history.append(sum(wages)/float(len(wages)))

    def run_iteration(self, silent=True):
        self.first_stage()

        while not self.can_finish_cycle():
            self.second_stage()
            self.third_stage()

        self.new_cycle()

        if not silent:
            print(self)

        return self.get_mean_wage()
    
if __name__ == "__main__":
    test_network = World(alpha=0.99, beta=0.99, N_workers=30, N_companies=3)
    print(test_network)

    print(test_network.social_network.nodes())

    for stage_num in range(2):
        print(f'starting stage {stage_num}')
        test_network.run_iteration()
    
    print('#'*30)

    print(test_network.mean_wage_history)
    for node in test_network.social_network.nodes:
        print(f'worker {node}')        
        w =  test_network.social_network.nodes[node]['worker']
        print(w.wage_history)
        print(w.employnment_history)
        print()
        print()

    print('__'*30)
    for emp in test_network.employers:
        print(f'employer {emp.uid}')
        print(emp.n_working_history)
    
        print()
        print()
