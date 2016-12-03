from collections import Counter

def normalize_counter(counter):
    'Normalize counts in a counter to sum to 1'
    total = sum(c for _, c in counter.most_common())
    float_counter = Counter()
    for k, v in counter.items():
        float_counter[k] = v / total
    return float_counter

def cumulative_table(counter):
    total = sum(c for _, c in counter.most_common())
    covered = 0
    table = []
    for item, count in counter.most_common():
        covered += count
        table.append((item, count, count / total, covered / total))
    return table

def at_percentile(table, percent):
    for i, row in enumerate(table):
        item, count, perc, cumu = row
        if cumu >= percent:
            return i + 1, item, count, perc, cumu

_default_benchmarks = [0.25, 0.5, 0.75, 0.85, 0.9, 0.925, 0.95, 0.965, 0.98, 0.99, 0.999, 1.0]
def full_table(counter, benchmarks=None):
    if not benchmarks:
        benchmarks = _default_benchmarks
    table = cumulative_table(counter)
    print('cum%\tindex\titem\t\t#\tevery')
    for mark in benchmarks:
        index, item, count, perc, cumu = at_percentile(table, mark)
        print('{:.3f}\t{}\t{:16}{}\t{}'.format(cumu, index, item, count, int(1/perc)))

def short_table_header(benchmarks=None):
    if not benchmarks:
        benchmarks = _default_benchmarks
    return '\t'.join('{:.3f}'.format(mark) for mark in benchmarks)

def short_table(counter, benchmarks=None):
    if not benchmarks:
        benchmarks = _default_benchmarks
    table = cumulative_table(counter)
    return '\t'.join(str(at_percentile(table, mark)[0]) for mark in benchmarks)
