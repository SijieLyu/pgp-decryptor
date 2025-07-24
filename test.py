from pgp_decryptor.decryptor import PGPDecryptor

# Example 1: Decrypt a single file (manual call to the static method)
from pathlib import Path

single_file = Path("H:/project/pgp_decrypter/encrypt/test/test1.gpg")
output_dir = Path("H:/project/pgp_decrypter/decrypt/test")
output_dir.mkdir(parents=True, exist_ok=True)

result = PGPDecryptor.decrypt_file((single_file, output_dir))
print("Single file decryption result:")
print(result)


# Example 2: Batch decrypt a dataset folder using the class
decryptor = PGPDecryptor(
    input_base_dir="H:/project/pgp_decrypter/encrypt",
    output_base_dir="H:/project/pgp_decrypter/decrypt",
    summary_dir="H:/project/pgp_decrypter/decrypt/summary",
    num_workers=4
)

# Dataset folder names (subfolder under encrypt/)
datasets = ["test", "dataset2"]
decryptor.batch_decrypt(datasets)

# Print stats
print("\nBatch decryption complete:")
print(f"  Files processed: {decryptor.total_files_processed}")
print(f"  Success: {decryptor.successfully_decrypted}")
print(f"  Failed: {decryptor.failed_decryption}")
print(f"  Time taken: {decryptor.time_taken_seconds:.2f} seconds")
