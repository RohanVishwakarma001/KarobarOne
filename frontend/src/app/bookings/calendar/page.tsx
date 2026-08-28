"use client";

import Link from "next/link";
import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { toast } from "sonner";
import { CalendarCheck, ChevronLeft, Loader2 } from "lucide-react";
import { CommerceShell } from "@/components/commerce/CommerceShell";
import { ApiError, completeCalendarAuth, getCalendarLoginUrl } from "@/lib/api/github";

function CalendarConnectContent() {
  const searchParams = useSearchParams();
  const code = searchParams.get("code");

  const [connecting, setConnecting] = useState(false);
  const [status, setStatus] = useState<"idle" | "connecting" | "connected" | "failed">("idle");

  useEffect(() => {
    if (!code) return;
    setStatus("connecting");
    // The callback response includes a raw OAuth access token — never surface or log it, just report success/failure.
    completeCalendarAuth(code)
      .then(() => setStatus("connected"))
      .catch((e) => {
        setStatus("failed");
        toast.error(e instanceof ApiError ? e.message : "Could not connect your calendar.");
      });
  }, [code]);

  async function handleConnect() {
    setConnecting(true);
    try {
      const { auth_url } = await getCalendarLoginUrl();
      window.location.href = auth_url;
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not start the calendar connection.");
      setConnecting(false);
    }
  }

  return (
    <CommerceShell title="Calendar" eyebrow="Orders & Payments">
      <div className="mx-auto max-w-2xl px-6 pb-16">
        <Link href="/bookings" className="mb-5 inline-flex items-center gap-1 text-sm font-medium text-gray-500 hover:text-[#5b4ef9]">
          <ChevronLeft className="h-4 w-4" /> Back to bookings
        </Link>

        <div className="rounded-2xl border border-gray-200 bg-white p-8 text-center">
          <span className="mx-auto inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-[#5b4ef9]/10 text-[#5b4ef9]">
            <CalendarCheck className="h-7 w-7" />
          </span>

          {status === "connecting" && (
            <div className="mt-5 flex flex-col items-center gap-2 text-sm text-gray-500">
              <Loader2 className="h-5 w-5 animate-spin" /> Connecting your calendar…
            </div>
          )}

          {status === "connected" && (
            <>
              <h2 className="mt-5 text-lg font-semibold">Calendar connected</h2>
              <p className="mt-2 text-sm text-gray-500">Your bookings and appointments can now sync to your calendar.</p>
            </>
          )}

          {status === "failed" && (
            <>
              <h2 className="mt-5 text-lg font-semibold text-red-600">Connection failed</h2>
              <p className="mt-2 text-sm text-gray-500">Something went wrong while connecting your calendar. Try again below.</p>
            </>
          )}

          {status === "idle" && (
            <>
              <h2 className="mt-5 text-lg font-semibold">Connect your calendar</h2>
              <p className="mt-2 text-sm text-gray-500">Sync bookings and appointments straight to Google Calendar.</p>
            </>
          )}

          {(status === "idle" || status === "failed") && (
            <button
              disabled={connecting}
              onClick={handleConnect}
              className="mt-6 inline-flex items-center gap-2 rounded-lg bg-[#5b4ef9] px-5 py-2.5 text-sm font-medium text-white hover:bg-[#4a3ee0] disabled:opacity-60"
            >
              {connecting ? "Redirecting…" : "Connect Google Calendar"}
            </button>
          )}
        </div>
      </div>
    </CommerceShell>
  );
}

export default function CalendarConnectPage() {
  return (
    <Suspense fallback={null}>
      <CalendarConnectContent />
    </Suspense>
  );
}
