import argparse
import os
from vit import VitV1
import urllib.request
from zipfile import ZipFile 

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

def clone_repo(args):
    repo_name=args.url.split("/")[-1].replace(".git",'')
    url=args.url.replace(".git","/archive/master.zip")
    # Repo Download
    print(repo_name)
    save_path=os.path.join(os.getcwd(),f"{repo_name}.zip")
    print(save_path)
    with urllib.request.urlopen(url) as dl_file:
        with open(save_path, 'wb') as out_file:
            out_file.write(dl_file.read())
    # unziping
    with ZipFile(save_path) as zObject: 
        zObject.extractall() 
    os.remove(save_path)

def merge_branches(args):
    vit = VitV1(repo_path=os.getcwd())
    vit.merge(args.branch)
    
def stash_commit(args):
    vit = VitV1(repo_path=os.getcwd())
    vit.stash()
    
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

    # Subparser for Clone
    parser_repo = subparsers.add_parser("clone", help="clones the repo")
    parser_repo.add_argument("url", help="url of the github repository")
    parser_repo.set_defaults(func=clone_repo)

    # Subparser for Merge
    parser_merge = subparsers.add_parser("merge", help="Merge the branches")
    parser_merge.add_argument("branch",  help="Branch that needs to merge")
    parser_merge.set_defaults(func=merge_branches)

    # Subparser for stash
    parser_stash = subparsers.add_parser("stash", help="Update the local changes to the last commit")
    parser_stash.set_defaults(func=stash_commit)


    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
