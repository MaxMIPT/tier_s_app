<script setup lang="ts">
defineProps<{ show: boolean }>();
</script>

<template>
    <div
        id="page_loading"
        :class="show ? 'show' : false"
    >
        <div class="loader-line"></div>
    </div>
</template>
