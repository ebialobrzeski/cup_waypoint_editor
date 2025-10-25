"""Main entry point for XCSoar CUP Editor."""

import tkinter as tk
from xcsoar_editor.gui import MainWindow


def main():
    """Launch the XCSoar CUP Editor application."""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
