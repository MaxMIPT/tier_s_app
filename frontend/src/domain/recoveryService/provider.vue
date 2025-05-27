<script setup lang="ts">
import { useTaskStore } from './model/store/task';

const taskStore = useTaskStore();
taskStore.loadClientID();
</script>

<template>
    <slot />
</template>
