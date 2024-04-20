# gpt-audio-ui
UI for audio features like TTS or STT


# Setup 
Create and activate a virtual environment
```bash
python3.11 -m venv env
source env/bin/activate
```

Install dependencies from requirements.txt
```bash
pip install -r requirements.txt
```

Pro tip: `.env` file can be used to store OPENAI_API_KEY and skip providing key every time app is initialized:
```toml
OPENAI_API_KEY=<YOUR_KEY_HERE>
```

# Runnig
```bash
streamlit run main.py 
```