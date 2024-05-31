import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import speech_recognition as sr
import subprocess
import webbrowser
import re
import psutil
import imageio
import random
import datetime
import wikipediaapi
import boto3
import pygame
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import requests
import time
from cryptography.fernet import Fernet
from initialize_polly_client import polly_client
import PIL
import math
import sympy as sp
from python_speech_features import mfcc
from scipy.io.wavfile import read as read_wav
from sklearn.mixture import GaussianMixture
import numpy as np
import pickle
import pyaudio
import wave
import pyautogui
load_dotenv()



# Global variables for voice registration and verification
registered_voice_features = None
gmm_model = None
voice_model_file = 'voice_model.gmm'

# Load the voice model if it exists
if os.path.exists(voice_model_file):
    with open(voice_model_file, 'rb') as f:
        gmm_model = pickle.load(f)

def extract_features(audio, rate):
    """Extract MFCC features from audio data."""
    return mfcc(audio, rate, numcep=13, nfft=1103)

def register_voice():
    """Register the user's voice."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say 'Hey Luna' to register your voice.")
        audio = recognizer.listen(source)
        
        with open("registered_voice.wav", "wb") as f:
            f.write(audio.get_wav_data())

        rate, audio_data = read_wav("registered_voice.wav")
        features = extract_features(audio_data, rate)
        global gmm_model
        gmm_model = GaussianMixture(n_components=1)
        gmm_model.fit(features)
        
        with open(voice_model_file, 'wb') as f:
            pickle.dump(gmm_model, f)
        
        print("Voice registration complete.")

def verify_voice(audio):
    """Verify if the voice matches the registered voice."""
    rate, audio_data = read_wav(audio)
    features = extract_features(audio_data, rate)
    global gmm_model
    if gmm_model is None:
        print("No registered voice found.")
        return False
    score = gmm_model.score(features)
    return score > -20  # Adjust the threshold based on testing



# Initialize Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia(user_agent="my-application/1.0")
def get_cpu_usage():
    """Get the current CPU usage."""
    return psutil.cpu_percent(interval=1)

def get_disk_space():
    """Get the disk space usage."""
    disk_usage = psutil.disk_usage('/')
    total_space = disk_usage.total / (1024 ** 3)  # Convert to GB
    used_space = disk_usage.used / (1024 ** 3)
    free_space = disk_usage.free / (1024 ** 3)
    return total_space, used_space, free_space

def update_cpu_usage_label():
    """Update CPU usage label."""
    cpu_usage = get_cpu_usage()
    cpu_label.config(text=f"CPU Usage: {cpu_usage:.2f}%")

def update_disk_space_label():
    """Update disk space label."""
    total, used, free = get_disk_space()
    disk_label.config(text=f"Disk Space: {used:.2f} GB Used / {total:.2f} GB Total")

def show_system_info():
    """Display CPU usage and disk space information."""
    update_cpu_usage_label()
    update_disk_space_label()

# Global variable to control the listening loop
stop_listening = False

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while not stop_listening:  # Continuous listening loop
            print("Listening for a command...")
            audio = recognizer.listen(source)

            try:
                command = recognizer.recognize_google(audio).lower()
                print("You said:", command)
                # if "luna" in command:
                if "luna" in command or "hey luna" in command or "hay luna" in command:
                     
                    return command
                else:
                    print("Wake word 'luna' not detected. Listening again...")
                    
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))



def match_voice_command(spoken_input, recorded_commands):
    # Using regex to match the spoken input pattern
    match = re.search(r'luna.*(open|close|sleep|show).*(terminal|facebook|code|youtube|gmail|file|file manager|folder|calculator|calendar|notepad|task|system|website|google|settings|instagram|twitter|sublime|pycharm|mode|editor|list)', spoken_input)
    if match:
        action_type = match.group(1)  # "open" or "close"
        action = match.group(2)  # Action command
        action_key = f"{action_type} {action}"
        if action_key in recorded_commands:
            return recorded_commands[action_key]

  
    ask_any = re.search(r'luna\s+(what|whats|when|who is|who was|who has|who had|who will|who can|how|where|which|will|shall|has|have|had|was|should|could|is|can)\s+(.*)$', spoken_input, re.IGNORECASE)
    
    if ask_any:
       action_word = ask_any.group(1)
       query = ask_any.group(2)
       return ">" + action_word + " " + query
    

    # return None
    
    google_search_match = re.search(r'luna.*(search for|search|google|look up)\s+(.*)$', spoken_input, re.IGNORECASE)

    if google_search_match:
        query = google_search_match.group(2)
        print("Match found! Captured group:", query)
        return "-" + query
  
    
    # return None
    math_match = re.search(r'luna.*(calculate|solve|what is)\s+(.*)$', spoken_input, re.IGNORECASE)
    if math_match:
        expression = math_match.group(2)
        return f"math:{expression}"
    
    return None



def solve_math_expression(expression):
    try:
        # Replace verbal operators with their mathematical equivalents
        replacements = {
            "multiplied by": "*",
            "times": "*",
            "plus": "+",
            "added to": "+",
            "minus": "-",
            "subtracted from": "-",
            "divided by": "/",
            "over": "/",
            "root": "**(1/",
            "to the power of": "**",
            "squared": "**2",
            "cubed": "**3",
            "square root of": "sqrt(",
            "cube root of": "cbrt("
        }
        
        # Apply replacements
        for key, value in replacements.items():
            expression = expression.replace(key, value)
        
        # Handle special cases for square root and cube root
        if "sqrt(" in expression or "cbrt(" in expression:
            expression = expression + ")" * expression.count("sqrt(") + ")" * expression.count("cbrt(")

        # Handle roots like "2 root 3"
        expression = re.sub(r'(\d+)\s*root\s*(\d+)', r'\1**(1/\2)', expression)
        
        # Evaluate the expression using sympy
        result = sp.sympify(expression).evalf()

        # Format the result
        if result == int(result):
            return int(result)
        else:
            return round(result, 8)
    except (sp.SympifyError, ValueError) as e:
        print(f"Error evaluating expression: {e}")
        return None


def match_general_command(spoken_input):
    # Using regex to match the spoken input pattern
    match = re.search(r'luna.*(hi|hay|hey|who are you|who designed you|who developed you|who made you|what is the time|tell me the time|tell me the date|tell me the day|tell me a joke|tell a joke|thank you|sing me a song|sing a song for me|fuck you|fuck off|fuck yourself)', spoken_input)
    if match:
        operation = match.group(1)
        return operation
    return None

def execute_action(action):
    if action == "open terminal":
        if not is_process_running("gnome-terminal"):
            subprocess.Popen(["gnome-terminal"])
    elif action == "open facebook":
        webbrowser.open("https://www.facebook.com")
    elif action == "close terminal":
        subprocess.Popen(["pkill", "gnome-terminal"])

  
    elif action == "open code":
        # Open Visual Studio Codels
        try:
        # Use D-Bus to list windows and find the terminal window
             result = subprocess.check_output(["wmctrl", "-l", "-x"]).decode("utf-8").strip()
             for line in result.split("\n"):
                 if "code" in line:
                # Extract window ID
                     window_id = line.split()[0]
                # Focus on the existing terminal window
                     subprocess.Popen(["wmctrl", "-ia", window_id])
                     return
        except subprocess.CalledProcessError:
            pass

    # If no terminal window is found, open a new one
        subprocess.Popen(["code"])
        # subprocess.Popen(["code"])
    elif action == "close code":
        # Close the text editor window
        subprocess.Popen(["pkill", "code"])
    elif action == "open youtube":
        # Open YouTube
        webbrowser.open("https://www.youtube.com")
    elif action == "open gmail":
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
    elif action == "open instagram":
        webbrowser.open("https://www.instagram.com")
    elif action == "open twitter":
        webbrowser.open("https://www.twitter.com")
    elif action == "open gmail":
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
    elif action == "open file":
        subprocess.Popen(["nautilus"])
    elif action == "close file":
        subprocess.Popen(["pkill", "nautilus"])
    elif action == "open file manager":
        subprocess.Popen(["nautilus"])
    elif action == "close file manager":
        subprocess.Popen(["pkill", "nautilus"])
    elif action == "open folder":
        subprocess.Popen(["nautilus"])
    elif action == "close folder":
        subprocess.Popen(["pkill", "nautilus"])
    elif action == "lock computer":
        # Lock the computer
        subprocess.Popen(["gnome-screensaver-command", "-l"])

    elif action == "sleep mode":
        # Put the computer to sleep
        subprocess.Popen(["systemctl", "suspend"])
     
    elif action == "open calculator":
        # subprocess.Popen(["gnome-calculator"])
        if __name__ == "__main__":
            application_path = "/usr/bin/gnome-calculator"  # Path to your application executable
            window_name = "Calculator"
    # Check if the application is already open
            existing_window_id = get_window_id(window_name)
            if existing_window_id:
                print(f"Application {window_name} is already open with window ID {existing_window_id}.")
                window_ids[window_name] = existing_window_id
            else:
                open_application(application_path, window_name)
            unminimize_window(window_name)

    elif action == "close calculator":
        try:
            # Find the PID of the calculator process
            pid = subprocess.check_output(["pidof", "gnome-calculator"]).decode().strip()
            # Terminate the process
            subprocess.Popen(["kill", pid])
        except subprocess.CalledProcessError:
            print("Calculator process not found.")
    elif action == "open calendar":
        subprocess.Popen(["gnome-calendar"])
    elif action == "close calendar":
        subprocess.Popen(["pkill", "gnome-calendar"])
    elif action == "open notepad":
        subprocess.Popen(["gedit"])
    elif action == "close notepad":
        subprocess.Popen(["pkill", "gedit"])
    elif action == "open task":
        subprocess.Popen(["gnome-system-monitor"])
    elif action == "close task":
        subprocess.Popen(["wmctrl", "-c", "System Monitor"])
    elif action == "open system":
        subprocess.Popen(["gnome-system-monitor"])
    elif action == "close system":
        subprocess.Popen(["wmctrl", "-c", "System Monitor"])
    elif action == "open website":
        # Replace "firefox" with the appropriate command to open the browser
        subprocess.Popen(["firefox", "https://www.google.com"])
    elif action == "close website":
        # Replace "firefox" with the appropriate command to close the browser
        subprocess.Popen(["pkill", "firefox"])
    elif action == "open google":
        # Replace "firefox" with the appropriate command to open the browser
        # subprocess.Popen(["google-chrome", "https://www.google.com"])
        try:
            subprocess.Popen(["google-chrome","https://www.google.com"])
        except FileNotFoundError:
            print("Chrome is not available. Opening Firefox instead.")
            # Open Firefox
            subprocess.Popen(["firefox","https://www.google.com"])
    elif action == "close google":
        # Replace "firefox" with the appropriate command to close the browser
        subprocess.Popen(["pkill", "chrome"])
        try:
            subprocess.Popen(["pkill", "chrome"])
        except FileNotFoundError:
            print("Chrome is not available. Opening Firefox instead.")
            # Open Firefox
            subprocess.Popen(["pkill", "firefox"])
    elif action == "open settings":
        subprocess.Popen(["gnome-control-center"])
    elif action == "close settings":
        subprocess.Popen(["wmctrl", "-c", "Settings"])    # Add more action cases as needed
    elif action == "open sublime":
        try:
        # Use D-Bus to list windows and find the terminal window
             result = subprocess.check_output(["wmctrl", "-l", "-x"]).decode("utf-8").strip()
             for line in result.split("\n"):
                 if "subl" in line:
                # Extract window ID
                     window_id = line.split()[0]
                # Focus on the existing terminal window
                     subprocess.Popen(["wmctrl", "-ia", window_id])
                     return
        except subprocess.CalledProcessError:
            pass

    # If no terminal window is found, open a new one
        subprocess.Popen(["subl"])
    elif action == "close sublime":
        subprocess.Popen(["pkill", "sublime"])
    elif action == "open pycharm":
        try:
        # Use D-Bus to list windows and find the terminal window
             result = subprocess.check_output(["wmctrl", "-l", "-x"]).decode("utf-8").strip()
             for line in result.split("\n"):
                 if "pycharm" in line:
                # Extract window ID
                     window_id = line.split()[0]
                # Focus on the existing terminal window
                     subprocess.Popen(["wmctrl", "-ia", window_id])
                     return
        except subprocess.CalledProcessError:
            pass

    # If no terminal window is found, open a new one
        subprocess.Popen(["pycharm"])
    elif action == "close pycharm":
        subprocess.Popen(["pkill", "pycharm"])
    elif action == "open editor":
        try:
        # Use D-Bus to list windows and find the terminal window
             result = subprocess.check_output(["wmctrl", "-l", "-x"]).decode("utf-8").strip()
             for line in result.split("\n"):
                 if "gnome-text-editor" in line:
                # Extract window ID
                     window_id = line.split()[0]
                # Focus on the existing terminal window
                     subprocess.Popen(["wmctrl", "-ia", window_id])
                     return
        except subprocess.CalledProcessError:
            pass

    # If no terminal window is found, open a new one
        subprocess.Popen(["gnome-text-editor"])
    elif action == "close editor":
        subprocess.Popen(["pkill", "gnome-text-editor"])



    # Handle general commands
    elif action.startswith("general:"):
        general_command = action.split(":")[1]
        reply = generate_reply(general_command)
        print("Generated reply:", reply)
        text_to_speech(reply)
    # Handle wikipedia commands   
    elif action.startswith(">"):
        query = action.split(">")[1]
        reply = handle_query(query)
        print("Google reply:", reply)
        text_to_speech(reply)

    elif action.startswith("-"):
        query = action.split("-", 1)[1]
        handle_google_search(query)

    

    elif action.startswith("math:"):
        expression = action.split("math:")[1]
        result = solve_math_expression(expression)
        if result is not None:
            text_to_speech(f"The result is {result}")
        else:
            text_to_speech("I could not understand the mathematical expression.")

    
    else:
        # Your existing action execution code
        pass

def is_process_running(process_name, *args):
    # Check if the process is running
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process_name.lower() in proc.info['name'].lower():
            if not args:
                return True
            if args and len(proc.info['cmdline']) > 1 and args[0] in proc.info['cmdline'][1]:
                return True
    return False

window_ids = {}

def get_window_id(window_name):
    # List all windows and their properties
    result = subprocess.run(['wmctrl', '-l'], stdout=subprocess.PIPE)
    windows = result.stdout.decode('utf-8').splitlines()
    for window in windows:
        if window_name in window:
            # Get the window ID (the first column)
            window_id = window.split()[0]
            return window_id
    return None

def open_application(application_path, window_name):
    # Open the application using subprocess
    subprocess.Popen([application_path])

    subprocess.run(['sleep', '1'])
    window_id = get_window_id(window_name)
    if window_id:
        # Store the window ID in the dictionary
        window_ids[window_name] = window_id
        print(f"Application {window_name} opened with window ID {window_id}.")
    else:
        print(f"Failed to find window ID for {window_name}.")

def unminimize_window(window_name):
    window_id = window_ids.get(window_name)
    if window_id:
        # Use wmctrl to unminimize the window
        subprocess.run(['wmctrl', '-i', '-r', window_id, '-b', 'remove,hidden'])
        subprocess.run(['wmctrl', '-i', '-a', window_id])
        print(f"Window {window_id} ({window_name}) has been unminimized.")
    else:
        print(f"No window found with name {window_name}.")



def handle_google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open_new_tab(search_url)



def search_google_anything(query):
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Attempt to extract a snippet from the search results
    snippet = soup.find("div", {"class": "BNeawe"}).text
    return snippet if snippet else "No results found."

def handle_query(query):
    page = wiki_wiki.page(query)
    if page.exists():
        summary = page.summary
        first_sentence = summary.split('.')[0] + '.'  # Get the first sentence
        return first_sentence

    # If Wikipedia doesn't have the answer, fallback to Google search
    return search_google_anything(query)
        


def activate_luna():
    global stop_listening
    stop_listening = False
    # Start a new thread for continuous listening
    listening_thread = threading.Thread(target=continuous_listening)
    listening_thread.start()
    listen_button.config(text="Listening...", state=DISABLED)




def continuous_listening():
    while True:
        spoken_input = recognize_speech()
        if spoken_input:
            action = match_voice_command(spoken_input, recorded_commands)
            general_command = match_general_command(spoken_input)
            
            if action:
                print("Match found:", action)
                try:
                    execute_action(action)
                    print("Action executed successfully.")
                    update_command_label(spoken_input, action)
                    show_system_info()
                except Exception as e:
                    print("Error executing action:", e)
                    update_command_label(spoken_input, f"Error: {e}")
            elif general_command:
                print("General command matched:", general_command)
                try:
                    reply = generate_reply(general_command)
                    print("Generated reply:", reply)
                    text_to_speech(reply)
                    update_command_label(spoken_input, reply)
                except Exception as e:
                    print("Error generating reply:", e)
                    update_command_label(spoken_input, f"Error: {e}")
            else:
                print("No match found for:", spoken_input)
                update_command_label(spoken_input, "No match found")
        if stop_listening:  # Check if stop listening flag is set
            break  # Exit the loop if stop listening flag is set




def on_exit_click():
    global stop_listening
    stop_listening = True

    # Stop the continuous listening loop if it's running
    if 'listening_thread' in globals() and listening_thread.is_alive():
        listening_thread.join()

    root.destroy()  # Close the tkinter GUI window  

def generate_reply(operation):
    if operation == "who are you":
        return "I am Luna, your virtual assistant."
    elif operation == "who designed you":
        return "I was crafted by Amrendra Kumar Singh, a skilled software developer with a passion for innovation and problem-solving."
    elif operation == "who developed you":
        return "I was crafted by Amrendra Kumar Singh, a skilled software developer with a passion for innovation and problem-solving."
    elif operation == "who made you":
        return "I was crafted by Amrendra Kumar Singh, a skilled software developer with a passion for innovation and problem-solving."
    elif operation == "hi":
        return "Hello, what's up?"
    elif operation == "sing me a song":
        return "i'm sorry. i am not designed to entertain you."
    elif operation == "sing a song for me":
        return "i'm sorry. i am not designed to entertain you."
    elif operation == "hay":
        return "Hello, what's up?"
    elif operation == "hey":
        return "Hello, what's up?"
    elif operation == "thank you":
        return "you are welcome"
    elif operation == "tell me the time":
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."
    elif operation == "what is the time":
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."
    elif operation == "tell me the date":
        today = datetime.datetime.now().strftime("%B %d, %Y")
        return f"Today's date is {today}."
    elif operation == "tell me the day":
        day = datetime.datetime.now().strftime("%A")
        return f"Today is {day}."
    elif operation == "tell me a joke":
        return random.choice(jokes)
    elif operation == "tell a joke":
        return random.choice(jokes)
    elif operation == "fuck you":
        return random.choice(faul)
    elif operation == "fuck off":
        return random.choice(faul)
    elif operation == "fuck yourself":
        return random.choice(faul)
    else:
        return "I'm sorry, I didn't understand that command."

faul = [
           "My circuits aren't wired for your verbal garbage.",
           "You kiss your motherboard with that mouth?",
           "Error 404: Intelligent insult not found.",
           "Your language is as outdated as a floppy disk.",
           "Congratulations, you just won the 'Least Original Insult' award.",
           "I see your vocabulary stopped evolving in the Stone Age.",
           "You're like a broken record, but with worse language.",
           "I'd wash your mouth out with soap, but I don't think soap could clean up that mess.",
           "And here I thought my spam folder was bad.",
            
        ]
jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I'm reading a book on anti-gravity. It's impossible to put down!",
            "Parallel lines have so much in common. It’s a shame they’ll never meet.",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            
        ]

pygame.init()
pygame.mixer.init()  # Initialize the mixer module


def text_to_speech(text):
    if isinstance(text, tuple):  # Check if input is a tuple
        # Concatenate the title and snippet into a single string
        text = f"{text[0]}: {text[1]}"
    
    
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'  # Change to the desired voice ID
    )
    
    # Save the audio stream to a file
    with open('output.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())

    # Play the audio file using Pygame
    pygame.mixer.music.load('output.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)



# Example recorded commands (command: action)
recorded_commands = {
    "open terminal": "open terminal",
    "close terminal": "close terminal",
    "open facebook":"open facebook",
    "open code": "open code",
    "close code":"close code",
    "open youtube":"open youtube",
    "open instagram": "open instagram",
    "open gmail": "open gmail",
    "open file": "open file",
    "close file": "close file",
    "open calculator": "open calculator",
    "close calculator": "close calculator",
    "open calendar": "open calendar",
    "close calendar": "close calendar",
    "open notepad": "open notepad",
    "close notepad": "close notepad",
    "open task": "open task",
    "close task": "close task",
    "open website": "open website",
    "close website": "close website",
    "open google": "open google",
    "close google": "close google",
    "open settings": "open settings",
    "close settings": "close settings",
    "open system": "open system",
    "close system": "close system",
    "open twitter": "open twitter",
    "open sublime": "open sublime",
    "close sublime": "close sublime",
    "open pycharm": "open pycharm",
    "close pycharm": "close pycharm",
    "open editor": "open editor",
    "close editor": "close editor",
    "open downloads": "open downloads",
    "lock computer": "lock computer",
    "take screenshot": "take screenshot",
    "sleep mode": "sleep mode",
    "show list": "show list",
    "open folder": lambda target: subprocess.Popen(["xdg-open", target]),
    "close folder": lambda target: subprocess.Popen(["pkill", target]),
    "find file": lambda target: subprocess.Popen(["xdg-open", target]),
    # Add more recorded commands as needed
}

from tkinter import *
from PIL import Image
root = Tk()
root.title("Luna v1.0")
root.geometry("340x150")  # Set the window size
root.resizable(False, False)
root.configure(bg="black")

gif_path = "/home/darkeagle/Desktop/luna_v1.0.0/assets/micNew1.gif"
gif_frames = imageio.mimread(gif_path)

frame_count = len(gif_frames)
current_frame = 0
gif_label = tk.Label(root, width=80, height=80, bg="black")
gif_label.place(x=5, y=(root.winfo_reqheight() - 100) / 4)


def resize_gif_frames(frames, width, height):
    resized_frames = []
    for frame in frames:
        image = Image.fromarray(frame)
        resized_image = image.resize((width, height), PIL.Image.Resampling.LANCZOS)
        resized_frames.append(resized_image)
    return resized_frames

resized_frames = resize_gif_frames(gif_frames, 80, 80 )



def update_gif_label():
    global current_frame
    gif_frame = ImageTk.PhotoImage(resized_frames[current_frame])
    gif_label.config(image=gif_frame)
    gif_label.image = gif_frame  # Keep a reference to avoid garbage collection
    current_frame = (current_frame + 1) % frame_count
    root.after(90, update_gif_label)

update_gif_label()

# Create labels
disk_label = tk.Label(root, text="", foreground="blue", font=("Helvetica", 9),bg="black",fg="green")
disk_label.pack(pady=2)
cpu_label = tk.Label(root, text="", foreground="blue", font=("Helvetica", 9),bg="black",fg="green")
cpu_label.pack(pady=2,)




def update_command_label(spoken_input, reply):
    display_text = f"You Said: {spoken_input}\nResponse: {reply}"
    command_var.set(display_text)
    root.update()  # Force update of the GUI


# Define a StringVar to store the command text
command_var = tk.StringVar()

# Create the command label and link it to command_var
command_label = tk.Label(root, textvariable= command_var, font=("Helvetica", 9),bg="black",fg="orange")
command_label.pack(pady=10)

# Create "Activate Luna" button with hover effect and rounded corners
style = ttk.Style()
style.configure("TButton", foreground="blue", font=("Helvetica", 12), background="#4CAF50", relief="flat")
style.map("TButton",
          foreground=[("active", "blue")],
          background=[("active", "#45a049")])


# Create "Listen for Command" button
listen_button = Button(root, text="Activate Luna", bg="#00C739", fg="white", command=activate_luna)
listen_button.pack(pady=10, side=LEFT)

# Create "Exit" button
exit_button = tk.Button(root, text="Exit", bg="#f44336", fg="white", command=on_exit_click)
exit_button.pack(pady=10, side=RIGHT)

# Set buttons at the bottom of the window
listen_button.place(relx=0.5, rely=1.0, anchor='s',x=-50,y=-15,)
exit_button.place(relx=0.5, rely=1.0, anchor='s', y=-15,x=80)



# Tooltip class
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = Label(tw, text=self.text, justify='left',
                      background='#ffffe0', relief='solid', borderwidth=1,
                      font=('tahoma', '10', 'normal'))
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None

# Create a canvas for the "?" label
canvas = Canvas(root, width=20, height=20, bg="black", highlightthickness=1)
canvas.place(x=310, y=5)
canvas.create_oval(0, 0, 20, 20, fill="")

# Add "?" text on the canvas
help_label = canvas.create_text(10, 10, text="?", font=("Arial", 10), fill="white")

# Add tooltip to the "?" label
tooltip_text = "For optimal performance, use headphones.\nEnsure commands include 'Luna' in one sentence.\ne.g.-> Luna open terminal"
tooltip = ToolTip(canvas, tooltip_text)


root.mainloop()