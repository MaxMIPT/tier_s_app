import type { IModalStorage } from '~/domain/app';
import { lockScroll, unlockScroll } from '~/shared/helpers/lock_scroll';

export const onAnyModalBeforeOpened = (id: string) => {
    const modalsStorage = useState<IModalStorage[]>('appModalsStorage');

    const scrollElement = (document.scrollingElement || document.documentElement) as HTMLElement;
    const scrollbarWidth = window.innerWidth - scrollElement.clientWidth;

    if (modalsStorage.value.length === 0) {
        lockScroll();

        if (scrollbarWidth > 0) {
            document.documentElement.style.setProperty('--modal-content-margin-right', `${scrollbarWidth}px`);
        }
    }

    if (!modalsStorage.value.find((item) => item.id === id)) {
        modalsStorage.value.push({
            id,
        });
    }
};

export const onAnyModalClosed = (id: string) => {
    const modalsStorage = useState<IModalStorage[]>('appModalsStorage');
    modalsStorage.value = modalsStorage.value.filter((item) => item.id !== id);

    if (modalsStorage.value.length === 0) {
        unlockScroll();
    }
};
