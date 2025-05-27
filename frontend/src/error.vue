<script setup lang="ts">
import type { NuxtError } from '#app';
import { AppProvider } from './domain/app';

defineProps({
    error: Object as () => NuxtError,
});
</script>

<template>
    <AppProvider>
        <div :class="$style.wrapper">
            <div>
                <div :class="$style.img"></div>
                Возникла ошибка <b>{{ error && error.statusCode }}</b>
                <div :class="$style.back">
                    <NuxtLink
                        to="/"
                        class="button_1"
                        >На главную</NuxtLink
                    >
                </div>
            </div>
        </div>
    </AppProvider>
</template>

<style lang="less" module>
@import '@styles/includes';

.wrapper {
    display: flex;
    height: 100dvh;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}

.img {
    width: 170px;
    height: 250px;
    background: url('@/assets/images/404.png') no-repeat center center;
    background-size: cover;
    margin: 0 auto 40px 0;

    .x2({
        background-image: url('@/assets/images/404_x2.png');
    });
}

.back {
    font-size: 0;
    margin-top: 40px;
    text-align: center;
}
</style>
