<script setup lang="ts">
const emit = defineEmits<{
    (e: 'load', result: File): void;
}>();

const props = defineProps<{
    isLoading: boolean;
}>();

const file = ref<File | null>(null);

watch(
    () => props.isLoading,
    () => {
        if (!props.isLoading) {
            file.value = null;
        }
    },
);

const load = () => {
    if (file.value) {
        emit('load', file.value);
    }
};

watch(
    () => props.isLoading,
    () => {
        if (!props.isLoading) {
            //resultRecord.value = null;
        }
    },
);
</script>

<template>
    <div :class="$style.wrapper">
        <div :class="$style.control_button">
            <SharedUiFileInput
                v-model="file"
                :disabled="isLoading"
                accept="audio/*"
                size="xl"
            />
        </div>

        <div
            v-if="file"
            :class="$style.file"
        >
            <div :class="$style.name">
                {{ file.name }}
            </div>
            <div :class="$style.button">
                <UButton
                    :loading="isLoading"
                    size="xl"
                    icon="i-lucide-upload"
                    variant="outline"
                    @click="load"
                >
                    Загрузить
                </UButton>
            </div>
        </div>
    </div>
</template>

<style lang="less" module>
@import '@styles/includes';

.wrapper {
    display: flex;
    align-items: center;
    gap: 20px;
    min-height: 70px;

    .width-size-sm-less({
        min-height: 0;
        flex-wrap: wrap
    });

    > .control_button {
        flex-shrink: 0;

        .width-size-sm-less({
            width: 100%;
        });
    }

    > .file {
        width: 100%;
        display: flex;
        align-items: center;
        gap: 20px;
        flex-wrap: wrap;
    }
}
</style>
