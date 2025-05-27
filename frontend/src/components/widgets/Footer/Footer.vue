<script setup lang="ts">
import { useAppProviderConfig } from '~/domain/app';

const appProviderConfig = useAppProviderConfig();
</script>

<template>
    <footer>
        <div>
            <div class="title">{{ appProviderConfig.title }} &copy; 2025</div>
        </div>
    </footer>
</template>
