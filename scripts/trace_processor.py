RAW_TRACE_FOLDER = './local/raw_trace/'
TRACE_FILE_LIST = [f"casa-110108-112108.{i}.blkparse" for i in range(1, 10)]
# TRACE_FILE_LIST = [f"ikki-110108-112108.{i}.blkparse" for i in range(1, 21)]
WRITE_TRACE_PATH = './traces/Home1.lis'


def process_blkparse(trace_file_list, write_trace_path):
    access = []
    for raw_trace_file in TRACE_FILE_LIST:
        raw_trace_path = RAW_TRACE_FOLDER + raw_trace_file
        f = open(raw_trace_path, 'r')
        for lines in f.readlines():
            ts, pid, user, offset, size, _1, _2, _3, _4 = lines.split(' ')
            # print(offset, size)
            access.append((int(offset), int(size)))
        f.close()
    fw = open(WRITE_TRACE_PATH, 'w')
    print(len(access))
    last = -1
    last_len = 0
    idx = 0
    for order, size in access:
        if order != last + 1 and last != -1:
            fw.write(f"{str(last - last_len + 1)} {str(last_len)} 0 {idx}\n")
            idx += 1
            last_len = 0
        last = order
        last_len += size
    fw.close()

def process_ssd_trace():
    f = open(RAW_TRACE_FOLDER + 'ssdtrace-00')
    # fw = open('./traces/Rocks1.lis', 'w')
    line = f.readline()
    idx = 0
    while line:
        ele = line.split(' ')
        while '' in ele:
            ele.remove('')
        if len(ele) != 11:
            line = f.readline()
            continue
        if ele[5] != 'D':
            line = f.readline()
            continue
        if ele[10].find('rocksdb') == -1:
            line = f.readline()
            continue
        offset = int(ele[7]) // 8
        size = int(ele[9]) // 8
        print(int(ele[7]), int(ele[9]))
        # fw.write(f'{offset} {size} 0 {idx}\n')
        # print(offset, size)
        idx += 1
        line = f.readline()
    # fw.close()
    f.close()

if __name__ == "__main__":
    # process(TRACE_FILE_LIST, WRITE_TRACE_PATH)
    process_ssd_trace()