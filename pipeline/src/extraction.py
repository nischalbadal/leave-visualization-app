import argparse
import api_loader
import bulk_upload


def main():
    parser = argparse.ArgumentParser(description="Data Loader")
    parser.add_argument(
        "--source",
        choices=["api", "upload"],
        help="Specify the data source (api/upload)",
    )
    parser.add_argument(
        "--file", help="Specify the file name for upload (required for upload)"
    )
    args = parser.parse_args()

    if args.source == "api":
        api_loader.main()
    elif args.source == "upload":
        if args.file:
            bulk_upload.load_data_from_file(args.file)
        else:
            print("Please specify a file name with --file option for bulk upload.")


if __name__ == "__main__":
    main()
