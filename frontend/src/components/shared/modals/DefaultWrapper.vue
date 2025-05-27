<script setup lang="ts">
import type { UseModalReturnType } from 'vue-final-modal';

defineProps<{
    modalObj: UseModalReturnType<any>;
    className?: string;
}>();

const emit = defineEmits<{
    (e: 'close'): void;
}>();
</script>

<template>
    <div :class="['modal-default-c', className]">
        <div class="modal-default-top">
            <div class="title"><slot name="title"></slot></div>
            <div class="close">
                <button
                    type="button"
                    title="Закрыть"
                    @click="modalObj.close()"
                ></button>
            </div>
        </div>
        <template v-if="$slots.content">
            <div class="modal-default-content">
                <slot name="content"></slot>
            </div>
        </template>
        <template v-if="$slots.buttons">
            <div class="modal-default-buttons">
                <slot name="buttons"></slot>
            </div>
        </template>
    </div>
</template>
