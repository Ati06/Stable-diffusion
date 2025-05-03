import tkinter as tk  # Importing the tkinter library for GUI components
from tkvideo import tkvideo  # Importing tkvideo for video playback in tkinter
import pygame  # For playing background music
import Register  # Importing the Register module
import Login  # Importing the Login module

# Define color and font settings for the GUI
button_color = "#573a2e"
label_title_color = "#45030f"
panel_bg_color = "#f0e3da"
font_family = "Comic Sans MS"

# Initialize the main application window
root = tk.Tk()
root.title("Login & Registration GUI")
root.attributes('-fullscreen', True)  # Set the window to fullscreen mode

# Retrieve screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set up a label to display the video background
video_label = tk.Label(root)
video_label.pack(expand=True, fill="both")

# Play the background video using tkvideo
player = tkvideo("B3.mp4", video_label, loop=1, size=(screen_width, screen_height))
player.play()

# Initialize pygame mixer for background music
pygame.mixer.init()
pygame.mixer.music.load("bg.mp3")  # Make sure bg.mp3 is in the same folder or provide full path
pygame.mixer.music.play(-1)  # Loop indefinitely

# Calculate dimensions and position for the central panel
panel_width = int(screen_width * 0.35)
panel_height = int(screen_height * 0.7)
panel_x = int(screen_width * 0.3)
panel_y = int(screen_height * 0.17)

# Create a frame to serve as the panel for login and registration
panel_frame = tk.Frame(root, bg=panel_bg_color, highlightthickness=0, bd=0)
panel_frame.place(x=panel_x, y=panel_y, width=panel_width, height=panel_height)

# Determine font sizes based on screen height for responsiveness
title_font_size = int(screen_height * 0.035)
button_font_size = int(screen_height * 0.025)
small_font_size = int(screen_height * 0.02)

def create_fake_button(parent, text, font_size, bg_color, fg_color, command, y_relative):
    """
    Creates a styled label that functions as a button.
    """
    canvas = tk.Canvas(parent, width=200, height=40, bg=panel_bg_color, highlightthickness=0, bd=0)
    canvas.place(relx=0.5, rely=y_relative, anchor="center")

    label = tk.Label(
        canvas,
        text=text,
        font=(font_family, font_size),
        bg=bg_color,
        fg=fg_color,
        width=15,
        height=1
    )
    label.pack(fill="both", expand=True)

    # Bind mouse events for click and hover effects
    label.bind("<Button-1>", lambda e: command())
    label.bind("<Enter>", lambda e: label.config(bg="#40291e" if bg_color == button_color else "#2e2c2b"))
    label.bind("<Leave>", lambda e: label.config(bg=bg_color))

    return label

def show_buttons():
    """
    Displays the main interface with options to Login, Register, or Exit.
    """
    # Remove any existing widgets from the panel
    for widget in panel_frame.winfo_children():
        widget.destroy()

    # Display the welcome title
    title_label = tk.Label(
        panel_frame,
        text=" Welcome! ",
        font=(font_family, title_font_size),
        fg="white",
        bg=label_title_color,
        relief="solid",
        width=15
    )
    title_label.place(relx=0.5, rely=0.2, anchor="center")

    # Display project information
    info_label = tk.Label(
        panel_frame,
        text="🧠 AI Image Generator\n"
             "Type anything — and we'll turn it into an image using deep learning magic!\n"
             "Built with PyTorch, CLIP, and Stable Diffusion under the hood."
             "\nProject by Shreya 💁‍♀ and Atirath 👨‍💻\n under Guidance of Prof. Helsing 🦹✨",
        font=(font_family, int(small_font_size * 0.6)),
        fg="black",
        bg=panel_bg_color,
        justify="center",
        wraplength=panel_width - 40
    )
    info_label.place(relx=0.5, rely=0.85, anchor="center")

    # Create the Login button
    create_fake_button(
        parent=panel_frame,
        text="Login",
        font_size=button_font_size,
        bg_color=button_color,
        fg_color="white",
        command=lambda: Login.show_login(panel_frame, show_buttons, player, button_color, label_title_color, panel_width, panel_height),
        y_relative=0.4
    )

    # Create the Register button
    create_fake_button(
        parent=panel_frame,
        text="Register",
        font_size=button_font_size,
        bg_color=button_color,
        fg_color="white",
        command=lambda: Register.show_register(panel_frame, show_buttons, player, button_color, label_title_color,
                                               panel_width),
        y_relative=0.5
    )

    # Create the Exit button
    create_fake_button(
        parent=panel_frame,
        text="Exit",
        font_size=small_font_size,
        bg_color=label_title_color,
        fg_color="white",
        command=root.destroy,
        y_relative=0.65
    )

# Display the initial set of buttons
show_buttons()

# Start the main event loop to run the application
root.mainloop()
