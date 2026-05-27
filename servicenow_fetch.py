# servicenow fetch data
from playwright.sync_api import sync_playwright
import pandas as pd

tickets = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state="auth.json"
    )

    page = context.new_page()

    url = """
    https://yourcompany.service-now.com/api/now/table/incident
    """
    response = page.goto(url)
    data = response.json()

    for item in data["result"]:
        tickets.append({
            "Number": item["number"],
            "Short Description": item["short_description"],
             "Case State": item["case_state"],
             "Site":item["site"],
             "Register Time":item["register_time"],
            "Close Time": item.get("close_time", "")
        })

    browser.close()

df = pd.DataFrame(tickets)
print(df.head())
