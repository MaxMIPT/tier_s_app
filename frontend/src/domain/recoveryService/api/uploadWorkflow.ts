import { tryToThrowApiErrors } from '~/shared/errors/errors';
import { useTaskStore } from '../model/store/task';

interface Response {
    workflow_id: string;
}

export async function uploadWorkflow(file: Blob, filename: string) {
    const taskStore = useTaskStore();

    const formdata = new FormData();
    formdata.append('file', file, filename);

    try {
        return await useNuxtApp().$apiFetch<Response>('/process', {
            method: 'POST',
            body: formdata,
            query: { client_id: taskStore.clientID },
        });
    } catch (e: unknown) {
        throw tryToThrowApiErrors(e);
    }
}
