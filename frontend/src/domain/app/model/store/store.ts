import { defineStore } from 'pinia';
import { getCurrentTheme } from '~/shared/theme/theme';
import type { THEME } from '~/shared/theme/types';

interface IAppProviderStore {
    title: string;
    theme: THEME;
    menuSel: [number, number];
}

export function initAppProviderStoreValues() {
    const config: IAppProviderStore = {
        title: 'speechRecovery',
        theme: getCurrentTheme(),
        menuSel: [0, 0],
    };

    return config;
}

export const useAppProviderStore = defineStore('appProviderStore', {
    state: initAppProviderStoreValues,
    actions: {
        setTheme(theme: THEME) {
            this.theme = theme;
        },
        setMenuSel(val: [number, number]) {
            this.menuSel = val;
        },
    },
});
