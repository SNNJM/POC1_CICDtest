import os
import time
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

endpoint = os.environ["SD_TEXT_ENDPOINT"]
base_endpoint = endpoint.split("/openai/deployments/")[0]
client = AzureOpenAI(azure_endpoint=base_endpoint, api_key=os.environ["SD_TEXT_API_KEY"], api_version=os.getenv("SD_TEXT_API_VERSION", "2024-12-01-preview"), timeout=float(os.getenv("SD_TEXT_TIMEOUT_SECONDS", "60")), max_retries=int(os.getenv("SD_TEXT_MAX_RETRIES", "3")))
print("Starting Smart Detailing W3 POC...", flush=True)
start = time.perf_counter()
try:
    response = client.chat.completions.create(model=os.environ["SD_TEXT_MODEL"], messages=[{"role": "system", "content": "Generate a short transition using only supplied approved sample content. Do not introduce additional claims."}, {"role": "user", "content": "Market: Italy. Synthetic test only. Module 1: Product introduction. Module 2: Approved usage information. Generate one short transition."}], max_completion_tokens=150)
    print("STATUS: SUCCESS", flush=True)
    print(f"Latency: {time.perf_counter() - start:.2f}s", flush=True)
    print("Response:", response.choices[0].message.content, flush=True)
except Exception as error:
    print(f"STATUS: FAILED - {type(error).__name__}: {error}", flush=True)
    raise
