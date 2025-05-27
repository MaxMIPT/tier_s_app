<script setup lang="ts">
const file = defineModel<File | null>();

withDefaults(
    defineProps<{
        disabled?: boolean;
        accept?: string;
        size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
    }>(),
    {
        disabled: false,
        accept: undefined,
        size: undefined,
    },
);

const inputRef = ref<HTMLInputElement | null>(null);

const triggerFileSelect = () => {
    inputRef.value?.click();
};

const onFileChange = (e: Event) => {
    const files = (e.target as HTMLInputElement).files;
    if (files?.[0]) {
        file.value = files[0];
    } else {
        clearFile();
    }
};

function clearFile() {
    file.value = null;
    if (inputRef.value) inputRef.value.value = '';
}
</script>

<template>
    <div :class="$style.wrapper">
        <div :class="$style.selector">
            <input
                ref="inputRef"
                :class="$style.hidden_input"
                type="file"
                :accept="accept"
                class="hidden"
                @change="onFileChange"
            />

            <UButton
                icon="i-lucide-paperclip"
                :disabled="disabled"
                :class="$style.button"
                :size="size"
                @click="triggerFileSelect"
            >
                Выберите файл ...
            </UButton>
        </div>
    </div>
</template>

<style lang="less" module>
@import '@styles/includes';

.selector {
    position: relative;
    cursor: pointer;

    > .hidden_input {
        opacity: 0;
        z-index: 1;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }

    > .button {
        position: relative;
        z-index: 2;
    }
}
</style>
