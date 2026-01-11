"use client";

import React, { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

type Mode = "idle" | "camera" | "preview";

// Backend API response types
interface ColorVisualization {
  combined: [number, number, number];
  l_channel: [number, number, number];
  a_channel: [number, number, number];
  b_channel: [number, number, number];
}

interface AnalysisResult {
  skinLAB: [number, number, number];
  undertone: string;
  pantone_family: string;
  fenty: string[];
  nars: string[];
  tooFaced: string[];
  mac: string[];
  maybelline: string[];
  loreal: string[];
  colors: ColorVisualization;
}

export default function CapturePage() {
  const router = useRouter();
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
      // First stop any existing camera
      stopCamera();

      // Check if mediaDevices is supported
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert("Your browser doesn't support camera access. Please use Chrome, Firefox, or Edge.");
        return;
      }

      console.log("📸 Requesting camera permission...");

      // Request camera access with simpler constraints first
      const s = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false,
      });

      console.log("✅ Camera permission granted!");

      // Set mode to "camera" so the video element renders
      setMode("camera");
      setStream(s);

      // Wait a tick for React to render the video element
      await new Promise(resolve => setTimeout(resolve, 100));

      const video = videoRef.current;
      if (!video) {
        console.error("Video element not found after render!");
        s.getTracks().forEach(track => track.stop());
        alert("Video element not ready. Please try again.");
        setMode("idle");
        setStream(null);
        return;
      }

      // Attach stream to video element
      video.srcObject = s;

      // Wait for video metadata to load
      await new Promise<void>((resolve, reject) => {
        const timeout = setTimeout(() => reject(new Error("Video metadata timeout")), 5000);
        video.onloadedmetadata = () => {
          clearTimeout(timeout);
          console.log("📹 Video metadata loaded");
          resolve();
        };
      });

      // Play the video
      console.log("▶️ Starting video playback...");
      await video.play();
      
      // Give camera a moment to warm up
      await new Promise(resolve => setTimeout(resolve, 500));

      console.log("✅ Camera ready - size:", video.videoWidth, "x", video.videoHeight);

    } catch (err: any) {
      console.error("❌ Camera error:", err);
      
      // Reset state on error
      setMode("idle");
      setStream(null);
      
      let errorMessage = "Camera failed to start. ";
      
      if (err.name === "NotAllowedError" || err.name === "PermissionDeniedError") {
        errorMessage += "Camera permission was denied. Please allow camera access in your browser settings.";
      } else if (err.name === "NotFoundError" || err.name === "DevicesNotFoundError") {
        errorMessage += "No camera found on your device.";
      } else if (err.name === "NotReadableError" || err.name === "TrackStartError") {
        errorMessage += "Camera is being used by another application. Close Zoom, Teams, Discord, or other apps using the camera.";
      } else {
        errorMessage += err.message || "Unknown error occurred.";
      }
      
      alert(errorMessage);
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
      // Call REAL backend API
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${apiUrl}/analyze`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Analysis failed");
      }

      // Parse the response
      const result: AnalysisResult = await response.json();
      
      // Helper to convert RGB array to hex
      const rgbToHex = (rgb: [number, number, number]) => {
        const toHex = (n: number) => {
          const hex = Math.round(n).toString(16);
          return hex.length === 1 ? "0" + hex : hex;
        };
        return `${toHex(rgb[0])}${toHex(rgb[1])}${toHex(rgb[2])}`;
      };

      // Convert color visualizations to hex for URL params
      const perfect = rgbToHex(result.colors.combined);
      const l = rgbToHex(result.colors.l_channel);
      const a = rgbToHex(result.colors.a_channel);
      const b = rgbToHex(result.colors.b_channel);

      // Store full result in sessionStorage for shades page
      sessionStorage.setItem('analysisResult', JSON.stringify(result));

      // Navigate to results page with color hex values
      router.push(`/results?perfect=${perfect}&l=${l}&a=${a}&b=${b}`);
      
    } catch (error) {
      console.error("Analysis error:", error);
      alert(`❌ Analysis failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
      setStatus("idle");
    }
  }

  const isAnalyzing = status === "analyzing";

  return (
    <main className="min-h-screen">
      {/* top nav */}
      <div className="mx-auto w-full max-w-4xl px-6 py-8">
        <div className="flex items-center justify-between">
          <Link href="/" className="text-sm font-semibold text-pink-600 hover:text-pink-700">
            ← Back
          </Link>
          <div className="tc-chip">TrueColor</div>
        </div>

        {/* header */}
        <div className="mt-10 text-center">
          <h1 className="tc-h1">
            {mode === "idle" ? "Lets find your true colour" : "Capture a photo"}
          </h1>

          <p className="tc-subtitle">
            {mode === "idle"
              ? "Use natural light if you can. No flash, no filters, no stress."
              : "Start the camera for a live preview, take a photo, or upload from your device."}
          </p>
        </div>

        {/* main card */}
        <div className="mt-10">
          <section className="tc-card mx-auto max-w-3xl p-5 sm:p-7">
            {/* hidden inputs */}
            <input
              ref={uploadInputRef}
              type="file"
              accept="image/*"
              className="hidden"
              onChange={onPickUpload}
            />
            <canvas ref={canvasRef} className="hidden" />

            {/* CONTENT */}
            {mode === "idle" && (
              <div className="grid gap-4 sm:grid-cols-2">
                <button
                  onClick={startCamera}
                  className="group tc-card flex flex-col items-start p-5 text-left transition hover:-translate-y-[1px]"
                >
                  <div className="tc-chip">Option 1</div>
                  <div className="mt-3 text-xl font-extrabold text-zinc-900">
                    Take photo
                  </div>
                  <div className="mt-1 text-sm text-zinc-600">
                    Use your camera for the most accurate match.
                  </div>
                  <div className="mt-4 inline-flex items-center text-sm font-bold text-pink-600">
                    Start camera <span className="ml-1 transition group-hover:translate-x-0.5">→</span>
                  </div>
                </button>

                <button
                  onClick={openUpload}
                  className="group tc-card flex flex-col items-start p-5 text-left transition hover:-translate-y-[1px]"
                >
                  <div className="tc-chip">Option 2</div>
                  <div className="mt-3 text-xl font-extrabold text-zinc-900">
                    Upload photo
                  </div>
                  <div className="mt-1 text-sm text-zinc-600">
                    Pick an existing image from your device.
                  </div>
                  <div className="mt-4 inline-flex items-center text-sm font-bold text-pink-600">
                    Choose file <span className="ml-1 transition group-hover:translate-x-0.5">→</span>
                  </div>
                </button>

                <div className="sm:col-span-2 mt-2 rounded-2xl border border-pink-200/60 bg-white/60 p-4 text-center text-sm text-zinc-700">
                  Pro tip: face a window, keep your camera at eye level, and don't use flash ✨
                </div>
              </div>
            )}

            {mode === "camera" && (
              <div>
                <div className="flex items-center justify-between">
                  <div className="tc-chip">Live camera</div>
                  <button
                    onClick={() => {
                      stopCamera();
                      setMode("idle");
                    }}
                    className="text-sm font-semibold text-pink-600 hover:text-pink-700"
                  >
                    Stop
                  </button>
                </div>

                <div className="mt-5 overflow-hidden rounded-3xl border border-pink-200/60 bg-white/40">
                  <div className="relative">
                    <video
                      ref={videoRef}
                      autoPlay
                      playsInline
                      muted
                      className="h-auto w-full bg-black object-cover"
                    />
                    {/* subtle overlay */}
                    <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-black/10 via-transparent to-white/10" />
                  </div>
                </div>

                <div className="mt-5 flex flex-wrap items-center justify-center gap-3">
                  <button onClick={takePhoto} className="tc-btn tc-btn-primary w-full sm:w-auto">
                    Take photo
                  </button>
                  <button
                    onClick={openUpload}
                    className="tc-btn tc-btn-secondary w-full sm:w-auto"
                  >
                    Upload instead
                  </button>
                </div>

                <p className="mt-4 text-center text-xs text-zinc-600">
                  If the preview is black: close Zoom/Teams/Discord and refresh. On macOS, the
                  camera can be held by another app.
                </p>
              </div>
            )}

            {mode === "preview" && (
              <div>
                <div className="flex items-center justify-between">
                  <div className="tc-chip">Preview</div>
                  <button
                    onClick={clearAll}
                    className="text-sm font-semibold text-pink-600 hover:text-pink-700"
                    disabled={isAnalyzing}
                  >
                    Clear
                  </button>
                </div>

                {/* preview */}
                <div className="mt-5 overflow-hidden rounded-3xl border border-pink-200/60 bg-white/40">
                  {!previewUrl ? (
                    <div className="grid place-items-center p-10 text-zinc-500">
                      No image yet. Start camera or upload.
                    </div>
                  ) : (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img src={previewUrl} alt="Preview" className="h-auto w-full object-cover" />
                  )}
                </div>

                {/* actions */}
                <div className="mt-5 grid gap-3 sm:grid-cols-3">
                  <button
                    onClick={startCamera}
                    className="tc-btn tc-btn-secondary"
                    disabled={isAnalyzing}
                  >
                    Retake
                  </button>

                  <button
                    onClick={openUpload}
                    className="tc-btn tc-btn-secondary"
                    disabled={isAnalyzing}
                  >
                    Choose another
                  </button>

                  <button
                    onClick={onAnalyze}
                    disabled={!file || isAnalyzing}
                    className="tc-btn tc-btn-primary"
                  >
                    {isAnalyzing ? "Analyzing..." : "Analyze"}
                  </button>
                </div>

                {/* analyzing screen */}
                {isAnalyzing && (
                  <div className="mt-6 rounded-3xl border border-pink-200/60 bg-white/60 p-6">
                    <div className="text-center">
                      <div className="mx-auto inline-flex items-center gap-2 rounded-full bg-pink-100 px-4 py-2 text-sm font-extrabold text-pink-700">
                        Finding your True colour
                        <span className="inline-flex gap-1">
                          <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-pink-500 [animation-delay:0ms]" />
                          <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-pink-500 [animation-delay:120ms]" />
                          <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-pink-500 [animation-delay:240ms]" />
                        </span>
                      </div>

                      <p className="mt-3 text-sm text-zinc-600">
                        Matching undertone, depth, and closest product shades ✨
                      </p>

                      {/* shimmer bar */}
                      <div className="mt-5 overflow-hidden rounded-full bg-pink-100">
                        <div className="h-3 w-1/2 animate-[tc-shimmer_1.2s_infinite] rounded-full bg-gradient-to-r from-pink-400 via-pink-200 to-pink-400" />
                      </div>

                      <p className="mt-3 text-xs text-zinc-500">
                        Analyzing your skin tone with AI-powered face detection...
                      </p>
                    </div>
                  </div>
                )}
              </div>
            )}
          </section>
        </div>

        {/* footer spacing */}
        <div className="h-10" />
      </div>

      {/* local keyframes */}
      <style jsx global>{`
        @keyframes tc-shimmer {
          0% {
            transform: translateX(-40%);
          }
          100% {
            transform: translateX(140%);
          }
        }
      `}</style>
    </main>
  );
}
