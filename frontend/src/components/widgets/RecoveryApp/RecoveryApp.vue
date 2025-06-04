<script setup lang="ts">
import { WidgetRecoveryAppUiTaskEntity } from '#components';
import type { IRecordResult, LoadType } from './model/types/types';
import { addNewTask, useTaskStore } from '~/domain/recoveryService';
import { uploadWorkflow } from '~/domain/recoveryService/api/uploadWorkflow';
import { StandartErrorList } from '~/shared/errors/errors';

const taskStore = useTaskStore();

const loadType = ref<LoadType>('record');

const isLoading = ref(false);

const setLoadType = (value: LoadType) => {
    if (isLoading.value) return;
    loadType.value = value;
};

const onAudioRecordLoad = async (data: IRecordResult) => {
    isLoading.value = true;
    try {
        const response = await uploadWorkflow(data.blob, data.name);
        addNewTask(response.workflow_id, data.name);
    } catch (e) {
        if (e instanceof StandartErrorList) {
            console.log(e);
        } else {
            console.log(e);
        }
    } finally {
        isLoading.value = false;
    }
};

const onAudioFileLoad = async (data: File) => {
    isLoading.value = true;
    try {
        const response = await uploadWorkflow(data, data.name);
        addNewTask(response.workflow_id, data.name);
    } catch (e) {
        if (e instanceof StandartErrorList) {
            console.log(e);
        } else {
            console.log(e);
        }
    } finally {
        isLoading.value = false;
    }
};
</script>

<template>
    <div :class="$style.wrapper">
        <div :class="$style.controls">
            <div :class="$style.selector">
                Вы можете записать
                <button
                    :class="[loadType == 'record' ? $style.active : null]"
                    @click="setLoadType('record')"
                >
                    звуковое сообщение
                </button>
                или
                <button
                    :class="[loadType == 'file' ? $style.active : null]"
                    @click="setLoadType('file')"
                >
                    загрузить аудиофайл
                </button>
            </div>
            <div :class="$style.data_loaders">
                <div :class="[$style.record_wrapper, loadType == 'record' ? $style.active : null]">
                    <WidgetRecoveryAppUiAudioRecorder
                        :is-loading="isLoading"
                        @load="onAudioRecordLoad"
                    />
                </div>
                <div :class="[$style.file_wrapper, loadType == 'file' ? $style.active : null]">
                    <WidgetRecoveryAppUiAudioFileLoader
                        :is-loading="isLoading"
                        @load="onAudioFileLoad"
                    />
                </div>
            </div>
        </div>
        <div
            v-if="taskStore.items.length"
            :class="$style.tasks"
        >
            <div :class="$style.head">
                <div :class="$style.time">Время</div>
                <div :class="$style.file_name">Исходный файл</div>
                <div :class="$style.status">Текущий статус</div>
                <div :class="$style.result">Результат</div>
            </div>
            <div :class="$style.items">
                <template
                    v-for="item in [...taskStore.items].toReversed()"
                    :key="item.id"
                >
                    <WidgetRecoveryAppUiTaskEntity :task="item" />
                </template>
            </div>
        </div>
    </div>
</template>

<style lang="less" module>
@import '@styles/includes';

.controls {
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    background-color: var(--bg-color-1);
    border-radius: 10px;
    padding: 30px;

    .width-size-sm-less({
        padding: 20px;
    });

    > .selector {
        font-size: 24px;
        line-height: 1.5;
        color: var(--font-color-3);

        > button {
            text-decoration: underline;
            transition: color 0.25s ease;

            &.active {
                color: var(--color-1);
            }
        }

        .width-size-sm-less({
            font-size: 18px;
        });
    }
}

.data_loaders {
    margin-top: 20px;

    .width-size-sm-less({
        margin-top: 30px;
    });

    .record_wrapper {
        display: none;

        &.active {
            display: block;
        }
    }

    .file_wrapper {
        display: none;

        &.active {
            display: block;
        }
    }
}

.tasks {
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    background-color: var(--bg-color-1);
    border-radius: 10px;
    margin-top: 40px;

    .width-size-sm-less({
        margin-top: 30px;
    });

    > .head {
        display: grid;
        align-items: center;
        grid-template-columns: 120px 3fr 3fr 6fr;
        gap: 30px;
        padding: 15px 30px;
        border-bottom: 1px solid var(--border-color-1);

        > div {
            font-size: 12px;
            color: var(--font-color-4);
        }

        .width-size-less(1000px, {
            display: none
        });
    }

    > .items {
    }
}
</style>
