from setuptools import setup, find_packages

setup(
    name="devops-platform-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langgraph>=0.1.0",
        "pydantic>=2.5.0",
        "structlog>=24.0.0",
        "python-dotenv>=1.0.0",
        "pytest>=7.0.0",
        "pytest-asyncio>=0.21.0",
        "httpx>=0.25.0",
        "openai>=1.0.0",
        "ollama>=0.1.0",
        "jinja2>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "devops-agent=devops_platform_agent.main:main",
        ],
    },
    python_requires=">=3.12",
)