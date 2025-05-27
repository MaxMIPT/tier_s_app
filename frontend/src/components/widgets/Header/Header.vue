<script setup lang="ts">
import { setAppTheme, useAppProviderConfig } from '~/domain/app';
import { windowScrollTo } from '~/shared/helpers/functions';

const route = useRoute();
const router = useRouter();

const appProviderConfig = useAppProviderConfig();

const onLogoClick = () => {
    if (!document.scrollingElement) {
        return;
    }

    if (document.scrollingElement.scrollTop > 100) {
        windowScrollTo(-100);
    } else if (route.fullPath != '/') {
        router.push('/');
    }
};
</script>

<template>
    <header class="default_header">
        <div id="top_header_spacer"></div>
        <div id="top_header_wrapper">
            <div
                id="top_header"
                class="fix_width_on_lock_scroll"
            >
                <div>
                    <div class="logo">
                        <a
                            href="/"
                            :title="appProviderConfig.title"
                            @click.stop.prevent="onLogoClick"
                        >
                            <span class="icon"></span>
                            <span class="text">{{ appProviderConfig.title }}</span>
                        </a>
                    </div>
                    <div class="buttons">
                        <div class="theme">
                            <SharedThemeSwitcher
                                :size="30"
                                :model-value="appProviderConfig.theme"
                                @update:model-value="setAppTheme"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>
</template>
