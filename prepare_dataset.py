from split_video import *
import csv

result_data = [["videoid", "duration", "page_dir", "name"]]
n = 1 # 206
foldername = "raw"
format = "mkv"

output_folder = "output_bw"
output_csv_folder = "csv_no_caption_bw"

if not os.path.exists("raw"):
    print("create folder \"raw\" and put input videos there")
    exit(1)

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

if not os.path.exists(output_csv_folder):
    os.mkdir(output_csv_folder)

for i in range(0, n):
    filename = f"[Beatrice-Raws] One Piece {(i + 1):03} [DVDRip 768x576 x264 AC3].{format}"
    # filename = f"one_piece_00{i + 1}_trimmed.mp4"
    video_path = foldername + "/" + filename
    timecodes = extract_timecodes(video_path, skip_intro=True) #, scene_limit=5)
    result_list = caption_and_save_clips(video_path, timecodes=timecodes, output_folder=output_folder)
    result_data.extend(result_list)

    output_csv = f"{output_csv_folder}/dataset_{(i + 1):03}.csv"
    with open(output_csv, "w") as out:
        csvWriter = csv.writer(out, delimiter=',')
        csvWriter.writerows(result_data)

    result_data = [["videoid", "duration", "page_dir", "name"]]
