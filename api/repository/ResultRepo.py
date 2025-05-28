from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from db_models.Result import Result
from schemas import ResultModel, UpdateResultMode

class ResultRepository:

# -----------------------------------------------------------------------------------

    async def insert(
            self,
            db: AsyncSession,
            resultSchema: ResultModel
    ) -> None:
        
        obj = Result(
            resultSchema.workflow_id,
            client_id=resultSchema.client_id,
            original_file=resultSchema.original_file,
            converted_file=resultSchema.converted_file,
            restored_text=resultSchema.restored_text,
            voiced_text=resultSchema.voiced_text
        )

        db.add(obj)
        await db.commit()

# ---------------------------------------------------------------

    async def update(self, 
                    db: AsyncSession, 
                    updateResultSchema: UpdateResultMode):
        
        await db.execute(
            update(Result).where(Result.workflow_id == updateResultSchema.workflow_id).values(
                status=updateResultSchema.status,
                converted_file=updateResultSchema.converted_file,
                restored_text=updateResultSchema.restored_text,
                voiced_text=updateResultSchema.voiced_text,
            )
        )

        await db.commit()

# -----------------------------------------------------------------------------------

ResultRepo = ResultRepository()