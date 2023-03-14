FILE_PATH = "./local/raw_trace/"
FILE_NAME = "human_readable_block_trace_test_example_12"
WRITE_TRACE_PATH = './traces/readseq_2.lis'

def parser():
    blocks = []
    with open(FILE_PATH + FILE_NAME, "r") as f:
        for line in f.readlines():
            items = line.strip().split(',')
            block = items[1]
            blocks.append(block)

    fw = open(WRITE_TRACE_PATH, 'w')
    print(len(blocks))
    last = -1
    last_len = 0
    idx = 0
    for order in blocks:
        fw.write(f"{order} {1} 0 {idx}\n")
        idx += 1
    fw.close()

def concat():
    SEQ = './traces/readseq_1.lis'
    RAND = './traces/readrandom_5.lis'
    seq_list = []
    rand_list = []
    with open(SEQ, "r") as f:
        for line in f.readlines():
            seq_list.append(line.strip().split(' ')[0])
    with open(RAND, "r") as f:
        for line in f.readlines():
            rand_list.append(line.strip().split(' ')[0])
    fw = open('./traces/randseq_1.lis', 'w')
    idx = 0
    for rand in rand_list:
        fw.write(f"{rand} {1} 0 {idx}\n")
        idx += 1
    for seq in seq_list:
        fw.write(f"{seq} {1} 0 {idx}\n")
        idx += 1
    for rand in rand_list:
        fw.write(f"{rand} {1} 0 {idx}\n")
        idx += 1
    print(idx)
    fw.close()

if __name__ == "__main__":
    # parser()
    concat()