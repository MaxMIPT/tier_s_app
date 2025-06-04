import { StandartErrorList } from '~/shared/errors/errors';
import { deleteWorkflow } from '../api/deleteWorkflow';
import { useTaskStore } from '../model/store/task';

export const removeWorkflow = async (id: string) => {
    try {
        await deleteWorkflow(id);
        const taskStore = useTaskStore();
        taskStore.remove(id);
    } catch (e) {
        if (e instanceof StandartErrorList) {
            console.log(e);
        } else {
            console.log(e);
        }
    }
};
