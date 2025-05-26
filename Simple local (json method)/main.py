import argparse
import personas

def main():
    parser = argparse.ArgumentParser(description="AI Trainer CLI for Sales Profiles")
    subparsers = parser.add_subparsers(dest="profile", required=True)

    subparsers.add_parser("relative", help="Start AI trainer for a personal relative")
    subparsers.add_parser("shopkeeper", help="Start AI trainer for a shopkeeper")

    args = parser.parse_args()

    if args.profile == "relative":
        personas.start_relative_session()
    elif args.profile == "shopkeeper":
        personas.start_shopkeeper_session()

if __name__ == "__main__":
    main()
