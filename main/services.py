def wildcard_elastic_query(q, lang):
    query = {
        "query": {
            "query_string": {
                "query": f"*{q}*",
                "fields": [f"district.name_{lang}", f"name_{lang}", f"tags_{lang}", f"extra_{lang}"]
            }
        }
    }
    return query
