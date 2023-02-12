RAW_TRACE_FOLDER = './local/raw_trace/'
TRACE_FILE_LIST = [f"casa-110108-112108.{i}.blkparse" for i in range(1, 10)]
# TRACE_FILE_LIST = [f"ikki-110108-112108.{i}.blkparse" for i in range(1, 21)]
WRITE_TRACE_PATH = './traces/Home1.lis'


def main():
    access = []
    for raw_trace_file in TRACE_FILE_LIST:
        raw_trace_path = RAW_TRACE_FOLDER + raw_trace_file
        f = open(raw_trace_path, 'r')
        for lines in f.readlines():
            ts, pid, user, offset, size, _1, _2, _3, _4 = lines.split(' ')
            # print(offset, size)
            access.append(int(offset) // 8)
        f.close()
    fw = open(WRITE_TRACE_PATH, 'w')
    print(len(access))
    last = -1
    last_len = 0
    idx = 0
    for order in access:
        if order != last + 1 and last != -1:
            fw.write(f"{str(last - last_len + 1)} {str(last_len)} 0 {idx}\n")
            idx += 1
            last_len = 0
        last = order
        last_len += 1
    fw.close()


if __name__ == "__main__":
    main()
