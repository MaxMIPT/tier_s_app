<script setup lang="ts">
defineProps<{
    className?: string;
}>();
</script>

<template>
    <div :class="['modal-default-loader', className]">
        <div class="loader"></div>
    </div>
</template>
