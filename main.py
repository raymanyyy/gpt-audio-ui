import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
user_input_token = st.text_input("place your OpenAI API token here", "")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or user_input_token)


def text_to_speech(text, file_name="audio_file.mp3"):
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=text,
            speed=1,
        )
        response.stream_to_file(file_name)
        return file_name
    except Exception as e:
        print(f"Error generating audio file: {e}")
        return None


def speech_to_text(audio_file) -> str | None:
    try:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file, response_format="text"
        )
        print(transcription.text)
    except Exception as e:
        print(f"Error generating audio file: {e}")
        return str(e)


# Streamlit app
def main():
    st.title("Text to Speech with OpenAI")

    # TTS
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

    # STT
    with st.container(border=True):
        uploaded_file = st.file_uploader("Choose an audiofile")
        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()
            # st.write(bytes_data)
            st.text(speech_to_text(bytes_data))


if __name__ == "__main__":
    main()  # streamlit run main.py --server.enableXsrfProtection false