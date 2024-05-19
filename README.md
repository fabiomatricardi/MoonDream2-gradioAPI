# MoonDream2-gradioAPI
Chat with your local images and MoonDream2 using Gradio Client API

<img src='https://github.com/fabiomatricardi/MoonDream2-gradioAPI/raw/main/moondream2logo.png' height=300>

Tested with Python 3.12
> will work with python 3.11+<br>
> Python 3.10 has broken dependencies with protobuf when installing Streamlit 1.34.0

### Description
This AI app works leveraging the powerful Gradio-client tool<br>
It connect through a **totally free API** an existing HuggingFace/Space
<br><br>

### Dependencies
- create a virtual environment
- install the following packages:
```
pip install gradio-client==0.16.0 streamlit==1.34.0 easygui
```

### Run the AI app
- Only textual interface, with easygui to file upload from your PC:
- `python test-terminal.py`
- With a Streamlit interface:
- `streamlit run st-MoonDream2-gradio.py`
