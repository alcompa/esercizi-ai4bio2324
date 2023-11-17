import sys
from collections import OrderedDict, Counter

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Wrong argument count")
        exit(1)

    GC_THRESHOLD = int(sys.argv[3])

    reads = OrderedDict()
    with open(sys.argv[1]) as fin:
        while True:
            line = fin.readline()
            if not line:
                break

            read_id = line[1:].rstrip()
            reads[read_id] = fin.readline().rstrip()

    bases_stats = Counter(A=0, T=0, C=0, G=0)
    low_comp_count = 0 # n. of reads having at least one low complexity sequence
    high_gc_count = 0 # n. of reads having GC content > GC_THRESHOLD
    high_gc_mapping = OrderedDict()

    for read_id, content in reads.items():
        bases_stats.update(content)

        if any([pattern in content for pattern in ["A"*6, "T"*6, "C"*6, "G"*6]]):
            low_comp_count += 1
        
        gc = content.count("GC")
        if gc > GC_THRESHOLD:
            high_gc_count += 1
            high_gc_mapping[read_id] = gc

    with open(sys.argv[2], "w") as fout:
        fout.write(f"bases stats:\n")
        for base in "ATCG":
            fout.write(f"\t{base}: {bases_stats[base]}\n")
        fout.write(f"n. of low complexity reads: {low_comp_count}\n")
        fout.write(f"n. of high GC reads: {high_gc_count}\n")

        if high_gc_count:
            fout.write(f"high GC reads stats:\n")
            for read_id, gc in high_gc_mapping.items():
                fout.write(f"\t{read_id}: {gc}\n")
