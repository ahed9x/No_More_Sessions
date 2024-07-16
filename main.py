import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui as pg
import time
import threading
from PIL import ImageGrab
from pynput import mouse

# Function to automate the clicking process
def automate_clicking(closed_chrome_logo, opened_tab_logo, closed_tab_logo, opened_image_logo, closed_image_logo):
    try:
        # Add a small delay between operations to reduce CPU usage
        time.sleep(0.5)

        # Click on Chrome
        closed_tab_location = pg.locateCenterOnScreen(closed_tab_logo, confidence=0.8)
        opened_tab_location = pg.locateCenterOnScreen(opened_tab_logo, confidence=0.8)
        closed_chrome_location = pg.locateCenterOnScreen(closed_chrome_logo, confidence=0.8)
        if closed_chrome_location and not opened_tab_location and not closed_tab_location:
            pg.click(closed_chrome_location)
            time.sleep(1)  # Adding delay to allow GUI to update

        # Click on the tab by logo
        
        if opened_tab_location:
            pg.click(opened_tab_location)
            time.sleep(0.5)

        
        if closed_tab_location:
            pg.click(closed_tab_location)
            time.sleep(0.5)

        # Click on the specific image
        opened_image_location = pg.locateCenterOnScreen(opened_image_logo, confidence=0.8)
        if opened_image_location:
            pg.click(opened_image_location)
            time.sleep(0.5)

        closed_image_location = pg.locateCenterOnScreen(closed_image_logo, confidence=0.8)
        if closed_image_location:
            pg.click(closed_image_location)
            time.sleep(0.5)
    except Exception as e:
        print(f"Error during automate_clicking: {e}")

# Function to start the automation
def start_automation():
    pg.FAILSAFE = True  # Ensure the failsafe feature is on for safety

    try:
        wait_time = float(entry_wait_time.get()) * 60
        run_time = float(entry_run_time.get()) * 60
        closed_chrome_logo = entry_closed_chrome_logo.cget("text")
        opened_tab_logo = entry_opened_tab_logo.cget("text")
        closed_tab_logo = entry_closed_tab_logo.cget("text")
        opened_image_logo = entry_opened_image_logo.cget("text")
        closed_image_logo = entry_closed_image_logo.cget("text")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for wait time.")
        return

    def run_automation():
        nonlocal wait_time, run_time
        real_start_time = time.time()
        start_time = time.time()

        def is_image_on_screen():
            return pg.locateOnScreen(opened_tab_logo, confidence=0.8) is not None

        def on_move(x, y):
            nonlocal start_time
            if is_image_on_screen():
                start_time = time.time()

        def on_click(x, y, button, pressed):
            nonlocal start_time
            if is_image_on_screen():
                start_time = time.time()

        def on_scroll(x, y, dx, dy):
            nonlocal start_time
            if is_image_on_screen():
                start_time = time.time()

        # Start the mouse listener
        listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
        listener.start()

        try:
            while time.time() - real_start_time < run_time:
                if time.time() - start_time > wait_time:
                    automate_clicking(closed_chrome_logo, opened_tab_logo, closed_tab_logo, opened_image_logo, closed_image_logo)
                    start_time = time.time()
                time.sleep(1)  # Reduce the loop frequency to ease CPU load
        except KeyboardInterrupt:
            print("Program exited by user")
        finally:
            listener.stop()

    # Start the automation in a separate thread to keep the GUI responsive
    threading.Thread(target=run_automation).start()

# Functions for file dialogs and screenshots
def select_logo(entry_widget):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        entry_widget.config(text=file_path)

def take_screenshot(entry_widget):
    screenshot_window = tk.Toplevel(root)
    screenshot_window.attributes('-fullscreen', True)
    screenshot_window.attributes('-alpha', 0.3)
    screenshot_window.configure(bg='grey')

    canvas = tk.Canvas(screenshot_window, cursor="cross")
    canvas.pack(fill=tk.BOTH, expand=True)

    def on_mouse_press(event):
        canvas.start_x = event.x
        canvas.start_y = event.y
        canvas.rect = canvas.create_rectangle(canvas.start_x, canvas.start_y, canvas.start_x, canvas.start_y, outline='red')

    def on_mouse_drag(event):
        canvas.coords(canvas.rect, canvas.start_x, canvas.start_y, event.x, event.y)

    def on_mouse_release(event):
        x1 = min(canvas.start_x, event.x)
        y1 = min(canvas.start_y, event.y)
        x2 = max(canvas.start_x, event.x)
        y2 = max(canvas.start_y, event.y)
        screenshot_window.destroy()
        capture(entry_widget, x1, y1, x2, y2)

    canvas.bind("<ButtonPress-1>", on_mouse_press)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)

def capture(entry_widget, x1, y1, x2, y2):
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if img_path:
        img.save(img_path)
        entry_widget.config(text=img_path)
    root.state('normal')

# Initialize the Tkinter GUI
root = tk.Tk()
root.title("Automation Tool")
root.geometry("300x600")
root.configure(bg='#1ec6ff')

frame = tk.Frame(root, bg='#1ec6ff')
frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(frame, bg='#1ec6ff')
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas.bind('<Configure>', on_frame_configure)
canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

inner_frame = tk.Frame(canvas, bg='#1ec6ff')
canvas.create_window((0, 0), window=inner_frame, anchor="nw")

# Create widgets
def create_label(parent, text):
    label = tk.Label(parent, text=text, bg='#1ec6ff', font=("Arial", 12))
    label.pack(pady=4.5)
    return label

def create_entry(parent):
    entry = tk.Label(parent, text="", width=30, bg='white', anchor='w')
    entry.pack(pady=4.5)
    return entry

def create_buttons(parent, browse_command, screenshot_command):
    button_frame = tk.Frame(parent, bg='#1ec6ff')
    browse_button = tk.Button(button_frame, text="Browse", command=browse_command, fg="white", bg='#ff561e', bd=0, highlightthickness=1, font=("Arial", 10))
    browse_button.pack(side=tk.LEFT, padx=2)
    screenshot_button = tk.Button(button_frame, text="Screenshot", command=screenshot_command, fg="white", bg='#ff561e', bd=0, highlightthickness=1, font=("Arial", 10))
    screenshot_button.pack(side=tk.LEFT, padx=2)
    button_frame.pack(pady=4.5)
    return button_frame

label_closed_chrome_logo = create_label(inner_frame, "1. Select Chrome logo when closed:")
entry_closed_chrome_logo = create_entry(inner_frame)
create_buttons(inner_frame, lambda: select_logo(entry_closed_chrome_logo), lambda: take_screenshot(entry_closed_chrome_logo))

label_opened_tab_logo = create_label(inner_frame, "2. Select tab logo when opened:")
entry_opened_tab_logo = create_entry(inner_frame)
create_buttons(inner_frame, lambda: select_logo(entry_opened_tab_logo), lambda: take_screenshot(entry_opened_tab_logo))

label_closed_tab_logo = create_label(inner_frame, "3. Select tab logo when closed:")
entry_closed_tab_logo = create_entry(inner_frame)
create_buttons(inner_frame, lambda: select_logo(entry_closed_tab_logo), lambda: take_screenshot(entry_closed_tab_logo))

label_opened_image_logo = create_label(inner_frame, "4. Select clicked image when opened:")
entry_opened_image_logo = create_entry(inner_frame)
create_buttons(inner_frame, lambda: select_logo(entry_opened_image_logo), lambda: take_screenshot(entry_opened_image_logo))

label_closed_image_logo = create_label(inner_frame, "5. Select clicked image when closed:")
entry_closed_image_logo = create_entry(inner_frame)
create_buttons(inner_frame, lambda: select_logo(entry_closed_image_logo), lambda: take_screenshot(entry_closed_image_logo))

label_wait_time = create_label(inner_frame, "6. Wait time (min):")
entry_wait_time = tk.Entry(inner_frame, width=30)
entry_wait_time.pack(pady=4.5)

label_run_time = create_label(inner_frame, "7. keep opened for (min):")
entry_run_time = tk.Entry(inner_frame, width=30)
entry_run_time.pack(pady=4.5)

start_button = tk.Button(inner_frame, text="Start Automation", command=start_automation, bg='#c6ff1e', fg='black', font=("Arial", 12))
start_button.pack(pady=20)

for widget in inner_frame.winfo_children():
    widget.pack_configure(anchor="center")

inner_frame.bind("<Configure>", lambda e: on_frame_configure(e))

root.mainloop()
