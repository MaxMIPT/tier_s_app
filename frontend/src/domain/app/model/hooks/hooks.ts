import { saveManualThemeValue, setTheme } from '~/shared/theme/theme';
import { useAppProviderStore } from '../store/store';
import type { THEME } from '~/shared/theme/types';

export function useInitAppProvider() {
    const appProviderStore = useAppProviderStore();

    const appProviderRefs = storeToRefs(appProviderStore);

    watch(appProviderRefs.theme, (theme) => {
        setTheme(theme);
    });

    return appProviderStore;
}

export function useAppProviderConfig() {
    const appProviderStore = useAppProviderStore();

    return readonly(reactive(storeToRefs(appProviderStore)));
}

export function setAppTheme(theme: THEME) {
    const appProviderStore = useAppProviderStore();
    appProviderStore.setTheme(theme);
    saveManualThemeValue(appProviderStore.theme);
}

export function setMenuSel(val: [number, number]) {
    const appProviderStore = useAppProviderStore();
    appProviderStore.setMenuSel(val);
}
