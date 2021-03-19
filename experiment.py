import matplotlib as plt

from world import World



class Experiment():
    def __init__(self, alpha_range, beta_range, n_iterations=100):
        self.alpha_range = alpha_range
        self.beta_range = beta_range
        self.n_iterations = n_iterations
        self.results = {}

    def run_variation(self, n_iterations, silent=True, **kwargs):
        test_network = World(**kwargs)
        if not silent:
            print(test_network)

        wages = []
        for stage_num in range(n_iterations):
            if not silent:
                print(f'starting stage {stage_num}')
            wages.append(test_network.run_iteration(silent=silent))

        return wages

    def visualize(self):
        pass

    def save(self):
        pass

    def run(self, silent=True):
        for alpha in self.alpha_range:
            for beta in self.beta_range:
                self.results[f'al_{alpha}_bet_{beta}'] = self.run_variation(self.n_iterations, silent=silent, alpha=alpha, beta=beta)

        if not silent:
            print(self.results)

decimal_range_hundreds = lambda s, f, step: [x/100 for x in range(int(s*100), int(f*100 + 1), int(step*100))]


if __name__ == '__main__':
    print(decimal_range_hundreds(0.5, 1., 0.05))
    exp = Experiment(decimal_range_hundreds(0.5, 1., 0.05), decimal_range_hundreds(0.5, 1., 0.05))
    exp.run()

    for r in exp.results:
        print(r, exp.results[r][-1])