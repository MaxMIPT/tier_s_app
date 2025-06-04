import { tryToThrowApiErrors } from '~/shared/errors/errors';

export const deleteWorkflow = async (id: string) => {
    try {
        await useNuxtApp().$apiFetch(`/process/${id}`, {
            method: 'DELETE',
        });
    } catch (e: unknown) {
        throw tryToThrowApiErrors(e);
    }
};
