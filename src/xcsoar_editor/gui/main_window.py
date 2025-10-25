"""Main window for the XCSoar CUP Editor."""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import List, Optional

from ..models import Waypoint
from ..file_io import parse_cup_file, write_cup_file, parse_csv_file, write_csv_file
from ..config import STYLE_OPTIONS
from .dialogs import WaypointDialog


class MainWindow:
    """Main application window for XCSoar CUP Editor."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the main window.
        
        Args:
            root: Root Tk window
        """
        self.root = root
        self.root.title("XCSoar CUP Editor")
        self.root.geometry("1200x600")  # Wider for more columns
        
        self.waypoints: List[Waypoint] = []
        self.cup_file_path: Optional[str] = None
        self.modified = False
        
        # Register close handler
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        self._create_widgets()
        self._update_title()
    
    def _create_widgets(self):
        """Create all GUI widgets."""
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(padx=10, pady=10)
        
        # File operations buttons
        tk.Button(button_frame, text="New", command=self._new_file).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Open CUP", command=self._load_cup).grid(row=0, column=1, padx=5)
        
        self.save_btn = tk.Button(button_frame, text="Save", command=self._save_cup, state=tk.DISABLED)
        self.save_btn.grid(row=0, column=2, padx=5)
        
        self.save_as_btn = tk.Button(button_frame, text="Save As", command=self._save_cup_as, state=tk.DISABLED)
        self.save_as_btn.grid(row=0, column=3, padx=5)
        
        tk.Label(button_frame, text="|").grid(row=0, column=4, padx=5)
        
        # Import/Export buttons
        tk.Button(button_frame, text="Import CSV", command=self._import_csv).grid(row=0, column=5, padx=5)
        tk.Button(button_frame, text="Export CSV", command=self._export_csv).grid(row=0, column=6, padx=5)
        
        tk.Label(button_frame, text="|").grid(row=0, column=7, padx=5)
        
        # Waypoint operations buttons
        tk.Button(button_frame, text="Add Point", command=self._add_point).grid(row=0, column=8, padx=5)
        tk.Button(button_frame, text="Edit Selected", command=self._edit_point).grid(row=0, column=9, padx=5)
        tk.Button(button_frame, text="Remove Selected", command=self._remove_selected).grid(row=0, column=10, padx=5)
        
        # Tree view with extended columns
        columns = ("Name", "Code", "Country", "Latitude", "Longitude", "Elevation", "Style", "Airfield")
        self.tree = ttk.Treeview(
            self.root, 
            columns=columns, 
            show='headings'
        )
        
        # Configure headings and columns
        self.tree.heading("Name", text="Name", command=self._sort_by_name)
        self.tree.heading("Code", text="Code")
        self.tree.heading("Country", text="Country")
        self.tree.heading("Latitude", text="Latitude")
        self.tree.heading("Longitude", text="Longitude")
        self.tree.heading("Elevation", text="Elevation (m)")
        self.tree.heading("Style", text="Type")
        self.tree.heading("Airfield", text="Airfield")
        
        # Configure column widths
        self.tree.column("Name", width=180)
        self.tree.column("Code", width=60)
        self.tree.column("Country", width=60)
        self.tree.column("Latitude", width=100)
        self.tree.column("Longitude", width=100)
        self.tree.column("Elevation", width=80)
        self.tree.column("Style", width=150)
        self.tree.column("Airfield", width=80)
        
        # Scrollbar for tree
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, padx=(10, 0), pady=10, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, padx=(0, 10), pady=10, fill=tk.Y)
        
        # Double-click to edit
        self.tree.bind('<Double-Button-1>', lambda e: self._edit_point())
    
    def _update_title(self):
        """Update window title to show filename and modified status."""
        filename = os.path.basename(self.cup_file_path) if self.cup_file_path else "Untitled"
        modified_marker = "*" if self.modified else ""
        self.root.title(f"XCSoar CUP Editor - {filename}{modified_marker}")
    
    def _mark_modified(self):
        """Mark the file as modified and update UI."""
        if not self.modified:
            self.modified = True
            self._update_title()
            self.save_btn.config(state=tk.NORMAL)
            self.save_as_btn.config(state=tk.NORMAL)
    
    def _mark_saved(self):
        """Mark the file as saved and update UI."""
        self.modified = False
        self._update_title()
    
    def _refresh_tree(self):
        """Refresh the tree view with current waypoint data."""
        self.tree.delete(*self.tree.get_children())
        for waypoint in self.waypoints:
            style_label = STYLE_OPTIONS.get(waypoint.style, 'Unknown')
            
            # Format elevation
            elev_str = f"{waypoint.elevation:.1f}" if waypoint.elevation is not None else ""
            
            # Check if airfield (has runway or frequency info)
            airfield_marker = "✓" if waypoint.is_airfield else ""
            
            self.tree.insert('', tk.END, values=(
                waypoint.name,
                waypoint.code,
                waypoint.country,
                f"{waypoint.latitude:.6f}",
                f"{waypoint.longitude:.6f}",
                elev_str,
                style_label,
                airfield_marker
            ))
    
    def _on_closing(self):
        """Handle window close event - check for unsaved changes."""
        if self.modified:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before closing?"
            )
            if response is None:  # Cancel
                return
            elif response:  # Yes - save
                if not self._save_cup():
                    return  # Save failed or was cancelled
        self.root.destroy()
    
    def _new_file(self):
        """Create a new empty waypoint file."""
        if self.modified:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before creating a new file?"
            )
            if response is None:  # Cancel
                return
            elif response:  # Yes - save
                if not self._save_cup():
                    return  # Save failed or was cancelled
        
        # Clear everything and start fresh
        self.waypoints = []
        self.cup_file_path = None
        self.modified = False
        self._refresh_tree()
        self._update_title()
        self.save_btn.config(state=tk.DISABLED)
        self.save_as_btn.config(state=tk.DISABLED)
    
    def _sort_by_name(self):
        """Sort waypoints by name."""
        self.waypoints.sort(key=lambda w: w.name.lower())
        self._refresh_tree()
        self._mark_modified()
    
    def _load_cup(self):
        """Load waypoints from a CUP file."""
        filepath = filedialog.askopenfilename(
            filetypes=[("CUP Files", "*.cup"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        
        try:
            self.waypoints = parse_cup_file(filepath)
            self.cup_file_path = filepath
            self.modified = False
            self._refresh_tree()
            self._update_title()
            messagebox.showinfo(
                "Loaded", 
                f"Loaded {len(self.waypoints)} waypoints from {os.path.basename(filepath)}"
            )
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load file:\n{str(e)}")
    
    def _import_csv(self):
        """Import waypoints from CSV file."""
        filepath = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        
        try:
            imported = parse_csv_file(filepath)
            self.waypoints.extend(imported)
            self._refresh_tree()
            self._mark_modified()
            messagebox.showinfo(
                "Imported", 
                f"Imported {len(imported)} waypoints from CSV"
            )
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import CSV:\n{str(e)}")
    
    def _export_csv(self):
        """Export current waypoints to CSV file."""
        if not self.waypoints:
            messagebox.showwarning("No Data", "No waypoints to export")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        
        try:
            write_csv_file(filepath, self.waypoints)
            messagebox.showinfo(
                "Exported", 
                f"Exported {len(self.waypoints)} waypoints to {os.path.basename(filepath)}"
            )
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export CSV:\n{str(e)}")
    
    def _add_point(self):
        """Show dialog to add a new waypoint."""
        def on_save(waypoint: Waypoint):
            self.waypoints.append(waypoint)
            self._refresh_tree()
            self._mark_modified()
        
        dialog = WaypointDialog(self.root, on_save=on_save)
        dialog.show()
    
    def _edit_point(self):
        """Edit the selected waypoint."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a waypoint to edit")
            return
        
        item = selected[0]
        # Get the index of the selected item in the tree
        tree_children = self.tree.get_children()
        tree_index = tree_children.index(item)
        
        # Use the tree index to get the corresponding waypoint
        if 0 <= tree_index < len(self.waypoints):
            def on_save(waypoint: Waypoint):
                self.waypoints[tree_index] = waypoint
                self._refresh_tree()
                self._mark_modified()
            
            dialog = WaypointDialog(self.root, waypoint=self.waypoints[tree_index], on_save=on_save)
            dialog.show()
    
    def _remove_selected(self):
        """Remove selected waypoints."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select waypoint(s) to remove")
            return
        
        if len(selected) > 1:
            response = messagebox.askyesno("Confirm Delete", f"Delete {len(selected)} waypoints?")
        else:
            response = messagebox.askyesno("Confirm Delete", "Delete selected waypoint?")
        
        if not response:
            return
        
        # Get indices of selected items in tree
        tree_children = self.tree.get_children()
        indices_to_remove = []
        for item in selected:
            tree_index = tree_children.index(item)
            indices_to_remove.append(tree_index)
        
        # Sort indices in reverse order to remove from end first
        indices_to_remove.sort(reverse=True)
        
        # Remove waypoints by index
        for index in indices_to_remove:
            if 0 <= index < len(self.waypoints):
                del self.waypoints[index]
        
        self._refresh_tree()
        self._mark_modified()
    
    def _save_cup(self) -> bool:
        """
        Save waypoints to current CUP file.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.cup_file_path:
            return self._save_cup_as()
        
        return self._write_cup_file(self.cup_file_path)
    
    def _save_cup_as(self) -> bool:
        """
        Save waypoints to a new CUP file.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.waypoints:
            messagebox.showwarning("No Data", "No waypoints to save")
            return False
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".cup",
            filetypes=[("CUP Files", "*.cup"), ("All Files", "*.*")]
        )
        
        if not filepath:
            return False
        
        if self._write_cup_file(filepath):
            self.cup_file_path = filepath
            self._update_title()
            return True
        return False
    
    def _write_cup_file(self, filepath: str) -> bool:
        """
        Write waypoints to CUP file format.
        
        Args:
            filepath: Path to save the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            write_cup_file(filepath, self.waypoints, fetch_elevation=True)
            self._mark_saved()
            messagebox.showinfo(
                "Saved", 
                f"Saved {len(self.waypoints)} waypoints to {os.path.basename(filepath)}"
            )
            return True
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file:\n{str(e)}")
            return False
