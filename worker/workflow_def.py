from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError
from activities.convertion_act import task_1_run_convertation
from activities.database_act import add_new_line_to_db
@workflow.defn
class Workflow:

    @workflow.run
    async def run(self, file_url : str, client_id : str) -> str:

        # конвертация аудио
        try:
            file_url = await workflow.execute_activity_method(
                task_1_run_convertation,
            )
            status = True
            # записать в базу результат
        except ActivityError as e:
            # записать в базу результат
            status = False
            raise e

        try:
            await workflow.execute_acitivity_method(
                add_new_line_to_db
            )




        """
        # распознавание текста из аудио
        from_2_path = await workflow.execute_activity_method(
            task_2_convert_to_text,
            from_1_path = from_1_path,
            retry_policy=retry_policy,
        )
        # если ошибка -> отменяем флоу (запускаем активити которое пишет в редис что пайплайн (воркфлоу) сломался)

        # озвучка текста
        from_3_path = await workflow.execute_activity_method(
            task_3_make_text_better,
            from_2_path = from_2_path,
            retry_policy=retry_policy,
        )
        # если ошибка ->  отменяем флоу (запускаем активити которое пишет в редис что пайплайн (воркфлоу) сломался)

        # если все норм, запускаем ласт флоу, которое запишет в редис task_type=ready и data={text:"", file:"url"}
        from_4_path = await workflow.execute_activity_method(
            task_4_convert_to_voice,
            from_3_path = from_3_path,
            retry_policy=retry_policy,
        )
        # если ошибка ->  отменяем флоу (запускаем активити которое пишет в редис что пайплайн (воркфлоу) сломался)
        """

        return from_4_path