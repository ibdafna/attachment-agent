from setuptools import setup, find_packages

setup(
    name="attachment-agent",
    version="0.1.0",
    description="An automated system that processes Gmail attachments and organizes them into categorized folders in Dropbox",
    author="Devin",
    author_email="devin@example.com",
    packages=find_packages(),
    install_requires=[
        "google-api-python-client>=2.116.0",
        "google-auth-httplib2>=0.2.0",
        "google-auth-oauthlib>=1.2.0",
        "python-magic>=0.4.27",
        "PyPDF2>=3.0.1",
        "Pillow>=10.2.0",
        "python-docx>=1.1.0",
        "python-dotenv>=1.0.1",
        "dropbox>=11.36.2",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
        ],
    },
    python_requires=">=3.12",
)
