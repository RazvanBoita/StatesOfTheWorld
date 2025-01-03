import requests
import tkinter as tk
from tkinter import ttk, messagebox
import json

BASE_URL = "http://127.0.0.1:5000/api/countries"

def fetch_data(endpoint, params=None):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
        return []

def display_results(data):
    results_box.configure(state="normal")  # Enable editing temporarily
    results_box.delete("1.0", tk.END)
    if isinstance(data, (list, dict)):
        formatted_data = json.dumps(data, indent=4)
        results_box.insert(tk.END, formatted_data)
    else:
        results_box.insert(tk.END, str(data))
    results_box.configure(state="disabled")  # Make it read-only again

def get_all_countries():
    data = fetch_data("/")
    display_results(data)

def get_top_by_population():
    n = 10  # Default value
    data = fetch_data("/top-population", {"n": n})
    display_results(data)

def get_top_by_density():
    n = 10  # Default value
    data = fetch_data("/top-density", {"n": n})
    display_results(data)

def get_countries_by_language():
    language = language_input.get()
    if not language:
        messagebox.showwarning("Warning", "Please enter a language.")
        return
    data = fetch_data("/speaking", {"language": language})
    display_results(data)

def get_countries_by_timezone():
    timezone = timezone_input.get()
    if not timezone:
        messagebox.showwarning("Warning", "Please enter a timezone.")
        return
    data = fetch_data("/timezone", {"timezone": timezone})
    display_results(data)

def get_countries_by_regime():
    regime = regime_input.get()
    if not regime:
        messagebox.showwarning("Warning", "Please enter a regime.")
        return
    data = fetch_data("/political", {"regime": regime})
    display_results(data)

# Set up the GUI
root = tk.Tk()
root.title("Country API Client")
root.geometry("700x500")

# Frame for inputs
input_frame = ttk.Frame(root)
input_frame.pack(pady=10, padx=10, fill="x")

ttk.Label(input_frame, text="Language:").grid(row=0, column=0, sticky="w")
language_input = ttk.Entry(input_frame)
language_input.grid(row=0, column=1)

ttk.Label(input_frame, text="Timezone:").grid(row=1, column=0, sticky="w")
timezone_input = ttk.Entry(input_frame)
timezone_input.grid(row=1, column=1)

ttk.Label(input_frame, text="Regime:").grid(row=2, column=0, sticky="w")
regime_input = ttk.Entry(input_frame)
regime_input.grid(row=2, column=1)

# Frame for buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10, padx=10, fill="x")

ttk.Button(button_frame, text="Get All Countries", command=get_all_countries).grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="Top by Population", command=get_top_by_population).grid(row=0, column=1, padx=5)
ttk.Button(button_frame, text="Top by Density", command=get_top_by_density).grid(row=0, column=2, padx=5)
ttk.Button(button_frame, text="By Language", command=get_countries_by_language).grid(row=1, column=0, padx=5)
ttk.Button(button_frame, text="By Timezone", command=get_countries_by_timezone).grid(row=1, column=1, padx=5)
ttk.Button(button_frame, text="By Regime", command=get_countries_by_regime).grid(row=1, column=2, padx=5)

# Frame for results
results_frame = ttk.Frame(root)
results_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Add a scrollbar
scrollbar = ttk.Scrollbar(results_frame)
scrollbar.pack(side="right", fill="y")

# Add the results box
results_box = tk.Text(results_frame, wrap="word", height=15, state="disabled", yscrollcommand=scrollbar.set)
results_box.pack(pady=5, padx=5, fill="both", expand=True)

# Configure the scrollbar to work with the text box
scrollbar.config(command=results_box.yview)

# Run the GUI
root.mainloop()
