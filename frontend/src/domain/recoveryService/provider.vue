<script setup lang="ts">
import { startBroadcast, stopBroadcast } from './hooks/broadcast';
import { loadWorkflows as loadWorkflows } from './hooks/loadWorflows';
import { useTaskStore } from './model/store/task';

const taskStore = useTaskStore();
taskStore.loadClientID();

let ws: WebSocket | null = null;

onMounted(() => {
    ws = startBroadcast();
    loadWorkflows();
});

onUnmounted(() => {
    if (ws !== null) {
        stopBroadcast(ws);
    }
});
</script>

<template>
    <slot />
</template>
