"""Setup script for Clinical Trial Matcher backend."""

from setuptools import setup, find_packages

setup(
    name="clinical-trial-matcher",
    version="0.1.0",
    description="AI-powered platform for matching patients with clinical trials",
    author="TrialMatch AI Team",
    python_requires=">=3.11",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "sqlalchemy>=2.0.25",
        "boto3>=1.34.34",
        "pydantic>=2.5.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "pytest-asyncio>=0.23.3",
            "pytest-cov>=4.1.0",
            "black>=24.1.1",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ],
    },
)
