import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
user_input_token = st.text_input("place your OpenAI API token here", "")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or user_input_token)


def text_to_speech(text, file_name="audio_file.mp3"):
    try:
        response = client.audio.speech.with_raw_response.create(
            model="tts-1",
            voice="onyx",
            input=text,
            speed=1,
        )
        with open(file_name, "wb") as file:
            file.write(response.content)
        return file_name
    except Exception as e:
        print(f"Error generating audio file: {e}")
        return None


def speech_to_text(audio_file):
    audio_file = open(audio_file, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text",
    )
    return transcription


# Streamlit app
def main():
    st.title("Text to Speech with OpenAI")

    # TTS entrypoint
    with st.container(border=True):
        text_provided = st.text_area("Enter text to convert to speech", "")
        if st.button("Convert") and text_provided:
            file_name = text_to_speech(text_provided)
            if file_name:
                # Display the audio player with the generated audio file
                st.audio(file_name, format="audio/mp3")

                # Button to download the audio file
                with open(file_name, "rb") as file:
                    st.download_button(
                        label="Download Audio",
                        data=file,
                        file_name=file_name,
                        mime="audio/mp3",
                    )
            else:
                st.error("Failed to convert text to speech.")

    # STT entrypoint
    with st.container(border=True):
        uploaded_file = st.file_uploader("Choose an audiofile")
        if uploaded_file is not None:
            # Save the file locally
            file_path = uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            # Pass the local file path to the speech_to_text function
            st.text(speech_to_text(file_path))


if __name__ == "__main__":
    main()  # streamlit run main.py --server.enableXsrfProtection false
