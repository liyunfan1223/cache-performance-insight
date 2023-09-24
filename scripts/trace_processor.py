import os
RAW_TRACE_FOLDER = './local/raw_trace/'
OUTPUT_FOLDER = './traces/'
# TRACE_FILE_LIST = [f"casa-110108-112108.{i}.blkparse" for i in range(1, 10)] # Home1
# TRACE_FILE_LIST = [f"ikki-110108-112108.{i}.blkparse" for i in range(1, 21)] # Home2
# TRACE_FILE_LIST = [f"webresearch-030409-033109.{i}.blkparse" for i in range(1, 29)] # websearch
# TRACE_FILE_LIST = [f"webusers-030409-033109.{i}.blkparse" for i in range(1, 29)] # webusers
TRACE_FILE_LIST = [f"topgun-110108-112108.{i}.blkparse" for i in range(1, 21)] # Home4
# WRITE_TRACE_PATH = './traces/websearch.lis'
WRITE_TRACE_PATH = './traces/Home4.lis'


def process_blkparse(trace_file_list, write_trace_path):
    access = []
    for raw_trace_file in TRACE_FILE_LIST:
        raw_trace_path = RAW_TRACE_FOLDER + raw_trace_file
        if not os.path.exists(raw_trace_path):
            continue
        f = open(raw_trace_path, 'r')
        for lines in f.readlines():
            ts, pid, user, offset, size, _1, _2, _3, _4 = lines.split(' ')
            # print(offset, size)
            access.append((int(offset) // 8, int(size) // 8))
        f.close()
    fw = open(WRITE_TRACE_PATH, 'w')
    print(len(access))
    last = -1
    last_len = 0
    idx = 0
    for order, size in access:
        if order != last + last_len and last_len != 0:
            if last != -1:
                fw.write(f"{str(last)} {str(last_len)} 0 {idx}\n")
            idx += 1
            last_len = 0
            last = order
        # last = order
        last_len += size
    if last_len != 0:
        fw.write(f"{str(last)} {str(last_len)} 0 {idx}\n")
        idx += 1
    print(idx)
    fw.close()

# def process_blkparse_websearch(trace_file_list, write_trace_path):
#     access = []
#     for raw_trace_file in TRACE_FILE_LIST:
#         raw_trace_path = RAW_TRACE_FOLDER + raw_trace_file
#         f = open(raw_trace_path, 'r')
#         for lines in f.readlines():
#             ts, pid, user, offset, size, _1, _2, _3, _4 = lines.split(' ')
#             # print(offset, size)
#             access.append((int(offset) // 8, int(size) // 8))
#         f.close()
#
#     fw = open(WRITE_TRACE_PATH, 'w')
#     print(len(access))
#     last = -1
#     last_len = 0
#     idx = 0
#     for order, size in access:
#         if order != last + 1 and last != -1:
#             fw.write(f"{str(last - last_len + 1)} {str(last_len)} 0 {idx}\n")
#             idx += 1
#             last_len = 0
#         last = order
#         last_len += size
#     fw.close()

def process_ssd_trace(input=None, output=None):
    f = open(input)
    fw = open(output, 'w')
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
        # print(int(ele[7]), int(ele[9]))
        fw.write(f'{offset} {size} 0 {idx}\n')
        # print(offset, size)
        idx += 1
        line = f.readline()
    fw.close()
    f.close()
    print(idx)

def process_msr(input=None, output=None, block=512):
    raw = open(input)
    processed = open(output, 'w')
    access = []
    for idx, line in enumerate(raw.readlines()):
        ts, host, disk_number, type, offset, size, response_time = line.split(',')
        access.append((int(offset) // block, int(size) // block))
        # processed.write(f'{int(offset) // block} {int(size) // block} 0 {idx}\n')
    raw.close()
    print(len(access))
    last = -1
    last_len = 0
    idx = 0
    for order, size in access:
        if order != last + last_len:
            if last != -1:
                processed.write(f"{str(last)} {str(last_len)} 0 {idx}\n")
            idx += 1
            last_len = 0
            last = order
        # last = order
        last_len += size
    if last_len != 0:
        processed.write(f"{str(last)} {str(last_len)} 0 {idx}\n")
        idx += 1
    print(idx)
    processed.close()

if __name__ == "__main__":
    # process_blkparse(TRACE_FILE_LIST, WRITE_TRACE_PATH)
    # process_blkparse(TRACE_FILE_LIST, WRITE_TRACE_PATH)
    # process_ssd_trace(RAW_TRACE_FOLDER + 'ssdtrace-07', './traces/Rocks8.lis')
    # process_msr(RAW_TRACE_FOLDER + 'CAMRESHMSA01-lvm0.csv', OUTPUT_FOLDER + 'msr_hm_0.lis')
    # process_msr(RAW_TRACE_FOLDER + 'CAMRESISAA02-lvm0.csv', OUTPUT_FOLDER + 'msr_prxy_0.lis')
    # process_msr(RAW_TRACE_FOLDER + 'CAM-02-SRV-lvm0.csv', OUTPUT_FOLDER + 'msr_proj_0.lis')
    # process_msr(RAW_TRACE_FOLDER + 'CAMRESWEBA03-lvm0.csv', OUTPUT_FOLDER + 'msr_web_0.lis')
    # process_msr(RAW_TRACE_FOLDER + 'CAMRESWMSA03-lvm0.csv', OUTPUT_FOLDER + 'msr_mds_0.lis')
    # process_msr(RAW_TRACE_FOLDER + 'CAMRESSTGA01-lvm0.csv', OUTPUT_FOLDER + 'msr_stg_0.lis')
    # process_msr(RAW_TRACE_FOLDER + 'CAM-02-SRV-lvm1.csv', OUTPUT_FOLDER + 'msr_proj_1.lis')
    process_msr(RAW_TRACE_FOLDER + 'CAM-01-SRV-lvm1.csv', OUTPUT_FOLDER + 'msr_usr_1.lis', 4096)