def rows_to_list(rows):
    return [[c.text for c in r.find_all("td")] for r in rows.find_all("tr")]

def head_rows_to_list(rows):
    return [[c.text for c in r.find_all("th")] for r in rows.find_all("tr")]

def get_table_head(table):
    return table.find("thead")

def get_table_body(table):
    return table.find("tbody")
