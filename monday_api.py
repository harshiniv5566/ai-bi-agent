import requests
import pandas as pd

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYxOTg0MDMwOCwiYWFpIjoxMSwidWlkIjo5OTcwNTYwMywiaWFkIjoiMjAyNi0wMi0xMVQwNjo0NDowMy40MzRaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MzM3NDgyNjAsInJnbiI6ImFwc2UyIn0.s5bho45Li-X1KMr3tvFsTut69cEWydHngx1SMUeeSmg"
API_URL = "https://api.monday.com/v2"

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json",
}


def fetch_board_items(board_id):
    query = """
    query ($board_id: [ID!]) {
      boards(ids: $board_id) {
        items_page(limit: 100) {
          items {
            name
            column_values {
              text
              column {
                title
              }
            }
          }
        }
      }
    }
    """

    response = requests.post(
        API_URL,
        json={"query": query, "variables": {"board_id": board_id}},
        headers=headers,
    )

    data = response.json()

    # 🔴 ADD SAFETY CHECK (prevents KeyError)
    if "data" not in data or not data["data"]["boards"]:
        raise Exception(f"Monday API Error: {data}")

    items = data["data"]["boards"][0]["items_page"]["items"]

    rows = []
    for item in items:
        row = {"Item Name": item["name"]}
        for col in item["column_values"]:
            row[col["column"]["title"]] = col["text"]
        rows.append(row)

    return pd.DataFrame(rows)
