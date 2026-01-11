"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";

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

export default function ShadesPage() {
  const [result, setResult] = useState<AnalysisResult | null>(null);

  useEffect(() => {
    // Read the full analysis result from sessionStorage
    const stored = sessionStorage.getItem("analysisResult");
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        console.log("📊 Shades page - Analysis data loaded:", parsed);
        setResult(parsed);
      } catch (err) {
        console.error("Failed to parse analysis result:", err);
      }
    }
  }, []);

  // If no data, show message
  if (!result) {
    return (
      <main className="min-h-screen tc-bg">
        <div className="mx-auto max-w-5xl px-6 py-10">
          <div className="tc-card p-10 text-center">
            <h1 className="text-2xl font-extrabold text-zinc-900">No analysis data found</h1>
            <p className="mt-3 text-zinc-600">
              Please capture and analyze a photo first.
            </p>
            <Link href="/capture" className="tc-btn tc-btn-primary mt-6 inline-block">
              Go to capture
            </Link>
          </div>
        </div>
      </main>
    );
  }

  // Collect all shades - backend returns arrays of shade names (strings)
  const allShades: Array<{ brand: string; brandKey: string; shadeName: string; emoji: string }> = [];
  
  const brandData = [
    { key: 'fenty', name: 'Fenty Beauty', emoji: '💎', shades: result.fenty || [] },
    { key: 'nars', name: 'NARS', emoji: '💄', shades: result.nars || [] },
    { key: 'tooFaced', name: 'Too Faced', emoji: '✨', shades: result.tooFaced || [] },
    { key: 'mac', name: 'MAC', emoji: '🎨', shades: result.mac || [] },
    { key: 'maybelline', name: 'Maybelline', emoji: '💅', shades: result.maybelline || [] },
    { key: 'loreal', name: "L'Oréal", emoji: '🌟', shades: result.loreal || [] },
  ];

  brandData.forEach((brand) => {
    brand.shades.forEach((shadeName) => {
      allShades.push({
        brand: brand.name,
        brandKey: brand.key,
        shadeName,
        emoji: brand.emoji,
      });
    });
  });

  return (
    <main className="min-h-screen tc-bg">
      <div className="mx-auto max-w-5xl px-6 py-10">
        <div className="flex items-center justify-between">
          <Link href="/results" className="text-sm text-pink-500/80 hover:text-pink-600">
            ← Back
          </Link>
          <div className="text-sm text-pink-500/60">TrueColor</div>
        </div>

        <div className="mt-10 text-center">
          <h1 className="tc-title">Your matches</h1>
          <p className="mt-2 text-pink-500/70">
            {allShades.length} foundation shades matched from 6 brands
          </p>
        </div>

        {/* Stats cards */}
        <div className="mt-8 grid gap-4 sm:grid-cols-3 max-w-3xl mx-auto">
          <div className="tc-card p-4 text-center">
            <div className="text-xs font-bold text-pink-600">Undertone</div>
            <div className="text-lg font-extrabold text-zinc-900 mt-1">
              {result.undertone.toUpperCase()}
            </div>
          </div>
          <div className="tc-card p-4 text-center">
            <div className="text-xs font-bold text-pink-600">Pantone Family</div>
            <div className="text-lg font-extrabold text-zinc-900 mt-1">
              {result.pantone_family}
            </div>
          </div>
          <div className="tc-card p-4 text-center">
            <div className="text-xs font-bold text-pink-600">Total Matches</div>
            <div className="text-lg font-extrabold text-zinc-900 mt-1">
              {allShades.length}
            </div>
          </div>
        </div>

        {/* Brand sections */}
        <div className="mt-10 space-y-8">
          {brandData.map((brand) => {
            if (brand.shades.length === 0) return null;
            
            return (
              <div key={brand.key}>
                <h2 className="text-xl font-extrabold text-zinc-900 mb-4">
                  {brand.emoji} {brand.name} <span className="text-pink-600">({brand.shades.length} matches)</span>
                </h2>
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {brand.shades.map((shadeName, idx) => (
                    <div key={idx} className="tc-card p-5">
                      <div className="flex items-center justify-between">
                        <div className="text-sm font-extrabold text-pink-600">
                          {brand.name}
                        </div>
                        <div className="tc-chip">Foundation</div>
                      </div>
                      
                      {/* Shade info */}
                      <div className="mt-4 text-center">
                        <div className="text-lg font-bold text-zinc-900">
                          {shadeName}
                        </div>
                        <div className="mt-2 inline-block rounded-lg bg-pink-100 px-3 py-1.5 text-xs font-extrabold text-pink-700">
                          ✓ Matched
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        {/* Explainer */}
        <div className="mt-10 max-w-3xl mx-auto">
          <div className="tc-card p-6">
            <div className="text-sm font-extrabold text-zinc-900">
              How we match your shades
            </div>
            <div className="mt-2 space-y-2 text-xs text-zinc-700">
              <p>
                We use CIELAB color space and Delta E (ΔE) distance to find the closest foundation shades to your skin tone.
              </p>
              <p>
                Your undertone ({result.undertone}) and Pantone family ({result.pantone_family}) help us narrow down the best matches across all brands.
              </p>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="mt-8 flex flex-wrap justify-center gap-4">
          <Link href="/capture" className="tc-btn tc-btn-primary">
            Analyze another photo
          </Link>
          <Link href="/" className="tc-btn tc-btn-secondary">
            Back to home
          </Link>
        </div>
      </div>
    </main>
  );
}
