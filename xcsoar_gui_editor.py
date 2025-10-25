import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import requests
import os

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

def deg_to_ddmm(value, is_lat):
    degrees = int(abs(value))
    minutes = (abs(value) - degrees) * 60
    suffix = "N" if is_lat and value >= 0 else "S" if is_lat else "E" if value >= 0 else "W"
    deg_format = "{:02d}" if is_lat else "{:03d}"
    return f"{deg_format.format(degrees)}{minutes:06.3f}{suffix}"

def get_elevation(lat, lon):
    try:
        url = "https://api.open-elevation.com/api/v1/lookup"
        resp = requests.get(url, params={"locations": f"{lat},{lon}"}, timeout=5)
        return resp.json()['results'][0]['elevation']
    except Exception as e:
        print(f"Elevation fetch error for {lat}, {lon}: {e}")
        return 0.0

class XCSoarGUI:
    def sort_by_name(self):
        self.points.sort(key=lambda x: x['name'].lower())
        self.refresh_tree()

    def __init__(self, root):
        self.root = root
        self.root.title("XCSoar CUP Editor")
        self.points = []
        self.csv_file_path = None

        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10)

        self.load_btn = tk.Button(frame, text="Load CSV", command=self.load_csv)
        self.load_btn.grid(row=0, column=0, padx=5)

        self.add_btn = tk.Button(frame, text="Add Point", command=self.add_point)
        self.add_btn.grid(row=0, column=1, padx=5)

        self.edit_btn = tk.Button(frame, text="Edit Selected", command=self.edit_point)
        self.edit_btn.grid(row=0, column=2, padx=5)

        self.remove_btn = tk.Button(frame, text="Remove Selected", command=self.remove_selected)
        self.remove_btn.grid(row=0, column=3, padx=5)

        self.export_btn = tk.Button(frame, text="Generate .cup", command=self.generate_cup)
        self.export_btn.grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(root, columns=("Name", "Latitude", "Longitude", "Style Code", "Style"), show='headings')
        self.tree.heading("Name", text="Name", command=lambda: self.sort_by_name())
        self.tree.heading("Latitude", text="Latitude")
        self.tree.heading("Longitude", text="Longitude")
        self.tree.heading("Style Code", text="Style Code")
        self.tree.heading("Style", text="Style")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def load_csv(self):
        self.csv_file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not self.csv_file_path:
            return
        with open(self.csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            self.points = list(reader)
        for p in self.points:
            try:
                p['style'] = int(p.get('style', 1))
            except:
                p['style'] = 1
        self.refresh_tree()
        messagebox.showinfo("Loaded", f"Loaded {len(self.points)} points.")

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.points:
            style_code = int(row.get('style', 1))
            style_label = STYLE_OPTIONS.get(style_code, 'Unknown')
            self.tree.insert('', tk.END, values=(row['name'], row['latitude'], row['longitude'], style_code, style_label))
        self.save_to_csv()

    def save_to_csv(self):
        if self.csv_file_path:
            try:
                with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['name', 'latitude', 'longitude', 'style']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for point in self.points:
                        writer.writerow(point)
            except Exception as e:
                print(f"CSV save error: {e}")

    def add_point(self, prefill=None, index=None):
        def save_point():
            name = name_entry.get()
            coord_text = coord_entry.get()
            style_label = style_var.get()
            try:
                lat_str, lon_str = coord_text.split(',')
                lat = float(lat_str.strip())
                lon = float(lon_str.strip())
                style_code = STYLE_LABELS.get(style_label, 1)
                point = {"name": name, "latitude": lat, "longitude": lon, "style": style_code}
                if index is not None:
                    self.points[index] = point
                else:
                    self.points.append(point)
                self.refresh_tree()
                add_win.destroy()
            except Exception:
                messagebox.showerror("Invalid input", "Coordinates must be in format: lat, lon")

        add_win = tk.Toplevel(self.root)
        add_win.title("Add/Edit Point")

        tk.Label(add_win, text="Name").grid(row=0, column=0)
        name_entry = tk.Entry(add_win)
        name_entry.grid(row=0, column=1)

        tk.Label(add_win, text="Coordinates (lat, lon)").grid(row=1, column=0)
        coord_entry = tk.Entry(add_win, width=40)
        coord_entry.grid(row=1, column=1)

        tk.Label(add_win, text="Style").grid(row=2, column=0)
        style_var = tk.StringVar()
        style_menu = ttk.Combobox(add_win, textvariable=style_var, values=list(STYLE_OPTIONS.values()), state="readonly")
        style_menu.grid(row=2, column=1)

        if prefill:
            name_entry.insert(0, prefill['name'])
            coord_entry.insert(0, f"{prefill['latitude']}, {prefill['longitude']}")
            style_menu.set(STYLE_OPTIONS.get(int(prefill.get('style', 1)), "Waypoint"))
        else:
            style_menu.set("Waypoint")

        save_btn = tk.Button(add_win, text="Save", command=save_point)
        save_btn.grid(row=3, column=0, columnspan=2, pady=5)

    def edit_point(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        values = self.tree.item(item, 'values')
        for i, p in enumerate(self.points):
            if (p['name'] == values[0] and str(p['latitude']) == values[1] and str(p['longitude']) == values[2]):
                self.add_point(prefill=p, index=i)
                break

    def remove_selected(self):
        selected = self.tree.selection()
        for item in selected:
            values = self.tree.item(item, 'values')
            self.points = [p for p in self.points if not (p['name'] == values[0] and str(p['latitude']) == values[1] and str(p['longitude']) == values[2])]
        self.refresh_tree()
        self.save_to_csv()

    def generate_cup(self):
        if not self.points:
            messagebox.showerror("Error", "No points loaded.")
            return

        rows = ["name,code,country,lat,lon,elev,style,rwdir,rwlen,rwwidth,freq,desc"]

      #rows = ["name,code,country,lat,lon,elev,style,rwdir,rwlen,rwwidth,freq,desc",
      #  "\"BIAŁYSTOK KRYWLANY\",\"EPBK\",,5306.058N,02310.317E,149M,4,267,1350M,\"123.205\",\"HOME\""]

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

        save_path = filedialog.asksaveasfilename(filetypes=[("CUP Files", "*.cup")])
        if save_path:
            try:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(rows))
                messagebox.showinfo("Done", f"Saved to {os.path.basename(save_path)}")
            except Exception as e:
                print(f"File save error: {e}")
                messagebox.showerror("Save Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x1000")
    app = XCSoarGUI(root)
    root.mainloop()
