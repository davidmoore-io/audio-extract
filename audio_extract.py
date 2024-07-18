import argparse
import os
import subprocess
import yt_dlp
import re
import logging
import shlex
from datetime import timedelta
import math

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def sanitize_filename(filename):
    return re.sub(r'[^\w\-_\. ]', '_', filename)

def parse_url_or_id(input_str):
    youtube_pattern = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    soundcloud_pattern = r'https?://soundcloud\.com/[\w-]+/[\w-]+'
    
    if re.match(youtube_pattern, input_str):
        return input_str if input_str.startswith('http') else f'https://www.youtube.com/watch?v={input_str}'
    elif re.match(soundcloud_pattern, input_str):
        return input_str
    elif len(input_str) == 11:  # Assume it's a YouTube video ID
        return f'https://www.youtube.com/watch?v={input_str}'
    else:
        raise ValueError("Invalid input. Please provide a valid YouTube/SoundCloud URL or YouTube video ID.")

def get_video_info(url):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['title'], info['duration']

def create_output_dir(video_title, duration):
    safe_title = sanitize_filename(video_title)
    runtime = str(timedelta(seconds=int(duration))).replace(':', '-')
    dir_name = f"{safe_title}-{runtime}"
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'OUTPUT', dir_name)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def get_audio_duration(filename):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

def split_audio(input_file, output_dir, chunk_size_mb):
    try:
        logging.info(f"Starting to split audio file: {input_file}")
        duration = get_audio_duration(input_file)
        logging.info(f"Audio duration: {duration} seconds")
        
        file_size = os.path.getsize(input_file)
        bitrate = file_size * 8 / duration / 1000  # kbps
        logging.info(f"Calculated bitrate: {bitrate} kbps")
        
        chunk_duration = chunk_size_mb * 8 * 1024 / bitrate  # seconds
        logging.info(f"Calculated chunk duration: {chunk_duration} seconds")
        
        num_chunks = math.ceil(duration / chunk_duration)
        logging.info(f"Number of chunks to create: {num_chunks}")
        
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        
        for i in range(num_chunks):
            start_time = i * chunk_duration
            output_file = os.path.join(output_dir, f"{base_name}_part{i+1}.wav")
            
            command = [
                'ffmpeg', '-i', input_file,
                '-ss', str(start_time),
                '-t', str(chunk_duration),
                '-c', 'copy',
                output_file
            ]
            
            logging.info(f"Running ffmpeg command: {' '.join(command)}")
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            logging.info(f"ffmpeg stdout: {result.stdout}")
            logging.info(f"ffmpeg stderr: {result.stderr}")
            
            logging.info(f"Created chunk: {output_file}")
        
        os.remove(input_file)  # Remove the original file after splitting
        logging.info(f"Removed original file: {input_file}")
        logging.info(f"Audio split into {num_chunks} parts in {output_dir}")
    except Exception as e:
        logging.error(f"An error occurred while splitting audio: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())

def download_and_process_audio(url, start_time, end_time, chunk_size_mb):
    try:
        logging.info(f"Processing URL: {url}")
        video_title, duration = get_video_info(url)
        logging.info(f"Video title: {video_title}, Duration: {duration} seconds")

        output_dir = create_output_dir(video_title, duration)
        logging.info(f"Output directory: {output_dir}")

        safe_title = sanitize_filename(video_title)
        output_template = os.path.join(output_dir, '%(title)s.%(ext)s')

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }],
            'outtmpl': output_template,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'verbose': True,
        }

        logging.info("Starting download with yt-dlp")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        logging.info("Download completed, searching for WAV file")
        wav_file = None
        for file in os.listdir(output_dir):
            if file.endswith(".wav"):
                wav_file = os.path.join(output_dir, file)
                break

        if not wav_file:
            raise FileNotFoundError("WAV file not found after download")
        logging.info(f"WAV file found: {wav_file}")

        if start_time:
            trimmed_file = os.path.join(output_dir, f"{safe_title}_trimmed.wav")
            trim_command = [
                'ffmpeg', '-i', wav_file,
                '-ss', start_time
            ]
            if end_time:
                trim_command.extend(['-to', end_time])
            trim_command.extend(['-c', 'copy', trimmed_file])
            
            logging.info(f"Running ffmpeg command: {' '.join(map(shlex.quote, trim_command))}")
            result = subprocess.run(trim_command, check=True, capture_output=True, text=True)
            logging.info(f"ffmpeg stdout: {result.stdout}")
            logging.info(f"ffmpeg stderr: {result.stderr}")
            
            os.remove(wav_file)  # Remove the original file after trimming
            wav_file = trimmed_file
            logging.info(f"Trimmed file created: {wav_file}")

        if chunk_size_mb:
            logging.info(f"Starting to split audio into {chunk_size_mb}MB chunks")
            split_audio(wav_file, output_dir, chunk_size_mb)
            logging.info("Chunking process completed")
        else:
            logging.info(f"Audio extracted and saved to: {wav_file}")

        return output_dir

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())
        return None

def main():
    parser = argparse.ArgumentParser(description="Download YouTube/SoundCloud audio, trim it, and optionally split into chunks.")
    parser.add_argument("-input", required=True, help="YouTube/SoundCloud URL or YouTube video ID")
    parser.add_argument("-start", help="Start time (HH:MM:SS)")
    parser.add_argument("-end", help="End time (HH:MM:SS)")
    parser.add_argument("-chunk", type=float, help="Split audio into chunks of specified size in MB")
    args = parser.parse_args()

    try:
        url = parse_url_or_id(args.input)
        logging.info(f"Parsed URL: {url}")
        output_dir = download_and_process_audio(url, args.start, args.end, args.chunk)
        
        if output_dir and os.path.exists(output_dir):
            logging.info(f"Opening output directory: {output_dir}")
            subprocess.run(["open", output_dir])
        else:
            logging.warning("Could not open output directory: Directory not found or processing failed.")
    except ValueError as e:
        logging.error(str(e))

if __name__ == "__main__":
    main()