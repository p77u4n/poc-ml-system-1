import React, { useEffect } from "react";
import { match } from "ts-pattern";
import { Task } from "../model/Task";
import cls from "classnames";

interface Props {
  tasks: Task[];
}

const TaskTable: React.FC<Props> = ({ tasks }) => {
  const ref = React.useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!ref.current) {
      return;
    }
    ref.current.scrollTo({
      behavior: "smooth",
      top: ref.current.scrollHeight,
    });
  }, [tasks]);
  return (
    <div className="h-48 overflow-x-auto" ref={ref}>
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Command</th>
            <th>Result</th>
            <th>Input</th>
            <th>Status</th>
            <th>Fail Reason</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task) => {
            const badgeClassName = match(task.status)
              .with("FAILED", () => "badge-warning")
              .with("FINISH", () => "badge-success")
              .with("PENDING", () => "badge-accent")
              .otherwise(() => "");
            console.log("task status", task.status, badgeClassName);
            return (
              <tr key={task.id}>
                <td>{task.id}</td>
                <td>{task.command}</td>
                <td>{task.result}</td>
                <td>{task.input}</td>
                <td>
                  {task.status === "PROCESSING" ? (
                    <span className="loading loading-dots loading-sm"></span>
                  ) : (
                    <span className={cls("badge", badgeClassName)}>
                      {task.status}
                    </span>
                  )}
                </td>
                <td>{task.reason}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default TaskTable;
