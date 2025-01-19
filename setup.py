from setuptools import setup, find_packages

# Define the required dependencies here
# If you have dependencies, you can specify them under install_requires
# For example, if you are using `argparse` and any other package, list them here.
# `argparse` is part of the Python Standard Library, so it's not strictly needed.
# If you had additional dependencies, you would include them in the list below.

setup(
    name="vit",  # Name of your package
    version="0.1",  # Version of your package
    description="A simple version control system inspired by Git",
    long_description=open("README.md").read(),  # Optional, if you have a README.md
    long_description_content_type="text/markdown",  # Optional, if you're using markdown
    author="Your Name",  # Replace with your name or the project's author
    author_email="your.email@example.com",  # Replace with the author's email
    url="https://github.com/yourusername/vit",  # Replace with your project’s URL
    packages=find_packages(),  # Automatically find and include all sub-packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Update license if needed
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Adjust the Python version requirement if needed
    install_requires=[  # List any third-party dependencies here (e.g., `argparse`, `requests`, etc.)
        # 'argparse',  # 'argparse' is in the Python Standard Library, so you don't need to include it.
    ],
    entry_points={
        "console_scripts": [
            "vit = vit.main:main",  # This will allow users to run vit as a command in terminal
        ],
    },
)
