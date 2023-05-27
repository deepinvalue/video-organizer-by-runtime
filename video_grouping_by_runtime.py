import cv2
from pathlib import Path


def group_videos_by_runtime(input_dir, output_dir='groups/', *, group_duration_minutes=60,
                            video_extension='.mp4', subtitle_extension=None):

    print(f'Starting video grouping with the following parameters:')
    print(f'Input Directory: {input_dir}')
    print(f'Output Directory: {output_dir}')
    print(f'Group Duration (minutes): {group_duration_minutes}')
    print(f'Video Extension: {video_extension}')
    print(f'Subtitle Extension: {subtitle_extension}\n')

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    if not output_dir.is_absolute():
        output_dir = input_dir / output_dir
    output_dir.mkdir(exist_ok=True)

    if not video_extension.startswith('.'):
        video_extension = '.' + video_extension
    if not subtitle_extension.startswith('.'):
        subtitle_extension = '.' + subtitle_extension

    total_duration_seconds = 0
    for video_file in sorted(input_dir.glob(fr'*{video_extension}')):
        video = cv2.VideoCapture(str(video_file))
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = video.get(cv2.CAP_PROP_FPS)

        # Update total duration with the duration of the current video
        total_duration_seconds += frame_count / fps

        # Determine group number based on total duration and chunk size
        group_number = int(total_duration_seconds / (group_duration_minutes*60)) + 1
        group_name = f'Group {group_number:0>2}'

        # Create symbolic links for the video and subtitle files in their respective groups
        video_link = output_dir / group_name / video_file.name
        video_link.parent.mkdir(exist_ok=True)
        video_link.symlink_to(video_file)

        # Get all subtitle files matching the video file stem
        subtitle_files = list(input_dir.glob(video_file.stem + '*' + subtitle_extension))

        if subtitle_files:
            # If there's only one subtitle file, ignore its original suffix and use video file stem
            if len(subtitle_files) == 1:
                subtitle_link = video_link.with_suffix(subtitle_extension)
                subtitle_link.symlink_to(subtitle_files[0])
            else:
                # If multiple subtitles exist, maintain their original names
                for subtitle_file in subtitle_files:
                    subtitle_link = output_dir / group_name / subtitle_file.name
                    subtitle_link.symlink_to(subtitle_file)

    # Calculate total duration in hours, minutes, and seconds
    hours, remaining_seconds = divmod(int(total_duration_seconds), 3600)
    minutes, seconds = divmod(remaining_seconds, 60)

    return f'Total duration: {hours:0>2}:{minutes:0>2.0f}:{seconds:0>2.0f}'

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Groups video files and their subtitles by runtime.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('input_dir', type=str, help='Input directory containing video files.')
    parser.add_argument('-o', '--output_dir', type=str, default='groups/', help='Output directory to store video groups.')
    parser.add_argument('-d', '--group_duration_minutes', type=int, default=60, help='Target duration for each video group in minutes.')
    parser.add_argument('-v', '--video_extension', type=str, default='.mp4', help='File extension for video files.')
    parser.add_argument('-s', '--subtitle_extension', type=str, default=None,
                        help='File extension for subtitle files. If provided, all files starting with the same name as a video file and ending with '\
                            'this extension will be linked. If not provided, no subtitles will be processed.')

    args = parser.parse_args()

    total_duration = group_videos_by_runtime(args.input_dir, args.output_dir,
                                             group_duration_minutes=args.group_duration_minutes,
                                             video_extension=args.video_extension,
                                             subtitle_extension=args.subtitle_extension)

    print('Process finished.')
    print(total_duration)

