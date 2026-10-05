import { invoke } from '@tauri-apps/api/core';
export function api<T>(command: string, payload: unknown = {}): Promise<T> { return invoke<T>('api', { command, payload }); }
