def pagination_to_skip(pagination):
    return (pagination["page"] - 1) * pagination["per_page"]