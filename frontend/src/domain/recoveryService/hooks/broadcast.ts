import { useTaskStore } from '../model/store/task';
import type { PipelineStatus, TaskStatus } from '../model/types/workflow';
import type { IWorkflowTask } from '../model/types/workflow_event';
import { handleTaskEventMessage } from './handleTaskEventMessage';

interface ClientMessageWorkflowData {
    task_log_id: number;
    workflow: {
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
    };
    created_at: string;
}

interface ClientMessageWorkflow {
    type: 'workflow';
    data: ClientMessageWorkflowData;
}

interface ServerMessagePing {
    type: 'ping';
}

type ServerMessage = ClientMessageWorkflow | ServerMessagePing;

export const startBroadcast = (): WebSocket => {
    const taskStore = useTaskStore();

    const nuxtApp = useNuxtApp();

    const host = nuxtApp.$config.public.apiWs ? nuxtApp.$config.public.apiWs : window.location.host;
    const socketUrl = `${nuxtApp.$config.public.apiWsProtocol}://${host}/ws/${taskStore.clientID}`;

    const ws = new WebSocket(socketUrl);

    ws.addEventListener('message', (event: MessageEvent) => {
        try {
            const data: ServerMessage = JSON.parse(event.data);

            if (data.type === 'workflow') {
                const taskEvent: IWorkflowTask = {
                    task_log_id: data.data.task_log_id,
                    workflow: {
                        workflow_id: data.data.workflow.workflow_id,
                        original_file: data.data.workflow.original_file,
                        original_file_name: data.data.workflow.original_file_name,
                        status: data.data.workflow.status,
                        converted_file: data.data.workflow.converted_file,
                        converted_file_duration: data.data.workflow.converted_file_duration,
                        dubbed_file: data.data.workflow.dubbed_file,
                        restored_text: data.data.workflow.restored_text,
                        task_status: data.data.workflow.task_status,
                        created_at: new Date(data.data.workflow.created_at),
                    },
                    created_at: new Date(data.data.created_at),
                };

                handleTaskEventMessage(taskEvent);
            }
        } catch (e) {
            console.error('Не удалось распарсить сообщение:', event.data, e);
        }
    });

    return ws;
};

export const stopBroadcast = (ws: WebSocket) => {
    ws.close(1000);
};
