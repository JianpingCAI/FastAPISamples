from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/results/{runner_id}/")
async def receive_results(runner_id: int, results: dict):
    print(f"Received results from runner {runner_id}: {results}")
    return {"status": "Results received"}
