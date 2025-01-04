async def pagination_params(page: int = 1, per_page: int = 5):
    return {"page": page, "per_page": per_page}