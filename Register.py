import pickle
import re
import tkinter as tk
import Login


def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True


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


def save_registration(name, email, password):
    user_data = {"name": name, "email": email, "password": password}
    with open("data.pkl", "ab") as file:
        pickle.dump(user_data, file)


def show_register(frame, go_back_callback, player, button_color, label_title_color, panel_width):
    for widget in frame.winfo_children():
        widget.destroy()

    form = tk.Frame(frame, bg="#f0e3da")
    form.pack(pady=30)

    tk.Label(form, text="  Register!  ", font=("Comic Sans MS", (int)(panel_width*0.05)), bg=label_title_color, fg="white", borderwidth=1).grid(
        row=0, column=0, columnspan=2, pady=30
    )

    labels = ["Name", "Email", "Password", "Re-Password"]
    entries, error_labels = {}, {}

    for i, label in enumerate(labels):
        tk.Label(form, text=label, font=("Comic Sans MS", (int)(panel_width*0.03)), bg=button_color, fg="white").grid(
            row=1 + i * 2, column=0, padx=10, sticky="e"
        )

        entry = tk.Entry(form, font=("Comic Sans MS", (int)(panel_width*0.03)), show="*" if "Password" in label else "", width=(int)(panel_width*0.06))
        entry.grid(row=1 + i * 2, column=1, padx=10, pady=(5, 10), sticky="w")
        entries[label] = entry

        error = tk.Label(form, text="", font=("Comic Sans MS", (int)(panel_width*0.02)), fg="white", bg="#7a0b29", justify="left", anchor="w")
        error.grid(row=2 + i * 2, column=1, columnspan=1, padx=10, pady=(0, 8), sticky="w")
        error.grid_remove()
        error_labels[label] = error

    def clear_errors():
        for label in error_labels.values():
            label.grid_remove()

    def validate_name(event=None):
        username = entries["Name"].get()
        if not username:
            error_labels["Name"].config(text="Name required")
            error_labels["Name"].grid()
        else:
            error_labels["Name"].grid_remove()

    def validate_email(event=None):
        email = entries["Email"].get()
        if not email:
            error_labels["Email"].config(text="Email required")
            error_labels["Email"].grid()
        elif not is_valid_email(email):
            error_labels["Email"].config(text="Invalid email format")
            error_labels["Email"].grid()
        else:
            for user in load_registrations():
                if user["email"] == email:
                    error_labels["Email"].config(text="Email already exists")
                    error_labels["Email"].grid()
                    break
            else:
                error_labels["Email"].grid_remove()

    def validate_password(event=None):
        password = entries["Password"].get()
        if not is_strong_password(password):
            error_labels["Password"].config(
                text="Expected:\nMinimum length:8\n1 special char, 1 uppercase\n1 lowercase, 1 digit"
            )
            error_labels["Password"].grid()
            return False
        else:
            error_labels["Password"].grid_remove()
            return True

    def validate_re_password(event=None):
        password = entries["Password"].get()
        confirm_password = entries["Re-Password"].get()
        if confirm_password and confirm_password != password:
            error_labels["Re-Password"].config(text="Passwords do not match")
            error_labels["Re-Password"].grid()
        else:
            error_labels["Re-Password"].grid_remove()

    entries["Name"].bind("<FocusOut>", validate_name)
    entries["Email"].bind("<FocusOut>", validate_email)
    entries["Password"].bind("<FocusOut>", validate_password)
    entries["Re-Password"].bind("<FocusOut>", validate_re_password)

    def register_logic():
        clear_errors()
        username = entries["Name"].get()
        email = entries["Email"].get()
        password = entries["Password"].get()
        confirm_password = entries["Re-Password"].get()
        has_error = False

        if not username:
            error_labels["Name"].config(text="Name required")
            error_labels["Name"].grid()
            has_error = True

        if not email:
            error_labels["Email"].config(text="Email required")
            error_labels["Email"].grid()
            has_error = True
        elif not is_valid_email(email):
            error_labels["Email"].config(text="Invalid email format")
            error_labels["Email"].grid()
            has_error = True
        else:
            for user in load_registrations():
                if user["email"] == email:
                    error_labels["Email"].config(text="Email already exists")
                    error_labels["Email"].grid()
                    has_error = True
                    break

        if not is_strong_password(password):
            error_labels["Password"].config(
                text="Expected:\nMinimum length:8\n1 special char, 1 uppercase\n1 lowercase, 1 digit"
            )
            error_labels["Password"].grid()
            has_error = True

        if confirm_password != password:
            error_labels["Re-Password"].config(text="Passwords do not match")
            error_labels["Re-Password"].grid()
            has_error = True

        if not has_error:
            save_registration(username, email, password)
            go_back_callback()

    register_canvas = tk.Canvas(form, width=(int)(panel_width*0.2), height=(int)(panel_width*0.5), bg="#f0e3da", highlightthickness=0, bd=0)
    register_canvas.grid(row=len(labels) * 2 + 1, column=0, columnspan=2, pady=10)

    register_button = tk.Label(
        register_canvas,
        text="Register",
        font=("Comic Sans MS", (int)(panel_width*0.035)),
        bg=label_title_color,
        fg="white",
        width=(int)(panel_width*0.030),
        height=1
    )
    register_button.pack(fill="both", expand=True)
    register_button.bind("<Button-1>", lambda e: register_logic())
    register_button.bind("<Enter>", lambda e: register_button.config(bg="#2f2b2a"))
    register_button.bind("<Leave>", lambda e: register_button.config(bg=label_title_color))

    back_canvas = tk.Canvas(form, width=(int)(panel_width*0.2), height=(int)(panel_width*0.5), bg="#f0e3da", highlightthickness=0, bd=0)
    back_canvas.grid(row=len(labels) * 2 + 2, column=0, columnspan=2, pady=5)

    back_button = tk.Label(
        back_canvas,
        text="Back",
        font=("Comic Sans MS", (int)(panel_width*0.035)),
        bg=label_title_color,
        fg="white",
        width=(int)(panel_width*0.03),
        height=1
    )
    back_button.pack(fill="both", expand=True)
    back_button.bind("<Button-1>", lambda e: go_back_callback())
    back_button.bind("<Enter>", lambda e: back_button.config(bg="#2f2b2a"))
    back_button.bind("<Leave>", lambda e: back_button.config(bg=label_title_color))
