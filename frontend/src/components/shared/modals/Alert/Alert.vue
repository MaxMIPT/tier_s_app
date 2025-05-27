<script setup lang="ts">
import type { UseModalReturnType } from 'vue-final-modal';

const props = defineProps<{
    title?: string;
    modalObj: () => UseModalReturnType<any>;
}>();

const emit = defineEmits<{
    (e: 'confirm'): void;
}>();
</script>

<template>
    <SharedModalsDefaultModal
        :modal-obj="props.modalObj()"
        @close="emit('confirm')"
    >
        <SharedModalsDefaultWrapper :modal-obj="props.modalObj()">
            <template #title>{{ title }}</template>
            <template #content>
                <div
                    v-if="$slots.default"
                    :class="$style.content"
                >
                    <slot />
                </div>
            </template>
            <template #buttons>
                <button
                    type="button"
                    :class="['button_1', $style.button_ok]"
                    title="Закрыть"
                    @click="props.modalObj().close()"
                >
                    OK
                </button>
            </template>
        </SharedModalsDefaultWrapper>
    </SharedModalsDefaultModal>
</template>

<style lang="less" module>
@import '@styles/includes';

.content {
    font-size: 18px;
}

.button_ok {
    padding-left: 40px;
    padding-right: 40px;
}
</style>
