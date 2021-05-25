import random

from utils import employer_challenge, make_qualifications_dict_from_market
from settings import QUALIFICATIONS, SELFESTEEM_QUALIFICATION_MOVE

class Worker():
    def __init__(
            self, 
            current_wage: int, 
            qualification: str,
            utype:str = "normal", 
            tell_wage: float = 1, 
            _id: int = None,
            employer_requrnments: dict = {},
        ):
        self.id = _id or random.randint(0, 10000)

        # TODO возможео имеет смысл зп отличать зп когда работает или когда просто хочет
        self.current_wage = current_wage
        self.next_iter_wage = current_wage
        self.type = utype
        self.tell_wage_coeff = tell_wage

        # wrold gives info about what employer need, TODO later possible to change it on each iteration
        self.employer_requrnments = employer_requrnments
        self.total_qualifiation_needed = sum([ employer_requrnments[q] * QUALIFICATIONS[q] for q in employer_requrnments]) 

        # check if qualification was initialised correctly
        if qualification not in QUALIFICATIONS:
            raise KeyError('Unknown qualification level')
        self.real_qualification = qualification

        # count how person estimates his qualification
        new_qualification_index = list(QUALIFICATIONS.keys()).index(qualification) + SELFESTEEM_QUALIFICATION_MOVE[utype]
        self.self_esteemed_qualification = list(QUALIFICATIONS.keys())[new_qualification_index]

        # TODO also here would be great to have all friends ?
        self.others_qualifications_wages = [] # [{totla: ttl:int, qal_lvl: {workers:[salary_1:int, ...] } }]
        self.offers = []

        self.is_employed = False
        self.employer_budget = 0

        # historical data
        self.wage_history = []
        self.employnment_history = []


    def new_cycle(self):
        '''Method used by World to drop state between iterations'''
        self.wage_history.append(self.current_wage)
        self.employnment_history.append(self.is_employed)
        self.is_employed = False
        self.current_wage = self.next_iter_wage

    def _fit_market(self, steps, salary, employer_answer=None, change=0, prev_salary=None ):
        ''''
        this is recursive function to calulate optimal salary, considering current market
        worker maximizes his  salary, considering that eployer will see the same market
        '''
        # print('     git in', steps, salary, employer_answer, change, prev_salary)
        coeff = {0:-1, 1:1}

        # add worker to the observed market
        self.others_qualifications_wages[self.self_esteemed_qualification].append(salary)
        
        # first worker thinks as employer and calculates who from the market will employer hire
        employment = {}
        employment['practice'], employment['junior'], employment['middle'], employment['senior'] = employer_challenge(
                self.total_qualifiation_needed, 
                self.employer_budget,
                self.others_qualifications_wages, 
                
            )
        last_employer_answer = employer_answer
        # take the decision of employer on your salary
        employer_answer = employment[self.self_esteemed_qualification][-1]

        # see if the decision was changed, if yes, we decrease step
        if last_employer_answer and employer_answer != last_employer_answer:
            change += 1
            # if we already mede all the steps, we need to return the salary
            if change >= len(steps):
                # if on the last step we would bave been hired, we return last salary
                print(salary, prev_salary, employer_answer)
                if employer_answer == 1:
                    self.next_iter_wage = salary
                    return
                # as we git here only on change of employers desision, if on this step worker wouldn't bave been hired
                # it means that on previous he would have been hired and we need that salary
                else:
                    self.next_iter_wage = prev_salary
                    return

        # update salary. If employer would have hired worker with current salary, on next iteration he will ask for more
        # if not - worker will try to ask less. Each time the decision is chnged, we decrease step
        # we save previous salary, bevore updating
        prev_salay = salary
        # print(steps, 'idx', change, 'cf', coeff,'idx', employer_answer)
        # print('prev salary', prev_salay, 'salary', salary, 'went for', steps[change], coeff[employer_answer] )
        # print('currnt answer',employer_answer, 'prev answer',  last_employer_answer, 'change no', change)
        
        salary  = (coeff[employer_answer] * steps[change] + 1) * salary
        # print('prev salary', prev_salay, 'salary', salary, 'went for', steps[change], coeff[employer_answer] )
        # print('currnt answer',employer_answer, 'prev answer',  last_employer_answer, 'change no', change)

        # delete previous salary of this worker from the observed market
        self.others_qualifications_wages[self.self_esteemed_qualification].pop(-1)

        self._fit_market(steps, salary, employer_answer=employer_answer, change=change, prev_salary=prev_salay)

    
    def _count_new_wage(self):
        if self.others_qualifications_wages:
            
            self.others_qualifications_wages = make_qualifications_dict_from_market(self.others_qualifications_wages)
            steps = [0.1, 0.05, 0.01]
            self._fit_market(steps, self.current_wage)


    def give_employer_qualification_wage(self):
        '''
        Method used by Employer to find out current wages level
        returns: qualification_level, wage
        '''
        return self, self.real_qualification, self.next_iter_wage

    def give_qualification_wage(self):
        '''
        Method used by Worker to find out current wages level
        returns: qualification_level, wage or None
        '''
        if random.random() <= self.tell_wage_coeff:
            return self, self.self_esteemed_qualification, self.current_wage 
    
    def stage_wage_recearch(self, qualifications_wages: list, market_data:dict):
        ''' Mehtod used by World to give Worker wages of surrounding Workers
        '''
        self.others_qualifications_wages = qualifications_wages
        self.employer_budget = [self.employer_requrnments[q] * market_data[q] for q in self.employer_requrnments]
        self._count_new_wage()
        

    def recieve_offer(self, employer, salary):
        ''''Method used by Employer to send job offer to Worker'''
        offer = Offer(employer, salary)
        self.offers.append(offer)

    def stage_choose_employer(self):
        '''
        Method used by World to cover stage 3 of simulation
        Worker already have all the offers and need to choose the employer
        if there are several employers that offers the same amoutn of money, worker choose randomly
        '''
        # mx_offers = []
        # mx_sal = 0
        # for of in self.offers:
        #     if of.salary > mx_sal:
        #         mx_sal = of.salary
        #         mx_offers = []
        #     if of.salary == mx_sal:
        #         mx_offers.append(of)
        print(self.offers)
        if len(self.offers) > 0:
            random.choice(self.offers).employer.get_answer_from_worker(self)
            print('agreed random')
            self.is_employed = True
            self.offers = []
        # print(len(self.offers),'offers on the way out')
        # if not self.is_employed and self.offers:
        #     self.stage_choose_employer()

    
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
    def __init__(self, employer, salary):
        self.salary = salary
        self.employer = employer
        # self.vacancy = vacancy
    
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
