import os
from PyPDF2 import PdfReader
from google.cloud import texttospeech
from google.oauth2 import service_account

# Create PDF reader object and extract text
# You can use your own pdf file instead of 'test.pdf'
# When using your own pdf file, make sure the file is in the same folder as 'test.pdf'
reader = PdfReader("test.pdf")
full_text = [page.extract_text() for page in reader.pages]

# Pull credentials from service account and create client object
# Make sure to use your own credentials when running this program
credentials = service_account.Credentials.from_service_account_file(os.environ["KEY"])
client = texttospeech.TextToSpeechClient(credentials=credentials)

# Set the text input to be synthesized
synthesis_input = [texttospeech.SynthesisInput(text=text) for text in full_text]

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
file_num = 1
for result in synthesis_input:
    response = client.synthesize_speech(
        input=result, voice=voice, audio_config=audio_config
    )
    with open(f"output{file_num}.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'Text-to-speech audio file saved as "page{file_num}.mp3"')
    file_num += 1
