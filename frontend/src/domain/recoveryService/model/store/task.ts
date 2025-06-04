import { defineStore } from 'pinia';
import type { IWorkflow } from '../types/workflow';
import { v4 as uuidv4 } from 'uuid';

const CLIENT_ID_LOCAL_STORAGE_KEY = 'task_client_id';

export const useTaskStore = defineStore('task_list', {
    state: () => ({
        clientID: '',
        items: [] as IWorkflow[],
    }),
    actions: {
        loadClientID() {
            const clientID = localStorage.getItem(CLIENT_ID_LOCAL_STORAGE_KEY);
            if (clientID) {
                this.clientID = clientID;
                return;
            }

            this.clientID = uuidv4();
            localStorage.setItem(CLIENT_ID_LOCAL_STORAGE_KEY, this.clientID);
        },
        getTaskByID(id: string) {
            return this.items.find((i) => i.workflow_id === id);
        },
        add(task: IWorkflow) {
            if (!this.getTaskByID(task.workflow_id)) {
                this.items.push(task);
                return true;
            }
            return false;
        },
        update(id: string, task: Partial<IWorkflow>) {
            const index = this.items.findIndex((i) => i.workflow_id === id);
            if (index !== -1) {
                this.items[index] = { ...this.items[index], ...task };
                return true;
            }
            return false;
        },
        remove(id: string) {
            this.items = this.items.filter((i) => i.workflow_id !== id);
        },
    },
});
