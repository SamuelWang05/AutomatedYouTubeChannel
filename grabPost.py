import praw
import voiceover
import screenshot
from termcolor import colored

def getContent(top_submissions):
    import reddit_bot
    import vidEdit

    for submission in top_submissions:
        if(submission.id == reddit_bot.pinned_ID):
            continue

        # Getting a bunch of info from the submission
        submission_ID = submission.id
        submission_title = submission.title + ". \n \n" # Combining title and body of Reddit post, adding a bunch of spaces and new lines to add a pause inbetween
        submission_text = submission.selftext

        print(colored("[+] Script grabbed.\n", "green"))

        # Create the voiceover
        voiceover_title_path = voiceover.createVoiceOver(submission_ID + "_title", submission_title)
        voiceover_path = voiceover.createVoiceOver(submission_ID, submission_text)

        print(colored("[+] Voiceover generated.\n", "green"))
        
        # Take a screenshot
        screenshot_path = screenshot.getScreenshot(submission)

        print(colored("[+] Screenshot taken.\n", "green"))

        # Generate subtitles from the voiceover
        subtitles_path = vidEdit.generate_subtitles(voiceover_path, submission)  # Assuming generate_subtitles is accessible

        print(colored("[+] Subtitles generated.\n", "green"))

        print(colored("[+] Editing video...\n", "green"))

        # Combine the video components into a final video
        vidEdit.combine_videos(
            BG_video_path = reddit_bot.bg_filePath,  # Replace with the path to your background video
            SC_path = screenshot_path,  # This should be the path of the screenshot taken
            audio_title_path = voiceover_title_path,
            audio_path = voiceover_path,
            subtitles_path = subtitles_path,
            submission = submission
        )

        print(colored("[+] Video Generated!\n", "green"))