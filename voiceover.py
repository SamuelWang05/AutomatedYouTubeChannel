import pyttsx3

def createVoiceOver(id, text):
    import reddit_bot
    
    # Initalizing voice
    engine = pyttsx3.init()
    voices = engine.getProperty('voices');

    # Select voice: 0 -> Man, 1 -> Woman, 2 -> Japanese accent
    engine.setProperty('voice', voices[0].id)

    # Creating mp3 file and saving it to the specified directory
    filePath = f"{reddit_bot.voiceoverDirectory}/" + id + ".mp3"
    engine.save_to_file(text, filePath)
    engine.runAndWait()
    return filePath