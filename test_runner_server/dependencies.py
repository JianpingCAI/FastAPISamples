from fastapi import HTTPException, Header

async def verify_token(x_token: str = Header(...)):
    if x_token != "expected_token":
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    return x_token
