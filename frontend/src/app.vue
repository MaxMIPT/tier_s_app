<script setup lang="ts">
import { ModalsContainer } from 'vue-final-modal';
import { AppProvider } from './domain/app';
import { RecoveryServiceProvider } from './domain/recoveryService';
</script>

<template>
    <AppProvider>
        <RecoveryServiceProvider>
            <NuxtLayout>
                <NuxtPage />
            </NuxtLayout>
            <ModalsContainer />
        </RecoveryServiceProvider>
    </AppProvider>
</template>
