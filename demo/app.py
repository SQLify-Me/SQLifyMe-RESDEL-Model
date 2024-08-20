from schema_transformation import _main
from scrip_demo import __my_main 
import json
from flask import Flask, render_template, request , make_response
import os
import subprocess
import shutil
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


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




def to_dev(question,db_id):
    # Step  1: Open the JSON file
    with open('dev.json', 'r') as json_file:
        # Step  2: Load the JSON data
        data = json.load(json_file)

    # Step  3: Modify the values
    print(data[0])
    data[0]['question'] = question
    data[0]['db_id'] = db_id

    # Step  4: Write the updated data back to the file
    with open('dev.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)



def get_generated_sql():
    with open('./predictions/{model_name}/pred.sql', 'r') as fd:
        sqlFile = fd.read()

    sqlCommands = sqlFile.split(';')
    return sqlCommands
   
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


@app.route('/predict', methods=['POST'])
def predict():
    # Get the question, database id, and schema file from the request
    # question = request.form['question']
    # database_id = request.form['database_id']

    data = request.get_json()

    # Extract the values from the JSON data
    question = data['question']
    database_id = data['database_id']

    print("am herrrrrrr")
    # schema_file = request.files['schema']

    # # Save the schema file to disk
    # folder_path = f'D:/GP/RESDSQL/demo/b/{database_id}'
    # os.makedirs(folder_path, exist_ok=True)
    # schema_path = f'{folder_path}/{database_id}.sqlite'
    # schema_file.save(schema_path)

    #_main()
    to_dev(question, database_id)
    __my_main()

    # Call your model to make the prediction
    predicted_sql = get_generated_sql()
    exec=read_results_from_json()
    # Convert the predicted SQL commands to a JSON response
    response = {'query': predicted_sql,'execution':exec}
    return response


TARGET_FOLDER_PATH = './demo/db'

@app.route('/dbs', methods=['GET'])
def perform_action():
    folder_names = [f.name for f in os.scandir(TARGET_FOLDER_PATH) if f.is_dir()]
    #print(folder_names)

    response = {'schema': folder_names}
    return response



# Define the directory path where you want to place the folder
TARGET_DIR = "./demo/new_DB"

@app.route("/upload", methods=["POST"])
def handle_file():
  # print("inside")
  # # Check if a file was uploaded
  # print(request)
  # print(request.files.keys)
  # print(request.files.to_dict)
  if "file" not in request.files:
    return make_response("No file uploaded!", 400)

  uploaded_file = request.files["file"]
  filename = uploaded_file.filename

  folder_names = [f.name for f in os.scandir(TARGET_FOLDER_PATH) if f.is_dir()]
  filename2, extension = os.path.splitext(uploaded_file.filename)

  if os.path.exists(os.path.join(TARGET_FOLDER_PATH, filename2)):
    return make_response("file already exists!", 400)
  # Create the folder name with the same name as the file
  folder_name = os.path.splitext(filename)[0]

  # Create the target folder path
  target_folder_path = os.path.join(TARGET_DIR, folder_name)

  # Check if the target directory exists, otherwise create it
  if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

  # Create the folder with the same name as the file
  os.makedirs(target_folder_path, exist_ok=True)

  # Save the uploaded file inside the created folder
  uploaded_file.save(os.path.join(target_folder_path, filename))

  ADD_NEW_SCHEMA()
  
  return make_response(f"File {folder_name}' uploaded succesfully ", 200)



if __name__ == '__main__':
    app.run(depug=True)
