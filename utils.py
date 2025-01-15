
import csv
import os
from datetime import datetime

# def read_log_file(filename):
#     entries = []
#     with open(filename, 'r') as csvfile:
#         reader = csv.reader(csvfile)
#         next(reader)  # Skip header
#         for row in reader:
#             entries.append({
#                 'date': row[0],
#                 'time': row[1],
#                 'id': row[2],
#                 'status': row[3]
#             })
#     return entries

# def log_timesheet(logs_dir, timesheets_dir, current_date, user_id, time_out):
#     # Ensure directories exist
#     os.makedirs(timesheets_dir, exist_ok=True)
    
#     # Get log entries
#     logs_file = os.path.join(logs_dir, f"{current_date.strftime('%m-%d-%y')}.csv")
#     entries = read_log_file(logs_file)
    
#     # Find matching "In" time
#     in_time = None
#     for entry in reversed(entries):
#         if entry['id'] == user_id:
#             if entry['status'] == 'In':
#                 in_time = datetime.strptime(f"{entry['date']} {entry['time']}", '%Y-%m-%d %H:%M:%S')
#                 break
    
#     if in_time:
#         # Calculate duration
#         duration = time_out - in_time
        
#         # Create timesheet file with date in mm-dd-yy format
#         timesheet_file = os.path.join(timesheets_dir, f"timesheet_{current_date.strftime('%m-%d-%y')}.csv")
#         file_exists = os.path.exists(timesheet_file)
        
#         with open(timesheet_file, 'a', newline='') as csvfile:
#             writer = csv.writer(csvfile)
#             if not file_exists:
#                 writer.writerow(['Date', 'ID', 'Time In', 'Time Out', 'Duration'])
#             writer.writerow([
#                 current_date.strftime('%Y-%m-%d'),
#                 user_id,
#                 in_time.strftime('%H:%M:%S'),
#                 time_out.strftime('%H:%M:%S'),
#                 str(duration)
#             ])

def extract_id(text: str) -> str:
    index = text.find("11")
    if index == -1:
        return ""
    return text[index:index + 8]