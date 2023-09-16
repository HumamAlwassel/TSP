from __future__ import division, print_function

import argparse
import os
import ffmpeg
import pandas as pd

from tqdm import tqdm
from pathlib import Path


def main(args):
    print(args)

    video_path_list = list(Path(args.video_folder).rglob(f"*.{args.ext}"))
    
    output_dict = {
        "filename": [],
        "video-duration": [],
        "fps": [],
        "video-frames": []
    }
    for video_path in tqdm(video_path_list, total=len(video_path_list)):
        video_path = str(video_path)

        try:
            video_info = ffmpeg.probe(video_path)
        except:
            print("Error in video:", video_path)
            continue

        video_fps = video_info["streams"][0]["r_frame_rate"]
        video_fps = int(video_fps.split("/")[0]) / int(video_fps.split("/")[1])

        video_frames = int(video_info["streams"][0]["nb_frames"])

        output_dict["filename"].append(os.path.basename(video_path))
        output_dict["video-duration"].append(video_frames / video_fps)
        output_dict["fps"].append(video_fps)
        output_dict["video-frames"].append(video_frames)

    df = pd.DataFrame(output_dict)
    df.to_csv(args.output_csv, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates a metadata CSV file with columns '
                                                 '[filename, video-duration, fps, video-frames] '
                                                 'for a given input video folder.')

    parser.add_argument('--video-folder', required=True, type=str,
                      help='Path to folder containing the raw video files')
    parser.add_argument('--ext', default='mp4', type=str,
                      help='Video files extension (default: mp4)')
    parser.add_argument('--output-csv', required=True, type=str,
                      help='Where to save the metadata CSV file')
    parser.add_argument('--workers', default=20, type=int,
                      help='Number of parallel processes to use to generate the output (default: 20)')

    args = parser.parse_args()

    main(args)
