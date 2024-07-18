# Audio Extract

Audio Extract is a command-line tool for downloading and processing audio from 

- YouTube videos
- SoundCloud tracks. 

It allows you to easily extract audio, trim it to specific timestamps, and split it into manageable chunks.

It's intended to be run on (my) mac but could be easily modified for other platforms.

## Features

- Download audio from YouTube videos (using video URL or ID)
- Download audio from SoundCloud tracks
- Trim audio to specified start and end times
- Split audio into chunks of a specified size
- Automatically organize output in a structured directory
- Open the output directory in Finder (macOS) upon completion

## Requirements

- Python 3.6+
- FFmpeg
- yt-dlp

## Installation

### Easy Installation (Recommended)

You can quickly install Audio Extract using our installation script:

```bash
curl -sSL https://raw.githubusercontent.com/davidmoore-io/audio-extract/main/install.sh | bash
```

This script will:
- Create a virtual environment
- Install all necessary dependencies
- Add the `audio-extract` command to your PATH

After installation, restart your terminal or run:
```bash
source ~/.zshrc  # or source ~/.bash_profile for bash users
```

### Manual Installation

1. Clone this repository:
   ```
   git clone https://github.com/davidmoore-io/audio-extract.git
   cd audio-extract
   ```

2. Install the required Python packages:
   ```
   pip install yt-dlp
   ```

3. Ensure FFmpeg is installed on your system. On macOS, you can use Homebrew:
   ```
   brew install ffmpeg
   ```

## Usage

If you used the easy installation method, you can run Audio Extract from anywhere:

```
audio-extract -input <URL_or_ID> [-start HH:MM:SS] [-end HH:MM:SS] [-chunk SIZE_IN_MB]
```

If you installed manually, run the script from the project directory:

```
python audio_extract.py -input <URL_or_ID> [-start HH:MM:SS] [-end HH:MM:SS] [-chunk SIZE_IN_MB]
```

### Arguments:

- `-input`: Required. The YouTube URL, YouTube video ID, or SoundCloud URL.
- `-start`: Optional. The start time of the audio to extract (format: HH:MM:SS).
- `-end`: Optional. The end time of the audio to extract (format: HH:MM:SS).
- `-chunk`: Optional. Split the audio into chunks of this size (in MB).

### Examples:

1. Download full audio from a YouTube video:
   ```
   audio-extract -input https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

2. Download audio from a YouTube video, starting at 1 minute:
   ```
   audio-extract -input dQw4w9WgXcQ -start 00:01:00
   ```

3. Download audio from a YouTube video, trim it, and split into 10MB chunks:
   ```
   audio-extract -input dQw4w9WgXcQ -start 00:00:30 -end 00:02:00 -chunk 10
   ```

4. Download audio from a SoundCloud track:
   ```
   audio-extract -input https://soundcloud.com/artist/track
   ```

## Output

The script will create an `OUTPUT` directory in the same location as the script. Inside this directory, it will create a subdirectory for each downloaded audio, named after the video/track title and its duration.

For example:
```
OUTPUT/
└── Video_Title-00-03-30/
    ├── Video_Title.wav
    ├── Video_Title_trimmed.wav (if trimmed)
    ├── Video_Title_part1.wav (if chunked)
    ├── Video_Title_part2.wav
    └── ...
```

On macOS, the script will automatically open the output directory in Finder upon completion.

## Notes

- This script is designed for personal use and should be used in accordance with the terms of service of YouTube and SoundCloud.
- Downloading copyrighted material without permission may be illegal in your country.

## Troubleshooting

If you encounter any issues, check the console output for error messages. The script provides detailed logging which can help identify the source of the problem.

Common issues:
- Ensure you have a stable internet connection.
- Verify that FFmpeg is correctly installed and accessible from the command line.
- Make sure you have the latest version of the script and yt-dlp installed.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/davidmoore-io/audio-extract/issues) if you want to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for providing the core functionality for downloading YouTube videos.
- [FFmpeg](https://ffmpeg.org/) for audio processing capabilities.

## Contact

David Moore - [@davidmoore_io](https://twitter.com/davidmoore_io)

Project Link: [https://github.com/davidmoore-io/audio-extract](https://github.com/davidmoore-io/audio-extract)
```

This README provides a comprehensive guide to your Audio Extract tool, including installation instructions (both easy and manual methods), usage examples, output explanation, troubleshooting tips, and other important information. You can copy this entire block and use it as your README.md file in your GitHub repository.

Remember to replace any placeholder information (like Twitter handle or specific URLs) with your actual information before publishing.