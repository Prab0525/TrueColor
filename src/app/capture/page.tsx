"use client";

import React, { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";

type Mode = "idle" | "camera" | "preview";

export default function CapturePage() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const uploadInputRef = useRef<HTMLInputElement | null>(null);

  const [mode, setMode] = useState<Mode>("idle");
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "analyzing">("idle");

  const previewUrl = useMemo(() => {
    if (!file) return null;
    return URL.createObjectURL(file);
  }, [file]);

  function stopCamera() {
    if (stream) {
      stream.getTracks().forEach((t) => t.stop());
    }
    setStream(null);
    const video = videoRef.current;
    if (video) video.srcObject = null;
  }

  async function startCamera() {
    try {
      stopCamera();

      // On Mac Chrome, this is more reliable than facingMode constraints
      const s = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false,
      });

      const video = videoRef.current;
      if (!video) {
        setStream(s);
        setMode("camera");
        return;
      }

      video.srcObject = s;

      // Wait until the video element knows its size
      await new Promise<void>((resolve) => {
        video.onloadedmetadata = () => resolve();
      });

      // Try to play (should work because startCamera is triggered by a click)
      await video.play();

      // Debug: proves frames are coming in
      console.log("video size:", video.videoWidth, video.videoHeight);

      setStream(s);
      setMode("camera");
    } catch (err) {
      console.error(err);
      alert(
        "Camera failed to start. Check Chrome camera permissions or close other apps using the camera."
      );
    }
  }

  async function takePhoto() {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return;

    const w = video.videoWidth;
    const h = video.videoHeight;

    if (!w || !h) {
      alert("Camera not ready yet. Try again in a second.");
      return;
    }

    canvas.width = w;
    canvas.height = h;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.drawImage(video, 0, 0, w, h);

    const blob = await new Promise<Blob | null>((resolve) =>
      canvas.toBlob(resolve, "image/jpeg", 0.92)
    );

    if (!blob) {
      alert("Could not capture image.");
      return;
    }

    const captured = new File([blob], "capture.jpg", { type: "image/jpeg" });
    setFile(captured);
    setMode("preview");
    stopCamera();
  }

  function openUpload() {
    uploadInputRef.current?.click();
  }

  function onPickUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const picked = e.target.files?.[0] ?? null;
    if (!picked) return;

    setFile(picked);
    setMode("preview");
    stopCamera();
  }

  function clearAll() {
    setFile(null);
    setMode("idle");
    stopCamera();
    if (uploadInputRef.current) uploadInputRef.current.value = "";
  }

  async function onAnalyze() {
    if (!file) return;
    setStatus("analyzing");
    try {
      await new Promise((r) => setTimeout(r, 800));
      alert("Analysis placeholder ✅ Next step: upload to backend and get hex.");
    } finally {
      setStatus("idle");
    }
  }

  useEffect(() => {
    return () => {
      stopCamera();
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main className="min-h-screen bg-neutral-950 text-white">
      <div className="mx-auto max-w-3xl px-6 py-10">
        <div className="flex items-center justify-between">
          <Link href="/" className="text-sm text-white/70 hover:text-white">
            ← Back
          </Link>
          <div className="text-sm text-white/50">TrueColor</div>
        </div>

        <h1 className="mt-6 text-3xl font-semibold">Capture a photo</h1>
        <p className="mt-2 text-white/70">
          Start the camera for a live preview, take a photo, or upload from your device.
        </p>

        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          <button
            onClick={startCamera}
            className="rounded-2xl border border-white/10 bg-white/5 px-5 py-4 text-left hover:bg-white/10"
          >
            <div className="text-lg font-medium">Start camera</div>
            <div className="mt-1 text-sm text-white/60">
              Live preview will appear below
            </div>
          </button>

          <button
            onClick={openUpload}
            className="rounded-2xl border border-white/10 bg-white/5 px-5 py-4 text-left hover:bg-white/10"
          >
            <div className="text-lg font-medium">Upload from device</div>
            <div className="mt-1 text-sm text-white/60">
              Choose an existing image
            </div>
          </button>
        </div>

        <input
          ref={uploadInputRef}
          type="file"
          accept="image/*"
          className="hidden"
          onChange={onPickUpload}
        />

        <canvas ref={canvasRef} className="hidden" />

        <section className="mt-8 rounded-2xl border border-white/10 bg-white/5 p-4">
          <div className="flex items-center justify-between">
            <div className="text-sm text-white/70">
              {mode === "camera" ? "Live camera" : "Preview"}
            </div>

            {mode === "camera" ? (
              <button
                onClick={() => {
                  stopCamera();
                  setMode("idle");
                }}
                className="text-sm text-white/70 hover:text-white"
              >
                Stop
              </button>
            ) : file ? (
              <button onClick={clearAll} className="text-sm text-white/70 hover:text-white">
                Clear
              </button>
            ) : null}
          </div>

          {mode === "camera" ? (
            <div className="mt-4 overflow-hidden rounded-xl border border-white/10">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="h-auto w-full bg-black object-cover"
              />
            </div>
          ) : !previewUrl ? (
            <div className="mt-4 grid place-items-center rounded-xl border border-dashed border-white/15 bg-black/20 p-10 text-white/50">
              No image yet. Start camera or upload.
            </div>
          ) : (
            <div className="mt-4 overflow-hidden rounded-xl border border-white/10">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={previewUrl} alt="Preview" className="h-auto w-full object-cover" />
            </div>
          )}

          <div className="mt-4 flex flex-wrap gap-3">
            {mode === "camera" ? (
              <button
                onClick={takePhoto}
                className="rounded-xl bg-white px-5 py-3 text-sm font-medium text-black"
              >
                Take photo
              </button>
            ) : (
              <>
                <button
                  onClick={onAnalyze}
                  disabled={!file || status === "analyzing"}
                  className="rounded-xl bg-white px-5 py-3 text-sm font-medium text-black disabled:opacity-40"
                >
                  {status === "analyzing" ? "Analyzing..." : "Analyze"}
                </button>

                <button
                  onClick={openUpload}
                  className="rounded-xl border border-white/15 px-5 py-3 text-sm font-medium text-white/90 hover:bg-white/5"
                >
                  Upload another
                </button>

                <button
                  onClick={startCamera}
                  className="rounded-xl border border-white/15 px-5 py-3 text-sm font-medium text-white/90 hover:bg-white/5"
                >
                  Use camera
                </button>
              </>
            )}
          </div>

          <p className="mt-4 text-xs text-white/50">
            If the preview is black: close Zoom/Teams/Discord and refresh. On macOS,
            camera can be held by another app.
          </p>
        </section>
      </div>
    </main>
  );
}
