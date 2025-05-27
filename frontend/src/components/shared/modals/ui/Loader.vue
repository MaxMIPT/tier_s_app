<script setup lang="ts"></script>

<template>
    <div :class="$style.wrapper">Загрузка...</div>
</template>

<style lang="less" module>
@import '@styles/includes';

.wrapper {
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    color: var(--font-color-1);
    background-color: var(--bg-color-1);
}
</style>
