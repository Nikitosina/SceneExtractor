from split_video import extract_timecodes, caption_and_save_clips
from post_processing import post_process_csv
import os
import csv
import torch
import subprocess
import sys
import time
import multiprocessing

foldername = "raw"
format = "mp4"

output_folder = "output_bw"
output_csv_folder = "csv_no_caption_bw"

if not os.path.exists("raw"):
    print("create folder \"raw\" and put input videos there")
    exit(1)

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

if not os.path.exists(output_csv_folder):
    os.mkdir(output_csv_folder)

def split_videos(start: int, end: int):
    torch.set_default_device("mps")
    result_data = [["videoid", "duration", "page_dir", "name"]]
    for i in range(start, end):
        filename = f"One Piece - {(i + 1):03} (1280x720 x264 AAC) [yibis].{format}"
        # filename = f"one_piece_00{i + 1}_trimmed.mp4"        
        video_path = foldername + "/" + filename
        if not os.path.exists(video_path):
            continue
        t0 = time.time()
        timecodes = extract_timecodes(video_path, skip_intro=True) #, scene_limit=5)
        t0 = time.time() - t0
        print(f"TIME {start * 27 - 585}: {t0}")
        result_list = caption_and_save_clips(video_path, timecodes=timecodes, output_folder=output_folder, bad_videos_folder=f"bad_videos/{(i + 1):03}")
        result_data.extend(result_list)

        output_csv = f"{output_csv_folder}/dataset_{(i + 1):03}.csv"
        with open(output_csv, "w") as out:
            csvWriter = csv.writer(out, delimiter=',')
            csvWriter.writerows(result_data)

# cwd = os.getcwd()
# os.chdir("../VILA")
# sys.path.append('../VILA')
# command = 'python -W ignore llava/eval/run_vila.py --query "<video>\n Provide a concise caption of the action" --input-csv-folder "../SceneExtractor/csv_no_caption_bw/"'
# proc = subprocess.Popen(command, shell=True)
# proc.communicate()
# os.chdir(cwd)

# for i in range(0, n):
#     output_csv = f"output_csv_bw/dataset_{(i + 1):03}.csv"
#     post_process_csv(input_path=output_csv)

if __name__ == "__main__":
    # Start = real video number - 1, end = real video number
    start, end = 578, 750
    threads_n = 6

    batch = int((end - start) / threads_n)
    for i in range(threads_n):
        from_i = (i * batch) + start
        to_i = ((i + 1) * batch) + start if i != threads_n - 1 else end
        t1 = multiprocessing.Process(name=f"Hello{i}", target=split_videos, args=[from_i, to_i])
        t1.start()
        print(f"Started {i}th thread with range: {from_i, to_i}")
