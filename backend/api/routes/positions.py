from fastapi import APIRouter, HTTPException
from typing import List
from api.schemas import Position, ClosedPosition

router = APIRouter()

# Mock data
mock_open_positions = []
mock_closed_positions = []

@router.get("/", response_model=List[Position])
async def get_positions():
    """All currently open positions with live P&L"""
    return mock_open_positions

@router.get("/history", response_model=List[ClosedPosition])
async def get_positions_history():
    """All closed positions for today with exit reason"""
    return mock_closed_positions

@router.get("/{id}", response_model=Position)
async def get_position(id: str):
    """Single position detail including full Greeks"""
    for pos in mock_open_positions:
        if pos.position_id == id:
            return pos
    raise HTTPException(status_code=404, detail="Position not found")

@router.post("/{id}/exit")
async def exit_position(id: str):
    """Manually trigger exit for a specific position"""
    return {"success": True, "order_id": f"exit_order_{id}"}
