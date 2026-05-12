"""AI service."""

from uuid import UUID

import redis.asyncio as aredis

from app.llm.llm import llm_handler


class AIService:
    """AI service."""

    async def ask_ai(
        self,
        collection_id: UUID,
        question: str,
        redis: aredis.Redis,
    ) -> dict:
        """Get AI answer based on the stored data in relevant collection."""
        context, meta = await llm_handler.invoke_llm(
            question=question,
            collection_name=collection_id,
            redis=redis,
        )

        return {
            "context": context,
            "meta": meta,
        }


ai_service = AIService()
