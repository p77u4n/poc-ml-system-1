import React from "react";
import { Task } from "../model/Task";

interface Props {
  tasks: Task[];
}

const TaskTable: React.FC<Props> = ({ tasks }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Command</th>
          <th>Result</th>
          <th>Input</th>
          <th>Status</th>
          <th>Reason</th>
        </tr>
      </thead>
      <tbody>
        {tasks.map((task) => (
          <tr key={task.id}>
            <td>{task.id}</td>
            <td>{task.command}</td>
            <td>{task.result}</td>
            <td>{task.input}</td>
            <td>{task.status}</td>
            <td>{task.reason}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default TaskTable;
