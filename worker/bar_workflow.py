from datetime import timedelta

from temporalio import workflow

from foo_activity import worker_task

@workflow.defn
class TestWorkflow:

    @workflow.run
    async def run(
        self,
        # file_name: str
    ):
        return await workflow.execute_activity(
            activity=worker_task,
            start_to_close_timeout=timedelta(seconds=60)
        )
