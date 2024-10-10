import assemblyai as aai
import srt_equalizer
from moviepy.editor import *
from moviepy.video.fx.all import crop
from moviepy.video.tools.subtitles import SubtitlesClip
import creds
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

def assembly_subtitles(audio_path):
    aai.settings.api_key = creds.assemblyAI_key
    config = aai.TranscriptionConfig(language_code = "en")
    transcriber = aai.Transcriber(config = config)
    transcript = transcriber.transcribe(audio_path)
    subtitles = transcript.export_subtitles_srt()

    return subtitles

def generate_subtitles(audio_path, submission):
    import reddit_bot
        
    def equalize_subtitles(srt_path, max_chars = 10) -> None:
        srt_equalizer.equalize_srt_file(srt_path, srt_path, max_chars)

    subtitles_path = f"{reddit_bot.subtitlesDirectory}/" + submission.id + ".srt"

    subtitles = assembly_subtitles(audio_path)

    with open(subtitles_path, "w") as file:
        file.write(subtitles)

    equalize_subtitles(subtitles_path)

    return subtitles_path

def combine_videos(BG_video_path, SC_path, audio_title_path, audio_path, subtitles_path, submission):
    import reddit_bot
    import random

    max_duration = 58  # Maximum duration in seconds
    video_id = submission.id
    combined_video_path = f"{reddit_bot.finalDirectory}/" + video_id + ".mp4"

    generator = lambda txt: TextClip(
        txt,
        font=reddit_bot.font,
        fontsize=100,
        color="white",
        stroke_color="black",
        stroke_width=5,
    )

    subtitles = SubtitlesClip(subtitles_path, generator)
    subtitles_position = "center", "center" 
    subtitles = subtitles.set_pos(subtitles_position)

    # Get start time of BG clip
    start_time = random.randint(3, 700)
    end_time = start_time + max_duration

    # Load the background video and set the subclip
    bg_clip = VideoFileClip(BG_video_path).subclip(start_time, end_time)

    # Resize the background video to fit a short-form aspect ratio (9:16)
    bg_clip = bg_clip.resize(height=1080)  # Resize to 1080p height

    # Load the image and audio files
    image_clip = ImageClip(SC_path)

    # Get length of title audio
    audio_title = AudioFileClip(audio_title_path)
    audio_title_length = audio_title.duration

    body_audio_clip = AudioFileClip(audio_path)

    audio_clip = concatenate_audioclips([audio_title, body_audio_clip])

    # Set audio duration to match the max_duration
    audio_clip = audio_clip.subclip(0, max_duration)

    # Set the duration of the background video to max_duration
    bg_clip = bg_clip.set_duration(max_duration)

    # Resize the image to fit within the background video dimensions
    bg_width, bg_height = bg_clip.size
    image_clip = image_clip.resize(height=bg_height / 3)  # Adjust height as needed
    image_clip = image_clip.resize(width=min(bg_width, image_clip.w))  # Ensure it fits within the width

    # Set the image duration to max_duration
    image_clip = image_clip.set_duration(audio_title_length).set_position("center")

    # Create a CompositeVideoClip
    composite = CompositeVideoClip([bg_clip, image_clip.set_start(0)])

    # Set the audio for the composite video
    composite = composite.set_audio(audio_clip)
     
    # Ensure composite video duration is set correctly
    composite = composite.set_duration(max_duration)
    
    # Set subtitles to start appearing after the image duration
    subtitles = subtitles.set_start(audio_title_length)

    # Create a final video with subtitles
    result = CompositeVideoClip([composite, subtitles])
    
    # Ensure final video duration is set correctly
    result = result.set_duration(max_duration)

    # Set the audio for the final video
    result = result.set_audio(audio_clip)

    # Write the final result to a file
    result.write_videofile(combined_video_path, codec="libx264", audio_codec="aac", fps=30, preset="ultrafast")