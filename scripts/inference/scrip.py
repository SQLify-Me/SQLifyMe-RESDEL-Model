
import os
import sys
import subprocess

# Set variables
device = "0"
tables_for_natsql = "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/data/preprocessed_data/test_tables_for_natsql.json"

if sys.argv[1] == "base":
    text2natsql_model_save_path = "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/models/Code-T5-Bimodal/checkpoint-8750"
    text2natsql_model_bs = 8
elif sys.argv[1] == "large":
    text2natsql_model_save_path = "./models/text2natsql-t5-large/checkpoint-21216"
    text2natsql_model_bs = 8
elif sys.argv[1] == "3b":
    text2natsql_model_save_path = "./models/text2natsql-t5-3b/checkpoint-78302"
    text2natsql_model_bs = 6
else:
    print("The first arg must be in [base, large, 3b].")
    sys.exit(1)

model_name = f"resdsql_{sys.argv[1]}_natsql"

if sys.argv[2] == "spider":
    # spider's dev set
    table_path = "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/data/spider/tables.json"
    input_dataset_path = "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/data/spider/dev.json"
    db_path = "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/database"
    output = "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/predictions/Spider-dev/{model_name6}/pred.sql"
elif sys.argv[2] == "spider-realistic":
    # spider-realistic
    table_path = "./data/spider/tables.json"
    input_dataset_path = "./data/spider-realistic/spider-realistic.json"
    db_path = "./database"
    output = "./predictions/spider-realistic/{model_name}/pred.sql"
    if sys.argv[1] == "3b":
        text2natsql_model_save_path = "./models/text2natsql-t5-3b/checkpoint-61642"
elif sys.argv[2] == "spider-syn":
    # spider-syn
    table_path = "./data/spider/tables.json"
    input_dataset_path = "./data/spider-syn/dev_syn.json"
    db_path = "./database"
    output = "./predictions/spider-syn/{model_name}/pred.sql"
# Add other conditions as per your original script


# Execute commands
try:
    # Prepare table file for natsql
    # subprocess.run(["python", "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/NatSQL/table_transform.py",
    #                 "--in_file", table_path,
    #                 "--out_file", tables_for_natsql,
    #                 "--correct_col_type",
    #                 "--remove_start_table",
    #                 "--analyse_same_column",
    #                 "--table_transform",
    #                 "--correct_primary_keys",
    #                 "--use_extra_col_types",
    #                 "--db_path", db_path], check=True)

    # # Preprocess test set
    # subprocess.run(["python", "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/preprocessing.py",
    #                 "--mode", "test",
    #                 "--table_path", table_path,
    #                 "--input_dataset_path", input_dataset_path,
    #                 "--output_dataset_path", "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/data/preprocessed_data/preprocessed_test_natsql.json",
    #                 "--db_path", db_path,
    #                 "--target_type", "natsql"], check=True)

    # Add other commands similarly
    #Predict probability for each schema item in the test set
    # schema_classifier_command = [
    #     "python", 
    #     "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/schema_item_classifier.py",
    #     "--batch_size", "32",
    #     "--device", device,
    #     "--seed", "42",
    #     "--save_path", "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/models/text2natsql_schema_item_classifier",
    #     "--dev_filepath", "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/data/preprocessed_data/preprocessed_test_natsql.json",
    #     "--output_filepath", "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/data/preprocessed_data/test_with_probs_natsql.json",
    #     "--use_contents",
    #     "--mode", "test"
    # ]
    # subprocess.run(schema_classifier_command, check=True)

    # Generate text2natsql test set
    # data_generator_command = [
    #     "python",
    #     "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/text2sql_data_generator.py",
    #     "--input_dataset_path", "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/data/preprocessed_data/test_with_probs_natsql.json",
    #     "--output_dataset_path", "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/data/preprocessed_data/resdsql_test_natsql.json",
    #     "--topk_table_num", "4",
    #     "--topk_column_num", "5",
    #     "--mode", "test",
    #     "--use_contents",
    #     "--output_skeleton",
    #     "--target_type", "natsql"
    # ]
    # subprocess.run(data_generator_command, check=True)

    # Inference using the best text2natsql checkpoint
    inference_command = [
        "python",
        "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/text2sql.py",
        "--batch_size", str(text2natsql_model_bs),
        "--device", device,
        "--seed", "42",
        "--save_path", text2natsql_model_save_path,
        "--mode", "eval",
        "--dev_filepath", "D:/mohamed/REDSQL/RESDSQL-main/RESDSQL-main/data/preprocessed_data/resdsql_test_natsql.json",
        "--original_dev_filepath", input_dataset_path,
        "--db_path", db_path,
        "--tables_for_natsql", tables_for_natsql,
        "--num_beams", "8",
        "--num_return_sequences", "8",
        "--target_type", "natsql",
        "--output", output
    ]
    subprocess.run(inference_command, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error executing command: {e}")
    sys.exit(1)
