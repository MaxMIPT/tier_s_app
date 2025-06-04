import { useTaskStore } from '../model/store/task';
import { PipelineStatus, TaskStatus, type IWorkflow } from '../model/types/workflow';

export const addNewTask = async (id: string, filename: string) => {
    const task: IWorkflow = {
        workflow_id: id,
        original_file: null,
        original_file_name: filename,
        task_status: TaskStatus.Created,
        status: PipelineStatus.Running,
        created_at: new Date(),
        converted_file: null,
        converted_file_duration: null,
        dubbed_file: null,
        restored_text: null,
    };

    const taskStore = useTaskStore();
    if (!taskStore.add(task)) {
        return;
    }

    // await new Promise((resolve) =>
    //     setTimeout(() => {
    //         taskStore.update(id, { status: TaskStatus.AudioConversionStarted });
    //         resolve(true);
    //     }, 1000),
    // );

    // await new Promise((resolve) =>
    //     setTimeout(() => {
    //         taskStore.update(id, { status: TaskStatus.AudioConversionFinished, audio_length_sec: 100 });
    //         resolve(true);
    //     }, 1000),
    // );

    // await new Promise((resolve) =>
    //     setTimeout(() => {
    //         taskStore.update(id, { status: TaskStatus.AudioTranscriptionStarted });
    //         resolve(true);
    //     }, 1000),
    // );

    // await new Promise((resolve) =>
    //     setTimeout(() => {
    //         taskStore.update(id, {
    //             status: TaskStatus.AudioTranscriptionFinished,
    //             audio_dub_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    //         });
    //         resolve(true);
    //     }, 1000),
    // );

    // await new Promise((resolve) =>
    //     setTimeout(() => {
    //         taskStore.update(id, { status: TaskStatus.AudioDubbingStarted });
    //         resolve(true);
    //     }, 1000),
    // );

    // await new Promise((resolve) =>
    //     setTimeout(() => {
    //         taskStore.update(id, { status: TaskStatus.AudioDubbingFinished, audio_transcription: 'Привет мир!' });
    //         resolve(true);
    //     }, 1000),
    // );

    // await new Promise((resolve) =>
    //     setTimeout(() => {
    //         // Типа с вероятностью 50% прилетела ошибка в одном из статусов
    //         if (Math.random() > 0.5) {
    //             taskStore.update(id, { status: TaskStatus.Canceled, is_process_finished: true, is_process_finished_with_error: true });
    //         } else {
    //             taskStore.update(id, { status: TaskStatus.Finished, is_process_finished: true, audio_transcription: 'Привет мир!' });
    //         }
    //         resolve(true);
    //     }, 1000),
    // );
};
