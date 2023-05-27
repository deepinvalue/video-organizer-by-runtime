# Video Grouping by Runtime

This Python script groups collections of short video segments and their corresponding subtitle files into larger units with an aggregate runtime not exceeding a user-defined limit (e.g., 30 minutes). This utility is especially useful for organizing educational content, bundling multiple short videos into manageable, time-bound sessions. The script achieves this organization using soft links, avoiding any additional storage requirements.

## Usage

1. Clone the repository.
2. Navigate to the repository's directory.
3. Run `python video_grouping_by_runtime.py --help` for usage information and available options.

Example usage:

`python video_grouping_by_runtime.py "input_directory" --output_dir "output_directory" --group_duration_minutes 30 --video_extension ".mp4" --subtitle_extension ".srt"`
