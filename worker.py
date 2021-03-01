import random

self_esteem_coefficients = {
    "normal": 1,
    "imposter": 0.9
}

class Worker():
    def __init__(self, current_wage, utype="normal", tell_wage=1):
        # возможео имеет смысл зп отличать зп когда работает или когда просто хочет
        self.current_wage = current_wage
        self.type = utype
        self.tell_wage_coeff = tell_wage
        try:
            self.self_esteem_coefficient = self_esteem_coefficients[utype]
        except KeyError:
            raise "No such self esteem type"

        # also here would be great to have all friends
        self.others_wage = []
        self.offers = []

        self.is_employed = False

        # historical data
        self.wage_history = []
        self.employnment_history = []


    def new_cycle(self):
        '''Method used by World to drop state between iterations'''
        self.wage_history.append(self.current_wage)
        self.employnment_history.append(self.is_employed)
        self.is_employed = False

    
    def _count_new_wage(self):
        if self.others_wage:
            self.current_wage = sum(self.others_wage)/len(self.others_wage)

    def give_employer_wage(self):
        return self.current_wage * self.self_esteem_coefficient 

    def give_wage(self):
        if random.random() <= self.tell_wage_coeff:
            return self.current_wage * self.self_esteem_coefficient
    
    def stage_wage_recearch(self, wages: list=[]):
        self.others_wage = wages
        self._count_new_wage()

    def recieve_offer(self, offer):
        ''''Method used by Employer to send job offer to Worker'''
        self.offers.append(offer)

    def stage_choose_employer(self):
        '''Method used by World to cover stage 3 of simulation'''
        if self.offers:
            chosen = random.choice(self.offers)
            self.is_employed = True
            chosen.close_vacancy()
    
    def __lt__(self, worker_2):
        if self.current_wage < worker_2.current_wage:
            return True
        return False

    def __gt__(self, worker_2):
        if self.current_wage < worker_2.current_wage:
            return True
        return False

    def __repr__(self):
        return f"Worker. type {self.type}, salary {self.current_wage}"

