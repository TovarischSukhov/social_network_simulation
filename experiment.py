import json

from world import World


class Experiment():
    def __init__(self, alpha_range, beta_range, n_iterations=100, early_stop=None, exp_no=None):
        self.alpha_range = alpha_range
        self.beta_range = beta_range
        self.n_iterations = n_iterations
        self.results = {}
        self.early_stop = early_stop
        self.exp_no = exp_no

    def set_config(self, config):
        self.additional_info = config

    def run_variation(self, n_iterations, silent=True, **kwargs):
        test_network = World(**kwargs)
        print(f'running variation alpha {kwargs["alpha"]}, beta {kwargs["beta"]}')
        if not silent:
            print(test_network)

        wages = []
        for stage_num in range(n_iterations):
            if not silent:
                print(f'starting stage {stage_num}')
            wages.append(test_network.run_iteration(silent=silent))
            print(wages[-1])
            print([w > self.early_stop for _, w in wages[-1].items()])
            if self.early_stop and any(
                w > self.early_stop for _, w in wages[-1].items()
                ):
                break

        return wages

    def visualize(self):
        raise NotImplementedError

    def save(self, exp):
        res = {}
        with open(f"./data/{exp}_exp_{self.exp_no}.json", "w") as f:
            results = self.results[exp]
            re = {'junior':[],'middle':[],'senior':[]}
            for r in results:
                re['junior'].append(r['junior'])
                re['middle'].append(r['middle'])
                re['senior'].append(r['senior'])
            json.dump(re, f)

    def run(self, silent=True):
        for alpha in self.alpha_range:
            for beta in self.beta_range:
                self.results[f'al_{alpha}_bet_{beta}'] = self.run_variation(
                    self.n_iterations, silent=silent, alpha=alpha, beta=beta, **self.additional_info
                    )
                self.save(f'al_{alpha}_bet_{beta}')

        if not silent:
            print(self.results)

decimal_range_hundreds = lambda s, f, step: [x/100 for x in range(int(s*100), int(f*100 + 1), int(step*100))]


if __name__ == '__main__':
    qualification_ratio={'junior': 0.5, 'middle': .3, 'senior': 0.2}
    exp = Experiment([1.0],[0.5], n_iterations=5, early_stop=10**6, exp_no=0)
    exp.set_config({
            'no_workers': 20,
            'no_employers': 1,
            'no_connections': 20,
            'qualification_ratio':qualification_ratio
        })

    exp.run()


    qualification_ratio={'junior': 0.5, 'middle': .3, 'senior': 0.2}
    exp = Experiment([1.0],[0.5, 0.8, 0.84, 0.9, 1.0], n_iterations=100, early_stop=10**6, exp_no=1)
    exp.set_config({
            'no_workers': 100,
            'no_employers': 10,
            'no_connections': 10,
            'qualification_ratio':qualification_ratio
        })

    exp.run()

    for r in exp.results:
        print(r, exp.results[r][-1])

    qualification_ratio={'junior': 0.5, 'middle': .3, 'senior': 0.2}
    exp = Experiment([0.5, 0.8, 0.9, 1.0],[0.84], n_iterations=100, early_stop=10**6, exp_no=1.5)
    exp.set_config({
            'no_workers': 100,
            'no_employers': 10,
            'no_connections': 10,
            'qualification_ratio':qualification_ratio
        })

    exp.run()

    for r in exp.results:
        print(r, exp.results[r][-1])

    qualification_ratio={'junior': 0.5, 'middle': .3, 'senior': 0.2}
    exp = Experiment([1.0],[0.84], n_iterations=100, early_stop=10**6, exp_no=2)
    exp.set_config({
            'no_workers': 100,
            'no_employers': 20,
            'no_connections': 10,
            'qualification_ratio':qualification_ratio
        })

    exp.run()

    for r in exp.results:
        print(r, exp.results[r][-1])


    qualification_ratio={'junior': 0.55, 'middle': .35, 'senior': 0.1}
    exp = Experiment([1.0],[0.84], n_iterations=100, early_stop=10**6, exp_no=3)
    exp.set_config({
            'no_workers': 100,
            'no_employers': 10,
            'no_connections': 10,
            'qualification_ratio':qualification_ratio
        })

    exp.run()

    for r in exp.results:
        print(r, exp.results[r][-1])

    qualification_ratio={'junior': 0.6, 'middle': .25, 'senior': 0.15}
    exp = Experiment([1.0],[0.84], n_iterations=100, early_stop=10**6, exp_no=4)
    exp.set_config({
            'no_workers': 100,
            'no_employers': 10,
            'no_connections': 10,
            'qualification_ratio':qualification_ratio
        })

    exp.run()

    for r in exp.results:
        print(r, exp.results[r][-1])


    qualification_ratio={'junior': 0.5, 'middle': .3, 'senior': 0.2}
    exp = Experiment([1.0],[0.84], n_iterations=100, early_stop=10**6, exp_no=5)
    exp.set_config({
            'no_workers': 200,
            'no_employers': 10,
            'no_connections': 10,
            'qualification_ratio':qualification_ratio
        })

    exp.run()

    for r in exp.results:
        print(r, exp.results[r][-1])


    qualification_ratio={'junior': 0.5, 'middle': .3, 'senior': 0.2}
    exp = Experiment([1.0],[0.84], n_iterations=100, early_stop=10**6, exp_no=6)
    exp.set_config({
            'no_workers': 100,
            'no_employers': 10,
            'no_connections': 20,
            'qualification_ratio':qualification_ratio
        })

    exp.run()

    for r in exp.results:
        print(r, exp.results[r][-1])


    qualification_ratio={'junior': 0.5, 'middle': .3, 'senior': 0.2}
    exp = Experiment([1.0],[0.84], n_iterations=100, early_stop=10**6, exp_no=7)
    exp.set_config({
            'no_workers': 100,
            'no_employers': 10,
            'no_connections': 5,
            'qualification_ratio':qualification_ratio
        })

    exp.run()

    for r in exp.results:
        print(r, exp.results[r][-1])


    qualification_ratio={'junior': 0.5, 'middle': .3, 'senior': 0.2}
    exp = Experiment([1.0],[0.84], n_iterations=100, early_stop=10**6, exp_no=8)
    exp.set_config({
            'no_workers': 50,
            'no_employers': 10,
            'no_connections': 10,
            'qualification_ratio':qualification_ratio
        })

    exp.run()

    for r in exp.results:
        print(r, exp.results[r][-1])