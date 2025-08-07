from setuptools import setup, find_packages

setup(
    name="adventure-learning-quest",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A desktop application for interactive learning through adventure-themed quizzes.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/adventure-learning-quest",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "customtkinter",
        "ollama",
        "requests",
        "pygame",
        "playsound"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)