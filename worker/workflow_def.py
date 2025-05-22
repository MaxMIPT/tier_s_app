from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError

from activities.Convert.convert import _1_run_convertation
from activities.Model1.model1 import _2_convert_to_text
from activities.Model2.model2 import _3_make_text_better
from activities.Model3.model3 import _4_convert_to_voice

RUN_WORKFLOW_TASK_QUEUE_NAME = "WORKFLOW_TASK_QUEUE"

@workflow.defn
class Workflow:

    @workflow.run
    async def run(self, voice_path: str) -> str:
        retry_policy = RetryPolicy(
            maximum_attempts=3,
            maximum_interval=timedelta(seconds=2),
        )

        from_1_path = await workflow.execute_activity_method(
            _1_run_convertation,
            file_url = voice_path,
            retry_policy=retry_policy,
        )

        from_2_path = await workflow.execute_activity_method(
            _2_convert_to_text,
            from_1_path = from_1_path,
            retry_policy=retry_policy,
        )

        from_3_path = await workflow.execute_activity_method(
            _3_make_text_better,
            from_2_path = from_2_path,
            retry_policy=retry_policy,
        )

        from_4_path = await workflow.execute_activity_method(
            _4_convert_to_voice,
            from_3_path = from_3_path,
            retry_policy=retry_policy,
        )

        return from_4_path