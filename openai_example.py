#!/usr/bin/env python3
"""
OpenAI Chat API Example
This script demonstrates how to use the OpenAI API to make chat completions.
"""

import os
import sys
from openai import OpenAI

def main():
    # Get API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    try:
        # Make a simple chat completion request
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello! Can you tell me a fun fact about Python programming?"}
            ],
            max_tokens=150
        )
        
        # Print the response
        print("OpenAI API Response:")
        print("-" * 50)
        print(response.choices[0].message.content)
        print("-" * 50)
        print(f"\nModel used: {response.model}")
        print(f"Tokens used: {response.usage.total_tokens}")
        
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
