import { useTaskStore } from '../model/store/task';
import type { IWorkflowTask } from '../model/types/workflow_event';

export const handleTaskEventMessage = (taskEvent: IWorkflowTask) => {
    const taskStore = useTaskStore();

    taskStore.update(taskEvent.workflow.workflow_id, taskEvent.workflow);
};
