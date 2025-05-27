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
    <SharedModalsDefaultModal :modal-obj="props.modalObj()">
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
                <div :class="$style.buttons">
                    <button
                        type="button"
                        :class="['button_1', $style.button_ok]"
                        title="ОК"
                        @click="
                            props.modalObj().close();
                            emit('confirm');
                        "
                    >
                        OK
                    </button>
                    <button
                        type="button"
                        :class="['button_1', 'gray', $style.button_cancel]"
                        title="Отмена"
                        @click="props.modalObj().close()"
                    >
                        Отмена
                    </button>
                </div>
            </template>
        </SharedModalsDefaultWrapper>
    </SharedModalsDefaultModal>
</template>

<style lang="less" module>
@import '@styles/includes';

.content {
    font-size: 18px;
}

.buttons {
    display: flex;
    gap: 20px;
    justify-content: center;
}

.button_ok {
    padding-left: 40px;
    padding-right: 40px;
}

.button_cancel {
    padding-left: 40px;
    padding-right: 40px;
}
</style>
