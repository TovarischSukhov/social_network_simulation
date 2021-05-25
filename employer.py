import random

from scipy.optimize import minimize

from settings import QUALIFICATIONS
from utils import employer_challenge, make_qualifications_dict_from_market

class Employer():
    def __init__(self, uid, requirements: dict = {}, market_size: int = None, market_size_per_vacancy: int = 2):
        '''

        imputs:
         - uid
         - requirements: dict, {'qualifiation': number_workers ...}
        '''

        # metadata
        self.uid  = uid
        self.requirements = requirements
        # amount of workers employer sees on market on each iteration
        self.market_size = market_size or sum([requirements[q] for q in requirements])
        self.current_market_size = self.market_size
        self.market_size_per_vacancy = market_size_per_vacancy

        # self.vacancies = []
        # for i in range(self.n_vacances):
        #     self.vacancies.append(Vacancy(i, self))

        # in-cycle data
        self.workers = []
        self.budget = 0

        # historical data
        self.qulification_level_history = []
        self.n_working_history = []
        self.worker_qulification_history = []
        
        # calculate current required qualification level
        self.total_qualifiation_needed = sum([ requirements[q] * QUALIFICATIONS[q] for q in requirements])
        

    def new_cycle(self, network):
        '''Method used by World to drop state between iterations'''
        self.budget = 0
        self.current_market_size = self.market_size

        q = self.total_qualifiation_needed
        self.total_qualifiation_needed = sum([ self.requirements[q] * QUALIFICATIONS[q] for q in self.requirements])
        self.qulification_level_history.append(self.total_qualifiation_needed - q)

        self.n_working_history.append(len(self.workers))
        w = [w.give_employer_qualification_wage() for w in self.workers ]
        self.worker_qulification_history.append(make_qualifications_dict_from_market(w))
        self.workers = []


    def _enreach_market_info(self, market, network):
        '''
        add info on qualification, worker and salary
        '''
        # print(network[market[0]])
        return [network.nodes[w]['worker'].give_employer_qualification_wage() for w in market ]

    
    def offer_candidates(self, network):
        '''Method used by World to cover stage 2'''
        workers = [i for i in network.nodes() if not network.nodes[i]['worker'].is_employed]
        # workers = list(network.nodes()).copy()
        random.shuffle(workers)
        print(workers, self.market_size, self.employees_needed())
        samplesize = min(self.market_size, len(workers))
        market = random.sample(workers, k=samplesize)
        # print(' mmark', market)
        market = self._enreach_market_info(market, network)
        # print('m1', market)
        market, workers = make_qualifications_dict_from_market(market, return_workers=True)
        # print('m2', market)

        prc, jun, mid, sen = employer_challenge(
            self.total_qualifiation_needed, self.budget, market, return_salaries=True,
            )
        mask = list(prc) + list(jun) + list(mid) + list(sen)
        for i in range(len(mask)):
            if mask[i] > 0:
                workers[i].recieve_offer(self, mask[i])
                print('w', workers[i])
                # print('wo', workers[i].offrs)
        print(self.uid, 'done offering')


    def employees_needed(self):
        '''Method used by World to determine if more workers needed'''
        return self.total_qualifiation_needed > 0


    def get_answer_from_worker(self, worker):
        '''Method used by Worker to agree for job'''
        self.workers.append(worker)
        self.total_qualifiation_needed -=  QUALIFICATIONS[worker.real_qualification]
        self.current_market_size -= self.market_size_per_vacancy
        self.budget -= worker.give_employer_qualification_wage()[2]
        print(self.uid,'got answer from ', worker)

    def set_budget(self, market_data):
        '''Method used by World to give new wages stats in the beginning of each round'''
        for q in self.requirements:
            self.budget += self.requirements[q] * market_data[q]
        
