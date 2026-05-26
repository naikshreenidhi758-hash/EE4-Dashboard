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
            "Priority": item["priority"],
            "State": item["state"],
            "Assigned To": item.get("assigned_to", "")
        })

    browser.close()

df = pd.DataFrame(tickets)
print(df.head())
