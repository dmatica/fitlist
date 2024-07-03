import os
import shutil
import re
import calendar as calendar

def extract_datetime(filename):
    # Define regular expression pattern to match date-time format
    pattern = r'(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})'

    # Find matches in the filename
    match = re.search(pattern, filename)

    if match:
        # Extract date-time components
        year, month, day, hour, minute, second = match.groups()
        return year, month, day, hour, minute, second
    else:
        return None

def organize_files(source_dir):
    for filename in os.listdir(source_dir):
        if filename.endswith('') and '-' in filename:
            print("____"+filename)
            datetime_info = extract_datetime(filename)
            workout_type=filename.split('-')[0]
            new_filename = filename.split('-', 1)[1]
            new_new_filename = new_filename.split('-',1)[0]+filename[-4:]
            if datetime_info:
                year, month, day, hour, minute, second = datetime_info
                # Create nested directories
                nested_dir = os.path.join(source_dir, year, month+" - "+calendar.month_name[int(month)], year+'-'+month+'-'+day, workout_type+'_'+year+'-'+month+'-'+day+'_'+hour+'-'+minute+'-'+second)
                os.makedirs(nested_dir, exist_ok=True)
                # Move the file to the nested directory
                shutil.move(os.path.join(source_dir, filename), os.path.join(nested_dir, new_new_filename))
                print(f"Moved {filename} to {nested_dir}")

# Example usage:
source_directory = "/Users/davindersandhu/PycharmProjects/Fitcheck/Data"
organize_files(source_directory)