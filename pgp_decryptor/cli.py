import argparse
from pgp_decryptor.decryptor import PGPDecryptor


def main():
    parser = argparse.ArgumentParser(description="Batch decrypt .gpg files using GPG.")
    parser.add_argument("--input", required=True, help="Path to input base directory")
    parser.add_argument("--output", required=True, help="Path to output base directory")
    parser.add_argument("--summary", required=True, help="Path to output summary directory")
    parser.add_argument("--datasets", nargs="+", required=True, help="List of dataset folder names")
    parser.add_argument("--workers", type=int, default=4, help="Number of parallel workers (default: 4)")

    args = parser.parse_args()

    decryptor = PGPDecryptor(
        input_base_dir=args.input,
        output_base_dir=args.output,
        summary_dir=args.summary,
        num_workers=args.workers
    )
    decryptor.batch_decrypt(args.datasets)


if __name__ == "__main__":
    main()
