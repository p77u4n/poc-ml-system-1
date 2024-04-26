import React, { useRef, useState, MouseEvent } from "react";
import { useSendCoordinates } from "../hooks/createCommandWithCoord";
import { Point } from "../model/Point";

const CanvasRectangle: React.FC = () => {
  const [startPoint, setStartPoint] = useState<Point | null>(null);
  const [endPoint, setEndPoint] = useState<Point | null>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState<boolean>(false);
  const { sendCoordinates } = useSendCoordinates(
    process.env.REACT_APP_API_ENDPOINT || "http://localhost:3003",
    "bf7ab410-03ad-11ef-a277-c31c49e4e709",
  );

  const handleMouseDown = (e: MouseEvent<HTMLCanvasElement>) => {
    if (!canvasRef.current) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    setStartPoint({ x, y });
    setIsDrawing(true);
  };

  const handleMouseMove = (e: MouseEvent<HTMLCanvasElement>) => {
    if (!canvasRef.current || !isDrawing || !startPoint) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const ctx = canvasRef.current.getContext("2d");
    if (!ctx) return;
    ctx.clearRect(0, 0, canvasRef.current!.width, canvasRef.current!.height);
    ctx.beginPath();
    ctx.rect(startPoint.x, startPoint.y, x - startPoint.x, y - startPoint.y);
    ctx.stroke();
  };

  const handleMouseUp = (e: MouseEvent<HTMLCanvasElement>) => {
    if (!canvasRef.current || !startPoint) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    setEndPoint({ x, y });
    setIsDrawing(false);
    sendCoordinates(startPoint, { x, y });
  };

  return (
    <div>
      <canvas
        ref={canvasRef}
        onMouseDown={handleMouseDown}
        onMouseUp={handleMouseUp}
        onMouseMove={handleMouseMove}
        width={800}
        height={600}
        style={{ border: "1px solid black" }}
      />
    </div>
  );
};

export default CanvasRectangle;
