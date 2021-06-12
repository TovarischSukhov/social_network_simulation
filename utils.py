import itertools
import gurobipy

import cvxpy as cp


from settings import QUALIFICATIONS


flatten = itertools.chain.from_iterable

def make_qualifications_dict_from_market(market: list, return_workers=False):
    ''''
    market = [ (worker, qal, salary) ...]
    returns {qal: [salary, salary ...] ...}
    if return workers also returns [worker, worker ...] in the same orger that in dict
    '''
    m = {}
    workers = []
    for q in QUALIFICATIONS:
        m[q] = [w[2] for w in market if w[1] == q]
        workers.extend([w[0] for w in market if w[1] == q])
    if return_workers:
        return m, workers
    return m


def minimize_costs(total_qualifiation, salaries, change_indexis, qualifications):
    end_prc, end_jun, end_mid = change_indexis
    # Our goal is to find vector x of 1 and 0, where each number corresponds to one worker
    x = cp.Variable(len(salaries), boolean=True)

    # lets make an objestive - to minimize total cost
    objective = cp.Minimize(x.T@salaries)

    # now we have the cost function and we need no minimize it, having limitation for total qalifiation
    # Limitaions
    constraints = [
        # calculate if total qualifiation is less or more than required qualificaton
        x.T@qualifications >= total_qualifiation
    ]

    num_prc = end_prc
    num_jun = end_jun - end_prc
    num_mid = end_mid - end_jun
    num_sen = len(salaries) - end_mid

    additional_constraints = [
        sum(x[end_prc:end_jun]) >= min([2, num_jun]) -1,
        # we require to have not less than one senior and middle per team
        sum(x[end_jun:end_mid]) >= min([2, num_mid])-1,
        sum(x[end_mid:]) >= min([2, num_sen])-1,
    ]
    lengths = [num_jun, num_mid, num_sen]
    additional_constraints = [c for i, c in enumerate(additional_constraints) if lengths[i] != 0]

    # print(lengths)
    # print(additional_constraints)
    # constraints.extend(additional_constraints)

    # print()
    # print(constraints, x)

    # lets define the problem and solve it
    prob = cp.Problem(objective, constraints)
    prob.solve(solver='GUROBI')
    return [round(a) for a in x.value]


def maximize_qualification(budget, qualifications, salaries):
    # end_prc, end_jun, end_mid = change_indexis

    # Our goal is to find vector x of 1 and 0, where each number corresponds to one worker
    x = cp.Variable(len(qualifications), boolean=True)

    # lets make an objestive - to minimize total cost
    objective = cp.Maximize(x.T@qualifications)

    # now we have the cost function and we need no minimize it, having limitation for total qalifiation
    # Limitaions
    constraints = [
        # calculate if total qualifiation is less or more than required qualificaton
        x.T@salaries <= budget
    ]

    # lets define the problem and solve it
    prob = cp.Problem(objective, constraints)

    # print('maximize', budget, qualifications, salaries)
    prob.solve(solver='GUROBI')

    return [round(a) for a in x.value]


def employer_challenge(total_qualifiation, budget, ratios, return_salaries=False):
    '''
    ratios : {'total': total: int, qual: {'ratio':ratio, 'wages':[ ints ]]}}, wages should be sorted ascending order

    ideal configuration - all as in requirenments, but if it is not piossible? or more expensive, then - 
    limitations - total qualification of workers should not be lower than in requirenments
    '''

    # Now lets define optimization problrm. To solve it we will use CVXPY library
    # for each worker we will have binary variable - do ve take him or not
    # we will minimize total salary with respect to the minimal qualification
    # also we will reqire to have at least one peroson of each qualification if it was in requirenments 
    # TODO make possible zero ppl for juniors and practitioners also
    
    # make sure tht we have all qualifications presented in ratios dictionary
    for k in QUALIFICATIONS:
        if k not in ratios:
            ratios[k] = []
    # print(ratios)

    # concatinate all salaries in one array, junes, middles, seniors and cave breaking points for every qualification-change
    salaries = ratios['practice'] + ratios['junior'] + ratios['middle'] + ratios['senior']
    qualifications = list(flatten([[QUALIFICATIONS[q]]*len(ratios[q]) for q in ratios]))

    
    end_prc = len(ratios['practice'])
    end_jun = end_prc + len(ratios['junior'])
    end_mid = end_jun + len(ratios['middle'])

    if total_qualifiation <= 0 or budget <= 0:
        return ([0]*end_prc, [0]*(end_jun - end_prc), [0]*(end_mid - end_jun), [0]*(len(salaries) - end_mid))

    total_qualifiation_on_market = sum(qualifications)
    
    if total_qualifiation_on_market <= total_qualifiation + QUALIFICATIONS['senior'] :
        # print('going to maximze')
        x = maximize_qualification(
                budget, qualifications, 
                # (end_prc, end_jun, end_mid),
                salaries,
            )
    else:
        # print('going to minimize')
        x = minimize_costs(
                total_qualifiation, 
                salaries, 
                (end_prc, end_jun, end_mid),
                qualifications
            )


    if return_salaries:
        mask_salaries = lambda x, sals: [x[i]*sals[i] for i in range(len(sals))]
        return (
                mask_salaries(x[:end_prc], ratios['practice']),
                mask_salaries(x[end_prc:end_jun], ratios['junior']), 
                mask_salaries(x[end_jun:end_mid], ratios['middle']), 
                mask_salaries(x[end_mid:], ratios['senior']) 
            )
    # print(x, ratios)

    return (x[:end_prc], x[end_prc:end_jun], x[end_jun:end_mid], x[end_mid:])


