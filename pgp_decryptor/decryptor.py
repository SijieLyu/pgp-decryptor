import subprocess
import csv
import time
import logging
from pathlib import Path
from multiprocessing import Pool


class PGPDecryptor:
    def __init__(self, input_base_dir, output_base_dir, summary_dir, num_workers=4):
        self.input_base_dir = Path(input_base_dir)
        self.output_base_dir = Path(output_base_dir)
        self.summary_dir = Path(summary_dir)
        self.num_workers = num_workers

        self.total_files_processed = 0
        self.successfully_decrypted = 0
        self.failed_decryption = 0
        self.time_taken_seconds = 0.0

        self.summary_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def decrypt_file(args):
        if not isinstance(args, tuple) or len(args) != 2:
            raise ValueError ("decrypt_file() expects a tuple: (pgp_file_path, output_dir)")
        pgp_file, output_dir = args
        output_file = output_dir / pgp_file.stem
        encrypted_size = pgp_file.stat().st_size

        command = [
            "gpg", "--batch", "--yes",
            "--output", str(output_file),
            "--decrypt", str(pgp_file)
        ]

        process = subprocess.run(command, capture_output=True, text=True)

        if process.returncode == 0 and output_file.exists():
            decrypted_size = output_file.stat().st_size
            return (pgp_file.name, output_file.name, encrypted_size, decrypted_size, "Success")
        else:
            return (pgp_file.name, "Decryption Failed", encrypted_size, 0, process.stderr.strip())

    def decrypt_dataset(self, dataset_name):
        input_dir = self.input_base_dir / dataset_name
        output_dir = self.output_base_dir / dataset_name
        output_dir.mkdir(parents=True, exist_ok=True)

        summary_file = self.summary_dir / f"decryption_summary_{dataset_name}.csv"

        pgp_files = list(input_dir.glob("*.gpg"))
        if not pgp_files:
            self.logger.warning(f"No .gpg files found in {input_dir}. Skipping.")
            return

        args = [(file, output_dir) for file in pgp_files]

        start_time = time.time()
        with Pool(processes=self.num_workers) as pool:
            results = pool.map(PGPDecryptor.decrypt_file, args)
        end_time = time.time()

        # Track and summarize stats
        self.time_taken_seconds = end_time - start_time
        self.total_files_processed = len(results)
        self.successfully_decrypted = sum(1 for r in results if r[4] == "Success")
        self.failed_decryption = self.total_files_processed - self.successfully_decrypted

        # Write CSV Summary
        with open(summary_file, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Encrypted File", "Decrypted File", "Encrypted Bytes", "Decrypted Bytes", "Status"])
            writer.writerows(results)

        mins, secs = divmod(self.time_taken_seconds, 60)

        self.logger.info(f"Dataset: {dataset_name}")
        self.logger.info(f"Files Processed: {self.total_files_processed}")
        self.logger.info(f"Successfully Decrypted: {self.successfully_decrypted}")
        self.logger.info(f"Failed Decryption: {self.failed_decryption}")
        self.logger.info(f"Time Taken: {int(mins)}m {int(secs)}s")
        self.logger.info(f"Summary CSV: {summary_file}")

    def batch_decrypt(self, dataset_names):
        for dataset in dataset_names:
            try:
                self.decrypt_dataset(dataset)
            except Exception as e:
                self.logger.error(f"Error processing dataset '{dataset}': {e} ")

    def decrypt_single_file(self, pgp_file_path, output_dir_path):
        """Conveience method for decrypting a single file directly."""
        pgp_file = Path(pgp_file_path)
        output_dir = Path(output_dir_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        result = self.decrypt_file((pgp_file, output_dir))
        status = result[4]

        # Update stats mannually
        self.total_files_processed = 1
        self.successfully_decrypted = 1 if status == "Success" else 0
        self.failed_decryption = 1 - self.successfully_decrypted

        self.logger.info(f"Single file decryption result: {result}")
        return result
    
    @staticmethod
    def check_gpg_installed():
        try:
            subprocess.run(["gpg", "--version"], check=True, capture_output=True)
        except Exception:
            raise RuntimeError("GPG is not installed or not available in PATH.")
