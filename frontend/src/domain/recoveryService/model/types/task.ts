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

export interface ITask {
    id: string;
    file_name: string;
    status: TaskStatus;
    is_process_finished: boolean;
    is_process_finished_with_error: boolean;
    created_at: Date;
    audio_length_sec: number;
    audio_dub_url: string;
    audio_transcription: string;
}
