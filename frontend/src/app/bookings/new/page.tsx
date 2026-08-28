"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { toast } from "sonner";
import { ChevronLeft } from "lucide-react";
import { CommerceShell } from "@/components/commerce/CommerceShell";
import { useCustomerSession } from "@/hooks/use-customer-session";
import { ApiError, type BookingMode, createBooking } from "@/lib/api/github";

export default function NewBookingPage() {
  const router = useRouter();
  const { customerId, ready } = useCustomerSession();

  const [serviceId, setServiceId] = useState("");
  const [bookingMode, setBookingMode] = useState<BookingMode>("BOOK_AND_PAY");
  const [bookingDate, setBookingDate] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [attendeeCount, setAttendeeCount] = useState(1);
  const [subtotal, setSubtotal] = useState(0);
  const [discount, setDiscount] = useState(0);
  const [tax, setTax] = useState(0);
  const [note, setNote] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!customerId) return;
    if (!serviceId.trim()) {
      toast.error("Enter a service id.");
      return;
    }
    if (!bookingDate || !startTime || !endTime) {
      toast.error("Pick a date and a start/end time.");
      return;
    }
    if (startTime >= endTime) {
      toast.error("Start time must be before end time.");
      return;
    }

    setSubmitting(true);
    try {
      const booking = await createBooking({
        service_id: serviceId.trim(),
        customer_id: customerId,
        booking_mode: bookingMode,
        booking_date: bookingDate,
        start_time: `${startTime}:00`,
        end_time: `${endTime}:00`,
        attendee_count: attendeeCount,
        subtotal_amount: subtotal,
        discount_amount: discount,
        tax_amount: tax,
        booking_note: note.trim() || undefined,
      });
      toast.success("Booking created.");
      router.push(`/bookings/${booking.id}`);
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Could not create this booking.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <CommerceShell title="New booking" eyebrow="Orders & Payments">
      <div className="mx-auto max-w-2xl px-6 pb-16">
        <Link href="/bookings" className="mb-5 inline-flex items-center gap-1 text-sm font-medium text-gray-500 hover:text-[#5b4ef9]">
          <ChevronLeft className="h-4 w-4" /> Back to bookings
        </Link>

        <form onSubmit={handleSubmit} className="space-y-5 rounded-2xl border border-gray-200 bg-white p-6">
          <div>
            <label className="mb-1.5 block text-sm font-medium text-gray-700">Service ID</label>
            <input
              className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
              placeholder="Service ID (UUID) — no service catalog wired up yet"
              value={serviceId}
              onChange={(e) => setServiceId(e.target.value)}
            />
          </div>

          <div>
            <label className="mb-1.5 block text-sm font-medium text-gray-700">Booking mode</label>
            <select
              className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
              value={bookingMode}
              onChange={(e) => setBookingMode(e.target.value as BookingMode)}
            >
              <option value="BOOK_AND_PAY">Book and pay</option>
              <option value="BOOK_ONLY">Book only</option>
            </select>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div>
              <label className="mb-1.5 block text-sm font-medium text-gray-700">Date</label>
              <input
                type="date"
                className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
                value={bookingDate}
                onChange={(e) => setBookingDate(e.target.value)}
              />
            </div>
            <div>
              <label className="mb-1.5 block text-sm font-medium text-gray-700">Start time</label>
              <input
                type="time"
                className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
              />
            </div>
            <div>
              <label className="mb-1.5 block text-sm font-medium text-gray-700">End time</label>
              <input
                type="time"
                className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
                value={endTime}
                onChange={(e) => setEndTime(e.target.value)}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            <div>
              <label className="mb-1.5 block text-sm font-medium text-gray-700">Attendees</label>
              <input
                type="number"
                min={1}
                className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
                value={attendeeCount}
                onChange={(e) => setAttendeeCount(Math.max(1, Number(e.target.value)))}
              />
            </div>
            <div>
              <label className="mb-1.5 block text-sm font-medium text-gray-700">Subtotal (₹)</label>
              <input
                type="number"
                min={0}
                step="0.01"
                className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
                value={subtotal}
                onChange={(e) => setSubtotal(Math.max(0, Number(e.target.value)))}
              />
            </div>
            <div>
              <label className="mb-1.5 block text-sm font-medium text-gray-700">Discount (₹)</label>
              <input
                type="number"
                min={0}
                step="0.01"
                className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
                value={discount}
                onChange={(e) => setDiscount(Math.max(0, Number(e.target.value)))}
              />
            </div>
            <div>
              <label className="mb-1.5 block text-sm font-medium text-gray-700">Tax (₹)</label>
              <input
                type="number"
                min={0}
                step="0.01"
                className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
                value={tax}
                onChange={(e) => setTax(Math.max(0, Number(e.target.value)))}
              />
            </div>
          </div>

          <div>
            <label className="mb-1.5 block text-sm font-medium text-gray-700">Note (optional)</label>
            <textarea
              rows={3}
              className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]"
              value={note}
              onChange={(e) => setNote(e.target.value)}
            />
          </div>

          <button
            disabled={submitting || !ready}
            type="submit"
            className="w-full rounded-lg bg-[#5b4ef9] px-4 py-2.5 text-sm font-medium text-white disabled:opacity-60"
          >
            {submitting ? "Creating booking…" : "Create booking"}
          </button>
        </form>
      </div>
    </CommerceShell>
  );
}
