import { useState } from "react";
import { Point } from "../model/Point";

export const useSendCoordinates = (url: string, userId: string) => {
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const sendCoordinates = async (startPoint: Point, endPoint: Point) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${url}/command/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          command: "PREDICT",
          userId: userId,
          input: {
            topLeftX: startPoint.x,
            topLeftY: startPoint.y,
            bottomRightX: endPoint.x,
            bottomRightY: endPoint.y,
          },
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to send coordinates");
      }

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

  return { sendCoordinates, isLoading, error };
};
