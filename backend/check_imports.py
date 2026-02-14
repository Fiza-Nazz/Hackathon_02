try:
    import fastapi
    print("fastapi: OK")
except ImportError as e:
    print(f"fastapi: FAIL - {e}")

try:
    import sqlmodel
    print("sqlmodel: OK")
except ImportError as e:
    print(f"sqlmodel: FAIL - {e}")

try:
    import groq
    print("groq: OK")
except ImportError as e:
    print(f"groq: FAIL - {e}")

try:
    import mcp
    print("mcp: OK")
except ImportError as e:
    print(f"mcp: FAIL - {e}")

try:
    import openai
    print("openai: OK")
except ImportError as e:
    print(f"openai: FAIL - {e}")
