"use client";

import Link from "next/link";
import { use, useCallback, useEffect, useState } from "react";
import { toast } from "sonner";
import { ChevronLeft, Loader2, XCircle, Star, RotateCcw } from "lucide-react";
import { CommerceShell } from "@/components/commerce/CommerceShell";
import {
  ApiError,
  type Booking,
  type BookingCancellation,
  type BookingRefund,
  type BookingFeedback,
  getBooking,
  listBookingCancellations,
  listBookingRefunds,
  listBookingFeedbacks,
  createBookingCancellation,
  createBookingFeedback,
} from "@/lib/api/github";
import { useCustomerSession } from "@/hooks/use-customer-session";

const money = (value: number) => `₹${value.toLocaleString("en-IN")}`;

const statusClass = (s: string) =>
  s === "COMPLETED"
    ? "bg-green-50 text-green-700"
    : s === "CANCELLED" || s === "REJECTED" || s === "NO_SHOW"
    ? "bg-red-50 text-red-700"
    : s === "CONFIRMED" || s === "APPROVED"
    ? "bg-blue-50 text-blue-700"
    : s === "REFUNDED"
    ? "bg-gray-100 text-gray-700"
    : "bg-amber-50 text-amber-700";

const CANCELLABLE_STATUSES = ["PENDING", "CONFIRMED", "APPROVED"];

export default function BookingDetailPage({ params }: { params: Promise<{ bookingId: string }> }) {
  const { bookingId } = use(params);
  const { customerId } = useCustomerSession();

  const [booking, setBooking] = useState<Booking | null>(null);
  const [cancellation, setCancellation] = useState<BookingCancellation | null>(null);
  const [refunds, setRefunds] = useState<BookingRefund[]>([]);
  const [feedback, setFeedback] = useState<BookingFeedback | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [showCancelForm, setShowCancelForm] = useState(false);
  const [cancelReason, setCancelReason] = useState("");
  const [cancelDescription, setCancelDescription] = useState("");
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [rating, setRating] = useState(5);
  const [reviewTitle, setReviewTitle] = useState("");
  const [reviewText, setReviewText] = useState("");
  const [actionBusy, setActionBusy] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [b, allCancellations, allRefunds, allFeedbacks] = await Promise.all([
        getBooking(bookingId),
        listBookingCancellations(),
        listBookingRefunds(),
        listBookingFeedbacks(),
      ]);
      setBooking(b);
      setCancellation(allCancellations.find((c) => c.booking_id === bookingId) ?? null);
      setRefunds(allRefunds.filter((r) => r.booking_id === bookingId));
      setFeedback(allFeedbacks.find((f) => f.booking_id === bookingId) ?? null);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Could not load this booking.");
    } finally {
      setLoading(false);
    }
  }, [bookingId]);

  useEffect(() => {
    load();
  }, [load]);

  async function handleCancel(e: React.FormEvent) {
    e.preventDefault();
    if (!cancelReason.trim()) {
      toast.error("Enter a cancellation reason.");
      return;
    }
    setActionBusy(true);
    try {
      const rec = await createBookingCancellation({
        booking_id: bookingId,
        cancellation_reason: cancelReason.trim(),
        cancellation_reason_description: cancelDescription.trim() || undefined,
        requested_by: customerId ?? undefined,
      });
      setCancellation(rec);
      setShowCancelForm(false);
      toast.success("Cancellation requested.");
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Could not request cancellation.");
    } finally {
      setActionBusy(false);
    }
  }

  async function handleFeedback(e: React.FormEvent) {
    e.preventDefault();
    if (!customerId) return;
    setActionBusy(true);
    try {
      const rec = await createBookingFeedback({
        booking_id: bookingId,
        customer_id: customerId,
        rating,
        review_title: reviewTitle.trim() || undefined,
        review_text: reviewText.trim() || undefined,
      });
      setFeedback(rec);
      setShowFeedbackForm(false);
      toast.success("Thanks for your feedback.");
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Could not submit feedback.");
    } finally {
      setActionBusy(false);
    }
  }

  return (
    <CommerceShell title={booking ? booking.booking_number : "Booking"} eyebrow="Orders & Payments">
      <div className="mx-auto max-w-7xl px-6">
        <Link href="/bookings" className="mb-5 inline-flex items-center gap-1 text-sm font-medium text-gray-500 hover:text-[#5b4ef9]">
          <ChevronLeft className="h-4 w-4" /> Back to bookings
        </Link>

        {loading && (
          <div className="flex items-center justify-center gap-2 rounded-2xl border border-gray-200 bg-white px-6 py-16 text-sm text-gray-500">
            <Loader2 className="h-4 w-4 animate-spin" /> Loading booking…
          </div>
        )}

        {!loading && error && <div className="rounded-2xl border border-gray-200 bg-white px-6 py-16 text-center font-medium text-red-600">{error}</div>}

        {!loading && !error && booking && (
          <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
            <div className="space-y-6">
              <section className="rounded-2xl border border-gray-200 bg-white p-5">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <h2 className="font-semibold">{booking.booking_number}</h2>
                    <p className="mt-1 text-sm text-gray-500">
                      {booking.booking_date} · {booking.start_time.slice(0, 5)}–{booking.end_time.slice(0, 5)}
                    </p>
                  </div>
                  <div className="flex gap-2">
                    <span className={`rounded-full px-2.5 py-1 text-xs font-medium ${statusClass(booking.booking_status)}`}>{booking.booking_status}</span>
                    <span className="rounded-full bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-700">{booking.payment_status}</span>
                  </div>
                </div>
                <div className="mt-4 grid grid-cols-2 gap-3 text-sm text-gray-600 sm:grid-cols-3">
                  <p>Mode: {booking.booking_mode}</p>
                  <p>Attendees: {booking.attendee_count}</p>
                  {booking.booking_note && <p className="col-span-2 sm:col-span-3">Note: {booking.booking_note}</p>}
                </div>
              </section>

              {cancellation && (
                <section className="rounded-2xl border border-red-100 bg-red-50/40 p-5">
                  <h2 className="font-semibold text-red-700">Cancellation</h2>
                  <p className="mt-1 text-sm text-red-700/80">{cancellation.cancellation_reason}</p>
                  {cancellation.cancellation_reason_description && <p className="mt-1 text-sm text-red-700/70">{cancellation.cancellation_reason_description}</p>}
                  <p className="mt-1 text-xs text-red-700/60">Status: {cancellation.status}</p>
                </section>
              )}

              {refunds.length > 0 && (
                <section className="rounded-2xl border border-gray-200 bg-white p-5">
                  <h2 className="font-semibold">Refunds</h2>
                  <div className="mt-3 space-y-3">
                    {refunds.map((r) => (
                      <div key={r.id} className="flex items-center justify-between rounded-lg border border-gray-100 px-4 py-3 text-sm">
                        <div>
                          <p className="font-medium">{money(r.refund_amount)}</p>
                          <p className="mt-0.5 text-gray-500">{r.refund_reason}</p>
                        </div>
                        <span className="rounded-full bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-700">{r.refund_status}</span>
                      </div>
                    ))}
                  </div>
                </section>
              )}

              {booking.booking_status === "COMPLETED" && (
                <section className="rounded-2xl border border-gray-200 bg-white p-5">
                  <h2 className="font-semibold">Feedback</h2>
                  {feedback ? (
                    <div className="mt-3">
                      <div className="flex items-center gap-1">
                        {Array.from({ length: 5 }).map((_, i) => (
                          <Star key={i} className={`h-4 w-4 ${i < feedback.rating ? "fill-amber-400 text-amber-400" : "text-gray-200"}`} />
                        ))}
                      </div>
                      {feedback.review_title && <p className="mt-2 text-sm font-medium">{feedback.review_title}</p>}
                      {feedback.review_text && <p className="mt-1 text-sm text-gray-600">{feedback.review_text}</p>}
                    </div>
                  ) : !showFeedbackForm ? (
                    <button
                      onClick={() => setShowFeedbackForm(true)}
                      className="mt-3 inline-flex items-center gap-2 rounded-lg border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:border-[#5b4ef9]/40 hover:text-[#5b4ef9]"
                    >
                      <Star className="h-4 w-4" /> Leave feedback
                    </button>
                  ) : (
                    <form onSubmit={handleFeedback} className="mt-3 space-y-3">
                      <div className="flex items-center gap-1">
                        {Array.from({ length: 5 }).map((_, i) => (
                          <button key={i} type="button" onClick={() => setRating(i + 1)}>
                            <Star className={`h-6 w-6 ${i < rating ? "fill-amber-400 text-amber-400" : "text-gray-200"}`} />
                          </button>
                        ))}
                      </div>
                      <input
                        className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm outline-none focus:border-[#5b4ef9]"
                        placeholder="Title (optional)"
                        value={reviewTitle}
                        onChange={(e) => setReviewTitle(e.target.value)}
                      />
                      <textarea
                        rows={3}
                        className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm outline-none focus:border-[#5b4ef9]"
                        placeholder="Tell us about your experience (optional)"
                        value={reviewText}
                        onChange={(e) => setReviewText(e.target.value)}
                      />
                      <div className="flex gap-2">
                        <button disabled={actionBusy} type="submit" className="flex-1 rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white disabled:opacity-60">
                          {actionBusy ? "Submitting…" : "Submit feedback"}
                        </button>
                        <button type="button" onClick={() => setShowFeedbackForm(false)} className="rounded-lg px-4 py-2 text-sm text-gray-500">
                          Back
                        </button>
                      </div>
                    </form>
                  )}
                </section>
              )}
            </div>

            <aside className="h-fit space-y-4 rounded-2xl border border-gray-200 bg-white p-5 lg:sticky lg:top-28">
              <h2 className="font-semibold">Booking total</h2>
              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex justify-between">
                  <span>Subtotal</span>
                  <span>{money(booking.subtotal_amount)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Discount</span>
                  <span>-{money(booking.discount_amount)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Tax</span>
                  <span>{money(booking.tax_amount)}</span>
                </div>
                <div className="border-t border-gray-100 pt-2">
                  <div className="flex justify-between text-base font-semibold text-gray-900">
                    <span>Total</span>
                    <span>{money(booking.total_amount)}</span>
                  </div>
                </div>
              </div>

              {CANCELLABLE_STATUSES.includes(booking.booking_status) && !cancellation && (
                <div className="border-t border-gray-100 pt-4">
                  {!showCancelForm ? (
                    <button
                      onClick={() => setShowCancelForm(true)}
                      className="inline-flex w-full items-center justify-center gap-2 rounded-lg border border-red-200 px-4 py-2.5 text-sm font-medium text-red-600 hover:bg-red-50"
                    >
                      <XCircle className="h-4 w-4" /> Cancel booking
                    </button>
                  ) : (
                    <form onSubmit={handleCancel} className="space-y-2">
                      <input
                        className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm outline-none focus:border-[#5b4ef9]"
                        placeholder="Reason"
                        value={cancelReason}
                        onChange={(e) => setCancelReason(e.target.value)}
                      />
                      <textarea
                        className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm outline-none focus:border-[#5b4ef9]"
                        rows={2}
                        placeholder="More detail (optional)"
                        value={cancelDescription}
                        onChange={(e) => setCancelDescription(e.target.value)}
                      />
                      <div className="flex gap-2">
                        <button disabled={actionBusy} type="submit" className="flex-1 rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-60">
                          {actionBusy ? "Requesting…" : "Confirm cancellation"}
                        </button>
                        <button type="button" onClick={() => setShowCancelForm(false)} className="rounded-lg px-4 py-2 text-sm text-gray-500">
                          Back
                        </button>
                      </div>
                    </form>
                  )}
                </div>
              )}

              {cancellation && (
                <div className="flex items-center gap-2 border-t border-gray-100 pt-4 text-sm text-gray-500">
                  <RotateCcw className="h-4 w-4" /> Cancellation {cancellation.status.toLowerCase()}
                </div>
              )}
            </aside>
          </div>
        )}
      </div>
    </CommerceShell>
  );
}
