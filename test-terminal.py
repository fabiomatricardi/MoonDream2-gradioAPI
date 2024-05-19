from gradio_client import Client, file
import sys
from PIL import Image
from time import sleep


import easygui   #https://easygui.readthedocs.io/en/master/api.html
file_path = easygui.fileopenbox(filetypes = ["*.png","*.jpg"])
print(f'Loaded image - {file_path}')
targetImage = Image.open(file_path)
targetImage.show()

def create_llava():   
# Set HF API token  and HF repo
    yourHFtoken = "hf_xxxxxxxxxxxxxxxxxxxx" #here your HF token
    print('loading the API gradio client for vikhyatk/moondream2')
    client = Client("vikhyatk/moondream2", hf_token=yourHFtoken)
    return client

client = create_llava()

while True:
    userinput = ""
    print("\033[1;30m")  #dark grey
    print("Enter your text (end input with Ctrl+D on Unix or Ctrl+Z on Windows) - type quit! to exit the chatroom:")    
    print("\033[91;1m")  #red
    lines = sys.stdin.readlines()
    for line in lines:
        userinput += line + "\n"
    if "quit!" in lines[0].lower():
        print("\033[0mBYE BYE!")
        break    
    print("\033[1;30m")  #dark grey
    print('Calling the gradio_client prediction...')
    result = client.submit(
            file(file_path),	# filepath  in 'Upload an Image' Image component
            "Describe with details the picture.",	# str  in 'Input' Textbox component
            api_name="/answer_question"
    )
    print("\033[38;5;99m")
    final = ''
    for chunk in result:
        if final == '':
            final=chunk
            print(chunk, end="", flush=True)
        else:
            try:
                print(chunk.replace(final,''), end="", flush=True)
                final = chunk
                sleep(0.025)
            except:
                pass   
