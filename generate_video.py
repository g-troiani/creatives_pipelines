#
# GENERATE_VIDEO.PY
#



import os
import subprocess

def create_video_from_images(image_directory, output_video, frame_rate=0.5):
    # Ensure the image directory exists
    if not os.path.exists(image_directory):
        raise FileNotFoundError(f"The directory {image_directory} does not exist.")

    # Build the ffmpeg command
    ffmpeg_command = [
        'ffmpeg',
        '-framerate', str(frame_rate),
        '-pattern_type', 'glob',
        '-i', os.path.join(image_directory, '*.png'),
        '-vf', 'format=yuv420p',  # Ensure no overlay text
        '-c:v', 'libx264',
        '-r', '30',
        '-pix_fmt', 'yuv420p',
        '-y',  # Overwrite output file if it exists
        output_video
    ]

    # Run the ffmpeg command
    result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("Error creating video:")
        print(result.stderr)
    else:
        print(f"Video created: {output_video}")

# Define the directory and output file
image_directory = "/home/gian/Desktop/daily_scripts/youtube_video_insights/instagram_creatives/upcoming_posts/"
output_video = "output.mp4"

# Create the video
create_video_from_images(image_directory, output_video)
