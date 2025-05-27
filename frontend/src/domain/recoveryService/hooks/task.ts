import { useTaskStore } from '../model/store/task';
import { TaskStatus, type ITask } from '../model/types/task';

export const addNewTask = async (id: string, fileName: string) => {
    const task: ITask = {
        id,
        file_name: fileName,
        status: TaskStatus.Created,
        is_process_finished: false,
        is_process_finished_with_error: false,
        created_at: new Date(),
        audio_length_sec: 0,
        audio_dub_url: '',
        audio_transcription: '',
    };

    const taskStore = useTaskStore();
    if (!taskStore.add(task)) {
        return;
    }

    await new Promise((resolve) =>
        setTimeout(() => {
            taskStore.update(id, { status: TaskStatus.AudioConversionStarted });
            resolve(true);
        }, 1000),
    );

    await new Promise((resolve) =>
        setTimeout(() => {
            taskStore.update(id, { status: TaskStatus.AudioConversionFinished, audio_length_sec: 100 });
            resolve(true);
        }, 1000),
    );

    await new Promise((resolve) =>
        setTimeout(() => {
            taskStore.update(id, { status: TaskStatus.AudioTranscriptionStarted });
            resolve(true);
        }, 1000),
    );

    await new Promise((resolve) =>
        setTimeout(() => {
            taskStore.update(id, {
                status: TaskStatus.AudioTranscriptionFinished,
                audio_dub_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            });
            resolve(true);
        }, 1000),
    );

    await new Promise((resolve) =>
        setTimeout(() => {
            taskStore.update(id, { status: TaskStatus.AudioDubbingStarted });
            resolve(true);
        }, 1000),
    );

    await new Promise((resolve) =>
        setTimeout(() => {
            taskStore.update(id, { status: TaskStatus.AudioDubbingFinished, audio_transcription: 'Привет мир!' });
            resolve(true);
        }, 1000),
    );

    await new Promise((resolve) =>
        setTimeout(() => {
            // Типа с вероятностью 50% прилетела ошибка в одном из статусов
            if (Math.random() > 0.5) {
                taskStore.update(id, { status: TaskStatus.Canceled, is_process_finished: true, is_process_finished_with_error: true });
            } else {
                taskStore.update(id, { status: TaskStatus.Finished, is_process_finished: true, audio_transcription: 'Привет мир!' });
            }
            resolve(true);
        }, 1000),
    );
};
