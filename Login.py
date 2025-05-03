import tkinter as tk
import pickle
from tkinter import messagebox
import re
from Prompt import show_prompt  # Importing the prompt display function

# Define UI color scheme and font
button_color = "#573a2e"
label_title_color = "#403835"
panel_bg_color = "#f0e3da"
font_family = "Comic Sans MS"

# Function to load registered users from a pickle file
def load_registrations():
    try:
        with open("data.pkl", "rb") as file:
            registrations = []
            while True:
                try:
                    registrations.append(pickle.load(file))
                except EOFError:
                    break
            return registrations
    except FileNotFoundError:
        return []

# Function to display the login form
def show_login(frame, show_buttons, player, button_color, label_title_color, panel_width, panel_height):
    # Clear existing widgets from the frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Create a form frame within the main frame
    form = tk.Frame(frame, bg=panel_bg_color)
    form.pack(pady=30)

    # Title label for the login form
    tk.Label(form, text="Login!", font=(font_family, int(panel_width * 0.05)), bg=label_title_color, fg="white", width=10).grid(
        row=0, column=0, columnspan=2, pady=40
    )

    # Labels and entry fields for Email and Password
    labels = ["Email", "Password"]
    entries, error_labels = {}, {}

    for i, label in enumerate(labels):
        # Label for the field
        tk.Label(form, text=label, font=(font_family, int(panel_width * 0.03)), bg=button_color, fg="white").grid(
            row=1 + i * 2, column=0, padx=10, sticky="e"
        )

        # Entry field for user input
        entry = tk.Entry(
            form, font=(font_family, int(panel_width * 0.03)),
            show="*" if "Password" in label else "",
            width=int(panel_width * 0.06)
        )
        entry.grid(row=1 + i * 2, column=1, padx=10, pady=(5, 10), sticky="w")
        entries[label] = entry

        # Label to display error messages
        error = tk.Label(
            form, text="", font=(font_family, 12),
            fg="white", bg="#c71306",
            justify="left", anchor="w"
        )
        error.grid(row=2 + i * 2, column=1, columnspan=1, padx=10, pady=(0, 8), sticky="w")
        error.grid_remove()
        error_labels[label] = error

    # Function to clear all error messages
    def clear_errors():
        for label in error_labels.values():
            label.grid_remove()

    # Function to handle login logic
    def login_logic():
        clear_errors()
        email = entries["Email"].get()
        password = entries["Password"].get()
        root = frame.winfo_toplevel()

        has_error = False

        # Validate email field
        if not email:
            error_labels["Email"].config(text="Email required")
            error_labels["Email"].grid()
            has_error = True

        # Validate password field
        if not password:
            error_labels["Password"].config(text="Password required")
            error_labels["Password"].grid()
            has_error = True

        # Proceed if no validation errors
        if not has_error:
            for user in load_registrations():
                if user["email"] == email and user["password"] == password:
                    print("Login successful!")
                    frame.destroy()
                    # Show the prompt screen upon successful login
                    show_prompt(
                        root,
                        emailId=email,
                        user_name=user.get("name", "User"),
                        show_buttons=show_buttons,
                        player=player,
                        screen_width=root.winfo_screenwidth(),
                        screen_height=root.winfo_screenheight()
                    )
                    return

            # Display error if credentials are invalid
            error_labels["Email"].config(text="Invalid email or password")
            error_labels["Email"].grid()

    # Create a canvas for the login button
    login_canvas = tk.Canvas(form, width=int(panel_width * 0.2), height=int(panel_width * 0.5), bg=panel_bg_color, highlightthickness=0, bd=0)
    login_canvas.grid(row=len(labels) * 2 + 1, column=0, columnspan=2, pady=10)

    # Login button
    login_button = tk.Label(
        login_canvas,
        text="Login",
        font=(font_family, int(panel_width * 0.035)),
        bg=label_title_color,
        fg="white",
        width=int(panel_width * 0.030),
        height=1
    )
    login_button.pack(fill="both", expand=True)
    login_button.bind("<Button-1>", lambda e: login_logic())
    login_button.bind("<Enter>", lambda e: login_button.config(bg="#2f2b2a"))
    login_button.bind("<Leave>", lambda e: login_button.config(bg=label_title_color))

    # Create a canvas for the back button
    back_canvas = tk.Canvas(form, width=int(panel_width * 0.2), height=int(panel_width * 0.5), bg=panel_bg_color, highlightthickness=0, bd=0)
    back_canvas.grid(row=len(labels) * 2 + 2, column=0, columnspan=2, pady=5)

    # Back button to return to the previous screen
    back_button = tk.Label(
        back_canvas,
        text="Back",
        font=(font_family, int(panel_width * 0.035)),
        bg=label_title_color,
        fg="white",
        width=int(panel_width * 0.03),
        height=1
    )
    back_button.pack(fill="both", expand=True)
    back_button.bind("<Button-1>", lambda e: show_buttons())
    back_button.bind("<Enter>", lambda e: back_button.config(bg="#2f2b2a"))
    back_button.bind("<Leave>", lambda e: back_button.config(bg=label_title_color))
