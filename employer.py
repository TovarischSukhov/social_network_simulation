import random

class Employer():
    def __init__(self, uid, N: int=3):

        # metadata
        self.uid  = uid
        self.n_vacances = N
        self.n_offers_per_vacancy = 3

        self.vacancies = []
        for i in range(self.n_vacances):
            self.vacancies.append(Vacancy(i, self))

        # in-cycle data
        self.n_currently_working = 0
        self.candidates = []

        # historical data
        self.n_working_history = []
        

    def new_cycle(self):
        '''Method used by World to drop state between iterations'''
        self.n_working_history.append(self.n_currently_working)
        self.n_currently_working = 0
        
        for vac in self.vacancies:
            vac.new_cycle()


    def get_open_vacancies(self):
        opn = []
        for vac in self.vacancies:
            if vac.is_open:
                opn.append(vac)
        return opn


    def create_candidates_list(self, network):
        for vac in self.get_open_vacancies():
            vac.candidates = [] # избавляемся от старых кандидатов, чтобы не смешивались с новыми предлжениями
            workers = list(network.nodes()).copy()
            random.shuffle(workers)
            while vac.candidates_needed() and len(workers) > 0:
                candidate = random.choice(workers)
                if not network.nodes[candidate]['worker'].is_employed:
                    vac.add_candidate(network.nodes[candidate]['worker'])
                workers.remove(candidate)


    def choose_workers(self, network):
        print('cndds',self.get_open_vacancies())
        for vac in self.get_open_vacancies():
            worker = min(vac.candidates)
            self.make_offer(worker, case='first_time', vacancy=vac, salary=worker.give_employer_wage())
    

    def make_offer(self, worker, case, salary, vacancy):
        if case == 'first_time':
            worker.recieve_offer(self, vacancy, salary)
        elif case == 'upsale':
            print('upsale', worker, 'upsalig from', salary)
            # TODO temrary thing, here will be utility function for employer
            salary += salary*0.1
            if random.random() > 0.5:
                print('2nd upsale')
                salary += salary*0.1
            if salary > 2*worker.give_employer_wage():
                print('break')
                return
            worker.recieve_offer(self, vacancy, salary)

            print(worker, len(worker.offers))


    def offer_candidates(self, network):
        '''Method used by World to cover stage 2'''
        self.create_candidates_list(network)
        self.choose_workers(network)


    def get_answer_from_worker(self, worker, answer, vacancy, salary=None):
        '''Method used by Worker to agree for job'''
        if answer == 'agree':
            self.n_currently_working += 1
            vacancy.close()      
        elif answer == 'multiple_equal_offers':
            self.make_offer(worker, case='upsale', salary=salary, vacancy=vacancy)
        else:
            raise KeyError('unknown answer')



class Vacancy():
    def __init__(self, _id, employer):
        self.employer = employer
        self._id = _id
        self.is_open = True
        self.candidates = []

    def add_candidate(self, candidate):
        self.candidates.append(candidate)
    
    def close(self):
        if not self.is_open:
            print('answer for closed vac')
        self.is_open = False

    def new_cycle(self):
        self.is_open = True
        self.candidates = []
    
    def candidates_needed(self):
        return len(self.candidates) < 3

    def __repr__(self):
        return f'Vacancy, is open - {self.is_open}, {len(self.candidates)} candidates'