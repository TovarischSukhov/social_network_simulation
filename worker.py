import random

self_esteem_coefficients = {
    "normal": 1,
    "imposter": 0.9
}

class Worker():
    def __init__(self, current_wage, utype="normal", tell_wage=1, _id=None):
        self.id = _id or random.randint(0, 10000)

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
            # TODO temrary thing, here will be utility function for employer
            self.current_wage = sum(self.others_wage)/len(self.others_wage)

    def give_employer_wage(self):
        return self.current_wage * self.self_esteem_coefficient 

    def give_wage(self):
        if random.random() <= self.tell_wage_coeff:
            return self.current_wage * self.self_esteem_coefficient
    
    def stage_wage_recearch(self, wages: list=[]):
        self.others_wage = wages
        self._count_new_wage()

    def recieve_offer(self, employer, vacancy, salary):
        ''''Method used by Employer to send job offer to Worker'''
        offer = Offer(employer, vacancy, salary)
        self.offers.append(offer)

    def stage_choose_employer(self):
        '''Method used by World to cover stage 3 of simulation'''
        mx_offers = []
        mx_sal = 0
        for of in self.offers:
            if of.salary > mx_sal:
                mx_sal = of.salary
                mx_offers = []
            if of.salary == mx_sal:
                mx_offers.append(of)
        
        if len(mx_offers) > 1:
            self.offers = []
            for of in mx_offers:
                of.employer.get_answer_from_worker(self, 'multiple_equal_offers', of.vacancy, of.salary)
                print('go for raise')
        elif len(mx_offers) == 1:
            chosen = mx_offers[0].employer
            print(f'arreeng for work with status {self.is_employed}, worker no {self.id}')
            self.is_employed = True
            chosen.get_answer_from_worker(self, 'agree', of.vacancy)
            print('agreed')
            self.current_wage = mx_offers[0].salary
            self.offers = []
        self.offers = []
        print(len(self.offers),'offers on the way out')
        if not self.is_employed and self.offers:
            self.stage_choose_employer()

    
    def __lt__(self, worker_2):
        if self.current_wage < worker_2.current_wage:
            return True
        return False

    def __gt__(self, worker_2):
        if self.current_wage > worker_2.current_wage:
            return True
        return False

    def __repr__(self):
        return f"Worker {self.id}. type {self.type}, salary {self.current_wage}"


class Offer:
    def __init__(self, employer, vacancy, salary):
        self.salary = salary
        self.employer = employer
        self.vacancy = vacancy
    
    def __lt__(self, offer_2):
        if self.salary < offer_2.salary:
            return True
        return False

    def __gt__(self, offer_2):
        if self.salary > offer_2.salary:
            return True
        return False

    def __repr__(self):
        return f'Offer for {self.salary} from employer {self.employer.uid}'

if __name__=='__main__':
    w1 = Worker(100)
    w2 = Worker(200)
    print(max([w1, w2]))
    print(w1 > w2)
    print(w1 < w2)
