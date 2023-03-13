FILE_PATH = "./local/raw_trace/"
FILE_NAME = "human_readable_block_trace_test_example_6"
WRITE_TRACE_PATH = './traces/readrandom_7.lis'

if __name__ == "__main__":
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
