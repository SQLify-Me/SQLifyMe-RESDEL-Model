import subprocess
import sys


def run_preprocessing(mode, input_dataset_path, natsql_dataset_path, output_dataset_path):
    command = [
        "python", "preprocessing.py",
        "--mode", mode,
        "--table_path", "./data/spider/tables.json",
        "--input_dataset_path", input_dataset_path,
        "--natsql_dataset_path", natsql_dataset_path,
        "--output_dataset_path", output_dataset_path,
        "--db_path", "./database",
        "--target_type", "natsql"
    ]
    subprocess.run(command, check=True)

def run_table_transform():
    command = [
        "python", "NatSQL/table_transform.py",
        "--in_file", "./data/spider/tables.json",
        "--out_file", "./data/preprocessed_data/tables_for_natsql.json",
        "--correct_col_type",
        "--remove_start_table",
        "--analyse_same_column",
        "--table_transform",
        "--correct_primary_keys",
        "--use_extra_col_types"
    ]
    subprocess.run(command, check=True)



def run_schema_item_classifier_training():
    command = [
        "python", "-u", "schema_item_classifier.py",
        "--batch_size", "8",
        "--gradient_descent_step", "2",
        "--device", "0",
        "--learning_rate", "1e-5",
        "--gamma", "2.0",
        "--alpha", "0.75",
        "--epochs", "128",
        "--patience", "16",
        "--seed", "42",
        "--save_path", "./models/text2natsql_schema_item_classifier",
        "--tensorboard_save_path", "./tensorboard_log/text2natsql_schema_item_classifier",
        "--train_filepath", "./data/preprocessed_data/preprocessed_train_spider_natsql.json",
        "--dev_filepath", "./data/preprocessed_data/preprocessed_dev_natsql.json",
        "--model_name_or_path", "roberta-large",
        "--use_contents",
        "--mode", "train"
    ]
    subprocess.run(command, check=True)



def run_text2sql_data_generator(mode, input_dataset_path, output_dataset_path, noise_rate=None):
    command = [
        "python", "text2sql_data_generator.py",
        "--input_dataset_path", input_dataset_path,
        "--output_dataset_path", output_dataset_path,
        "--topk_table_num", "4",
        "--topk_column_num", "5",
        "--mode", mode,
        "--use_contents",
        "--output_skeleton",
        "--target_type", "natsql"
    ]
    if noise_rate is not None:
        command.extend(["--noise_rate", str(noise_rate)])
    subprocess.run(command, check=True)

def run_schema_item_classifier_prediction():
    command = [
        "python", "schema_item_classifier.py",
        "--batch_size", "32",
        "--device", "0",
        "--seed", "42",
        "--save_path", "./models/text2natsql_schema_item_classifier",
        "--dev_filepath", "./data/preprocessed_data/preprocessed_dev_natsql.json",
        "--output_filepath", "./data/preprocessed_data/dev_with_probs_natsql.json",
        "--use_contents",
        "--mode", "eval"
    ]
    subprocess.run(command, check=True)

def run_text2sql_training():
    command = [
        "python", "-u", "text2sql.py",
        "--batch_size", "4",
        "--gradient_descent_step", "2",
        "--device", "0",
        "--learning_rate", "1e-4",
        "--epochs", "8",
        "--seed", "42",
        "--save_path", "./models/Code-T5-Bimodal",
        "--tensorboard_save_path", "./tensorboard_log/Code-T5-Bimodal",
        "--model_name_or_path", "t5-base",
        "--use_adafactor",
        "--mode", "train",
        "--train_filepath", "./data/preprocessed_data/resdsql_train_spider_natsql.json"
    ]
    subprocess.run(command, check=True)

def run_evaluate_text2sql_ckpts():
    command = [
        "python", "-u", "evaluate_text2sql_ckpts.py",
        "--batch_size", "32",
        "--device", "0",
        "--seed", "42",
        "--save_path", "./models/text2natsql-t5-base",
        "--eval_results_path", "./eval_results/text2natsql-t5-base",
        "--mode", "eval",
        "--dev_filepath", "./data/preprocessed_data/resdsql_dev_natsql.json",
        "--original_dev_filepath", "./data/spider/dev.json",
        "--db_path", "./database",
        "--tables_for_natsql", "./data/preprocessed_data/tables_for_natsql.json",
        "--num_beams", "8",
        "--num_return_sequences", "8",
        "--target_type", "natsql"
    ]
    subprocess.run(command, check=True)


if __name__ == "__main__":
    # Preprocess train_spider dataset
    # run_preprocessing(
    #     mode="train",
    #     input_dataset_path="./data/spider/train_spider.json",
    #     natsql_dataset_path="./NatSQL/NatSQLv1_6/train_spider-natsql.json",
    #     output_dataset_path="./data/preprocessed_data/preprocessed_train_spider_natsql.json"
    # )

    # # Preprocess dev dataset
    # run_preprocessing(
    #     mode="eval",
    #     input_dataset_path="./data/spider/dev.json",
    #     natsql_dataset_path="./NatSQL/NatSQLv1_6/dev-natsql.json",
    #     output_dataset_path="./data/preprocessed_data/preprocessed_dev_natsql.json"
    # )

    # Preprocess tables.json for natsql
    #run_table_transform()

    ######################
    #run_schema_item_classifier_training()

    # run_text2sql_data_generator(
    #     mode="train",
    #     input_dataset_path="./data/preprocessed_data/preprocessed_train_spider_natsql.json",
    #     output_dataset_path="./data/preprocessed_data/resdsql_train_spider_natsql.json",
    #     noise_rate=0.2
    # )

    # # Predict probability for each schema item in the eval set
    # run_schema_item_classifier_prediction()

    # # Generate text2natsql development dataset
    # run_text2sql_data_generator(
    #     mode="eval",
    #     input_dataset_path="./data/preprocessed_data/dev_with_probs_natsql.json",
    #     output_dataset_path="./data/preprocessed_data/resdsql_dev_natsql.json"
    # )



    # Train text2natsql-t5-base model
    run_text2sql_training()

    # Select the best text2natsql-t5-base checkpoint
    # run_evaluate_text2sql_ckpts()