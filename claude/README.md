# Pydocs Generator - Claude Haiku

Pydocs Generator is a Python tool that uses Anthropic's Claude 3 Haiku model to generate package documentation from PyPI. It allows you to easily fetch documentation for Python packages and generate prompts for AI-assisted coding tasks.

## Features

- Fetch and generate documentation for any Python package available on PyPI
- Generate AI-ready prompts for coding tasks using specific packages
- Cache generated documentation for faster subsequent access

## Requirements

- Python 3.6+
- Anthropic API key

## Installation

1. Clone this repository:
```python
git clone https://github.com/yourusername/pydocs-generator.git
cd pydocs-generator
```
2. Install the required dependencies:
```python
pip install -r requirements.txt
```
3. Set up your Anthropic API key:
- Create a `.env` file in the project root
- Add your API key: `ANTHROPIC_API_KEY=your_api_key_here`

## Usage

### As a module

```python
from pydocs import get_package_docs, prompt_generator

# Fetch documentation for a package
docs = get_package_docs("requests")

# Generate a prompt for a coding task
prompt = prompt_generator("requests", "Setup a universal API client")
```

### For testing
Uncomment the testprint or testsubmit function calls at the bottom of the script to see it in action:
```python
# Print the generated prompt
testprint("anthropic", "Setup a Claude chat client.")

# Submit the prompt to Claude 3 Haiku and get a response
testsubmit("requests", "Setup a universal API client.")
```
### Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
### License
MIT License Copyright (c) 2024 AEOTools
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
