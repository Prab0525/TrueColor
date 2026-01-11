import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "TrueColor",
  description: "Find your true shade",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={[
          geistSans.variable,
          geistMono.variable,
          "antialiased",
          "min-h-screen",
          "bg-gradient-to-b from-[#FCE7F3] via-[#FDF2F8] to-white",
          "text-zinc-900",
        ].join(" ")}
      >
        <div className="mx-auto w-full max-w-5xl px-4 py-10">{children}</div>
      </body>
    </html>
  );
}
