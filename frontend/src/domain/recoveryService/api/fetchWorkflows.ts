import { tryToThrowApiErrors } from '~/shared/errors/errors';
import { useTaskStore } from '../model/store/task';
import type { IWorkflow, PipelineStatus, TaskStatus } from '../model/types/workflow';

interface ResponseItem {
    workflow_id: string;
    original_file: string | null;
    original_file_name: string;
    status: PipelineStatus;
    converted_file: string | null;
    converted_file_duration: number | null;
    dubbed_file: string | null;
    restored_text: string | null;
    task_status: TaskStatus;

    created_at: string;
}

export async function fetchWorkflows(): Promise<IWorkflow[]> {
    const taskStore = useTaskStore();

    try {
        const items = await useNuxtApp().$apiFetch<ResponseItem[]>(`/workflows/${taskStore.clientID}`, {
            method: 'GET',
        });

        const result: IWorkflow[] = [];
        items.forEach((item) => {
            result.push({
                workflow_id: item.workflow_id,
                original_file: item.original_file,
                original_file_name: item.original_file_name,
                status: item.status,
                converted_file: item.converted_file,
                converted_file_duration: item.converted_file_duration,
                dubbed_file: item.dubbed_file,
                restored_text: item.restored_text,
                task_status: item.task_status,
                created_at: new Date(item.created_at),
            });
        });

        return result;
    } catch (e: unknown) {
        throw tryToThrowApiErrors(e);
    }
}
