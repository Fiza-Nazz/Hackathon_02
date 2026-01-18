from setuptools import setup, find_packages

setup(
    name="todo-app",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'todo-app=src.cli.todo_app:main',
        ],
    },
    install_requires=[
        # No external dependencies for basic functionality
    ],
    author="AI Developer",
    description="AI-Native Todo Application",
    python_requires='>=3.11',
)