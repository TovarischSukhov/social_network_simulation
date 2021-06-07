import random


class Worker():
    def __init__(
            self, 
            current_wage: int, 
            utype:str = "normal", 
            tell_wage: float = 1, 
            _id: int = None, 
            self_esteem_coefficients: dict = {}
        ):
        self.id = _id or random.randint(0, 10000)

        self.current_wage = current_wage
        self.previous_wage = current_wage
        self.type = utype
        self.tell_wage_coeff = tell_wage
        try:
            self.self_esteem_coefficient = self_esteem_coefficients[utype]
        except KeyError:
            raise "No such self esteem type or no coefficients given"

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
        self.offers = []
        self.previous_wage = self.current_wage

    
    def _count_new_wage(self):
        self.others_wage = [w for w in self.others_wage if w]
        if self.others_wage:
            self.current_wage = sum(self.others_wage) * self.self_esteem_coefficient /len(self.others_wage)

    def give_employer_wage(self):
        return self.current_wage

    def give_wage(self):
        if random.random() <= self.tell_wage_coeff:
            return self.previous_wage 
    
    def stage_wage_recearch(self, wages: list=[]):
        self.others_wage = wages
        self._count_new_wage()

    def recieve_offer(self, employer, vacancy, salary):
        ''''Method used by Employer to send job offer to Worker'''
        offer = Offer(employer, vacancy, salary)
        self.offers.append(offer)

    def stage_choose_employer(self):
        '''Method used by World to cover stage 3 of simulation'''
        # print(self, 'choosing job, got offres', self.offers)
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
                # print('go for raise')
        elif len(mx_offers) == 1:
            chosen = mx_offers[0].employer
            # print(f'arreeng for work with status {self.is_employed}, worker no {self.id}')
            self.is_employed = True
            chosen.get_answer_from_worker(self, 'agree', of.vacancy)
            # print('agreed')
            self.current_wage = mx_offers[0].salary
            self.offers = []
        # self.offers = []
        # print(len(self.offers),'offers on the way out')
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
    self_esteem_coefficients = {
            "normal":  1,
            "imposter": 0.9
        }
    w_imposter = Worker(current_wage=100, utype="imposter", 
        tell_wage=1, _id='test_1', self_esteem_coefficients=self_esteem_coefficients
        )

