import sys
import io
from collections import OrderedDict

def load_fasta(filename) -> OrderedDict:
    reads = OrderedDict()

    with open(filename) as f:
        read_id = None
        content = None

        while True:
            line = f.readline()
            if not line:
                if content:
                    content = ''.join(content)
                    reads[read_id] = content
                break

            if line[0] == ">":
                if content:
                    content = ''.join(content)
                    reads[read_id] = content
                    
                content = []

                read_id = line[1:].rstrip()
            else:
                content.append(line.rstrip())

    return reads

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Wrong argument count")
        exit(1)

    reads_a = load_fasta(sys.argv[1])
    reads_b = load_fasta(sys.argv[2])
    common_ids = set(reads_a.keys()) & set(reads_b.keys())
    
    with open(sys.argv[3], "w") as f:
        for read_id in sorted(common_ids):
            f.write(f">{read_id+read_id}\n")
            f.write(f"{reads_a[read_id]+reads_b[read_id]}\n")
