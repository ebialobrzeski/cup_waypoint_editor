"""Dialog windows for the XCSoar CUP Editor."""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional, Callable

from ..config import STYLE_OPTIONS, STYLE_LABELS, LATITUDE_MIN, LATITUDE_MAX, LONGITUDE_MIN, LONGITUDE_MAX
from ..models import Waypoint


class WaypointDialog:
    """Dialog for adding or editing a waypoint."""
    
    def __init__(self, parent: tk.Tk, waypoint: Optional[Waypoint] = None, 
                 on_save: Optional[Callable[[Waypoint], None]] = None):
        """
        Initialize the waypoint dialog.
        
        Args:
            parent: Parent window
            waypoint: Existing waypoint to edit (None for new waypoint)
            on_save: Callback function to call when waypoint is saved
        """
        self.parent = parent
        self.waypoint = waypoint
        self.on_save = on_save
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Waypoint" if waypoint else "Add Waypoint")
        self.dialog.geometry("400x180")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        
        # Bind keyboard shortcuts
        self.dialog.bind('<Return>', lambda e: self._save())
        self.dialog.bind('<Escape>', lambda e: self.dialog.destroy())
        
        # Center dialog on parent
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Create dialog widgets."""
        # Name
        tk.Label(self.dialog, text="Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.name_entry = tk.Entry(self.dialog, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Latitude
        tk.Label(self.dialog, text="Latitude:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.lat_entry = tk.Entry(self.dialog, width=30)
        self.lat_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Longitude
        tk.Label(self.dialog, text="Longitude:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.lon_entry = tk.Entry(self.dialog, width=30)
        self.lon_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Style
        tk.Label(self.dialog, text="Style:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.style_var = tk.StringVar()
        self.style_menu = ttk.Combobox(
            self.dialog, 
            textvariable=self.style_var, 
            values=list(STYLE_OPTIONS.values()), 
            state="readonly", 
            width=27
        )
        self.style_menu.grid(row=3, column=1, padx=5, pady=5)
        
        # Prefill if editing
        if self.waypoint:
            self.name_entry.insert(0, self.waypoint.name)
            self.lat_entry.insert(0, str(self.waypoint.latitude))
            self.lon_entry.insert(0, str(self.waypoint.longitude))
            self.style_menu.set(STYLE_OPTIONS.get(self.waypoint.style, "Waypoint"))
        else:
            self.style_menu.set("Waypoint")
        
        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        save_btn = tk.Button(button_frame, text="Save", command=self._save, width=10)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self.dialog.destroy, width=10)
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Focus on name entry
        self.name_entry.focus()
    
    def _save(self):
        """Validate and save the waypoint."""
        name = self.name_entry.get().strip()
        lat_text = self.lat_entry.get().strip()
        lon_text = self.lon_entry.get().strip()
        style_label = self.style_var.get()
        
        # Validation
        if not name:
            messagebox.showerror("Invalid Input", "Name cannot be empty", parent=self.dialog)
            return
        
        if not lat_text or not lon_text:
            messagebox.showerror("Invalid Input", "Latitude and Longitude cannot be empty", parent=self.dialog)
            return
        
        try:
            lat = float(lat_text)
            lon = float(lon_text)
        except ValueError:
            messagebox.showerror(
                "Invalid Input", 
                "Latitude and Longitude must be valid numbers (e.g., 52.7652, 23.1867)",
                parent=self.dialog
            )
            return
        
        # Validate coordinate ranges
        if not (LATITUDE_MIN <= lat <= LATITUDE_MAX):
            messagebox.showerror(
                "Invalid Input", 
                f"Latitude must be between {LATITUDE_MIN} and {LATITUDE_MAX}",
                parent=self.dialog
            )
            return
        
        if not (LONGITUDE_MIN <= lon <= LONGITUDE_MAX):
            messagebox.showerror(
                "Invalid Input", 
                f"Longitude must be between {LONGITUDE_MIN} and {LONGITUDE_MAX}",
                parent=self.dialog
            )
            return
        
        style_code = STYLE_LABELS.get(style_label, 1)
        
        # Create or update waypoint
        if self.waypoint:
            # Update existing waypoint
            self.waypoint.name = name
            self.waypoint.latitude = lat
            self.waypoint.longitude = lon
            self.waypoint.style = style_code
            self.result = self.waypoint
        else:
            # Create new waypoint
            self.result = Waypoint(
                name=name,
                latitude=lat,
                longitude=lon,
                style=style_code
            )
        
        # Call callback if provided
        if self.on_save:
            self.on_save(self.result)
        
        self.dialog.destroy()
    
    def show(self) -> Optional[Waypoint]:
        """
        Show the dialog and wait for result.
        
        Returns:
            Waypoint object if saved, None if cancelled
        """
        self.dialog.wait_window()
        return self.result
