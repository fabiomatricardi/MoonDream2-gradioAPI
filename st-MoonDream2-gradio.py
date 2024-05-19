import streamlit as st
from gradio_client import Client, file
import datetime
import os
from time import sleep
from PIL import Image

st.set_page_config(layout="wide", page_title="MoonDream2 GradioAPI chat with your images")

@st.cache_resource 
def create_llava():   
# Set HF API token  and HF repo
    yourHFtoken = "hf_xxxxxxxxxxxxxxxxxxxxxxxx" #here your HF token
    print('loading the API gradio client for vikhyatk/moondream2')
    client = Client("vikhyatk/moondream2", hf_token=yourHFtoken)
    return client
    
# FUNCTION TO LOG ALL CHAT MESSAGES INTO chathistory.txt
def writehistory(text):
    with open('chathistory-moonDream2.txt', 'a', encoding='utf-8') as f:
        f.write(text)
        f.write('\n')
    f.close()

#AVATARS
av_us = '🧑‍💻'  # './man.png'  #"🦖"  #A single emoji, e.g. "🧑‍💻", "🤖", "🦖". Shortcodes are not supported.
av_ass = "✨"   #'./robot.png'

if "gentime" not in st.session_state:
    st.session_state.gentime = "none yet"
if "imagefile" not in st.session_state:
    st.session_state.imagefile = ''   
if "keyimagefile" not in st.session_state:
    st.session_state.keyimagefile = 0     
if "chatimage" not in st.session_state:
    st.session_state.chatimage = 0   
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []   
if "chatUImessages" not in st.session_state:
    st.session_state.chatUImessages = [{"role": "assistant", "content": "Hi there! I am here to assist you with this Image. What do you want to know?"}]   
if "uploadedImage" not in st.session_state:
    st.session_state.uploadedImage = '' 
if "data_uri" not in st.session_state:
    st.session_state.data_uri = '' 

st.markdown("# 💬🖼️ Talk to your Images\n\n### *with MoonDream2 and Gradio-client API*\n\n\n")
st.markdown('\n---\n', unsafe_allow_html=True)
st.sidebar.image('moondream2logo.png')
vllm = create_llava()

file1=None
#image_btn = st.button('✨ **Start AI Magic**', type='primary')
def resetall():
    # tutorial to reset the to 0 the file_uploader from 
    # https://discuss.streamlit.io/t/clear-the-file-uploader-after-using-the-file-data/66178/4
    st.session_state.keyimagefile += 1
    st.session_state.chatimage = 0
    st.session_state.chatUImessages = [{"role": "assistant", "content": "Hi there! I am here to assist you with this Image. What do you want to know?"}]
    st.rerun()
    

st.sidebar.write("## Upload an image :gear:")
st.markdown('\n\n')
message1 = st.sidebar.empty()
message11 = st.sidebar.empty()
message2 = st.sidebar.empty()
message2.write(f'**:green[{st.session_state.gentime}]**')
message3 = st.empty()

# Upload the audio file
file1 = st.sidebar.file_uploader("Upload an image", 
                                    type=["jpg", "png"],accept_multiple_files=False, 
                                    key=st.session_state.keyimagefile)
#gentimetext = st.sidebar.empty()
reset_btn = st.sidebar.button('🧻✨ **Reset Image** ', type='primary')

if file1:
    st.session_state.chatimage = 1
    st.session_state.imagefile = file1
    st.session_state.uploadedImage = Image.open(st.session_state.imagefile)
    st.session_state.uploadedImage.save('temp.jpg')
    message1.write('image file selected!')
    # https://stackoverflow.com/questions/52411503/convert-image-to-base64-using-python-pil
    # https://huggingface.co/docs/api-inference/detailed_parameters
    st.session_state.data_uri =file('temp.jpg')
    message11.write('Ready to **CHAT**')        
    if reset_btn:
        resetall()
        try:
            os.remove('temp.jpg')
        except:
            pass

    with st.chat_message("user",avatar=av_us):
        st.image(st.session_state.uploadedImage, width=350)
    # Display chat messages from history on app rerun
    for message in st.session_state.chatUImessages:
        if message["role"] == "user":
            with st.chat_message(message["role"],avatar=av_us):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"],avatar=av_ass):
                st.markdown(message["content"])
    # Accept user input
    if myprompt := st.chat_input("What is this?"): #,key=str(datetime.datetime.now())
        # Add user message to chat history
        st.session_state.messages = [
                    st.session_state.data_uri,
                    myprompt
                ]
        st.session_state.chatUImessages.append({"role": "user", "content": myprompt})
        # Display user message in chat message container
        with st.chat_message("user", avatar=av_us):
            st.markdown(myprompt)
            usertext = f"user: {myprompt}"
            writehistory(usertext)
            # Display assistant response in chat message container
        with st.chat_message("assistant",avatar=av_ass):
            message_placeholder = st.empty()
            with st.spinner("Thinking..."):
                full_response = ""
                start = datetime.datetime.now()
                result = vllm.submit(
                        st.session_state.messages[0],	# filepath  in 'Upload an Image' Image component
                        st.session_state.messages[1],	# str  in 'Input' Textbox component
                        api_name="/answer_question"
                ) 
                for chunk in result:
                    if full_response == '':
                        full_response=chunk
                        message_placeholder.markdown(full_response + "🔷")
                    else:
                        try:
                            full_response = chunk
                            message_placeholder.markdown(full_response + "🔷")
                            sleep(0.08)
                        except:
                            pass                                           
            message_placeholder.markdown(full_response)
            st.session_state.gentime = datetime.datetime.now() - start 
            message2.write(f'**:green[{str(st.session_state.gentime)}]**') 
            print(full_response)
            asstext = f"assistant: {full_response}"
            writehistory(asstext)       
            st.session_state.chatUImessages.append({"role": "assistant", "content": full_response})

if  not file1:
    message3.warning("  Upload an image", icon='⚠️')

