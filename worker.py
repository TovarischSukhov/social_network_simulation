import random

# qualification levels should be in accending order
QUALIFICATIONS = ['practice', 'junior', 'middle', 'senior']

SELFESTEEM_QUALIFICATION_MOVE = {
    'normal': 0,
    'imposter': -1 # imposter thinks that he is one qalification lever lower than it is in reality
}

class Worker():
    def __init__(self, current_wage, qualification, utype="normal", tell_wage=1, _id=None):
        self.id = _id or random.randint(0, 10000)

        # TODO возможео имеет смысл зп отличать зп когда работает или когда просто хочет
        self.current_wage = current_wage
        self.type = utype
        self.tell_wage_coeff = tell_wage

        # check if qualification was initialised correctly
        if qualification not in QUALIFICATIONS:
            raise KeyError('Unknown qualification level')
        self.real_qualification = qualification

        # count how person estimates his qualification
        new_qualification_index = QUALIFICATIONS.index(qualification) + SELFESTEEM_QUALIFICATION_MOVE[utype]
        self.self_esteemed_qualification = QUALIFICATIONS[new_index]

        # TODO also here would be great to have all friends ?
        self.others_qualifications_wages = [] # [(qual: str, wage: int), (...)]
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
        '''
        Method used by Employer to find out current wages level
        returns: qualification_level, wage
        '''
        return self.self_esteemed_qualification, self.current_wage

    def give_wage(self):
        '''
        Method used by Worker to find out current wages level
        returns: qualification_level, wage or None
        '''
        if random.random() <= self.tell_wage_coeff:
            return self.self_esteemed_qualification, self.current_wage 
    
    def stage_wage_recearch(self, qualifications_wages: list=[]):
        ''' Mehtod used by World to give Worker wages of surrounding Workers
        '''
        self.others_qualifications_wages = qualifications_wages
        self._count_new_wage()

    def recieve_offer(self, employer, vacancy, salary):
        ''''Method used by Employer to send job offer to Worker'''
        offer = Offer(employer, vacancy, salary)
        self.offers.append(offer)

    def stage_choose_employer(self):
        '''
        Method used by World to cover stage 3 of simulation
        Worker already have all the offers and need to choose the employer
        if there are several employers that offers the same amoutn of money, worker choose randomly
        '''
        mx_offers = []
        mx_sal = 0
        for of in self.offers:
            if of.salary > mx_sal:
                mx_sal = of.salary
                mx_offers = []
            if of.salary == mx_sal:
                mx_offers.append(of)
        
        if len(mx_offers) > 0:
            self.offers = []
            random.choice(mx_offers).employer.get_answer_from_worker(self, 'agree', of.vacancy)
            print('agreed random')
        print(len(self.offers),'offers on the way out')
        if not self.is_employed and self.offers:
            self.stage_choose_employer()

    
    def __lt__(self, worker_2):
        '''comparing two workers by <> signes, commaring by their current wages'''
        if self.current_wage < worker_2.current_wage:
            return True
        return False

    def __gt__(self, worker_2):
        '''comparing two workers by <> signes, commaring by their current wages'''
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
