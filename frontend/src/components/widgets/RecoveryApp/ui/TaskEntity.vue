<script setup lang="ts">
import { useModalConfirm } from '~/components/shared/modals/Confirm/useModalConfirm';
import { useTaskStore } from '~/domain/recoveryService';
import { TaskStatus, TaskStatusText, type ITask } from '~/domain/recoveryService/model/types/task';

const props = defineProps<{ task: ITask }>();

const taskStore = useTaskStore();

const progress = computed(() => {
    switch (props.task.status) {
        case TaskStatus.Created:
            return 10;
        case TaskStatus.AudioConversionStarted:
            return 20;
        case TaskStatus.AudioConversionFinished:
            return 30;
        case TaskStatus.AudioTranscriptionStarted:
            return 40;
        case TaskStatus.AudioTranscriptionFinished:
            return 50;
        case TaskStatus.AudioDubbingStarted:
            return 60;
        case TaskStatus.AudioDubbingFinished:
            return 90;
        case TaskStatus.Finished:
            return 100;
        default:
            return 0;
    }
});

const formatDuration = (value: number) => {
    const hours = Math.floor(value / 3600);
    const minutes = Math.floor((value % 3600) / 60);
    const seconds = value % 60;

    const pad = (num: number) => String(num).padStart(2, '0');

    return `[${pad(hours)}:${pad(minutes)}:${pad(seconds)}]`;
};

const remove = () => {
    const confirmModal = useModalConfirm({
        slot: 'Вы действительно хотите удалить задачу?',
        onConfirm: () => {
            taskStore.remove(props.task.id);
        },
    });
    confirmModal.open();
};
</script>

<template>
    <div :class="$style.wrapper">
        <div :class="$style.task">
            <div :class="$style.time">
                <div :class="$style.value">
                    {{
                        task.created_at.toLocaleString(undefined, {
                            day: '2-digit',
                            month: '2-digit',
                            year: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit',
                        })
                    }}
                </div>
                <div :class="$style.remove">
                    <UButton
                        icon="i-lucide-trash-2"
                        size="xs"
                        color="neutral"
                        variant="outline"
                        @click="remove"
                    />
                </div>
            </div>
            <div :class="$style.file_name">
                <div :class="$style.name">{{ task.file_name }}</div>
                <div :class="$style.duration">{{ formatDuration(task.audio_length_sec) }}</div>
            </div>
            <div :class="$style.status">
                <template v-if="task.is_process_finished_with_error"> Процесс завершился с ошибкой. Попробуйте повторить запрос </template>
                <template v-else>
                    {{ TaskStatusText[task.status] }}
                </template>
            </div>
            <div :class="$style.result">
                <div :class="$style.dub_link">
                    <span :class="$style.title">Ссылка на озвучку:</span>
                    <template v-if="task.audio_dub_url">
                        <a
                            :href="task.audio_dub_url"
                            target="_blank"
                        >
                            {{ task.audio_dub_url }}
                        </a>
                    </template>
                    <template v-else>
                        <template v-if="task.is_process_finished_with_error">ошибка</template>
                        <template v-else>обрабатывается...</template>
                    </template>
                </div>
                <div :class="$style.transcription">
                    <span :class="$style.title">Транскрипция:</span>
                    <template v-if="task.audio_transcription">
                        <div :class="$style.text">{{ task.audio_transcription }}</div>
                    </template>
                    <template v-else>
                        <template v-if="task.is_process_finished_with_error">ошибка</template>
                        <template v-else>обрабатывается...</template>
                    </template>
                </div>
            </div>
        </div>
        <div :class="$style.progress">
            <template v-if="!task.is_process_finished">
                <div :class="$style.progress_bar">
                    <div :style="{ width: progress + '%' }"></div>
                </div>
            </template>
        </div>
    </div>
</template>

<style lang="less" module>
@import '@styles/includes';

.wrapper {
    padding: 20px 0 15px 0;

    .width-size-sm-less({
        padding: 10px 0 5px 0;
    });

    &:last-child {
        > .progress {
            border-bottom: 0 !important;
        }
    }
}

.task {
    display: grid;
    grid-template-columns: 120px 3fr 3fr 6fr;
    gap: 30px;
    padding: 0 30px;

    .width-size-less(1000px, {
        display: flex;
        flex-direction: column;
    });

    .width-size-sm-less({
        gap:15px;
        padding:0 20px;
    });

    > div {
        overflow: hidden;
        white-space: normal;
        word-break: break-word;
        overflow-wrap: break-word;
    }

    > .time {
        > .value {
            font-size: 12px;
            color: var(--font-color-3);
        }

        > .remove {
            font-size: 0;
            margin-top: 10px;
        }

        .width-size-less(1000px, {
            display: flex;
            gap:15px;
            align-items: center;

            > .remove {
                margin-top: 0;
            }
        });
    }

    > .file_name {
        > .name {
            font-size: 12px;
            color: var(--font-color-3);
        }

        > .duration {
            font-size: 12px;
            color: var(--font-color-3);
            margin-top: 5px;
        }
    }

    > .status {
        font-size: 14px;
        color: var(--font-color-3);
    }

    > .result {
        display: flex;
        flex-direction: column;
        gap: 15px;

        > .dub_link {
            font-size: 12px;
            color: var(--font-color-3);

            > .title {
                margin-right: 5px;
                color: var(--font-color-4);
            }

            > a {
                color: var(--color-1);
                text-decoration: underline;
            }
        }

        > .transcription {
            font-size: 12px;
            color: var(--font-color-3);

            > .title {
                margin-right: 5px;
                color: var(--font-color-4);
            }
        }
    }
}

.progress {
    margin-top: 15px;
    height: 10px;
    border-bottom: 1px solid var(--border-color-1);
}

.progress_bar {
    width: 100%;
    height: 10px;
    background-color: #eee;
    overflow: hidden;

    position: relative;

    > div {
        height: 100%;
        background-color: var(--color-1);
        background-image: linear-gradient(
            45deg,
            rgba(255, 255, 255, 0.15) 25%,
            transparent 25%,
            transparent 50%,
            rgba(255, 255, 255, 0.15) 50%,
            rgba(255, 255, 255, 0.15) 75%,
            transparent 75%,
            transparent
        );
        background-size: 40px 40px;
        transition: width 0.5s ease;
        animation: stripe-move 1s linear infinite;
    }
}

@keyframes stripe-move {
    from {
        background-position: 0 0;
    }
    to {
        background-position: 40px 0;
    }
}
</style>
