import { useState } from "react";
import { Point } from "../model/Point";
import { Task } from "../model/Task";

export const useGetMyCommands = (url: string, userId: string) => {
  const [error, setError] = useState<string | null>(null);
  const [myCommands, setMyCommands] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const fetchMyCommands = async () => {
    setIsLoading(true);
    setError(null);
    try {
      console.log("fetch my commands", url);
      const response = await fetch(`${url}/command?userId=${userId}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      console.log("response", response);

      if (!response.ok) {
        throw new Error("Failed to send coordinates");
      }
      const tasks = (await response.json()).tasks;
      setMyCommands(tasks);

      setIsLoading(false);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Not known error");
      }

      setIsLoading(false);
    }
  };

  return { fetchMyCommands, isLoading, error, myCommands };
};
