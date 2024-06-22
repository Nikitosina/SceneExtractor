from split_video import *
import csv

result_data = [["videoid", "duration", "page_dir", "name"]]
n = 5 # 206
foldername = "raw"
format = "mkv"

if not os.path.exists("raw"):
    print("create folder \"raw\" and put input videos there")
    exit(1)

if not os.path.exists("output"):
    os.mkdir("output")

if not os.path.exists("csv_no_caption"):
    os.mkdir("csv_no_caption")

for i in range(0, n):
    filename = f"[Beatrice-Raws] One Piece {(i + 1):03} [DVDRip 768x576 x264 AC3].{format}"
    # filename = f"one_piece_00{i + 1}_trimmed.mp4"
    video_path = foldername + "/" + filename
    timecodes = extract_timecodes(video_path, skip_intro=True) #, scene_limit=5)
    result_list = caption_and_save_clips(video_path, timecodes=timecodes, output_folder="output")
    result_data.extend(result_list)

    output_csv = f"csv_no_caption/dataset_{(i + 1):03}.csv"
    with open(output_csv, "w") as out:
        csvWriter = csv.writer(out, delimiter=',')
        csvWriter.writerows(result_data)

    result_data = [["videoid", "duration", "page_dir", "name"]]
