#!/usr/bin/env python3
# File Name: Print_tree.py
# Version 1.0
# Author: Sarah Schoem

"""
File name: HPAI_Human_map.py
Author: Sarah Schoem
Created: 2/13/25
Version: 1.0
Description:
    This script displays a phylogenetic tree of the H5 virus using the tree_analysis_output.txt file.

License: MIT License
"""

import os
import tkinter as tk
from tkinter import scrolledtext


def show_file_content(filename):
    # Get the directory of the current script (Print_tree.py)
    script_dir = os.path.dirname(os.path.abspath(__file__))  # This is the folder where Print_tree.py is located
    file_path = os.path.join(script_dir, filename)  # Combine the script directory with the filename

    # Create the main window
    window = tk.Tk()
    window.title("File Content Viewer")

    # Setting window parameters
    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=150,
                                          height=30)  # Adjust height to be less vertical
    text_area.pack(padx=10, pady=10)

    # Open and read the file
    try:
        with open(file_path, "r") as file:
            file_content = file.read()

        # Insert the file content into the text area
        text_area.insert(tk.END, file_content)

        # Run the application
        window.mainloop()  # Keep the window open
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found in {script_dir}")
