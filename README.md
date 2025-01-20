
# VIT - Version Information Tracker

VIT (Version Information Tracker) is a simple command-line version control system inspired by Git. It allows users to initialize repositories, add files to staging, commit changes, manage branches, and view diffs, all through a terminal interface.

---

## Features

- **Clone a repository** (`vit clone`)
- **Initialize a new repository** (`vit init`)
- **Add files to the staging area** (`vit add`)
- **Commit changes** with a message (`vit commit`)
- **Checkout branches** (`vit checkout`)
- **List available branches** (`vit branch`)
- **List available branches** (`vit merge`)
- **Show differences** between file versions (`vit diff`)

---

## Installation

To install VIT, you can clone the repository and install it using `pip`.

### Step 1: Clone the repository

```bash
git clone https://github.com/imaditya123/VIT.git
cd VIT
```

### Step 2: Install the package in editable mode

```bash
pip install -e .
```

This will install VIT and make it available as a command-line tool.

---

## Usage

Once VIT is installed, you can run it from the terminal by typing `vit` followed by one of the available commands. Below is the general syntax for using the tool:

### `vit init`

Initializes a new version control repository.

```bash
vit init
```

### `vit add <file1> <file2> ...`

Adds files to the staging area.

```bash
vit add file1.txt file2.py
```

### `vit commit -m "Your commit message"`

Commits the staged changes with a message.

```bash
vit commit -m "Initial commit"
```

### `vit checkout <branch_name> [-b]`

Checks out an existing branch or creates a new branch if the `-b` option is used.

```bash
vit checkout new_feature_branch
```

Create and check out a new branch:

```bash
vit checkout -b new_feature_branch
```

### `vit branch`

Lists all the available branches in the repository.

```bash
vit branch
```

### `vit diff <file1> <file2> ...`

Shows the differences between the working directory and the staged files for the given files.

```bash
vit diff file1.txt file2.py
```

---

## Contributing

If you'd like to contribute to VIT, please fork the repository and submit a pull request. All contributions are welcome!

---

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/imaditya123/CommitHub?tab=Apache-2.0-1-ov-file#) file for details.

---

