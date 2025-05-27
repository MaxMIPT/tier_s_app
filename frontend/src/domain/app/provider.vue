<script setup lang="ts">
import { ru } from '@nuxt/ui/locale';
import { getCurrentTheme, setTheme } from '~/shared/theme/theme';
import { useInitAppProvider } from './model/hooks/hooks';
import { nextAnimFrame } from '~/shared/helpers/functions';
import type { IModalStorage } from './model/types/types';
import { unlockScroll } from '~/shared/helpers/lock_scroll';

const appProviderStore = useInitAppProvider();

const appTitle = useState('appTitle', () => appProviderStore.title);

const route = useRoute();

useHead({
    htmlAttrs: {
        lang: 'ru',
        'data-app-theme': () => appProviderStore.theme,
    },
    titleTemplate: (titleChunk) => {
        return titleChunk ? `${titleChunk} - ${toValue(appTitle)}` : toValue(appTitle);
    },
    link: [
        { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/favicon_16.png' },
        { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon_32.png' },
    ],
});

onNuxtReady(() => {
    const clientTheme = getCurrentTheme();
    if (clientTheme != appProviderStore.theme) {
        setTheme(clientTheme);
    }
});

// const colorMode = useColorMode();

// watch(
//     () => appProviderStore.theme,
//     (theme) => {
//         colorMode.preference = theme === 'dark' ? 'dark' : 'light';
//     },
//     {
//         immediate: true,
//     },
// );

if (import.meta.client) {
    const scrollingElement = (document.scrollingElement || document.documentElement) as HTMLElement;

    if (scrollingElement) {
        scrollingElement.classList.add('scrolling_element');
        if (scrollingElement.nodeName != 'HTML') {
            document.documentElement.classList.add('no_scrolling_element');
        }
    }
}

useState<IModalStorage[]>('appModalsStorage', () => []);

useState('appLayoutChangedTimes', () => 0);

const appLayoutChangedNextSkip = useState('appLayoutChangedNextSkip', () => false);

useNuxtApp().hook('page:start', () => {
    if (appLayoutChangedNextSkip.value) {
        appLayoutChangedNextSkip.value = false;
        return;
    }
    const main = document.getElementsByTagName('main')[0];
    if (main) {
        main.style.setProperty('min-height', `${main.offsetHeight}px`);
        main.style.setProperty('overflow', 'hidden');
    }
});

useNuxtApp().hook('page:transition:finish', () => {
    nextAnimFrame(() => {
        unlockScroll();
        if (route.hash.length === 0) {
            window.scrollTo({ top: -100 });
        }
        nextAnimFrame(() => {
            const main = document.getElementsByTagName('main')[0];
            if (main) {
                main.style.removeProperty('min-height');
                main.style.removeProperty('overflow');
            }
        });
    });
});

const isPageLoading = useState<boolean>('isPageLoading', () => false);

let isLoadingInterval: ReturnType<typeof setTimeout> | null = null;

useNuxtApp().hook('page:loading:start', () => {
    if (isLoadingInterval) {
        clearInterval(isLoadingInterval);
    }
    isLoadingInterval = setTimeout(() => {
        isPageLoading.value = true;
    }, 1000);
});

useNuxtApp().hook('page:loading:end', () => {
    if (isLoadingInterval) {
        clearInterval(isLoadingInterval);
    }
    isPageLoading.value = false;
});

const onResize = () => {
    const scrollElement = (document.scrollingElement || document.documentElement) as HTMLElement;
    const scrollbarWidth = window.innerWidth - scrollElement.clientWidth;

    document.documentElement.style.setProperty('--modal-content-margin-right', `${scrollbarWidth}px`);
};

onMounted(() => {
    window.addEventListener('resize', onResize);
    onResize();
});

onUnmounted(() => {
    window.removeEventListener('resize', onResize);
});
</script>

<template>
    <UApp
        :locale="ru"
        :toaster="{ position: 'top-center', expand: false }"
    >
        <slot />
    </UApp>
</template>
