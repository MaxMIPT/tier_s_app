<script setup lang="ts">
import { VueFinalModal, type UseModalReturnType } from 'vue-final-modal';
import { onAnyModalBeforeOpened, onAnyModalClosed } from './lib/stdEvents';

const props = defineProps<{
    clickToClose?: boolean;
    modalObj: UseModalReturnType<any>;
}>();

const emit = defineEmits<{
    (e: 'close'): void;
}>();

const modalDefaultWrapperRef = useTemplateRef('modalDefaultWrapperRef');

const id = useId();

const onClick = (e: MouseEvent) => {
    if (props.clickToClose === true) {
        if (e.target === modalDefaultWrapperRef.value) {
            props.modalObj.close();
        }
    }
};
</script>

<template>
    <VueFinalModal
        :modal-id="id"
        class="modal"
        content-class="modal-content"
        overlay-class="modal-overlay"
        overlay-transition="vfm-fade"
        content-transition="modal-fade"
        :lock-scroll="false"
        :click-to-close="clickToClose === true ? true : false"
        :reserve-scroll-bar-gap="false"
        @closed="
            emit('close');
            onAnyModalClosed(id);
        "
        @before-open="onAnyModalBeforeOpened(id)"
    >
        <div
            ref="modalDefaultWrapperRef"
            class="modal-default-wrapper"
            @mouseup="onClick"
        >
            <slot></slot>
        </div>
    </VueFinalModal>
</template>
