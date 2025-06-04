import { StandartErrorList } from '~/shared/errors/errors';
import { fetchWorkflows } from '../api/fetchWorkflows';
import { useTaskStore } from '../model/store/task';

export const loadWorkflows = async () => {
    const taskStore = useTaskStore();

    try {
        const data = await fetchWorkflows();

        data.forEach((item) => {
            taskStore.add(item);
        });
    } catch (e) {
        if (e instanceof StandartErrorList) {
            console.log(e);
        } else {
            console.log(e);
        }
    }
};
