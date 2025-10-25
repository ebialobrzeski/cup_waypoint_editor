import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import requests
import os
import re
from typing import Dict, List, Optional

# XCSoar style options
STYLE_OPTIONS = {
    0: "Unknown",
    1: "Waypoint",
    2: "Airfield (grass)",
    3: "Outlanding",
    4: "Gliding airfield",
    5: "Airfield (solid)",
    6: "Mountain Pass",
    7: "Mountain Top",
    8: "Transmitter Mast",
    9: "VOR",
    10: "NDB",
    11: "Cooling Tower",
    12: "Dam",
    13: "Tunnel",
    14: "Bridge",
    15: "Power Plant",
    16: "Castle",
    17: "Intersection",
    18: "Marker",
    19: "Reporting Point",
    20: "PG Take Off",
    21: "PG Landing"
}

STYLE_LABELS = {v: k for k, v in STYLE_OPTIONS.items()}


def ddmm_to_deg(coord_str: str) -> float:
    """Convert DDMM.MMM format to decimal degrees."""
    coord_str = coord_str.strip()
    direction = coord_str[-1]
    coord_str = coord_str[:-1]
    
    # Find where minutes start (after 2 or 3 digits for lat/lon)
    if direction in ['N', 'S']:
        degrees = int(coord_str[:2])
        minutes = float(coord_str[2:])
    else:  # E, W
        degrees = int(coord_str[:3])
        minutes = float(coord_str[3:])
    
    decimal = degrees + (minutes / 60.0)
    
    if direction in ['S', 'W']:
        decimal = -decimal
    
    return decimal

def deg_to_ddmm(value, is_lat):
    degrees = int(abs(value))
    minutes = (abs(value) - degrees) * 60
    suffix = "N" if is_lat and value >= 0 else "S" if is_lat else "E" if value >= 0 else "W"
    deg_format = "{:02d}" if is_lat else "{:03d}"
    return f"{deg_format.format(degrees)}{minutes:06.3f}{suffix}"

def parse_cup_file(filepath: str) -> List[Dict]:
    """Parse a CUP file and return list of waypoint dictionaries."""
    points = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Skip header line
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        
        # Parse CSV line respecting quoted fields
        parts = []
        current = []
        in_quotes = False
        
        for char in line:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                parts.append(''.join(current).strip().strip('"'))
                current = []
            else:
                current.append(char)
        parts.append(''.join(current).strip().strip('"'))
        
        # Ensure we have enough fields
        while len(parts) < 12:
            parts.append('')
        
        name, code, country, lat_str, lon_str, elev_str, style_str, rwdir, rwlen, rwwidth, freq, desc = parts[:12]
        
        try:
            lat = ddmm_to_deg(lat_str)
            lon = ddmm_to_deg(lon_str)
            style = int(style_str) if style_str else 1
            
            point = {
                'name': name,
                'latitude': lat,
                'longitude': lon,
                'style': style
            }
            points.append(point)
        except Exception as e:
            print(f"Error parsing line: {line}\nError: {e}")
            continue
    
    return points

def get_elevation(lat, lon):
    try:
        url = "https://api.open-elevation.com/api/v1/lookup"
        resp = requests.get(url, params={"locations": f"{lat},{lon}"}, timeout=5)
        return resp.json()['results'][0]['elevation']
    except Exception as e:
        print(f"Elevation fetch error for {lat}, {lon}: {e}")
        return 0.0

class XCSoarGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("XCSoar CUP Editor")
        self.points = []
        self.cup_file_path = None
        self.modified = False
        
        # Register close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Button frame
        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10)

        self.new_btn = tk.Button(frame, text="New", command=self.new_file)
        self.new_btn.grid(row=0, column=0, padx=5)

        self.load_btn = tk.Button(frame, text="Open CUP", command=self.load_cup)
        self.load_btn.grid(row=0, column=1, padx=5)

        self.save_btn = tk.Button(frame, text="Save", command=self.save_cup, state=tk.DISABLED)
        self.save_btn.grid(row=0, column=2, padx=5)

        self.save_as_btn = tk.Button(frame, text="Save As", command=self.save_cup_as, state=tk.DISABLED)
        self.save_as_btn.grid(row=0, column=3, padx=5)

        tk.Label(frame, text="|").grid(row=0, column=4, padx=5)

        self.import_csv_btn = tk.Button(frame, text="Import CSV", command=self.import_csv)
        self.import_csv_btn.grid(row=0, column=5, padx=5)

        self.export_csv_btn = tk.Button(frame, text="Export CSV", command=self.export_csv)
        self.export_csv_btn.grid(row=0, column=6, padx=5)

        tk.Label(frame, text="|").grid(row=0, column=7, padx=5)

        self.add_btn = tk.Button(frame, text="Add Point", command=self.add_point)
        self.add_btn.grid(row=0, column=8, padx=5)

        self.edit_btn = tk.Button(frame, text="Edit Selected", command=self.edit_point)
        self.edit_btn.grid(row=0, column=9, padx=5)

        self.remove_btn = tk.Button(frame, text="Remove Selected", command=self.remove_selected)
        self.remove_btn.grid(row=0, column=10, padx=5)

        # Tree view
        self.tree = ttk.Treeview(root, columns=("Name", "Latitude", "Longitude", "Style Code", "Style"), show='headings')
        self.tree.heading("Name", text="Name", command=lambda: self.sort_by_name())
        self.tree.heading("Latitude", text="Latitude")
        self.tree.heading("Longitude", text="Longitude")
        self.tree.heading("Style Code", text="Style Code")
        self.tree.heading("Style", text="Style")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.update_title()

    def update_title(self):
        """Update window title to show filename and modified status."""
        filename = os.path.basename(self.cup_file_path) if self.cup_file_path else "Untitled"
        modified_marker = "*" if self.modified else ""
        self.root.title(f"XCSoar CUP Editor - {filename}{modified_marker}")

    def mark_modified(self):
        """Mark the file as modified and update UI."""
        if not self.modified:
            self.modified = True
            self.update_title()
            self.save_btn.config(state=tk.NORMAL)
            self.save_as_btn.config(state=tk.NORMAL)

    def mark_saved(self):
        """Mark the file as saved and update UI."""
        self.modified = False
        self.update_title()

    def on_closing(self):
        """Handle window close event - check for unsaved changes."""
        if self.modified:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before closing?"
            )
            if response is None:  # Cancel
                return
            elif response:  # Yes - save
                if not self.save_cup():
                    return  # Save failed or was cancelled
        self.root.destroy()

    def new_file(self):
        """Create a new empty waypoint file."""
        if self.modified:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before creating a new file?"
            )
            if response is None:  # Cancel
                return
            elif response:  # Yes - save
                if not self.save_cup():
                    return  # Save failed or was cancelled
        
        # Clear everything and start fresh
        self.points = []
        self.cup_file_path = None
        self.modified = False
        self.refresh_tree()
        self.update_title()
        self.save_btn.config(state=tk.DISABLED)
        self.save_as_btn.config(state=tk.DISABLED)

    def sort_by_name(self):
        self.points.sort(key=lambda x: x['name'].lower())
        self.refresh_tree()
        self.mark_modified()


    def load_cup(self):
        """Load waypoints from a CUP file."""
        filepath = filedialog.askopenfilename(filetypes=[("CUP Files", "*.cup"), ("All Files", "*.*")])
        if not filepath:
            return
        
        try:
            self.points = parse_cup_file(filepath)
            self.cup_file_path = filepath
            self.modified = False
            self.refresh_tree()
            self.update_title()
            messagebox.showinfo("Loaded", f"Loaded {len(self.points)} waypoints from {os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load file:\n{str(e)}")

    def import_csv(self):
        """Import waypoints from CSV file."""
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if not filepath:
            return
        
        try:
            with open(filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                imported_points = list(reader)
            
            for p in imported_points:
                try:
                    p['latitude'] = float(p['latitude'])
                    p['longitude'] = float(p['longitude'])
                    p['style'] = int(p.get('style', 1))
                except (ValueError, KeyError) as e:
                    print(f"Skipping invalid point: {p}, Error: {e}")
                    continue
            
            self.points.extend(imported_points)
            self.refresh_tree()
            self.mark_modified()
            messagebox.showinfo("Imported", f"Imported {len(imported_points)} waypoints from CSV")
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import CSV:\n{str(e)}")

    def export_csv(self):
        """Export current waypoints to CSV file."""
        if not self.points:
            messagebox.showwarning("No Data", "No waypoints to export")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['name', 'latitude', 'longitude', 'style']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for point in self.points:
                    writer.writerow({
                        'name': point['name'],
                        'latitude': point['latitude'],
                        'longitude': point['longitude'],
                        'style': point['style']
                    })
            messagebox.showinfo("Exported", f"Exported {len(self.points)} waypoints to {os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export CSV:\n{str(e)}")

    def refresh_tree(self):
        """Refresh the tree view with current waypoint data."""
        self.tree.delete(*self.tree.get_children())
        for row in self.points:
            style_code = int(row.get('style', 1))
            style_label = STYLE_OPTIONS.get(style_code, 'Unknown')
            self.tree.insert('', tk.END, values=(
                row['name'], 
                f"{row['latitude']:.6f}", 
                f"{row['longitude']:.6f}", 
                style_code, 
                style_label
            ))


    def add_point(self, prefill=None, index=None):
        """Add or edit a waypoint."""
        def save_point():
            name = name_entry.get().strip()
            lat_text = lat_entry.get().strip()
            lon_text = lon_entry.get().strip()
            style_label = style_var.get()
            
            if not name:
                messagebox.showerror("Invalid Input", "Name cannot be empty")
                return
            
            if not lat_text or not lon_text:
                messagebox.showerror("Invalid Input", "Latitude and Longitude cannot be empty")
                return
            
            try:
                lat = float(lat_text)
                lon = float(lon_text)
                
                # Validate coordinate ranges
                if not (-90 <= lat <= 90):
                    messagebox.showerror("Invalid Input", "Latitude must be between -90 and 90")
                    return
                if not (-180 <= lon <= 180):
                    messagebox.showerror("Invalid Input", "Longitude must be between -180 and 180")
                    return
                
                style_code = STYLE_LABELS.get(style_label, 1)
                point = {"name": name, "latitude": lat, "longitude": lon, "style": style_code}
                
                if index is not None:
                    self.points[index] = point
                else:
                    self.points.append(point)
                
                self.refresh_tree()
                self.mark_modified()
                add_win.destroy()
            except ValueError:
                messagebox.showerror("Invalid input", "Latitude and Longitude must be valid numbers (e.g., 52.7652, 23.1867)")

        add_win = tk.Toplevel(self.root)
        add_win.title("Add Point" if index is None else "Edit Point")
        add_win.geometry("400x180")

        tk.Label(add_win, text="Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        name_entry = tk.Entry(add_win, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_win, text="Latitude:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        lat_entry = tk.Entry(add_win, width=30)
        lat_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_win, text="Longitude:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        lon_entry = tk.Entry(add_win, width=30)
        lon_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_win, text="Style:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        style_var = tk.StringVar()
        style_menu = ttk.Combobox(add_win, textvariable=style_var, values=list(STYLE_OPTIONS.values()), state="readonly", width=27)
        style_menu.grid(row=3, column=1, padx=5, pady=5)

        if prefill:
            name_entry.insert(0, prefill['name'])
            lat_entry.insert(0, str(prefill['latitude']))
            lon_entry.insert(0, str(prefill['longitude']))
            style_menu.set(STYLE_OPTIONS.get(int(prefill.get('style', 1)), "Waypoint"))
        else:
            style_menu.set("Waypoint")

        button_frame = tk.Frame(add_win)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        save_btn = tk.Button(button_frame, text="Save", command=save_point, width=10)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", command=add_win.destroy, width=10)
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to save
        add_win.bind('<Return>', lambda e: save_point())
        add_win.bind('<Escape>', lambda e: add_win.destroy())

    def edit_point(self):
        """Edit the selected waypoint."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a waypoint to edit")
            return
        
        item = selected[0]
        values = self.tree.item(item, 'values')
        name = values[0]
        
        # Find the point by index in tree
        for i, p in enumerate(self.points):
            if p['name'] == name:
                self.add_point(prefill=p, index=i)
                break

    def remove_selected(self):
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
        
        # Collect names to remove
        names_to_remove = []
        for item in selected:
            values = self.tree.item(item, 'values')
            names_to_remove.append(values[0])
        
        # Remove from points list
        self.points = [p for p in self.points if p['name'] not in names_to_remove]
        self.refresh_tree()
        self.mark_modified()


    def save_cup(self) -> bool:
        """Save waypoints to current CUP file. Returns True if successful."""
        if not self.cup_file_path:
            return self.save_cup_as()
        
        return self._write_cup_file(self.cup_file_path)

    def save_cup_as(self) -> bool:
        """Save waypoints to a new CUP file. Returns True if successful."""
        if not self.points:
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
            self.update_title()
            return True
        return False

    def _write_cup_file(self, filepath: str) -> bool:
        """Write waypoints to CUP file format."""
        try:
            rows = ["name,code,country,lat,lon,elev,style,rwdir,rwlen,rwwidth,freq,desc"]

            for p in self.points:
                try:
                    name = p['name']
                    lat = float(p['latitude'])
                    lon = float(p['longitude'])
                    style = int(p.get('style', 1))
                    desc = f"{STYLE_OPTIONS.get(style, 'Point')}: {name}"
                    elev = get_elevation(lat, lon)
                    lat_str = deg_to_ddmm(lat, True)
                    lon_str = deg_to_ddmm(lon, False)
                    row = f'"{name}",,PL,{lat_str},{lon_str},{elev:.1f}m,{style},,,,"{desc}"'
                    rows.append(row)
                except Exception as e:
                    print(f"Error generating row for {p}: {e}")
                    continue

            with open(filepath, "w", encoding="utf-8") as f:
                f.write("\n".join(rows))
            
            self.mark_saved()
            messagebox.showinfo("Saved", f"Saved {len(self.points)} waypoints to {os.path.basename(filepath)}")
            return True
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file:\n{str(e)}")
            return False

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x1000")
    app = XCSoarGUI(root)
    root.mainloop()
