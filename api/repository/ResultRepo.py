from typing import List, Optional
from uuid import UUID

from sqlalchemy import and_, delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from db_models.result import Result
from schemas import ResultModel, UpdateResultModel


class ResultRepository:

    async def get(
        self,
        db: AsyncSession,
        client_id: str,
        workflow_id: Optional[str] = None,
    ) -> List[ResultModel]:
        query = (
            select(
                Result.client_id,
                Result.workflow_id,
                Result.status,
                Result.original_file,
                Result.converted_file,
                Result.restored_text,
                Result.voiced_text,
            )
            .select_from(Result)
            .where(
                and_(
                    Result.client_id == client_id,
                    (
                        Result.workflow_id == workflow_id
                        if workflow_id
                        else 1 == 1
                    ),
                )
            )
        )
        try:
            result = await db.execute(query)
            return [
                ResultModel.model_validate(arg) for arg in result.fetchall()
            ]
        except SQLAlchemyError as e:
            await db.rollback()
            raise SQLAlchemyError(str(e))
        except Exception as e:
            await db.rollback()
            raise Exception(str(e))

    async def insert(
        self, db: AsyncSession, resultSchema: ResultModel
    ) -> ResultModel | None:
        try:
            obj = Result(
                workflow_id=resultSchema.workflow_id,
                client_id=resultSchema.client_id,
                original_file=resultSchema.original_file,
                converted_file=resultSchema.converted_file,
                restored_text=resultSchema.restored_text,
                voiced_text=resultSchema.voiced_text,
                status=resultSchema.status,
            )
            db.add(obj)
            await db.commit()
            await db.refresh(obj)
            return ResultModel.model_validate(obj)
        except SQLAlchemyError as e:
            await db.rollback()
            raise SQLAlchemyError(str(e))
        except Exception as e:
            await db.rollback()
            raise Exception(str(e))

    async def update(
        self, db: AsyncSession, schema: UpdateResultModel
    ) -> None:
        try:
            update_values = {
                key: value
                for key, value in schema.model_dump().items()
                if value
            }
            await db.execute(
                update(Result)
                .where(Result.workflow_id == schema.workflow_id)
                .values(**update_values)
            )
            await db.commit()
            return
        except SQLAlchemyError as e:
            await db.rollback()
            raise SQLAlchemyError(str(e))
        except Exception as e:
            await db.rollback()
            raise Exception(str(e))

    async def delete(
        self, db: AsyncSession, workflow_id: UUID
    ) -> None:
        try:
            await db.execute(
                delete(Result)
                .where(Result.workflow_id == workflow_id)
            )
            await db.commit()
            return
        except SQLAlchemyError as e:
            await db.rollback()
            raise SQLAlchemyError(str(e))
        except Exception as e:
            await db.rollback()
            raise Exception(str(e))

