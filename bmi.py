import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# --- Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- Backend: Database Manager ---
class DatabaseManager:
    def __init__(self, db_name="bmi_history_v2.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                weight REAL,
                height REAL,
                bmi REAL,
                category TEXT,
                date TEXT
            )
        ''')
        self.conn.commit()

    def add_record(self, name, weight, height, bmi, category):
        date_str = datetime.now().isoformat()
        self.cursor.execute('''
            INSERT INTO bmi_records (user_name, weight, height, bmi, category, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, weight, height, bmi, category, date_str))
        self.conn.commit()

    def get_user_history(self, name):
        self.cursor.execute('''
            SELECT date, bmi FROM bmi_records 
            WHERE user_name = ? 
            ORDER BY date ASC
        ''', (name,))
        return self.cursor.fetchall()

    def delete_user_history(self, name):
        self.cursor.execute('DELETE FROM bmi_records WHERE user_name = ?', (name,))
        self.conn.commit()
        return self.cursor.rowcount

# --- Logic: Math & Validation ---
class BMICalculator:
    def calculate(self, weight, height):
        if weight <= 0 or height <= 0:
            raise ValueError("Height and Weight must be positive.")
        if height > 3.0: 
            raise ValueError("Height seems too high (are you using meters?)")
        if weight > 500:
            raise ValueError("Weight seems too high (are you using kg?)")
        return round(weight / (height ** 2), 2)

    def get_category(self, bmi):
        if bmi < 18.5: return "Underweight"
        elif bmi < 25: return "Normal Weight"
        elif bmi < 30: return "Overweight"
        else: return "Obese"

# --- Frontend: The Final GUI ---
class BMIApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BMI Tracker Ultimate")
        self.geometry("420x600")
        self.resizable(False, False)
        
        self.db = DatabaseManager()
        self.logic = BMICalculator()
        self.entries = {} 

        # Grid Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)

        # 1. Title Section
        self.title_label = ctk.CTkLabel(self, text="BMI Tracker Ultimate", 
                                      font=ctk.CTkFont(size=26, weight="bold"),
                                      text_color="#3B8ED0")
        self.title_label.grid(row=0, column=0, padx=20, pady=(25, 15))

        # 2. Input Section
        self.input_frame = ctk.CTkFrame(self, corner_radius=15)
        self.input_frame.grid(row=1, column=0, padx=25, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)

        self.create_input_field("User Name:", 0, "Enter unique name")
        self.create_input_field("Weight (kg):", 1, "e.g. 70.5")
        self.create_input_field("Height (m):", 2, "e.g. 1.75")

        # 3. Action Buttons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, padx=25, pady=15, sticky="ew")
        self.btn_frame.grid_columnconfigure((0, 1), weight=1)

        self.calc_btn = ctk.CTkButton(self.btn_frame, text="Calculate & Save", 
                                    command=self.calculate_bmi, 
                                    height=45, font=ctk.CTkFont(weight="bold"))
        self.calc_btn.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        self.graph_btn = ctk.CTkButton(self.btn_frame, text="📈 Stats & Trends", 
                                     command=self.show_graph, 
                                     fg_color="#2B2B2B", border_width=2, border_color="#3B8ED0")
        self.graph_btn.grid(row=1, column=0, padx=(0, 5), sticky="ew")

        self.clear_btn = ctk.CTkButton(self.btn_frame, text="🗑 Reset History", 
                                     command=self.confirm_delete,
                                     fg_color="#2B2B2B", border_width=2, border_color="#C53030", hover_color="#C53030")
        self.clear_btn.grid(row=1, column=1, padx=(5, 0), sticky="ew")

        # 4. Result Display
        self.result_frame = ctk.CTkFrame(self, corner_radius=15, fg_color=("#EBEBEB", "#242424"))
        self.result_frame.grid(row=3, column=0, padx=25, pady=10, sticky="ew")
        
        self.result_label = ctk.CTkLabel(self.result_frame, text="Ready to calculate...", 
                                         font=ctk.CTkFont(size=16), text_color="gray")
        self.result_label.pack(pady=25, padx=15)

    def create_input_field(self, label_text, row, placeholder):
        label = ctk.CTkLabel(self.input_frame, text=label_text, anchor="w", font=ctk.CTkFont(weight="bold"))
        label.grid(row=row, column=0, padx=20, pady=(15, 5), sticky="w")
        
        entry = ctk.CTkEntry(self.input_frame, placeholder_text=placeholder, height=35)
        entry.grid(row=row, column=1, padx=20, pady=(15, 5), sticky="ew")
        
        key = label_text.split(":")[0].strip()
        self.entries[key] = entry

    def calculate_bmi(self):
        try:
            if "User Name" not in self.entries or "Weight (kg)" not in self.entries:
                raise Exception("Input fields missing.")

            name = self.entries["User Name"].get().strip()
            w_str = self.entries["Weight (kg)"].get().strip()
            h_str = self.entries["Height (m)"].get().strip()

            if not name or not w_str or not h_str:
                messagebox.showwarning("Missing Info", "Please fill in all fields.")
                return

            weight = float(w_str)
            height = float(h_str)
            
            bmi = self.logic.calculate(weight, height)
            category = self.logic.get_category(bmi)
            
            self.db.add_record(name, weight, height, bmi, category)
            
            color_map = {"Underweight": "#FFD700", "Normal Weight": "#2CC985", "Overweight": "#FFA500", "Obese": "#FF5555"}
            self.result_label.configure(text=f"{category}\nBMI: {bmi}", 
                                      text_color=color_map.get(category, "white"),
                                      font=ctk.CTkFont(size=22, weight="bold"))
            
            self.entries["Weight (kg)"].delete(0, 'end')
            self.entries["Height (m)"].delete(0, 'end')

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid number format.\n{str(e)}")
        except Exception as e:
            messagebox.showerror("System Error", f"Error: {str(e)}")

    def show_graph(self):
        try:
            name = self.entries["User Name"].get().strip()
            if not name:
                messagebox.showwarning("Input Needed", "Please enter a User Name.")
                return

            history = self.db.get_user_history(name)
            if len(history) < 2:
                messagebox.showinfo("Data Needed", "Add at least 2 records to see trends & stats.")
                return

            dates = [datetime.fromisoformat(row[0]) for row in history]
            bmis = [row[1] for row in history]

            # --- NEW: Statistics Calculation ---
            avg_bmi = sum(bmis) / len(bmis)
            max_bmi = max(bmis)
            min_bmi = min(bmis)
            
            # REMOVED emoji to fix font warning
            stats_text = (f"STATISTICS\n"
                          f"Average: {avg_bmi:.1f}\n"
                          f"Highest: {max_bmi}\n"
                          f"Lowest:  {min_bmi}")

            # Plotting
            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(9, 6))
            
            ax.plot(dates, bmis, marker='o', linestyle='-', color='#3B8ED0', linewidth=2.5, markersize=8, zorder=5)
            
            # --- NEW: Add Stats Box to Graph ---
            # boxstyle='round' creates rounded corners
            props = dict(boxstyle='round,pad=0.5', facecolor='#2B2B2B', alpha=0.9, edgecolor='#3B8ED0')
            
            # Place text in top-left (0.03, 0.95) relative to axes
            ax.text(0.03, 0.95, stats_text, transform=ax.transAxes, fontsize=11,
                    verticalalignment='top', bbox=props, color='white', fontfamily='monospace')

            # Time vs Date handling
            time_diff = dates[-1] - dates[0]
            if time_diff < timedelta(days=1) and dates[0].date() == dates[-1].date():
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                ax.set_xlabel("Time (Today)", color="gray")
            else:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
                ax.set_xlabel("Date", color="gray")

            fig.autofmt_xdate() 
            ax.set_title(f"Health Trend for {name}", fontsize=14, color="white", pad=15)
            ax.set_ylabel("BMI Value")
            ax.grid(True, color="#404040", linestyle='--', alpha=0.5)

            # Zones
            ax.axhspan(0, 18.5, color='#3498db', alpha=0.2, label='Underweight')
            ax.axhspan(18.5, 25, color='#2ecc71', alpha=0.2, label='Normal')
            ax.axhspan(25, 30, color='#f1c40f', alpha=0.2, label='Overweight')
            ax.axhspan(30, 100, color='#e74c3c', alpha=0.2, label='Obese')

            # Adjust Y limit to make sure zones are visible
            ax.set_ylim(min(15, min(bmis) - 2), max(35, max(bmis) + 2))
            ax.legend(loc='lower right', fontsize='small', frameon=True, facecolor='#2B2B2B')
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            messagebox.showerror("Graph Error", f"Could not load graph:\n{str(e)}")

    def confirm_delete(self):
        name = self.entries["User Name"].get().strip()
        if not name:
            return
        
        confirm = messagebox.askyesno("Confirm Reset", f"Delete all history for user '{name}'?")
        if confirm:
            count = self.db.delete_user_history(name)
            self.result_label.configure(text=f"🗑 Deleted {count} records.", text_color="gray")

if __name__ == "__main__":
    app = BMIApp()
    app.mainloop()