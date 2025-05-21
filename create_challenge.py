#!/usr/bin/env python3
"""
Create template files for new challenges.

This script helps create new Python, SQL, or data modeling challenge files 
with the proper structure.
"""

import os
import sys
import argparse
from datetime import datetime

# Templates
PYTHON_TEMPLATE = '''"""
Question: {description}

{details}
"""

def {function_name}({args}):
    """
    {docstring}
    
    Args:
        {arg_descriptions}
        
    Returns:
        {return_description}
    """
    # TODO: Implement your solution here
    {return_placeholder}

# Test cases
def test_{function_name}():
    # TODO: Add test cases
    print("All test cases passed!")

if __name__ == "__main__":
    test_{function_name}()
'''

SQL_TEMPLATE = '''/*
Question: {description}

{details}

Schema:
{schema}

Expected Output:
{expected_output}
*/

-- Write your SQL query here:
{sql_placeholder}

/*
Explanation:

{explanation}
*/'''

MERMAID_TEMPLATE = '''erDiagram
    {entities}

    {relationships}

    {entity_attributes}
'''

def create_python_challenge(challenge_number, description, details, function_name, args, 
                          arg_descriptions, return_description, return_placeholder):
    """Create a Python challenge file."""
    file_path = f"src/python/q{challenge_number:03d}_{function_name}.py"
    
    # Check if file already exists
    if os.path.exists(file_path):
        print(f"Error: File {file_path} already exists.")
        return False
    
    # Create content
    content = PYTHON_TEMPLATE.format(
        description=description,
        details=details,
        function_name=function_name,
        args=args,
        docstring=description,
        arg_descriptions=arg_descriptions,
        return_description=return_description,
        return_placeholder=return_placeholder
    )
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Write file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Created Python challenge file: {file_path}")
    return True

def create_sql_challenge(challenge_number, description, details, schema, expected_output, 
                        sql_placeholder="-- TODO: Write your SQL query here", explanation="TODO: Explain your approach"):
    """Create a SQL challenge file."""
    # Use description to create a file name
    file_name = f"q{challenge_number:03d}_" + "_".join(description.lower().split()[:3])
    file_path = f"src/sql/{file_name}.sql"
    
    # Check if file already exists
    if os.path.exists(file_path):
        print(f"Error: File {file_path} already exists.")
        return False
    
    # Create content
    content = SQL_TEMPLATE.format(
        description=description,
        details=details,
        schema=schema,
        expected_output=expected_output,
        sql_placeholder=sql_placeholder,
        explanation=explanation
    )
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Write file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Created SQL challenge file: {file_path}")
    return True

def create_data_model_challenge(challenge_number, model_name, entities="", relationships="", entity_attributes=""):
    """Create a data model challenge file using Mermaid syntax."""
    file_path = f"src/data_models/q{challenge_number:03d}_{model_name}.mmd"
    
    # Check if file already exists
    if os.path.exists(file_path):
        print(f"Error: File {file_path} already exists.")
        return False
    
    # Create content
    content = MERMAID_TEMPLATE.format(
        entities=entities,
        relationships=relationships,
        entity_attributes=entity_attributes
    )
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Write file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Created data model challenge file: {file_path}")
    return True

def main():
    parser = argparse.ArgumentParser(description='Create template files for new challenges.')
    parser.add_argument('type', choices=['python', 'sql', 'datamodel'], 
                        help='Type of challenge to create')
    parser.add_argument('number', type=int, help='Challenge number')
    
    # Common arguments
    parser.add_argument('--description', '-d', help='Brief description of the challenge')
    
    # Python-specific arguments
    parser.add_argument('--function', '-f', help='Function name for Python challenge')
    parser.add_argument('--args', '-a', help='Function arguments for Python challenge')
    
    # SQL-specific arguments
    parser.add_argument('--schema', '-s', help='Schema description for SQL challenge')
    
    # Data model-specific arguments
    parser.add_argument('--model-name', '-m', help='Model name for data model challenge')
    
    args = parser.parse_args()
    
    # Handle different challenge types
    if args.type == 'python':
        if not args.function:
            args.function = input("Enter function name: ")
        if not args.args:
            args.args = input("Enter function arguments: ")
        if not args.description:
            args.description = input("Enter brief description: ")
        
        details = input("Enter detailed problem statement (blank line to finish):\n")
        lines = []
        line = input()
        while line:
            lines.append(line)
            line = input()
        if lines:
            details = details + "\n" + "\n".join(lines)
        
        arg_descriptions = input("Enter argument descriptions: ")
        return_description = input("Enter return value description: ")
        return_placeholder = input("Enter return placeholder (e.g., 'return []'): ")
        
        create_python_challenge(
            args.number, args.description, details, args.function, args.args,
            arg_descriptions, return_description, return_placeholder
        )
    
    elif args.type == 'sql':
        if not args.description:
            args.description = input("Enter brief description: ")
        if not args.schema:
            args.schema = input("Enter schema description: ")
        
        details = input("Enter detailed problem statement (blank line to finish):\n")
        lines = []
        line = input()
        while line:
            lines.append(line)
            line = input()
        if lines:
            details = details + "\n" + "\n".join(lines)
        
        expected_output = input("Enter expected output description: ")
        
        create_sql_challenge(
            args.number, args.description, details, args.schema, expected_output
        )
    
    elif args.type == 'datamodel':
        if not args.model_name:
            args.model_name = input("Enter model name: ")
        
        entities = input("Enter entities (blank line to finish):\n")
        lines = []
        line = input()
        while line:
            lines.append(line)
            line = input()
        if lines:
            entities = entities + "\n" + "\n".join(lines)
        
        relationships = input("Enter relationships (blank line to finish):\n")
        lines = []
        line = input()
        while line:
            lines.append(line)
            line = input()
        if lines:
            relationships = relationships + "\n" + "\n".join(lines)
        
        entity_attributes = input("Enter entity attributes (blank line to finish):\n")
        lines = []
        line = input()
        while line:
            lines.append(line)
            line = input()
        if lines:
            entity_attributes = entity_attributes + "\n" + "\n".join(lines)
        
        create_data_model_challenge(
            args.number, args.model_name, entities, relationships, entity_attributes
        )

if __name__ == '__main__':
    main() 