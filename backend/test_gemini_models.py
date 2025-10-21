"""
Test script to list available Gemini models
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

api_key = os.environ.get('GOOGLE_API_KEY')

if not api_key:
    print("❌ GOOGLE_API_KEY not found in .env file")
    exit(1)

print("🔑 API Key found, configuring...")
genai.configure(api_key=api_key)

print("\n📋 Available Models:\n")
print("-" * 60)

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
            print(f"  Description: {model.description}")
            print(f"  Supports: {', '.join(model.supported_generation_methods)}")
            print("-" * 60)
except Exception as e:
    print(f"❌ Error listing models: {e}")
    exit(1)

print("\n🧪 Testing a model...")

# Try to use the first available model
try:
    for model_info in genai.list_models():
        if 'generateContent' in model_info.supported_generation_methods:
            model_name = model_info.name
            print(f"\n✓ Testing model: {model_name}")
            
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Hello, I'm working!' in JSON format: {\"message\": \"...\"}")
            print(f"✓ Response: {response.text}")
            print(f"\n✅ SUCCESS! Use this model name: {model_name}")
            break
except Exception as e:
    print(f"❌ Test failed: {e}")
