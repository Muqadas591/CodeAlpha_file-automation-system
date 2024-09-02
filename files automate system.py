import os
import shutil
import time
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import requests
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext

# Define color codes for output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# File Organization
def organize_files_by_extension(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_ext = filename.split('.')[-1]
            target_dir = os.path.join(directory, file_ext)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            shutil.move(file_path, os.path.join(target_dir, filename))

# Data Cleaning
def clean_csv(input_file, output_file):
    df = pd.read_csv(input_file)
    df_cleaned = df.dropna()
    df_cleaned.to_csv(output_file, index=False)

# System Maintenance
def delete_temp_files(directory, age_in_days):
    current_time = time.time()
    age_in_seconds = age_in_days * 24 * 60 * 60
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > age_in_seconds:
                os.remove(file_path)

# Automated Email Sending
def send_email(subject, body, to_email):
    from_email = 'your-email@example.com'
    password = 'your-password'
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

# Web Scraping
def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = ''
    for item in soup.find_all('h2'):
        result += item.get_text() + '\n'
    return result

# Backup Automation
def backup_files(source_dir, backup_dir):
    date_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_subdir = os.path.join(backup_dir, f'backup_{date_str}')
    os.makedirs(backup_subdir)
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path):
            shutil.copy(file_path, backup_subdir)

# GUI
def run_task():
    task = task_var.get()

    if task == 'Organize Files':
        directory = filedialog.askdirectory(title="Select Directory to Organize")
        if directory:
            organize_files_by_extension(directory)
            messagebox.showinfo("Success", "Files organized successfully!")

    elif task == 'Clean CSV':
        input_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Select CSV File to Clean")
        output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save Cleaned CSV File")
        if input_file and output_file:
            clean_csv(input_file, output_file)
            messagebox.showinfo("Success", "CSV cleaned and saved successfully!")

    elif task == 'Delete Temp Files':
        directory = filedialog.askdirectory(title="Select Directory to Clean")
        age_in_days = int(age_entry.get())
        if directory:
            delete_temp_files(directory, age_in_days)
            messagebox.showinfo("Success", "Temporary files deleted successfully!")

    elif task == 'Send Email':
        subject = subject_entry.get()
        body = body_text.get("1.0", tk.END)
        to_email = email_entry.get()
        if subject and body and to_email:
            send_email(subject, body, to_email)
            messagebox.showinfo("Success", "Email sent successfully!")

    elif task == 'Scrape Website':
        url = url_entry.get()
        if url:
            result = scrape_website(url)
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, result)

    elif task == 'Backup Files':
        source_dir = filedialog.askdirectory(title="Select Source Directory")
        backup_dir = filedialog.askdirectory(title="Select Backup Directory")
        if source_dir and backup_dir:
            backup_files(source_dir, backup_dir)
            messagebox.showinfo("Success", "Files backed up successfully!")

# Create GUI window
window = tk.Tk()
window.title("Task Automation")

# Create and place widgets
task_var = tk.StringVar()
tk.Label(window, text="Select Task:").pack(pady=10)
task_menu = tk.OptionMenu(window, task_var, 'Organize Files', 'Clean CSV', 'Delete Temp Files', 'Send Email', 'Scrape Website', 'Backup Files')
task_menu.pack(pady=10)

# Widgets for email task
tk.Label(window, text="Subject:").pack(pady=5)
subject_entry = tk.Entry(window, width=50)
subject_entry.pack(pady=5)

tk.Label(window, text="To Email:").pack(pady=5)
email_entry = tk.Entry(window, width=50)
email_entry.pack(pady=5)

tk.Label(window, text="Body:").pack(pady=5)
body_text = scrolledtext.ScrolledText(window, width=60, height=10)
body_text.pack(pady=5)

# Widgets for CSV and temp file tasks
tk.Label(window, text="Age in Days (for temp files):").pack(pady=5)
age_entry = tk.Entry(window, width=10)
age_entry.pack(pady=5)

tk.Label(window, text="Website URL (for scraping):").pack(pady=5)
url_entry = tk.Entry(window, width=50)
url_entry.pack(pady=5)

# Widgets for displaying results
tk.Label(window, text="Scraping Results:").pack(pady=5)
result_text = scrolledtext.ScrolledText(window, width=60, height=10)
result_text.pack(pady=5)

# Execute the selected task
run_button = tk.Button(window, text="Run Task", command=run_task)
run_button.pack(pady=20)

# Start the GUI main loop
window.mainloop()
