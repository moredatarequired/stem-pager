import counter_stats
import lemmatizer
import sys

benchmarks = [0.01 * n for n in range(0, 100)]

if len(sys.argv) > 1:
    header = 'book ' + counter_stats.short_table_header(benchmarks)
    print(','.join(header.split()))
    for filename in sys.argv[1:]:
        name = '_'.join(filename.split())
        row = name + ' ' + counter_stats.short_table(lemmatizer.examine(filename), benchmarks)
        print(','.join(row.split()))
