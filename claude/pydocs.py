# Pydocs Generator - Uses Anthropic's Claude 3 Haiku to generate package documentation from PyPi. Requires ANTHROPIC_API_KEY in env or .env

# Usage: from pydocs import get_package_docs # to just fetch docs
# Usage: from pydocs import prompt_generator # to generate a prompt with docs

import os
import re
import json
import requests
from dotenv import load_dotenv
from anthropic import Anthropic

def prompt_generator(package_name, task_description):
    docs = get_package_docs(package_name)
    
    if isinstance(docs, str):  # This means an error occurred
        return docs

    prompt = f"""
    The assistant needs to write code that uses the '{package_name}' package. Before beginning, review the following docs:

    Package Name: {docs['name']}
    Version: {docs['version']}
    Installation: {docs['installation']}
    Description: {docs['description']}
    
    Example Usage:
    {docs['example_usage']}
    
    Key Variables:
    {json.dumps(docs['key_variables'], indent=2)}

    Now, using the documentation effectively, write code for the following:

    Task: {task_description}

    Include any necessary imports and provide comments explaining your code.
    """

    return(prompt)

def get_package_docs(package_name):
    docs_dir = os.path.abspath("package_docs")
    doc_file = os.path.join(docs_dir, f"{package_name}.json")
    
    if not os.path.exists(doc_file):
        print(f"Documentation for {package_name} not found. Generating...")
        success = generate_package_doc(package_name)
        if not success:
            return f"Failed to generate documentation for {package_name}."
    
    with open(doc_file, 'r') as f:
        docs = json.load(f)
    
    return docs

def generate_package_doc(package_name):
    def get_api_key():
        load_dotenv()
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("Anthropic API key not found in environment variables or .env file")
        return api_key

    def get_package_info(package_name):
        url = f"https://pypi.org/project/{package_name}/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            content = response.text
            
            # Extract package name
            name_match = re.search(r'<h1 class="package-header__name">(.*?)</h1>', content, re.DOTALL)
            extracted_name = name_match.group(1).strip() if name_match else package_name
            
            # Extract description
            desc_match = re.search(r'<div class="project-description">(.*?)</div>', content, re.DOTALL)
            if desc_match:
                description = desc_match.group(1)
                description = re.sub(r'<[^>]+>', '', description) # Remove any nested HTML tags
                description = re.sub(r'\s+', ' ', description).strip() # Remove extra whitespace
            else:
                description = "Description not found."
            
            return f"Name: {extracted_name}\n\nDescription: {description}"
        except requests.exceptions.RequestException as e:
            print(f"Error fetching package info: {e}")
            return None

    def get_package_details(client, package_name, page_content):
        prompt = f""" 
            Package Name: {package_name}
            PyPI URL: https://pypi.org/project/{package_name}/

            Here's the content of the PyPI page for this package:

            {page_content}

            Based on the above content from the PyPI page, generate a JSON object describing how to best use this package, including its main 
            variables and requirements. Follow this structure:
            {{
                "name": "package_name",
                "version": "current_version",
                "installation": "pip install package_name",
                "description": "A detailed description of the package",
                "example_usage": "A comprehensive code snippet demonstrating common usage, including multiple features and best practices",
                "key_variables": [
                    {{"name": "variable_name", "description": "Detailed variable description"}},
                    ... (at least 5 key variables, more if applicable)
                ]
            }}
            
            Ensure all information is extracted from the provided PyPI page content, not from prior knowledge.
            """

        try:
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                system="You are a helpful assistant that provides information about Python packages in a structured JSON format. Use only the information provided in the PyPI page content to generate your response.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.content[0].text
            return json.loads(content)
        except Exception as e:
            print(f"Error processing {package_name}: {str(e)}")
            return None

    try:
        api_key = get_api_key()
        client = Anthropic(api_key=api_key)

        page_content = get_package_info(package_name)
        
        if not page_content:
            return False

        detailed_info = get_package_details(client, package_name, page_content)

        if detailed_info:
            output_dir = os.path.abspath("package_docs")
            os.makedirs(output_dir, exist_ok=True)
            file_path = os.path.join(output_dir, f"{package_name}.json")

            with open(file_path, 'w') as f:
                json.dump(detailed_info, f, indent=2)
            
            return True
        else:
            return False
    
    except Exception as e:
        print(f"Error generating documentation for {package_name}: {str(e)}")
        return False

def testprint(package_name, task_description): # Unnecessary in production
    """
    Print the generated prompt for the given package and task.
    """
    prompt = prompt_generator(package_name, task_description)
    print(prompt)

def testsubmit(package_name, task_description):
    load_dotenv()
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in environment variables")
        return
    
    print(f"API key found: {api_key[:5]}...{api_key[-5:]}")
    
    prompt = prompt_generator(package_name, task_description)
    
    try:
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            system="You are a coding assistant that loves package documentation. Return code only.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        content = response.content[0].text
        
        content = re.sub(r'^```python\s*\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'\n```\s*$', '', content, flags=re.MULTILINE | re.DOTALL)
        content = content.strip()

        print(content, end='')

    except Exception as e:
        print(f"Error submitting to Anthropic API: {str(e)}")

# Example usage (print only)
# testprint("anthropic", "Setup a Claude chat client.")

# Example usage (submitted to Claude 3 Haiku)
# testsubmit("colorama", "Create an extensive colorama quick-reference.")
