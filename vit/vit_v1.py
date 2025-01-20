import os
import json
import hashlib
from datetime import datetime
from urllib.parse import urlparse
from difflib import unified_diff


class VitV1:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.git_dir = os.path.join(repo_path, ".vit")
        self.object_dir = os.path.join(self.git_dir, "objects")
        self.refs_dir = os.path.join(self.git_dir, "refs")
        self.hooks_dir = os.path.join(self.git_dir, "hooks")
        self.head_path = os.path.join(self.git_dir, "HEAD")
        self.index_path = os.path.join(self.git_dir, "index")
        self.remote_url = None
        # repo_path/
        # ├── .mygit/                # Main directory for the Git-like structure
        # │   ├── objects/           # Directory for objects
        # │   ├── refs/              # Directory for references
        # │   ├── hooks/             # Directory for hooks
        # │   ├── HEAD               # File to store the HEAD reference
        # │   └── index              # File to store the index

    def read_file(self, file_path: str):
        with open(file_path, "r") as file:
            return file.read()

    def write_file(self, file_path: str, data: object):
        with open(file_path, "w") as file:
            file.write(data)

    def hash_objects(self, data: str) -> str:
        """
        Hashes the given data, saves it to the specified location, and returns the hash.
        Args:
            data (str): The data to hash and store.
        Returns:
            str: The SHA-1 hash (object ID) of the data.
        """
        try:
            oid = hashlib.sha1(data.encode()).hexdigest()
            object_path = os.path.join(self.object_dir, oid)
            self.write_file(object_path, data)

            return oid
        except Exception as e:
            raise RuntimeError(f"Failed to hash and save object: {e}")

    def get_current_branch(self) -> str:
        """
        Retrieves the name of the current branch by reading the HEAD file.

        Returns:
            str: The name of the current branch.
        """
        try:
            with open(self.head_path, "r") as head:
                # The HEAD file typically contains "refs: refs/heads/<branch_name>"
                return head.read().strip().split("/")[-1]
        except (FileNotFoundError, IndexError) as e:
            raise RuntimeError(f"Failed to determine the current branch: {e}")

    def get_current_commit(self) -> str:
        """
        Retrieves the current commit hash of the current branch.
        Returns:
            str: The commit hash of the current branch, or an empty string if none exists.
        """
        try:
            branch = self.get_current_branch()
            branch_ref = os.path.join(self.refs_dir, "heads", branch)

            if os.path.exists(branch_ref):
                # Read the commit hash from the branch reference file
                with open(branch_ref, "r") as branch_file:
                    return branch_file.read().strip()

            # If the branch reference does not exist, return an empty string
            return ""

        except Exception as e:
            raise RuntimeError(f"Failed to retrieve the current commit: {e}")

    def get_branch_last_commit(self, branch: str) -> str:
        """
        Retrieves the current commit hash of the current branch.
        Returns:
            str: The commit hash of the current branch, or an empty string if none exists.
        """
        try:
            branch_ref = os.path.join(self.refs_dir, "heads", branch)

            if os.path.exists(branch_ref):
                # Read the commit hash from the branch reference file
                with open(branch_ref, "r") as branch_file:
                    return branch_file.read().strip()

            # If the branch reference does not exist, return an empty string
            return ""

        except Exception as e:
            raise RuntimeError(f"Failed to retrieve the current commit: {e}")

    def _get_diverge_commit(self, branch1, branch2):
        def prev(node1):
            with open(os.path.join(self.object_dir, node1), "r") as commit_content:
                content = json.load(commit_content)
            return content["parent"]

        first1 = self.get_branch_last_commit(branch1)
        first2 = self.get_branch_last_commit(branch2)

        node1 = first1
        node2 = first2

        while True:
            if node1 == node2 and node1 != "":
                return node1
            node1 = prev(node1) if node1 != "" else first1
            node2 = prev(node2) if node2 != "" else first2
            node2 = prev(node2) if node2 != "" else first2

    def _get_list_commits(self, branch, commit):
        def prev(node1):
            with open(os.path.join(self.object_dir, node1), "r") as commit_content:
                content = json.load(commit_content)
            return content["parent"]

        node = self.get_branch_last_commit(branch)
        list_node = []
        while node != commit:
            list_node.append(node)
            node = prev(node)

        list_node.append(commit)
        return list_node

    def _get_comment_character(self, file_path: str, content) -> str:
        extention = file_path.split(".")[-1]
        if extenstion in (".c", ".cpp", ".java", ".js", ".cs", ".swift", ".go"):
            return f"/* f{content} */"
        elif extenstion in (".py", ".rb", ".pl", ".sh", ".r"):
            return "\n".join(["# f{cont}" for cont in content.splitlines()])
        elif extenstion in (".html", ".md", ".xml"):
            return f"<!-- {content} -->"
        else:
            return content

    def init(self) -> None:
        """
        Initializes and creates the required directories and files for the repository.
        """
        try:
            # Create required directories
            os.makedirs(self.object_dir, exist_ok=True)
            os.makedirs(self.hooks_dir, exist_ok=True)
            os.makedirs(os.path.join(self.refs_dir, "heads"), exist_ok=True)
            os.makedirs(os.path.join(self.refs_dir, "tags"), exist_ok=True)

            # Initialize HEAD file pointing to the main branch
            self.write_file(self.head_path, "refs: refs/heads/main")

            # Initialize an empty index file
            with open(self.index_path, "w") as index:
                json.dump({}, index)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize repository: {e}")

    def add(self, file: str) -> None:
        """
        Hashes the given data, saves it to the specified location, and returns the hash.
        Args:
            file_path (str): file that needs to be added.
        Returns: -> None
        """
        try:
            file_path = os.path.join(self.repo_path, file)

            content = self.read_file(file_path)

            oid = self.hash_objects(content)

            with open(self.index_path, "r+") as index:
                staged = json.load(index)
                staged[file_path] = oid
                index.seek(0)
                json.dump(staged, index)
                # index.truncate() #No need
            print(f"Added {file_path} to staging area.")
        except FileNotFoundError:
            print(f"Error: {file_path} does not exist.")
        except Exception as e:
            print(f"An error occurred while adding the file: {e}")

    def commit(self, message: str) -> None:
        """
        Creates a new commit with the given message.
        Args:
            message (str): The commit message.
        Raises:
            RuntimeError: If an error occurs during the commit process.
        """
        try:
            # Load the staged changes from the index
            with open(self.index_path, "r") as index_file:
                staged = json.load(index_file)
            if not staged:
                print("Nothing to commit")
                return
            # Get the parent commit (if any)
            parent = self.get_current_commit()
            tree = json.dumps(staged)
            tree_oid = self.hash_objects(tree)
            # Prepare the commit content
            commit_content = {
                "tree": tree_oid,
                "parent": parent,
                "message": message,
                "timestamp": datetime.now().isoformat(),
            }
            commit_oid = self.hash_objects(json.dumps(commit_content))
            branch = self.get_current_branch()
            branch_ref = os.path.join(self.refs_dir, "heads", branch)
            self.write_file(branch_ref, commit_oid)

            # Clear the staging area (index)
            with open(self.index_path, "w") as index_file:
                json.dump({}, index_file)

        except FileNotFoundError as e:
            raise RuntimeError(f"File not found during commit process: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON format in index file: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while committing: {e}")

    def create_branch(self, branch_name: str) -> None:
        """
        Creates a new branch with the given name.
        Args:
            branch_name (str): The name of the branch to create.
        Returns:-> None
        """
        try:
            # Define the path for the new branch reference
            branch_ref = os.path.join(self.refs_dir, "heads", branch_name)

            # Check if the branch already exists
            if os.path.exists(branch_ref):
                print(f"Branch '{branch_name}' already exists.")
                return

            # Get the current commit hash
            current_commit = self.get_current_commit()

            # Create the new branch and point it to the current commit
            os.makedirs(os.path.dirname(branch_ref), exist_ok=True)
            self.write_file(branch_ref, current_commit or "")
            # Remove
            # with open(branch_ref, "w") as branch_file:
            #     branch_file.write(current_commit or "")

            print(f"Created branch '{branch_name}'.")
        except Exception as e:
            print(f"An error occurred while creating the branch '{branch_name}': {e}")

    def branch(self) -> None:
        """
        Displays all the branches available, highlighting the current branch.
        Args:
            None
        Returns:
            None
        """
        try:
            # Get the directory for branch references
            branches_dir = os.path.join(self.refs_dir, "heads")
            # List all branches
            if not os.path.exists(branches_dir):
                print("No branches available.")
                return

            branches = os.listdir(branches_dir)
            if not branches:
                print("No branches available.")
                return
            # Get the current branch
            current_branch = self.get_current_branch()
            # Display the branches
            for branch in branches:
                if branch == current_branch:
                    print(f"-> {branch} (current)")
                else:
                    print(f"- {branch}")
        except Exception as e:
            print(f"An error occurred while displaying branches: {e}")

    def remote(self, remote_url: str) -> None:
        result = urlparse(remote_url)
        assert all([result.scheme, result.netloc]), "Enter a valid url"
        self.remote_url = remote_url

    def checkout(self, branch_name: str) -> None:
        """
        Checks out the specified branch by updating the HEAD file.

        Args:
            branch_name (str): The name of the branch to check out.

        Returns:
            None
        """
        try:
            # Construct the reference path for the branch
            branch_ref = os.path.join(self.refs_dir, "heads", branch_name)

            # Check if the branch exists
            if not os.path.exists(branch_ref):
                print(f"Branch '{branch_name}' does not exist.")
                return

            # Update the HEAD file to point to the new branch
            self.write_file(self.head_path, f"ref: refs/heads/{branch_name}")
            # Remove
            # with open(self.head_path, "w") as head:
            #     head.write(f"ref: refs/heads/{branch_name}")

            print(f"Checked out branch '{branch_name}'")
        except Exception as e:
            print(f"An error occurred while checking out branch '{branch_name}': {e}")

    def diff(self, file: str) -> None:
        """
        Shows the differences between the current file and the staged version.
        Args:
            file_path (str): The path to the file to compare.
        Returns:
            None
        """
        try:
            file_path = os.path.join(self.repo_path, file)
            with open(self.index_path, "r") as index:
                staged = json.load(index)
            if file_path not in staged:
                print(f"File '{file_path}' is not staged for commit.")
                return
            staged_oid = staged[file_path]
            staged_path = os.path.join(self.object_dir, staged_oid)

            staged_content = self.read_file(staged_path)
            current_content = self.read_file(file_path)

            # with open(file_path, "r") as current_file:
            #     current_content = current_file.read()

            diff = unified_diff(
                staged_content.splitlines(),
                current_content.splitlines(),
                fromfile="Staged",
                tofile="Current",
                lineterm="",
            )
            diff_output = "\n".join(diff)
            if diff_output:
                print(diff_output)
            else:
                print(f"No differences between '{file_path}' and its staged version.")

        except FileNotFoundError:
            print(f"Error: '{file_path}' or its staged version does not exist.")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode the index file. It may be corrupted.")
        except Exception as e:
            print(f"An error occurred while generating the diff: {e}")

    def merge_files(base_path, commit1_file_path, commit2_file_path):
        """
        If there are conflicts, it marks them in the output file.
        Parameters:
            base_path (str): Path to the base file.
            branch1_path (str): Path to the first branch's file.
            branch2_path (str): Path to the second branch's file.
            output_path (str): Path to write the merged output.
        """

        # Read files
        base = self.read_file(base_path)
        commit1_file = self.read_file(commit1_file_path)
        commit2_file = self.read_file(commit2_file_path)

        # Create a Differ object for comparison
        differ = difflib.Differ()

        # Perform three-way merge
        merged_content = []
        conflict = False

        diff1 = list(differ.compare(base, commit1_file))
        diff2 = list(differ.compare(base, commit2_file))

        comment_character = self._get_comment_character(base_path)

        for line1, line2 in zip(diff1, diff2):
            if line1.startswith("  ") and line2.startswith("  "):
                # No changes in either branch
                merged_content.append(line1[2:])
            elif line1.startswith("- ") and line2.startswith("- "):
                # Deletion in both branches
                continue
            elif line1.startswith("+ ") and line2.startswith("+ "):
                if line1 == line2:
                    # Same addition in both branches
                    merged_content.append(line1[2:])
                else:
                    # Conflict: Different additions in both branches
                    conflict = True
                    merged_content.append(
                        self._get_comment_character(base_path, "Choice1") + "\n"
                    )
                    merged_content.append(line1[2:])
                    merged_content.append(
                        self._get_comment_character(base_path, "=======") + "\n"
                    )
                    merged_content.append(line2[2:])
                    merged_content.append(
                        self._get_comment_character(base_path, "Choice2") + "\n"
                    )
            elif line1.startswith("+ "):
                # Addition in branch1 only
                merged_content.append(line1[2:])
            elif line2.startswith("+ "):
                # Addition in branch2 only
                merged_content.append(line2[2:])

        # Write the merged content to the output file
        self.write_file(base_path, merged_content)

    def merge_commits(self, commit1: str, commit2: str):
        def read_json(self, path_name: str):
            with open(path_name, "r") as file:
                return json.load(file)

        commit1_content = read_json(os.path.join(self.object_dir, commit1))
        commit2_content = read_json(os.path.join(self.object_dir, commit2))

        commit1_files = read_json(
            os.path.join(self.object_dir, commit1_content["tree"])
        )
        commit2_files = read_json(
            os.path.join(self.object_dir, commit2_content["tree"])
        )

        all_files = set(commit1_files.keys() + commit2_files.keys())

        for file in all_files:
            self.merge_files(
                file,
                os.path.join(self.object_dir, commit1_files[file]),
                os.path.join(self.object_dir, commit2_files[file]),
            )

    def merge(self, branch: str):
        current_branch = self.get_current_branch()
        divergent_commit = self._get_diverge_commit(current_branch, branch)
        list_of_commits = self._get_list_commits(branch, divergent_commit)
        list_of_commits = list(reversed(list_of_commits))

        for commit1, commit2 in zip(list_of_commits, list_of_commits[1:]):
            self.merge_commits(commit1, commit2)
        current_branch = self.get_current_commit()
        self.merge_commits(current_branch, list_of_commits[-1])

    def stash(self):
        current_commit = self.get_current_commit()

        commit_content = read_json(os.path.join(self.object_dir, current_commit))
        commit_files = read_json(os.path.join(self.object_dir, commit_content["tree"]))

        for commit_file, commit_file_oid in commit_files:
            commit_file_content = self.read_file(
                os.path.join(self.object_dir, commit_file_oid)
            )
            self.write_file(commit_file, commit_file_content)

    def push(self, branch=None) -> None:
        # TODO

        if self.remote_url is None:
            print("Remote url is not set")
            return
        try:
            if branch is None:
                branch = self.get_current_branch()
            # TODO
        except Exception as e:
            raise RuntimeError(f"An error occurred while Pushing: {e}")
