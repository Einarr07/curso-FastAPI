def user_schemas(user) -> dict:
    return {"id": str(user["_id"]),
            "user_name": user["user_name"],
            "email": user["email"]
            }