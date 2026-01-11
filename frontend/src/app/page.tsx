import Image from "next/image";
import Link from "next/link";

export default function HomePage() {
  return (
    <main className="tc-bg min-h-screen">
      <div className="mx-auto max-w-5xl px-6 py-14">
        <div className="tc-card p-10 sm:p-14">
          <div className="flex flex-col items-center text-center">
            <Image
              src="/logo-removebg-preview.png"
              alt="logo"
              width={720}
              height={420}
              priority
              className="h-auto w-[320px] sm:w-[420px]"
            />

            <p className="mt-6 max-w-2xl text-base sm:text-lg text-zinc-700">
              Find your perfect shade match in seconds using a quick photo in natural light.
            </p>

            <div className="mt-10 flex flex-col gap-3 sm:flex-row">
              <Link
                href="/capture"
                className="tc-btn tc-btn-primary w-full sm:w-auto"
              >
                Let&apos;s find your True Colour
              </Link>
            </div>

            <div className="mt-10 flex flex-wrap justify-center gap-2">
              <span className="tc-chip">Natural light tips</span>
              <span className="tc-chip">Undertone aware</span>
              <span className="tc-chip">Brand matches</span>
            </div>
          </div>
        </div>

        <p className="mt-6 text-center text-xs text-zinc-500">
          Tip: avoid flash and heavy filters for the best match.
        </p>
      </div>
    </main>
  );
}
