"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense, useEffect, useState } from "react";

interface AnalysisResult {
  undertone: string;
  pantone_family: string;
  skinLAB: [number, number, number];
  colors: {
    combined: [number, number, number];
    l_channel: [number, number, number];
    a_channel: [number, number, number];
    b_channel: [number, number, number];
  };
  fenty: string[];
  nars: string[];
  tooFaced: string[];
  mac: string[];
  maybelline: string[];
  loreal: string[];
}

function ResultsContent() {
  const searchParams = useSearchParams();
  // Add # prefix to hex colors from URL params
  const perfect = `#${searchParams.get("perfect") || "FFFFFF"}`;
  const l = `#${searchParams.get("l") || "FFFFFF"}`;
  const a = `#${searchParams.get("a") || "FFFFFF"}`;
  const b = `#${searchParams.get("b") || "FFFFFF"}`;

  const [analysisData, setAnalysisData] = useState<AnalysisResult | null>(null);

  useEffect(() => {
    // Read the full analysis result from sessionStorage
    const stored = sessionStorage.getItem("analysisResult");
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        console.log("📊 Analysis data loaded:", parsed);
        setAnalysisData(parsed);
      } catch (err) {
        console.error("Failed to parse analysis result:", err);
      }
    }
  }, []);

  // Extract LAB values from array
  const [L, A, B] = analysisData?.skinLAB || [0, 0, 0];

  return (
    <main className="min-h-screen">
      <div className="mx-auto w-full max-w-4xl px-6 py-8">
        {/* top nav */}
        <div className="flex items-center justify-between">
          <Link href="/capture" className="text-sm font-semibold text-pink-600 hover:text-pink-700">
            ← Back
          </Link>
          <div className="tc-chip">TrueColor</div>
        </div>

        {/* header */}
        <div className="mt-10 text-center">
          <h1 className="tc-h1">Your True Colour</h1>
          <p className="tc-subtitle">
            Here's your skin tone broken down by L, A, B colour channels. Pretty cool, right?
          </p>
        </div>

        {/* main card */}
        <div className="mt-10">
          <section className="tc-card mx-auto max-w-3xl p-6 sm:p-8">
            {/* combined color */}
            <div className="text-center">
              <div className="tc-chip mx-auto">Perfect match</div>
              <div className="mt-6 flex justify-center">
                <div className="relative">
                  <div
                    className="tc-main-circle"
                    style={{ backgroundColor: perfect }}
                  />
                  <div className="absolute inset-0 rounded-full ring-4 ring-pink-500/20 ring-offset-4 ring-offset-white/60" />
                </div>
              </div>
              <div className="mt-4 text-sm font-bold text-zinc-700">
                {perfect}
              </div>
            </div>

            <div className="my-8 h-px bg-gradient-to-r from-transparent via-pink-200 to-transparent" />

            {/* L, A, B channels */}
            <div className="grid gap-6 sm:grid-cols-3">
              {/* L channel */}
              <div className="text-center">
                <div className="tc-chip mx-auto">L · Lightness</div>
                <div className="mt-4 flex justify-center">
                  <div
                    className="w-20 h-20 rounded-full border-2 border-zinc-300 shadow-md"
                    style={{ backgroundColor: l }}
                  />
                </div>
                <div className="mt-3 text-xs font-semibold text-zinc-600">
                  {l}
                </div>
              </div>

              {/* A channel */}
              <div className="text-center">
                <div className="tc-chip mx-auto">A · Red/Green</div>
                <div className="mt-4 flex justify-center">
                  <div
                    className="w-20 h-20 rounded-full border-2 border-zinc-300 shadow-md"
                    style={{ backgroundColor: a }}
                  />
                </div>
                <div className="mt-3 text-xs font-semibold text-zinc-600">
                  {a}
                </div>
              </div>

              {/* B channel */}
              <div className="text-center">
                <div className="tc-chip mx-auto">B · Blue/Yellow</div>
                <div className="mt-4 flex justify-center">
                  <div
                    className="w-20 h-20 rounded-full border-2 border-zinc-300 shadow-md"
                    style={{ backgroundColor: b }}
                  />
                </div>
                <div className="mt-3 text-xs font-semibold text-zinc-600">
                  {b}
                </div>
              </div>
            </div>

            {/* LAB Values from backend */}
            {analysisData && (
              <div className="mt-8 rounded-2xl border border-pink-200/60 bg-white/60 p-5">
                <div className="text-sm font-extrabold text-zinc-900 text-center mb-4">
                  📊 LAB Color Values (CIELAB Format)
                </div>
                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className="text-xs font-bold text-pink-600">L</div>
                    <div className="text-2xl font-extrabold text-zinc-900">
                      {L.toFixed(1)}
                    </div>
                    <div className="text-xs text-zinc-600">Lightness (0-100)</div>
                  </div>
                  <div className="text-center">
                    <div className="text-xs font-bold text-pink-600">A</div>
                    <div className="text-2xl font-extrabold text-zinc-900">
                      {A.toFixed(1)}
                    </div>
                    <div className="text-xs text-zinc-600">Green(-) to Red(+)</div>
                  </div>
                  <div className="text-center">
                    <div className="text-xs font-bold text-pink-600">B</div>
                    <div className="text-2xl font-extrabold text-zinc-900">
                      {B.toFixed(1)}
                    </div>
                    <div className="text-xs text-zinc-600">Blue(-) to Yellow(+)</div>
                  </div>
                </div>
              </div>
            )}

            {/* Undertone & Pantone */}
            {analysisData && (
              <div className="mt-6 grid grid-cols-2 gap-4">
                <div className="text-center rounded-2xl border border-pink-200/60 bg-white/60 p-4">
                  <div className="text-xs font-bold text-pink-600">Undertone</div>
                  <div className="text-lg font-extrabold text-zinc-900 mt-1">
                    {analysisData.undertone.toUpperCase()}
                  </div>
                </div>
                <div className="text-center rounded-2xl border border-pink-200/60 bg-white/60 p-4">
                  <div className="text-xs font-bold text-pink-600">Pantone Family</div>
                  <div className="text-lg font-extrabold text-zinc-900 mt-1">
                    {analysisData.pantone_family}
                  </div>
                </div>
              </div>
            )}

            {/* explainer */}
            <div className="mt-8 rounded-2xl border border-pink-200/60 bg-white/60 p-5">
              <div className="text-sm font-extrabold text-zinc-900">
                What are L, A, B?
              </div>
              <div className="mt-2 space-y-2 text-xs text-zinc-700">
                <p>
                  <span className="font-bold">L</span> = Lightness. How bright
                  or dark your skin tone is (0–100).
                </p>
                <p>
                  <span className="font-bold">A</span> = Red/Green axis. Positive
                  means red undertone, negative means green.
                </p>
                <p>
                  <span className="font-bold">B</span> = Blue/Yellow axis. Positive
                  means yellow undertone, negative means blue.
                </p>
              </div>
            </div>

            {/* Foundation Matches Preview */}
            {analysisData && (
              <div className="mt-8 rounded-2xl border border-pink-200/60 bg-white/60 p-5">
                <div className="text-sm font-extrabold text-zinc-900 text-center mb-4">
                  💄 Your Foundation Matches
                </div>
                <div className="space-y-3">
                  {analysisData.fenty?.length > 0 && (
                    <div className="flex items-center justify-between text-xs">
                      <div className="font-bold text-zinc-700">💎 Fenty Beauty</div>
                      <div className="text-pink-600 font-semibold">{analysisData.fenty.length} matches</div>
                    </div>
                  )}
                  {analysisData.nars?.length > 0 && (
                    <div className="flex items-center justify-between text-xs">
                      <div className="font-bold text-zinc-700">💄 NARS</div>
                      <div className="text-pink-600 font-semibold">{analysisData.nars.length} matches</div>
                    </div>
                  )}
                  {analysisData.tooFaced?.length > 0 && (
                    <div className="flex items-center justify-between text-xs">
                      <div className="font-bold text-zinc-700">✨ Too Faced</div>
                      <div className="text-pink-600 font-semibold">{analysisData.tooFaced.length} matches</div>
                    </div>
                  )}
                  {analysisData.mac?.length > 0 && (
                    <div className="flex items-center justify-between text-xs">
                      <div className="font-bold text-zinc-700">🎨 MAC</div>
                      <div className="text-pink-600 font-semibold">{analysisData.mac.length} matches</div>
                    </div>
                  )}
                  {analysisData.maybelline?.length > 0 && (
                    <div className="flex items-center justify-between text-xs">
                      <div className="font-bold text-zinc-700">💅 Maybelline</div>
                      <div className="text-pink-600 font-semibold">{analysisData.maybelline.length} matches</div>
                    </div>
                  )}
                  {analysisData.loreal?.length > 0 && (
                    <div className="flex items-center justify-between text-xs">
                      <div className="font-bold text-zinc-700">🌟 L'Oréal</div>
                      <div className="text-pink-600 font-semibold">{analysisData.loreal.length} matches</div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* CTA */}
            <div className="mt-6 text-center">
              <Link href="/shades" className="tc-btn tc-btn-primary inline-block">
                See all your shades
              </Link>
            </div>
          </section>
        </div>

        {/* footer spacing */}
        <div className="h-10" />
      </div>
    </main>
  );
}

export default function ResultsPage() {
  return (
    <Suspense
      fallback={
        <div className="grid min-h-screen place-items-center text-pink-600">
          Loading...
        </div>
      }
    >
      <ResultsContent />
    </Suspense>
  );
}
