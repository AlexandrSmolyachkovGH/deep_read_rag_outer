"""Collection router."""

from typing import Annotated
from uuid import UUID

import redis.asyncio as aredis
from fastapi import (
    APIRouter,
    Body,
    Depends,
    Path,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.connections.pg import get_session
from app.connections.redis import get_redis
from app.schemes.collections import (
    AskAIResp,
    CollResp,
    CreateCollReq,
)
from app.services.ai import ai_service
from app.services.collections import coll_service

router = APIRouter(
    prefix="/collections",
    tags=["collections"],
)


@router.post(
    path="/",
    response_model=CollResp,
    status_code=status.HTTP_201_CREATED,
    description="Create new collection.",
)
async def create_collection(
    create_data: Annotated[CreateCollReq, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CollResp:
    """Create new collection."""
    collection = await coll_service.create_collection(
        create_data=create_data,
        session=session,
    )

    return CollResp.model_validate(collection)


@router.get(
    path="/{collection_id}",
    response_model=CollResp,
    status_code=status.HTTP_200_OK,
    description="Get collection.",
)
async def get_collection(
    collection_id: Annotated[UUID, Path(...)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CollResp:
    """Get collection by collection_id."""
    collection = await coll_service.get_collection(
        collection_id=collection_id,
        session=session,
    )

    return CollResp.model_validate(collection)


@router.get(
    path="/",
    response_model=list[CollResp],
    status_code=status.HTTP_200_OK,
    description="Get collections.",
)
async def get_collections(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[CollResp]:
    """Get collections."""
    collections = await coll_service.get_collections(
        session=session,
    )

    return [CollResp.model_validate(coll) for coll in collections]


@router.post(
    path="/{collection_id}/ask-ai",
    response_model=AskAIResp,
    status_code=status.HTTP_201_CREATED,
    description="Ask AI anything.",
)
async def ask_ai(
    collection_id: Annotated[UUID, Path(...)],
    question: Annotated[str, Body(...)],
    redis: Annotated[aredis.Redis, Depends(get_redis)],
) -> AskAIResp:
    """Ask AI anything. Get an answer based on the stored data in the collected."""
    ai_response = await ai_service.ask_ai(
        collection_id=collection_id,
        question=question,
        redis=redis,
    )

    return AskAIResp.model_validate(ai_response)
