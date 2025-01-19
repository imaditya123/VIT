import argparse
import os
from vit import VitV1


def init_repo(args):
    vit = VitV1(repo_path=os.getcwd())
    vit.init()


def add_files(args):
    vit = VitV1(repo_path=os.getcwd())
    for file in args.files:
        vit.add(file)


def commit_changes(args):
    vit = VitV1(repo_path=os.getcwd())
    vit.commit(args.message)


def checkout_branch(args):
    vit = VitV1(repo_path=os.getcwd())
    if args.b:
        vit.create_branch(args.branch)
    vit.checkout(args.branch)


def show_branch(args):
    vit = VitV1(repo_path=os.getcwd())
    vit.branch()


def diff_changes(args):
    vit = VitV1(repo_path=os.getcwd())
    for file in args.files:
        vit.diff(file)


def main():

    parser = argparse.ArgumentParser(description="VIT: Version Information Tracker is a version control tool.")
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Subparser for initializing a repository
    parser_init = subparsers.add_parser("init", help="Initialize a new Git repository")
    parser_init.set_defaults(func=init_repo)

    # Subparser for stagging the file
    parser_add = subparsers.add_parser("add", help="Add files to the staging area")
    parser_add.add_argument("files", nargs="+", help="Files to add to the staging area")
    parser_add.set_defaults(func=add_files)

    # Subparser for commit changes
    parser_commit = subparsers.add_parser("commit", help="Commit changes")
    parser_commit.add_argument("--message", "-m", required=True, help="Commit message")
    parser_commit.set_defaults(func=commit_changes)

    # Subparser for checkout
    parser_checkout = subparsers.add_parser("checkout", help="Checkout a branch")
    parser_checkout.add_argument(
        "-b", action="store_true", help="Create and checkout a new branch"
    )
    parser_checkout.add_argument("branch", help="Create and checkout a new branch")
    parser_checkout.set_defaults(func=checkout_branch)

    # Subparser for Branch
    parser_branch = subparsers.add_parser(
        "branch", help="list out all the branches available"
    )
    parser_branch.set_defaults(func=show_branch)

    # Subparser for Diif
    parser_diff = subparsers.add_parser("diff", help="Show the diff in the file")
    parser_diff.add_argument("files", nargs="+", help="Files to show the diff")
    parser_diff.set_defaults(func=diff_changes)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
