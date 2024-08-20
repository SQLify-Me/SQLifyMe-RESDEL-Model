import os
import sys
import subprocess
import time


def __my_main():
    # Set variables
    device = "0"
    tables_for_natsql = "./preprocessed_data/test_tables_for_natsql.json"
    text2natsql_model_save_path = "./models/text2natsql-t5-base/checkpoint-14352"
    text2natsql_model_bs = 8
    # if sys.argv[1] == "base":
    #     text2natsql_model_save_path = "./models/text2natsql-t5-base/checkpoint-14352"
    #     text2natsql_model_bs = 8
    # elif sys.argv[1] == "large":
    #     text2natsql_model_save_path = "./models/text2natsql-t5-large/checkpoint-21216"
    #     text2natsql_model_bs = 8
    # elif sys.argv[1] == "3b":
    #     text2natsql_model_save_path = "./models/text2natsql-t5-3b/checkpoint-78302"
    #     text2natsql_model_bs = 6
    # else:
    #     print("The first arg must be in [base, large, 3b].")
    #     sys.exit(1)

    model_name = f"resdsql_base_natsql"

    # if sys.argv[2] == "spider":
    #     # spider's dev set
    #     table_path = "./tables.json"
    #     input_dataset_path = "./dev.json"
    #     db_path = "./db"
    #     output = "./predictions/{model_name}/pred.sql"
    # elif sys.argv[2] == "spider-realistic":
    #     # spider-realistic
    #     table_path = "./data/spider/tables.json"
    #     input_dataset_path = "./data/spider-realistic/spider-realistic.json"
    #     db_path = "./database"
    #     output = "./predictions/spider-realistic/{model_name}/pred.sql"
    #     if sys.argv[1] == "3b":
    #         text2natsql_model_save_path = "./models/text2natsql-t5-3b/checkpoint-61642"
    # elif sys.argv[2] == "spider-syn":
    #     # spider-syn
    #     table_path = "./data/spider/tables.json"
    #     input_dataset_path = "./data/spider-syn/dev_syn.json"
    #     db_path = "./database"
    #     output = "./predictions/spider-syn/{model_name}/pred.sql"
    # # Add other conditions as per your original script



    table_path = "./tables.json"
    input_dataset_path = "./dev.json"
    db_path = "./db"
    output = "./predictions/{model_name}/pred.sql"

    
    # Execute commands
    try:
        # Prepare table file for natsql
        # start_time = time.perf_counter()  # Get start time

        # subprocess.run(["python", "./NatSQL/table_transform.py",
        #                 "--in_file", table_path,
        #                 "--out_file", tables_for_natsql,
        #                 "--correct_col_type",
        #                 "--remove_start_table",
        #                 "--analyse_same_column",
        #                 "--table_transform",
        #                 "--correct_primary_keys",
        #                 "--use_extra_col_types",
        #                 "--db_path", db_path], check=True)
        # end_time = time.perf_counter()  # Get end time

        # elapsed_time = end_time - start_time
        # print(f"Execution time for func1: {elapsed_time:.6f} seconds")


        start_time = time.perf_counter()  # Get start time

        # # Preprocess test set
        subprocess.run(["python", "./preprocessing.py",
                        "--mode", "test",
                        "--table_path", table_path,
                        "--input_dataset_path", input_dataset_path,
                        "--output_dataset_path", "./preprocessed_data/preprocessed_test_natsql.json",
                        "--db_path", db_path,
                        "--target_type", "natsql"], check=True)

        end_time = time.perf_counter()  # Get end time

        elapsed_time = end_time - start_time
        print(f"Execution time for func2: {elapsed_time:.6f} seconds")
        # Add other commands similarly
        #Predict probability for each schema item in the test set
        start_time = time.perf_counter()  # Get start time

        schema_classifier_command = [
            "python", 
            "./schema_item_classifier.py",
            "--batch_size", "32",
            "--device", device,
            "--seed", "42",
            "--save_path", "./models/text2natsql_schema_item_classifier",
            "--dev_filepath", "./preprocessed_data/preprocessed_test_natsql.json",
            "--output_filepath", "./preprocessed_data/test_with_probs_natsql.json",
            "--use_contents",
            "--mode", "test"
        ]
        subprocess.run(schema_classifier_command, check=True)

        end_time = time.perf_counter()  # Get end time

        elapsed_time = end_time - start_time
        print(f"Execution time func3: {elapsed_time:.6f} seconds")
        # Generate text2natsql test set
        start_time = time.perf_counter()  # Get start time

        data_generator_command = [
            "python",
            "./text2sql_data_generator.py",
            "--input_dataset_path", "./preprocessed_data/test_with_probs_natsql.json",
            "--output_dataset_path", "./preprocessed_data/resdsql_test_natsql.json",
            "--topk_table_num", "4",
            "--topk_column_num", "5",
            "--mode", "test",
            "--use_contents",
            "--output_skeleton",
            "--target_type", "natsql"
        ]
        subprocess.run(data_generator_command, check=True)

        end_time = time.perf_counter()  # Get end time

        elapsed_time = end_time - start_time
        print(f"Execution time for func4: {elapsed_time:.6f} seconds")
        # Inference using the best text2natsql checkpoint
        start_time = time.perf_counter()  # Get start time

        inference_command = [
            "python",
            "./text2sql.py",
            "--batch_size", str(text2natsql_model_bs),
            "--device", device,
            "--seed", "42",
            "--save_path", text2natsql_model_save_path,
            "--mode", "test",
            "--dev_filepath", "./preprocessed_data/resdsql_test_natsql.json",
            "--original_dev_filepath", input_dataset_path,
            "--db_path", db_path,
            "--tables_for_natsql", tables_for_natsql,
            "--num_beams", "8",
            "--num_return_sequences", "8",
            "--target_type", "natsql",
            "--output", output
        ]
        subprocess.run(inference_command, check=True)
        end_time = time.perf_counter()  # Get end time

        elapsed_time = end_time - start_time
        print(f"Execution time func5: {elapsed_time:.6f} seconds")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    # sys.exit(1)
