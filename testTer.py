


# import subprocess
# import os

# # Global dictionary to store window IDs
# window_ids = {}

# def get_window_id(window_name):
#     # List all windows and their properties
#     result = subprocess.run(['wmctrl', '-l'], stdout=subprocess.PIPE)
#     windows = result.stdout.decode('utf-8').splitlines()
#     for window in windows:
#         if window_name in window:
#             # Get the window ID (the first column)
#             window_id = window.split()[0]
#             return window_id
#     return None

# def open_application(application_path, window_name):
#     # Open the application using subprocess
#     subprocess.Popen([application_path])

#     subprocess.run(['sleep', '1'])
#     window_id = get_window_id(window_name)
#     if window_id:
#         # Store the window ID in the dictionary
#         window_ids[window_name] = window_id
#         print(f"Application {window_name} opened with window ID {window_id}.")
#     else:
#         print(f"Failed to find window ID for {window_name}.")

# def unminimize_window(window_name):
#     window_id = window_ids.get(window_name)
    
#     if window_id:
#         # Use wmctrl to unminimize the window
#         subprocess.run(['wmctrl', '-i', '-r', window_id, '-b', 'remove,hidden'])
#         subprocess.run(['wmctrl', '-i', '-a', window_id])
#         print(f"Window {window_id} ({window_name}) has been unminimized.")
   
#     else:
#         print(f"No window found with name {window_name}.")

# if __name__ == "__main__":
#     application_path = "/usr/bin/gnome-terminal"  # Path to your application executable
#     window_name = "gnome-terminal.real"


#     # Check if the application is already open
#     existing_window_id = get_window_id(window_name)
#     if existing_window_id:
#         print(f"Application {window_name} is already open with window ID {existing_window_id}.")
#         window_ids[window_name] = existing_window_id
#     else:
#         open_application(application_path, window_name)


#     unminimize_window(window_name)


# import dbus

# def check_terminal_open():
#     try:
#         session_bus = dbus.SessionBus()
#         proxy = session_bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
#         interface = dbus.Interface(proxy, 'org.freedesktop.DBus')
#         names = interface.ListNames()
#         for name in names:
#             if name == 'org.gnome.Terminal':
#                 return True
#         return False
#     except Exception as e:
#         print(f"Error checking if terminal is open: {e}")
#         return False

# if __name__ == "__main__":
#     terminal_open = check_terminal_open()
#     if terminal_open:
#         print("Terminal is open.")
#     else:
#         print("Terminal is not open.")












# import dbus
# import subprocess
# def check_terminal_open():
#     try:
#         session_bus = dbus.SessionBus()
#         terminal_proxy = session_bus.get_object('org.gnome.Terminal', '/org/gnome/Terminal')
#         terminal_interface = dbus.Interface(terminal_proxy, dbus_interface='org.gnome.Terminal')
#         return terminal_interface.HasCurrentWindow()
#     except Exception as e:
#         print(f"Error checking if terminal is open: {e}")
#         return False

# def activate_terminal():
#     try:
#         session_bus = dbus.SessionBus()
#         terminal_proxy = session_bus.get_object('org.gnome.Terminal', '/org/gnome/Terminal')
#         terminal_interface = dbus.Interface(terminal_proxy, dbus_interface='org.gnome.Terminal')
#         terminal_interface.SetWindowAsCurrent()
#         print("Activated existing terminal window.")
#     except Exception as e:
#         print(f"Error while activating terminal window: {e}")

# def open_new_terminal():
#     try:
#         subprocess.Popen(["gnome-terminal"])
#         print("Opened new terminal instance.")
#     except Exception as e:
#         print(f"Failed to open new terminal: {e}")

# if __name__ == "__main__":
#     if check_terminal_open():
#         activate_terminal()
#     else:
#         open_new_terminal()

















# ye hai main betichod

# import dbus
# import subprocess

# def check_terminal_open():
#     try:
#         session_bus = dbus.SessionBus()
#         proxy = session_bus.get_object('org.gtk.Application', '/org/gnome/Terminal')
#         interface = dbus.Interface(proxy, 'org.gtk.Application')
#         names = interface.ListNames()
#         return 'org.gnome.Terminal' in names
#     except Exception as e:
#         print(f"Error checking if terminal is open: {e}")
#         return False

# def activate_terminal():
#     try:
#         session_bus = dbus.SessionBus()
#         terminal_proxy = session_bus.get_object('org.gtk.Application', '/org/gnome/Terminal')
#         terminal_interface = dbus.Interface(terminal_proxy, dbus_interface='org.gtk.Application')
#         terminal_interface.Activate()
#         print("Activated existing terminal window.")
#     except Exception as e:
#         print(f"Error while activating terminal window: {e}")

# def open_new_terminal():
#     try:
#         subprocess.Popen(["gnome-terminal"])
#         print("Opened new terminal instance.")
#     except Exception as e:
#         print(f"Failed to open new terminal: {e}")

# if __name__ == "__main__":
#     if check_terminal_open():
#         activate_terminal()
#     else:
#         open_new_terminal()









# import subprocess
# import dbus

# def activate_terminal():
#     try:
#         session_bus = dbus.SessionBus()
#         terminal_proxy = session_bus.get_object('org.gnome.Terminal', '/org/gnome/Terminal/window/1')
#         terminal_interface = dbus.Interface(terminal_proxy, dbus_interface='org.gtk.Actions')
#         terminal_interface.Activate()
#         print("Activated existing terminal window.")
#     except Exception as e:
#         print(f"Error while activating terminal window: {e}")
#         # If there's an error, fall back to opening a new terminal
#         open_new_terminal()

# def open_new_terminal():
#     try:
#         subprocess.Popen(["gnome-terminal"])
#         print("Opened new terminal instance.")
#     except Exception as e:
#         print(f"Failed to open new terminal: {e}")

# if __name__ == "__main__":
#     activate_terminal()












# import pyautogui
# import time

# def click_terminal_icon():
#     # Adjust the confidence level and path to the terminal icon image as necessary
#     icon_path = "/home/darkeagle/Desktop/luna_v1.0.0/assets/icons/terminal.png"  # Path to the screenshot of the terminal icon
#     confidence_level = 0.8  # Adjust this if necessary

#     # Locate the terminal icon on the screen
#     icon_location = pyautogui.locateCenterOnScreen(icon_path, confidence=confidence_level)
#     if icon_location is not None:
#         print(f"Terminal icon found at: {icon_location}")
#         # Move the mouse to the terminal icon and click
#         pyautogui.moveTo(icon_location)
#         pyautogui.click()
#         print("Clicked on the terminal icon.")
#     else:
#         print("Terminal icon not found on the screen.")

# if __name__ == "__main__":
#     time.sleep(2)  # Optional: Wait for 2 seconds before executing to give you time to switch to the desktop
#     click_terminal_icon()



# wo wala h ls command activate krne wala

    # elif action == "show list":
    #     terminal_window_id = find_terminal_window()

    #     if terminal_window_id:
    #         # Focus the existing terminal window
    #         print(f"Activating window ID: {terminal_window_id}")
    #         subprocess.run(['xdotool', 'windowactivate', '--sync', terminal_window_id])
    #         time.sleep(0.5)  # Give some time for the window to focus
    #         pyautogui.typewrite("ls\n", interval=0.05)
    #     else:
    #         # Open a new terminal window and execute the command
    #         print("No existing terminal found, opening a new one.")
    #         subprocess.Popen(["gnome-terminal", "--", "bash", "-c", "ls; exec bash"])






import subprocess

def open_terminal():
    # Check if a terminal window is already open
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

if __name__ == "__main__":
    open_terminal()




