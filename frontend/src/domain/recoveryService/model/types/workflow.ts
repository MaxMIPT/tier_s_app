export enum TaskStatus {
    Created = 'created',
    AudioConversionStarted = 'audio_conversion_started',
    AudioConversionFinished = 'audio_conversion_finished',
    AudioTranscriptionStarted = 'audio_transcription_started',
    AudioTranscriptionFinished = 'audio_transcription_finished',
    AudioDubbingStarted = 'audio_dubbing_started',
    AudioDubbingFinished = 'audio_dubbing_finished',
    Finished = 'finished',
    Canceled = 'canceled',
}

export const TaskStatusText = {
    [TaskStatus.Created]: 'В очереди на обработку',
    [TaskStatus.AudioConversionStarted]: 'Конвертация аудио началась',
    [TaskStatus.AudioConversionFinished]: 'Конвертация аудио завершена',
    [TaskStatus.AudioTranscriptionStarted]: 'Транскрипция аудио началась',
    [TaskStatus.AudioTranscriptionFinished]: 'Транскрипция аудио завершена',
    [TaskStatus.AudioDubbingStarted]: 'Озвучивание аудио началось',
    [TaskStatus.AudioDubbingFinished]: 'Озвучивание аудио завершено',
    [TaskStatus.Finished]: 'Завершено',
    [TaskStatus.Canceled]: 'Отменено',
};

export enum PipelineStatus {
    Running = 'running',
    Success = 'success',
    Failed = 'failed',
}

export interface IWorkflow {
    workflow_id: string;
    original_file: string | null;
    original_file_name: string;
    status: PipelineStatus;
    converted_file: string | null;
    converted_file_duration: number | null;
    dubbed_file: string | null;
    restored_text: string | null;
    task_status: TaskStatus;

    created_at: Date;
}
