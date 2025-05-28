from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from api.repository.ResultRepo import ResultRepo
from api.repository.TaskRepo import TaskRepo
from schemas import ResultModel, UpdateResultModel, TaskModel

class DBService:

    async def resultInsert(self,
            db: AsyncSession,
            resultModelSchema: ResultModel) -> None:
        
        await ResultRepo.insert(db, resultModelSchema)

# -------------------------------------------------------

    async def resultUpdate(self,
            db: AsyncSession,
            updateResultModelSchema: UpdateResultModel
            ) -> None:
        
        await ResultRepo.update(db, updateResultModelSchema)

# -------------------------------------------------------

    async def taskInsert(self,
                        db: AsyncSession, 
                        taskModelSchema: TaskModel) -> None:
        
        await TaskRepo.insert(db, taskModelSchema)

    async def taskGet(self,
                    db: AsyncSession,
                    start_id : int ) -> None:
        
        await TaskRepo.get(db, start_id)

# -------------------------------------------------------

dbService = DBService()
        
