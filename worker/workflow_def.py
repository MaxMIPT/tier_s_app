from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError

from activities.Convert.convert import task_1_run_convertation
from activities.Model1.model import task_2_convert_to_text
from activities.Model2.model import task_3_make_text_better
from activities.Model3.model import task_4_convert_to_voice

@workflow.defn
class Workflow:

    @workflow.run
    async def run(self, voice_path : str, client_id : str) -> str:
        retry_policy = RetryPolicy(
            maximum_attempts=3,
            maximum_interval=timedelta(seconds=2),
        )

        # конвертация аудио
        from_1_path = await workflow.execute_activity_method(
            task_1_run_convertation,
            file_url = voice_path,
            retry_policy=retry_policy,
        )
        # если ошибка -> отменяем флоу

        # распознавание текста из аудио
        from_2_path = await workflow.execute_activity_method(
            task_2_convert_to_text,
            from_1_path = from_1_path,
            retry_policy=retry_policy,
        )
        # если ошибка -> отменяем флоу

        # озвучка текста
        from_3_path = await workflow.execute_activity_method(
            task_3_make_text_better,
            from_2_path = from_2_path,
            retry_policy=retry_policy,
        )
        # если ошибка -> отменяем флоу

        # если все норм, запускаем ласт флоу, которое запишет в редис task_type=ready и data={text:"", file:"url"}
        from_4_path = await workflow.execute_activity_method(
            task_4_convert_to_voice,
            from_3_path = from_3_path,
            retry_policy=retry_policy,
        )
        # если ошибка -> отменяем флоу

        return from_4_path