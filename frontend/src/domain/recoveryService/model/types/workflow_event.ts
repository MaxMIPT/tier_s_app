import type { IWorkflow, PipelineStatus, TaskStatus } from './workflow';

export interface IWorkflowTask {
    task_log_id: number;
    workflow: IWorkflow;

    created_at: Date;
}
