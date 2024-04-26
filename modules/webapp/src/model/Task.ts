export interface Task {
  id: string;
  command: string;
  result?: string;
  input: string;
  status: string;
  reason?: string;
}
