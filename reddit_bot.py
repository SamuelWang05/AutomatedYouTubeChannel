import praw
import creds # Making sure I don't leak my API keys :)
import grabPost

# Setting up Reddit API

reddit_instance = praw.Reddit(
    client_id = creds.client_id,
    client_secret = creds.client_secret,
    username = creds.username,
    password = creds.password,
    user_agent="test_bot"
)

########################## Select settings for script ##########################

subreddit = "AmItheAsshole"
# filterTime = "day" # Currently not being used, "hot" has no filter for time
numVideos = 1; # Note number of videos generated may be off - currently compensating for pinned post
voiceoverDirectory = "Voiceovers"
subtitlesDirectory = "Subtitles"
bg_filePath = "Background/MinecraftBG.mp4"
finalDirectory = "finalVideo"
font = "Comic Sans MS" # Font of subtitles

# Posts we don't want (like pinned posts)
pinned_ID = "1ftvu8w"

#################################### Script ####################################

top_submissions = reddit_instance.subreddit(subreddit).hot(limit = numVideos + 1)

grabPost.getContent(top_submissions)