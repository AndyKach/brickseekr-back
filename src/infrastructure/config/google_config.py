import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
load_dotenv()

# Замените 'YOUR_API_KEY' и 'YOUR_SEARCH_ENGINE_ID' на ваши данные
api_key = os.getenv("GOOGLE_CLOUD_API")
search_engine_id = os.getenv("GOOGLE_CLOUD_ENGINE_CODE")

service = build("customsearch", "v1", developerKey=api_key)
response = service.cse().list(q="75375", cx=search_engine_id,fields="items(pagemap)").execute()
print(response)

"AIzaSyCnDFoU7M9r4k4OPEIccuz16QIXmQDPEq0"
"6408d6a8b72474329"

"""
<script async src="https://cse.google.com/cse.js?cx=">
</script>
<div class="gcse-search"></div>
"""