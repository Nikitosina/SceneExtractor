import scenedetect
from scenedetect import save_images
from moviepy.editor import VideoFileClip
from scenedetect.frame_timecode import FrameTimecode
import random
from random import randint
import os
import subprocess

random.seed(123)

def caption_and_save_clips(video_path, timecodes, output_folder, black_and_white: bool = False) -> list:
    """ Returns array [["videoid", "duration", "page_dir", "name"]] """
    result_data = []
    video = VideoFileClip(video_path)
    # video = moviepy.video.fx.all.blackwhite(video, RGB=None)#, preserve_luinosity=True)

    for i, (start_time, end_time) in enumerate(timecodes):
        page_dir, video_id = f"{randint(1, 999999):06}_{randint(1, 999999):06}", randint(1, 2000000000)
        video_clip = video.subclip(start_time, end_time)
        
        folder_path = f"{output_folder}/{page_dir}"
        output_filename = f"{folder_path}/{video_id}.mp4"
        
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        video_clip.write_videofile(output_filename, codec='libx264')

        # cwd = os.getcwd()
        # os.chdir("../VILA")
        # caption = caption_video_VILA("../SceneExtractor/" + output_filename)
        # os.chdir(cwd)
        result_data.append([video_id, duration_to_iso(int(video_clip.duration)), page_dir, ""])
        
        print(f"Segment {i+1} saved as {output_filename}")

    video.close()
    return result_data


def extract_timecodes(video_path: str, scene_limit: int = None) -> list[tuple[str, str]]:
    scene_list = scenedetect.detect(video_path, scenedetect.ContentDetector(threshold=32, min_scene_len=30))

    small_batch = scene_list
    if scene_limit:
        small_batch = small_batch[:scene_limit]
    small_batch = list(map(lambda x: (FrameTimecode(x[0].frame_num + 1, fps=x[0].framerate), x[1]), small_batch))
    timecodes = map(lambda x: (x[0].get_timecode(), x[1].get_timecode()), small_batch)
    print(small_batch)
    return timecodes


def caption_video_VILA(video_path: str):
    eval_script_path = "llava/eval/run_vila.py"
    model_path = "VILA1.5-3b"
    query = "Give a concise caption"

    command = f"""python -W ignore {eval_script_path} --model-path {model_path} --conv-mode vicuna_v1 --query "<video>{query}" --video-file {video_path}"""
    try:
        out = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True).decode()
        print(out.split("\n")[-2])
        return out.split("\n")[-2]
    except subprocess.CalledProcessError as e:
        print(e.output.decode("utf-8"))
        exit(1)


def duration_to_iso(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"PT{hours:02d}H{minutes:02d}M{seconds:02d}S"

# python -W ignore llava/eval/run_vila.py \
#     --model-path Efficient-Large-Model/VILA1.5-3b \
#     --conv-mode vicuna_v1 \
#     --query "<video>\n Please describe this video." \
#     --video-file "demo.mp4"

# video = VideoFileClip(video_path)
# print(video.reader.nframes)
# for frame in video.iter_frames():
#     plt.imshow(frame, interpolation ='nearest') 
#     plt.show()

# for item in small_batch:
#     frame = video.frame get_frame(item[0].frame_num)
    # print(item[0].frame_num)
    # plt.imshow(frame, interpolation ='nearest') 
    # plt.show()

# converted_timecodes = [(sum(x * int(t) for x, t in zip([3600, 60, 1], start.split(':'))),
#                          sum(x * int(t) for x, t in zip([3600, 60, 1], end.split(':'))))
#                         for start, end in timecodes]

# split_video(video_path, timecodes, output_folder)

# 2(1) In the video, a green alien is seen standing on a grassy field and then suddenly appears in a cartoon. The cartoon shows a green alien fighting a character in a red suit. The green alien is seen hitting the red character with a hammer and then picking him up and throwing him.
# 