import argparse
import CMD as cmd

def main():
    parser = argparse.ArgumentParser(description="AI Trainer CLI for Sales Profiles")
    subparsers = parser.add_subparsers(dest="profile", required=True)

    # Relative profile
    subparsers.add_parser("relative", help="Start AI trainer for a personal relative")

    # Shopkeeper profile
    subparsers.add_parser("shopkeeper", help="Start AI trainer for a shopkeeper")

    args = parser.parse_args()

    if args.profile == "relative":
        cmd.relative()
    elif args.profile == "shopkeeper":
        cmd.shopkeeper()

if __name__ == "__main__":
    main()
