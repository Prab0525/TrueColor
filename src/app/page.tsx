import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-neutral-950 text-white">
      <div className="mx-auto max-w-3xl px-6 py-16">
        <h1 className="text-4xl font-semibold">TrueColor</h1>
        <p className="mt-3 text-white/70">
          Take a photo, we estimate a representative skin tone and suggest
          matching products.
        </p>

        <div className="mt-10 flex gap-3">
          <Link
            href="/capture"
            className="rounded-xl bg-white px-6 py-3 text-sm font-medium text-black"
          >
            Start shade match
          </Link>

          <Link
            href="/capture"
            className="rounded-xl border border-white/15 px-6 py-3 text-sm font-medium text-white/90 hover:bg-white/5"
          >
            Demo flow
          </Link>
        </div>

        <div className="mt-10 rounded-2xl border border-white/10 bg-white/5 p-5 text-sm text-white/70">
          Hackathon MVP plan: upload or capture a face photo → preview → analyze →
          show hex + product cards.
        </div>
      </div>
    </main>
  );
}
