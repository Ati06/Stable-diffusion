import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import threading
from demo import generate_from_prompt

# Theme settings
button_color = "#573a2e"
label_title_color = "#403835"
panel_bg_color = "#f0e3da"
font_family = "Comic Sans MS"

def show_prompt(root, emailId, user_name,show_buttons, player, screen_width, screen_height):
    panel_relwidth = 0.6
    panel_relheight = 0.4

    old_panel = tk.Frame(root, bg=panel_bg_color)
    old_panel.place(relx=0.5, rely=0.5, anchor="center", relwidth=panel_relwidth, relheight=panel_relheight)

    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) and hasattr(widget, 'image'):
            widget.lower()

    old_panel.lift()

    panel = tk.Frame(old_panel, bg=panel_bg_color)
    panel.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

    title_font_size = int(screen_height * 0.025)
    entry_font_size = int(screen_height * 0.020)
    button_font_size = int(screen_height * 0.019)

    title_label = tk.Label(
        panel,
        text=f"Welcome {user_name}! Enter prompt below to generate image! ",
        font=(font_family, title_font_size),
        bg="#47131d",
        fg="white",
        relief="solid"
    )
    title_label.place(relx=0.5, rely=0.18, anchor="center")

    input_frame = tk.Frame(panel, bg=panel_bg_color)
    input_frame.place(relx=0.5, rely=0.38, anchor="center", relwidth=0.8, relheight=0.15)

    prompt_entry = tk.Entry(
        input_frame,
        font=(font_family, entry_font_size)
    )
    prompt_entry.pack(side="left", fill="both", expand=True, padx=(int(screen_width * 0.01), 5), pady=5)

    loading_label = tk.Label(panel, text="", font=(font_family, button_font_size), bg=panel_bg_color, fg="black")
    loading_label.place(relx=0.5, rely=0.58, anchor="center")

    progress = ttk.Progressbar(panel, orient='horizontal', length=300, mode='determinate', maximum=100)
    progress.place(relx=0.5, rely=0.66, anchor='center')
    progress.place_forget()

    percentage_label = tk.Label(panel, text="0%", font=(font_family, button_font_size), bg=panel_bg_color, fg="black")
    percentage_label.place(relx=0.5, rely=0.70, anchor="center")
    percentage_label.place_forget()

    def set_generation_progress(percent):
        progress.after(0, lambda: progress.config(value=percent))
        percentage_label.after(0, lambda: percentage_label.config(text=f"{percent}%"))

    def simulate_generation():
        prompt = prompt_entry.get().strip()
        image = generate_from_prompt(prompt, progress_callback=set_generation_progress)
        progress.stop()
        progress.place_forget()
        percentage_label.place_forget()
        loading_label.config(text="")

        img_win = tk.Toplevel(root)
        img_win.title("Generated Image")
        img_win.geometry("512x512")

        tk_image = ImageTk.PhotoImage(image)
        label = tk.Label(img_win, image=tk_image)
        label.image = tk_image
        label.pack(expand=True, fill="both")
        submit_button.config(state="normal")

    def submit_prompt():
        prompt = prompt_entry.get().strip()
        if not prompt:
            messagebox.showerror("Error", "Prompt cannot be empty!")
        else:
            submit_button.config(state="disabled")
            loading_label.config(text="Generating......")
            progress.place(relx=0.5, rely=0.66, anchor='center')
            percentage_label.place(relx=0.5, rely=0.70, anchor="center")
            threading.Thread(target=simulate_generation, daemon=True).start()

    submit_canvas = tk.Canvas(input_frame, width=120, height=40, bg=panel_bg_color, highlightthickness=0, bd=0)
    submit_canvas.pack(side="right", padx=(5, 10), pady=5)

    submit_button = tk.Label(
        submit_canvas,
        text="Submit",
        font=(font_family, button_font_size + 1),
        bg="#7a2534",
        fg="white"
    )
    submit_button.pack(fill="both", expand=True)
    submit_button.bind("<Button-1>", lambda e: submit_prompt())
    submit_button.bind("<Enter>", lambda e: submit_button.config(bg="#63071a"))
    submit_button.bind("<Leave>", lambda e: submit_button.config(bg="#450511"))

    exit_canvas = tk.Canvas(panel, bg=panel_bg_color, highlightthickness=0, bd=0)
    exit_canvas.place(relx=0.5, rely=0.90, anchor="center", relwidth=0.18, relheight=0.10)

    exit_button = tk.Label(
        exit_canvas,
        text="Exit",
        font=(font_family, button_font_size),
        bg=button_color,
        fg="white"
    )
    exit_button.pack(fill="both", expand=True)
    exit_button.bind("<Button-1>", lambda e: root.destroy())
    exit_button.bind("<Enter>", lambda e: exit_button.config(bg="#40291e"))
    exit_button.bind("<Leave>", lambda e: exit_button.config(bg=button_color))

    info_label = tk.Label(
        root,
        text="Information: This is an image generation application.\nYou need to enter an appropriate prompt!",
        font=(font_family, int(screen_height * 0.018), "bold"),
        bg=panel_bg_color,
        fg="#3a3a3a",
        justify="center"
    )
    info_label.place(relx=0.5, rely=0.72, anchor="n", relwidth=panel_relwidth, relheight=0.1)
