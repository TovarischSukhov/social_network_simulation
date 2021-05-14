import matplotlib as plt

from world import World



class Experiment():
    def __init__(self, alpha_range, beta_range, n_iterations=100):
        self.alpha_range = alpha_range
        self.beta_range = beta_range
        self.n_iterations = n_iterations
        self.results = {}
        self.current_world = None
    
    def set_config(self, config):
        self.additional_info = config

    def run_variation(self, n_iterations, silent=True, **kwargs):
        self.current_world  = World(**kwargs)
        print(f'running variation alpha {kwargs["alpha"]}, beta {kwargs["beta"]}')
        if not silent:
            print(self.current_world)

        wages = []
        for stage_num in range(n_iterations):
            # if not silent:
            # print(f'starting stage {stage_num}')
            wages.append(self.current_world.run_iteration(silent=silent))

        return wages

    def visualize(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def run(self, silent=True):
        for alpha in self.alpha_range:
            for beta in self.beta_range:
                self.results[f'al_{alpha}_bet_{beta}'] = self.run_variation(
                    self.n_iterations, silent=silent, alpha=alpha, beta=beta, **self.additional_info
                    )
                print(f'finisched {alpha}, {beta}')
        if not silent:
            print(self.results)

decimal_range_hundreds = lambda s, f, step: [x/100 for x in range(int(s*100), int(f*100 + 1), int(step*100))]


if __name__ == '__main__':
    exp = Experiment(decimal_range_hundreds(0.5, 1.0, 0.05), decimal_range_hundreds(0.5, 1.0, 0.05))
    exp.set_config({
        'no_workers': 1000,
        'no_employers': 100,
        'no_vacancys_per_employer': 10,
        'no_connections': 10,
        'imposter_wage_coeff': 0.7,
    })
    try:
        exp.run()
    except KeyboardInterrupt:
        print(exp.current_world)
        exit(0)

    for r in exp.results:
        print(r, exp.results[r][-1])