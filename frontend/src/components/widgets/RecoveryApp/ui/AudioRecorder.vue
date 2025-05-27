<script setup lang="ts">
import type { IRecordResult } from '../model/types/types';

const emit = defineEmits<{
    (e: 'load', result: IRecordResult): void;
}>();

const props = defineProps<{
    isLoading: boolean;
}>();

const isRecording = ref(false);
let mediaRecorder: MediaRecorder | null = null;
const audioChunks: Blob[] = [];

const startTime = ref(0);
const elapsed = ref(0);
let timerInterval: number | null = null;

const resultRecord = ref<IRecordResult | null>(null);

const formattedTime = computed(() => {
    const ms = elapsed.value;
    const m = String(Math.floor(ms / 60000)).padStart(2, '0');
    const s = String(Math.floor((ms % 60000) / 1000)).padStart(2, '0');
    const t = Math.floor((ms % 1000) / 100);
    return `${m}:${s},${t}`;
});

const waveCanvas = ref<HTMLCanvasElement>();
let audioCtx: AudioContext | null = null;
let analyser: AnalyserNode | null = null;
let dataArray: Uint8Array;
let animationId: number;

const startRecording = async (): Promise<void> => {
    if (props.isLoading) return;

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    audioChunks.length = 0;
    mediaRecorder = new MediaRecorder(stream);

    audioCtx = new AudioContext();
    const source = audioCtx.createMediaStreamSource(stream);
    analyser = audioCtx.createAnalyser();
    analyser.fftSize = 2048;
    source.connect(analyser);
    dataArray = new Uint8Array(analyser.fftSize);

    mediaRecorder.ondataavailable = (e: BlobEvent) => {
        if (e.data.size) audioChunks.push(e.data);
    };
    mediaRecorder.onstop = async () => {
        const blob = new Blob(audioChunks, { type: 'audio/webm' });
        await setAudioBlob(blob);
        stopWaveAnimation();
    };

    mediaRecorder.start();
    isRecording.value = true;

    startTime.value = Date.now();
    elapsed.value = 0;
    timerInterval = window.setInterval(() => {
        elapsed.value = Date.now() - startTime.value;
    }, 100);

    await nextTick();
    drawWave();
};

const stopRecording = () => {
    if (mediaRecorder && isRecording.value) mediaRecorder.stop();
    isRecording.value = false;
    if (timerInterval) clearInterval(timerInterval);
    if (audioCtx) audioCtx.close();
};

const drawWave = () => {
    if (!analyser || !waveCanvas.value) return;
    const canvas = waveCanvas.value;
    const ctx = canvas.getContext('2d')!;
    canvas.width = canvas.clientWidth * devicePixelRatio;
    canvas.height = 100 * devicePixelRatio;

    function draw() {
        if (!analyser) return;
        analyser.getByteTimeDomainData(dataArray);

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.lineWidth = 2;
        ctx.beginPath();

        const sliceWidth = canvas.width / dataArray.length;
        let x = 0;
        for (let i = 0; i < dataArray.length; i++) {
            const v = dataArray[i] / 128;
            const y = (v * canvas.height) / 2;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
            x += sliceWidth;
        }

        ctx.strokeStyle = '#e8363d';
        ctx.stroke();

        animationId = requestAnimationFrame(draw);
    }

    draw();
};

const load = () => {
    if (resultRecord.value) {
        emit('load', resultRecord.value);
    }
};

function stopWaveAnimation() {
    cancelAnimationFrame(animationId);
}

const setAudioBlob = (blob: Blob) => {
    const now = new Date();

    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hour = String(now.getHours()).padStart(2, '0');
    const minute = String(now.getMinutes()).padStart(2, '0');

    resultRecord.value = {
        blob,
        name: `Запись-${year}-${month}-${day}-${hour}-${minute}.webm`,
    };
    //   const form = new FormData()
    //   form.append('audio', blob, 'recording.webm')
    //   await fetch('/api/speech', { method: 'POST', body: form })
};

watch(
    () => props.isLoading,
    () => {
        if (!props.isLoading) {
            resultRecord.value = null;
        }
    },
);

onBeforeUnmount(() => {
    if (timerInterval) clearInterval(timerInterval);
    if (audioCtx) audioCtx.close();
    cancelAnimationFrame(animationId);
});
</script>

<template>
    <div :class="$style.wrapper">
        <div :class="$style.control_button">
            <template v-if="!isRecording">
                <UButton
                    icon="i-lucide-mic"
                    size="xl"
                    @click="startRecording"
                >
                    Начать запись
                </UButton>
            </template>
            <template v-else>
                <UButton
                    icon="i-lucide-pause"
                    size="xl"
                    color="neutral"
                    variant="outline"
                    @click="stopRecording"
                >
                    Завершить
                </UButton>
            </template>
        </div>
        <div
            v-if="resultRecord && !isRecording"
            :class="$style.result"
        >
            <div :class="$style.name">{{ resultRecord.name }}</div>
            <div :class="$style.send">
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
        <div
            v-if="isRecording"
            :class="$style.record_panel"
        >
            <div :class="$style.timer">
                <span class="recording-dot"></span>
                <span class="time">{{ formattedTime }}</span>
            </div>

            <div :class="$style.waves">
                <canvas
                    ref="waveCanvas"
                    :class="$style['wave-canvas']"
                ></canvas>
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

    > .result {
        width: 100%;
        display: flex;
        align-items: center;
        gap: 20px;
        flex-wrap: wrap;
    }

    > .record_panel {
        width: 100%;
        display: flex;
        align-items: center;
        gap: 10px;

        > .timer {
            flex-shrink: 0;
            min-width: 90px;
        }

        > .waves {
            width: 100%;
        }
    }
}

.timer {
    display: flex;
    align-items: center;

    .recording-dot {
        width: 10px;
        height: 10px;
        background: var(--color-1);
        border-radius: 50%;
        margin-right: 0.5em;
        animation: blink 1s steps(1) infinite;
    }
}

@keyframes blink {
    50% {
        opacity: 0;
    }
}

.wave-canvas {
    width: 100%;
    height: 70px;

    .width-size-sm-less({
        height: 50px;
    });
}
</style>
