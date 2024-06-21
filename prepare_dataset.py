import pandas as pd
from split_video import *
import csv

result_data = [["videoid", "duration", "page_dir", "name"]]
n = 1 # 206
foldername = "raw"
format = "mkv"
output_csv = "dataset.csv"

if os.path.exists(output_csv):
    os.remove(output_csv)

for i in range(n):
    # filename = f"[Beatrice-Raws] One Piece {(i + 1):03} [DVDRip 768x576 x264 AC3].{format}"
    filename = f"one_piece_00{i + 1}.mkv"
    # filename = f"one_piece_00{i + 1}_trimmed.mp4"
    video_path = foldername + "/" + filename
    timecodes = extract_timecodes(video_path) #, scene_limit=5)
    result_list = caption_and_save_clips(video_path, timecodes=timecodes, output_folder="output")
    result_data.extend(result_list)

    with open(output_csv, "a") as out:
        csvWriter = csv.writer(out, delimiter=',')
        csvWriter.writerows(result_data)

    result_data = []
