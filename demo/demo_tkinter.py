import tkinter as tk
from tkinter import filedialog
from schema_transformation import _main
from scrip_demo import __my_main
import json
import os
import time
import shutil
import subprocess

# def browse_folder():
#     folder_selected = filedialog.askdirectory()
#     if folder_selected:
#         input_path.set(folder_selected)
def to_dev():
    # Step  1: Open the JSON file
    with open('./demo/dev.json', 'r') as json_file:
        # Step  2: Load the JSON data
        data = json.load(json_file)

    # Step  3: Modify the values
    print(data[0])
    data[0]['question'] = Question.get()
    data[0]['db_id'] = db_idd.get()

    # Step  4: Write the updated data back to the file
    with open('./dev.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

def read_sql():
    with open('./predictions/{model_name}/pred.sql', 'r') as fd:
        sqlFile = fd.read()

    sqlCommands = sqlFile.split(';')
    output_sql.set(sqlCommands)

def create_folder_and_move_file(file_path, target_dir):
  """
  Creates a folder with the same name as the file (including extension) in the target directory and moves the file inside.

  Args:
    file_path: Path to the file.
    target_dir: Path to the target directory where the folder will be created.
  """
  # Get the filename with extension
  filename = os.path.basename(file_path)

  # Get the filename without extension
  filename_without_extension, _ = os.path.splitext(os.path.basename(file_path))
  # Create the folder path inside the target directory
  folder_path = os.path.join(target_dir, filename_without_extension)

  # Try creating the folder and moving the file
  try:
    os.mkdir(folder_path)
    # Move the file while preserving the extension
    shutil.move(file_path, folder_path)
    print(f"Folder '{folder_path}' created and file moved successfully!")
  except FileExistsError:
    print(f"Folder '{folder_path}' already exists. Skipping file move.")

def read_results_from_json():
  filename='./execution.json'
  try:
    with open(filename, 'r') as f:
      return json.load(f)
  except FileNotFoundError:
    print(f"JSON file not found: {filename}")
    return None
  except json.JSONDecodeError as e:
    print(f"Error decoding JSON file: {e}")
    return None

def ADD_NEW_SCHEMA():
    
    
  # file_path = "./demo/concert_singer/concert_singer.sqlite"
  # target_dir = "./demo/new_DB"

  # create_folder_and_move_file(file_path, target_dir)

  _main()

  subprocess.run(["python", "./NatSQL/table_transform.py",
              "--in_file", "./demo/tables_new.json",
              "--out_file", "./preprocessed_data/test_tables_for_natsql.json",
              "--correct_col_type",
              "--remove_start_table",
              "--analyse_same_column",
              "--table_transform",
              "--correct_primary_keys",
              "--use_extra_col_types",
              "--db_path", "./demo/new_DB"], check=True)

        # Define paths
  source_dir = "./demo/new_DB"  # Directory containing the folder to move (Folder Y)
  destination_path = "./demo/db" # Destination folder (Folder X)

  # Get list of directories in source directory
  try:
    directories = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]
  except OSError as e:
    print(f"Error accessing directory: {e}")
    exit()

  # Check if directories exist
  if not directories:
    print("No directories found in the source directory.")
    exit()

  # Move the first directory (assuming there's only one folder to move)
  source_path = os.path.join(source_dir, directories[0])
  try:
    shutil.move(source_path, destination_path)
    print(f"Moved folder: {directories[0]} to {destination_path}")
  except shutil.Error as e:
    print(f"Error moving folder: {e}")    


TARGET_FOLDER_PATH = './demo/db'
def perform_action():
  #ADD_NEW_SCHEMA()
    # folder_names = [f.name for f in os.scandir(TARGET_FOLDER_PATH) if f.is_dir()]
    # print(folder_names)



    # start_time = time.perf_counter()
    # end_time = time.perf_counter()  # Get end time

    # elapsed_time = end_time - start_time
    # print(f"Execution time for schema transformation: {elapsed_time:.6f} seconds")

    to_dev()
    __my_main()
    read_sql()
    print(read_results_from_json())



root = tk.Tk()
root.title("SQL Generator")

root.geometry("800x600")

# Create variables to hold paths
Question = tk.StringVar()
db_idd=tk.StringVar()
output_sql=tk.StringVar()

# Input path entry box
# input_path_label = tk.Label(root, text="Input Folder:")
# input_path_label.grid(row=0, column=0, pady=10)

# input_path_entry = tk.Entry(root, textvariable=input_path, width=60)
# input_path_entry.grid(row=0, column=1, pady=10)

# # Browse button for input path
# browse_button = tk.Button(root, text="Browse Folder", command=browse_folder)
# browse_button.grid(row=0, column=3, pady=10)

db_label = tk.Label(root, text="DB ID")
db_label.grid(row=1, column=0, pady=10)
db_id_entry = tk.Entry(root, textvariable=db_idd, width=60)
db_id_entry.grid(row=1, column=1, pady=10)


db_label = tk.Label(root, text="Question")
db_label.grid(row=2, column=0, pady=10)
Question_entry = tk.Entry(root, textvariable=Question, width=60)
Question_entry.grid(row=2, column=1, pady=10)

action_button = tk.Button(root, text="SQLIFY ME", command=perform_action)
action_button.grid(row=3, column=1, pady=10)


output_final = tk.Entry(root, textvariable=output_sql, width=80,font=("Arial",  18))
output_final.grid(row=4, column=4, pady=10)

root.mainloop()
