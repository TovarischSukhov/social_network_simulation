import random
import math

import networkx as nx

from settings import EMPLOYER_NEEDS, INITIAL_WAGE
from employer import Employer
from worker import Worker
from utils import make_qualifications_dict_from_market


NETWORK_REPRESENATION_TEMPLATE = """Social Network simulation
Iteration   {}
Mean wage   {}

Initial parameters:
Percent of low self esteemed people {}
Probability of giving information {}
Number of "friends" per worker {}
"""


class World():
    
    def __init__(
                self,
                qualification_ratio, 
                beta=1, 
                alpha=1, 
                no_workers=10, 
                no_employers=3, 
                no_connections=2,
                no_vacancys_per_employer=3,
                **kwargs

            ):
        self.beta = beta
        self.alpha = alpha
        self.N_workers = 0
        self.iteration = 0
        self.mean_wage_history = {}
        self.n_connections_per_worker = no_connections

        self.social_network = nx.Graph()

        #creating Employers
        self.employers = []
        for i in range(no_employers):
            self.employers.append(Employer(i, requirements=EMPLOYER_NEEDS, market_size_per_vacancy=3) )

        #creating workers
        for qual, ratio in qualification_ratio.items():
            n_qual_workers = round(no_workers*ratio)

            n_low = math.ceil(n_qual_workers * (1-self.beta))
            n_norm = math.floor(n_qual_workers * self.beta)
            #prtint(n_low, n_norm)

            low = [(self.N_workers + i, {'worker': self._init_worker('imposter', qual)}) for i in range(n_low)]
            norm = [(self.N_workers + n_low + i, {'worker': self._init_worker('normal', qual)}) for i in range(n_norm)]

            self.N_workers += n_qual_workers

            self.social_network.add_nodes_from(low)
            self.social_network.add_nodes_from(norm)
        
        #creating connections between them, for now - fixed and getting as a param when init
        all_workers = list(range(self.N_workers))
        for i in all_workers:
            connections = random.choices(all_workers, k=self.n_connections_per_worker)
            if i in connections:
                connections.remove(i)
            self.social_network.add_edges_from([ (i, c) for c in connections ])
        
        self.market_data = INITIAL_WAGE # here we will store the data abot mean wages for previous iteration
        

    def _init_worker(self, tpe, qual):
        return Worker(
                utype=tpe, 
                current_wage=INITIAL_WAGE[qual], 
                qualification=qual, 
                employer_requrnments=EMPLOYER_NEEDS,
            )


    def _all_workers_employed(self):
        # print([not self.social_network.nodes[w]['worker'].is_employed for w in self.social_network.nodes])
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
        if self.mean_wage_history:
            lasts = {q: self.mean_wage_history[q][-1] for q in self.mean_wage_history}
            return lasts
        return None

    def first_stage(self):
        for emp in self.employers:
            emp.set_budget(self.market_data) 

        for node in self.social_network.nodes:
            wages = []
            for neighbor in self.social_network.neighbors(node):
                # print(neighbor, self.social_network.nodes[neighbor])
                wages.append(self.social_network.nodes[neighbor]['worker'].give_qualification_wage())
            # print(self.social_network.nodes[node])
            self.social_network.nodes[node]['worker'].stage_wage_recearch(wages, self.market_data)


    def second_stage(self):
        for emp in self.employers:
            emp.offer_candidates(self.social_network)

    def third_stage(self):
        for node in list(self.social_network.nodes):
            self.social_network.nodes[node]['worker'].stage_choose_employer()

    def can_finish_cycle(self):
        if self._all_workers_employed():
            # print('here')
            return True
        for emp in self.employers:
            if emp.employees_needed():
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
            emp.new_cycle(self.social_network)

        wages = []
        for node in self.social_network.nodes:
            wages.append(self.social_network.nodes[node]['worker'].give_employer_qualification_wage())
            self.social_network.nodes[node]['worker'].new_cycle()
        
        wages = make_qualifications_dict_from_market(wages)
        
        self.market_data = {q: sum(wages[q])/len(wages[q]) for q in wages if wages[q]}
        
        for q in self.market_data:
            if q not in self.mean_wage_history:
                self.mean_wage_history[q] = []
            self.mean_wage_history[q].append(self.market_data[q])

    def run_iteration(self, silent=True):
        self.first_stage()

        while not self.can_finish_cycle():
            self.second_stage()
            self.third_stage()

        self.new_cycle()

        if not silent:
            print(self)

        print(self.iteration, 'ready to statrt')

        return self.get_mean_wage()

    
if __name__ == "__main__":
    test_network = World(alpha=0.5, beta=0.5,n_conn=2, N_workers=10, N_companies=3, qualification_ratio={'junior': 0.5, 'middle': .3, 'senior': 0.2})
    print(test_network)

    print(test_network.social_network.nodes())

    for stage_num in range(2):
        print(f'starting stage {stage_num}')
        test_network.run_iteration()
    
    print('#'*30)

    print(test_network.mean_wage_history)
    for node in test_network.social_network.nodes:
              
        w =  test_network.social_network.nodes[node]['worker']
        print(w)  
        print(w.wage_history)
        print(w.employnment_history)
        print()
        print()

    print('__'*30)
    for emp in test_network.employers:
        print(f'employer {emp.uid}')
        print(emp.qulification_level_history)
        print(emp.worker_qulification_history)
        print(emp.n_working_history)
    
        print()
        print()
