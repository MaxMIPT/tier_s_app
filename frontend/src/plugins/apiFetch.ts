export default defineNuxtPlugin((nuxtApp) => {
    const apiFetch = $fetch.create({
        baseURL: nuxtApp.$config.public.apiBase,
    });

    return {
        provide: {
            apiFetch,
        },
    };
});
