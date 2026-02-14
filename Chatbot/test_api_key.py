import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load environment
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")
print(f"API Key loaded: {bool(api_key)}")

if api_key:
    print(f"Key length: {len(api_key)}")
    print(f"Key preview: {api_key[:15]}...")

    # Test the API key by creating a client and making a simple request
    try:
        client = AsyncOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key,
        )

        # Make a simple API call to test the key
        async def test_key():
            try:
                models = await client.models.list()
                print("✅ API Key is VALID!")
                print(f"Available models: {len(models.data)}")
                for model in models.data[:3]:  # Show first 3 models
                    print(f"  - {model.id}")
                return True
            except Exception as e:
                print(f"❌ API Key test failed: {e}")
                return False

        is_valid = asyncio.run(test_key())

        if is_valid:
            print("\n🎉 GROQ API KEY IS WORKING CORRECTLY!")
        else:
            print(f"\n❌ GROQ API KEY IS INVALID: {api_key}")

    except Exception as e:
        print(f"❌ Client creation failed: {e}")
else:
    print("❌ No API key found!")