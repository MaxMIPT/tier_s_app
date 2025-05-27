<script setup lang="ts">
import '@/assets/styles/layouts/default.less';
const isPageLoading = useState<boolean>('isPageLoading');

onMounted(() => {
    const appLayoutChangedTimes = useState<number>('appLayoutChangedTimes');
    appLayoutChangedTimes.value += 1;
    if (appLayoutChangedTimes.value > 1) {
        window.scrollTo({ top: -100 });
    }
});
</script>

<template>
    <div id="all">
        <SharedPageLoadingIndicator :show="isPageLoading" />
        <WidgetHeader />
        <main class="default">
            <slot />
        </main>
        <WidgetFooter />
    </div>
</template>

<style lang="less"></style>
