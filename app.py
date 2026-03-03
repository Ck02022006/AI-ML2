import streamlit as st
import openai
import os
from audio_recorder_streamlit import audio_recorder
from dotenv import load_dotenv

# Load API Key
load_dotenv()
openai.api_key = os.getenv("OPEN_API_KEY")

st.set_page_config(page_title="AI Voice Agent", page_icon="🎤")
st.title("🗣️ AI Voice-to-Text Agent")
st.markdown("Record your voice and convert it into text using OpenAI Whisper.")

# Audio Recorder Component
audio_bytes = audio_recorder()

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    
    # Save recording temporarily to send to API
    with open("temp_audio.wav","wb") as f:
        f.write(audio_bytes)
        
    if st.button("Transcribe Audio"):
        st.info("Transcribing...")
        try:
            # Send to Whisper
            with open("temp_audio.wav", "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)
            
            # Display result
            st.success("Transcription:")
            st.write(transcript["text"])
            
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            # Clean up temp file
            if os.path.exists("temp_audio.wav"):
                os.remove("temp_audio.wav")

