import tkinter as tk

COLOR_RED = "#990000"
COLOR_FRAME = "#151E3F"
COLOR_BG = "#080E27"

# Frame grid dimensions
ROWS_NE = 8
COLS_NE = 8
PADDING = 2

def main():
    # Create the main window
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.config(bg=COLOR_BG)

    frame_left = tk.Frame(root, bg=COLOR_FRAME)
    frame_ne = tk.Frame(root, bg=COLOR_FRAME)
    frame_se = tk.Frame(root, bg=COLOR_FRAME)
    frame_left.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=PADDING, pady=PADDING)
    frame_ne.grid(row=0, column=1, sticky="nsew", padx=PADDING, pady=PADDING)
    frame_se.grid(row=1, column=1, sticky="nsew", padx=PADDING, pady=PADDING)

    for i in range(ROWS_NE):
        frame_ne.grid_rowconfigure(i, weight=1)
    for i in range(COLS_NE):
        frame_ne.grid_columnconfigure(i, weight=1)

    quit_button = tk.Button(
        frame_ne,
        text="Bye",
        command=root.quit
    )

    quit_button.grid(
        row=0,
        column=7,
        sticky="nsew",
        padx=10,
        pady=10
    )

    for i in range(2):
        root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(i, weight=1)            

    # Start the GUI event Loop
    root.mainloop()

if __name__ == "__main__":
    main()