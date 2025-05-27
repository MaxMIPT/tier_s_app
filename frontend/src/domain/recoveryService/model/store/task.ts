import { defineStore } from 'pinia';
import type { ITask } from '../types/task';
import { v4 as uuidv4 } from 'uuid';

const CLIENT_ID_LOCAL_STORAGE_KEY = 'task_client_id';

export const useTaskStore = defineStore('task_list', {
    state: () => ({
        clientID: '',
        items: [] as ITask[],
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
            return this.items.find((i) => i.id === id);
        },
        add(task: ITask) {
            if (!this.getTaskByID(task.id)) {
                this.items.push(task);
                return true;
            }
            return false;
        },
        update(id: string, task: Partial<ITask>) {
            const index = this.items.findIndex((i) => i.id === id);
            if (index !== -1) {
                this.items[index] = { ...this.items[index], ...task };
                return true;
            }
            return false;
        },
        remove(id: string) {
            this.items = this.items.filter((i) => i.id !== id);
        },
    },
});
