**BMI Calculator**

- **Description:** Lightweight command-line BMI (Body Mass Index) calculator written in Python. The program prompts for weight (kg) and height (m), computes BMI rounded to two decimals, and shows the standard BMI category.

**Features**

- **Simple CLI:** Run directly with Python — no GUI required.
- **Clear validation:** Rejects non-positive values for weight/height.
- **Categorization:** Uses standard BMI ranges (Underweight, Normal Weight, Overweight, Obese).

**Requirements**

- **Python:** 3.8 or newer (3.x series). No external packages required.

**Quick Start**

- Clone or download this repository and open a terminal in the project folder.

**Run (PowerShell)**

```powershell
python .\bmi.py
```

**Example session**

- Program prints: `--- Welcome to the BMI Calculator ---`
- Input prompts:
  - `Enter weight (kg): 70`
  - `Enter height (meters): 1.75`
- Output (example):

```
------------------------------
📊 Your BMI is: 22.86
🩺 Category: Normal Weight
------------------------------
```

**What the code contains**

- **`bmi.py`**: single-file CLI program with:
  - `BMICalculator` class — `calculate_bmi(weight_kg, height_m)` and `get_category(bmi_value)`.
  - `get_valid_number(prompt)` — helper that loops until the user enters a valid numeric value.
  - `main()` — interactive loop that gathers input, shows results, and optionally repeats.

**Design notes & edge cases**

- The calculator expects **weight in kilograms** and **height in meters**.
- The program raises an error for zero or negative height/weight and prompts again.
- BMI is rounded to two decimal places. Category boundaries are inclusive (e.g., 18.5 → Normal Weight).

**Contributing**

- Feel free to open issues or pull requests to add features (tests, CLI args, GUI, persistence).

**License**

- This repository does not include a license file.

A modern, desktop-based Body Mass Index (BMI) calculator and health tracker built with Python.

✨ Features

Advanced GUI: Built with CustomTkinter for a sleek, dark-mode interface.

Data Persistence: Uses SQLite to save user history locally.

Smart Visualizations: Interactive Matplotlib graphs with color-coded health zones (Underweight, Normal, Obese).

Statistical Analysis: Automatically calculates Average, Max, and Min BMI.

Multi-User Support: Track history for different users independently.

🚀 Installation

Clone the repository

git clone [https://github.com/YOUR_USERNAME/BMI-Tracker.git](https://github.com/YOUR_USERNAME/BMI-Tracker.git)
cd BMI-Tracker

Install dependencies

pip install -r requirements.txt

Run the App

python bmi.py

🛠 Tech Stack

Python 3.10+

CustomTkinter (UI Framework)

Matplotlib (Data Visualization)

SQLite3 (Database)
