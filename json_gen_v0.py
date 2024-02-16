import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import ttk
import json

key_descriptions = {
    "key1": {"description": "Integer value for key1", "type": "integer"},
    "key2": {"description": "Real-numbered value for key2", "type": "float"},
    "key3": {"description": "Description for key3, which can be quite long and may wrap to the next line if necessary", "type": "text"},
    "key4": {"description": "Float type vector values for key4 (comma-separated)", "type": "float_vector"},
    "key5": {"description": "Float type matrix values for key5 (linebreak-separated rows, comma-separated columns)", "type": "float_matrix"},
    "key6": {"description": "Integer type vector values for key6 (comma-separated)", "type": "int_vector"},
    "key7": {"description": "Integer type matrix values for key7 (linebreak-separated rows, comma-separated columns)", "type": "int_matrix"},
    "key8": {"description": "Text type vector values for key8 (comma-separated)", "type": "text_vector"},
    "key9": {"description": "Text type matrix values for key9 (linebreak-separated rows, comma-separated columns)", "type": "text_matrix"}
}

# Grouping keys into categories
key_categories = {
    "cat1": ["key1", "key2", "key3"],
    "cat2": ["key4", "key5", "key6"],
    "cat3": ["key7", "key8", "key9"]
}

# Set the width for user entry, scrolled text, key label, and description label
user_entry_width = 20
scrolled_text_width = 20
key_label_width = 10
description_label_width = 30

def generate_json(file_name, entry_values):
    data = {}
    for category_keys in key_categories.values():
        for key in category_keys:
            info = key_descriptions[key]
            value = get_entry_value(key, info["type"], entry_values)

            if value is not None:
                data[key] = value
            print(f"Generating '{key}': {value}")

    with open(file_name, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"JSON file '{file_name}' generated successfully.")

def load_json(entry_values):
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])

    if file_path:
        try:
            with open(file_path, 'r') as f:
                loaded_data = json.load(f)

            for key, info in key_descriptions.items():
                if key in entry_values and key in loaded_data:
                    formatted_value = format_loaded_value(loaded_data[key], info["type"])
                    set_entry_value(key, formatted_value, entry_values)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON file '{file_path}'.")

def clean_input(value):
    return value.strip()

def parse_vector(value, data_type=float):
    return [data_type(v.strip()) if v.strip() else None for v in value.replace(" ", "").split(',')]

def parse_matrix(value, data_type=float):
    rows = [row.strip().split(',') for row in value.split('\n') if row.strip()]
    return [
        [data_type(cell.strip()) if cell.strip() else None for cell in row]
        for row in rows if any(cell.strip() for cell in row)
    ]

def parse_text_vector(value):
    return [v.strip() for v in value.replace(" ", "").split(',') if v.strip()]

def parse_text_matrix(value):
    rows = [row.strip().split(',') for row in value.split('\n') if row.strip()]
    return [
        [cell.strip() for cell in row if cell.strip()]
        for row in rows if any(cell.strip() for cell in row)
    ]

def parse_int_vector(value):
    return [int(v.strip()) if v.strip() else None for v in value.replace(" ", "").split(',')]

def parse_int_matrix(value):
    rows = [row.strip().split(',') for row in value.split('\n')]
    return [
        [int(cell.strip()) if cell.strip() else None for cell in row]
        for row in rows if any(cell.strip() for cell in row)
    ]

def get_entry_value(key, entry_type, entry_values):
    if isinstance(entry_values[key], scrolledtext.ScrolledText):
        value = entry_values[key].get("1.0", tk.END)
    else:
        value = entry_values[key].get()

    cleaned_value = clean_input(value)

    if cleaned_value:
        try:
            if entry_type == "integer":
                return int(cleaned_value)
            elif entry_type == "float":
                return float(cleaned_value)
            elif entry_type == "text":
                return cleaned_value
            elif entry_type == "int_vector":
                return parse_int_vector(cleaned_value)
            elif entry_type == "int_matrix":
                return parse_int_matrix(cleaned_value)
            elif "float_vector" in entry_type:
                return parse_vector(cleaned_value, float)
            elif "float_matrix" in entry_type:
                return parse_matrix(cleaned_value, float)
            elif "text_vector" in entry_type:
                return parse_text_vector(cleaned_value)
            elif "text_matrix" in entry_type:
                return parse_text_matrix(cleaned_value)
        except ValueError:
            print(f"Error: Invalid input for '{key}'. Expected type: {entry_type}.")
    return None

def format_loaded_value(value, entry_type):
    if entry_type in ["float_matrix", "int_matrix", "text_matrix"]:
        return "\n".join([', '.join(map(str, row)) for row in value])
    elif entry_type in ["float_vector", "int_vector", "text_vector"]:
        return ", ".join(map(str, value))
    else:
        return str(value)

def set_entry_value(key, formatted_value, entry_values):
    if isinstance(entry_values[key], scrolledtext.ScrolledText):
        entry_values[key].delete("1.0", tk.END)
        entry_values[key].insert(tk.END, formatted_value)
    else:
        entry_values[key].delete(0, tk.END)
        entry_values[key].insert(tk.END, formatted_value)

def generate_json_with_user_input(entry_values):
    file_name = filedialog.asksaveasfilename(defaultextension="", filetypes=[("JSON files", "*.json")])
    if file_name:
        generate_json(file_name, entry_values)

def add_entry(frame, key, description, entry_type, entry_values, user_entry_width=20, scrolled_text_width=40, key_label_width=10, description_label_width=30):
    entry_frame = tk.Frame(frame, relief=tk.FLAT, borderwidth=0)
    entry_frame.grid(sticky="w", pady=5)

    label_key_text = f"{key} ({entry_type}):"
    label_key = tk.Label(entry_frame, text=label_key_text, width=key_label_width, anchor='w', wraplength=100)  # Adjust wraplength as needed
    label_description = tk.Label(entry_frame, text=description, wraplength=300, justify="left", width=description_label_width, anchor='w')

    if entry_type == "float_matrix" or entry_type == "int_matrix" or entry_type == "text_matrix":
        entry_values[key] = scrolledtext.ScrolledText(entry_frame, width=scrolled_text_width, height=5, wrap=tk.WORD)
    else:
        entry_values[key] = tk.Entry(entry_frame, width=user_entry_width)

    label_key.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    label_description.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    entry_values[key].grid(row=0, column=2, padx=5, pady=5, sticky='w')

def on_key_press(event):
    # Check if the focus is on an entry widget
    if root.focus_get() and isinstance(root.focus_get(), (tk.Entry, scrolledtext.ScrolledText)):
        return

    # Get the current position of the canvas
    x, y = canvas.canvasx(0), canvas.canvasy(0)

    # Define the amount to scroll in both x and y directions
    scroll_delta = 20
    page_scroll_delta = 200  # Adjust as needed

    # Check the pressed key and update the canvas position accordingly
    if event.keysym == "Up":
        canvas.yview_scroll(-1, "units")
    elif event.keysym == "Down":
        canvas.yview_scroll(1, "units")
    elif event.keysym == "Left":
        canvas.xview_scroll(-1, "units")
    elif event.keysym == "Right":
        canvas.xview_scroll(1, "units")
    elif event.keysym == "Prior":  # Page Up
        canvas.yview_scroll(-page_scroll_delta, "pages")
    elif event.keysym == "Next":  # Page Down
        canvas.yview_scroll(page_scroll_delta, "pages")

    # Get the new position of the canvas after scrolling
    new_x, new_y = canvas.canvasx(0), canvas.canvasy(0)

    # Adjust the scroll region of the canvas based on the new position
    canvas.scan_dragto(new_x, new_y, gain=1)

def on_click(event):
    # Check if the click event happened outside of entry widgets
    if not any(isinstance(event.widget, widget_type) for widget_type in (tk.Entry, scrolledtext.ScrolledText)):
        # Set focus to a dummy widget (e.g., the root window) to disable entry widget cursor
        root.focus_set()


# Create the root window
root = tk.Tk()
root.title("JSON Generator")

# Bind the click event to the root window
root.bind("<Button-1>", on_click)

# Bind arrow key events to the on_key_press function
root.bind("<Up>", on_key_press)
root.bind("<Down>", on_key_press)
root.bind("<Left>", on_key_press)
root.bind("<Right>", on_key_press)
root.bind("<Prior>", on_key_press)  # Page Up
root.bind("<Next>", on_key_press)   # Page Down

# Create a frame for the category frames
frame_container = tk.Frame(root)
frame_container.pack(expand=True, fill=tk.BOTH)

canvas = tk.Canvas(frame_container)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a vertical scrollbar to the canvas
scrollbar = ttk.Scrollbar(frame_container, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas and scrollbar to work together
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
# Bind mouse wheel event to the entire window


# Create a frame to contain the category frames within the canvas
frame_inner = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_inner, anchor=tk.NW)

entry_values = {}  # Define entry_values here to avoid the NameError

# Add frames for each category with the maximum width
cumulative_height = 0  # Track the total height of the frames
for category, keys in key_categories.items():
    frame = tk.Frame(frame_inner, relief=tk.GROOVE, borderwidth=2)
    frame.grid(row=cumulative_height, column=0, columnspan=3, padx=5, pady=5, sticky='w')
    tk.Label(frame, text=f"{category.capitalize()} Keys", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=3)

    for key in keys:
        add_entry(frame, key, key_descriptions[key]["description"], key_descriptions[key]["type"], entry_values,
                  user_entry_width=user_entry_width, scrolled_text_width=scrolled_text_width,
                  key_label_width=key_label_width, description_label_width=description_label_width)

    # Update the cumulative height for the next category
    cumulative_height += len(frame.grid_info())

# Buttons
generate_button = tk.Button(root, text="Generate JSON", command=lambda: generate_json_with_user_input(entry_values))
generate_button.pack(pady=10)

load_button = tk.Button(root, text="Load JSON", command=lambda: load_json(entry_values))
load_button.pack(pady=10)

root.geometry("800x800")
root.mainloop()