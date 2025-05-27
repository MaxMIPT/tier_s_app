export const lockScroll = () => {
    const scrollElement = document.scrollingElement || document.documentElement;
    fixWidthForScrollLock();
    scrollElement.classList.add('lock_scroll');
};

export const isLockedScroll = () => {
    const scrollElement = document.scrollingElement || document.documentElement;
    return scrollElement.classList.contains('lock_scroll');
};

export const fixWidthForScrollLock = () => {
    const scrollElement = document.scrollingElement || document.documentElement;
    const scrollbarWidth = window.innerWidth - scrollElement.clientWidth;
    document.querySelectorAll<HTMLElement>('.fix_width_on_lock_scroll').forEach((item) => {
        if (item.getAttribute('data-width-fixed')) return;
        item.style.maxWidth = `calc(100vw - ${scrollbarWidth}px)`;
        item.setAttribute('data-width-fixed', '1');
    });
};

export const unlockScroll = () => {
    return new Promise<void>((resolve) => {
        const scrollElement = document.scrollingElement || document.documentElement;
        scrollElement.classList.remove('lock_scroll');
        setTimeout(() => {
            document.querySelectorAll<HTMLElement>('.fix_width_on_lock_scroll').forEach((item) => {
                item.style.maxWidth = '';
                item.removeAttribute('data-width-fixed');
            });
            resolve();
        }, 100);
    });
};
