import { apiGet, apiPost, apiPut, apiDelete } from "../client";
import { TENANT_ID, STORE_ID, assertStoreConfig } from "../config";

export type BookingStatus = "PENDING" | "CONFIRMED" | "APPROVED" | "REJECTED" | "COMPLETED" | "CANCELLED" | "NO_SHOW" | "REFUNDED";
export type BookingPaymentStatus = "PENDING" | "PAID" | "FAILED" | "PARTIALLY_REFUNDED" | "REFUNDED";
export type BookingMode = "BOOK_ONLY" | "BOOK_AND_PAY";

export interface Booking {
  id: string;
  tenant_id: string;
  store_id: string;
  service_id: string;
  customer_id: string;
  payment_id?: string | null;
  booking_number: string;
  booking_status: BookingStatus;
  payment_status: BookingPaymentStatus;
  booking_mode: BookingMode;
  booking_date: string;
  start_time: string;
  end_time: string;
  attendee_count: number;
  subtotal_amount: number;
  discount_amount: number;
  tax_amount: number;
  total_amount: number;
  currency_code?: string | null;
  booking_note?: string | null;
  approved_by?: string | null;
  approved_at?: string | null;
  booked_at?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
}

export interface CreateBookingInput {
  service_id: string;
  customer_id: string;
  booking_mode: BookingMode;
  /** ISO date, e.g. "2026-09-05" */
  booking_date: string;
  /** "HH:MM:SS" — server rejects start_time >= end_time */
  start_time: string;
  end_time: string;
  attendee_count?: number;
  subtotal_amount?: number;
  discount_amount?: number;
  tax_amount?: number;
  currency_code?: string;
  booking_note?: string;
  payment_id?: string;
}
/** booking_number and total_amount are computed server-side. */
export function createBooking(input: CreateBookingInput) {
  assertStoreConfig();
  return apiPost<Booking>("/bookings/", {
    tenant_id: TENANT_ID,
    store_id: STORE_ID,
    attendee_count: 1,
    subtotal_amount: 0,
    discount_amount: 0,
    tax_amount: 0,
    currency_code: "INR",
    ...input,
  });
}
// No customer-scoped list filter server-side — fetch all and filter client-side by customer_id.
export const listBookings = () => apiGet<Booking[]>("/bookings/");
export const getBooking = (bookingId: string) => apiGet<Booking>(`/bookings/${bookingId}`);
export const updateBooking = (
  bookingId: string,
  data: Partial<
    Pick<
      Booking,
      "payment_id" | "booking_status" | "payment_status" | "attendee_count" | "subtotal_amount" | "discount_amount" | "tax_amount" | "booking_note" | "approved_by" | "approved_at"
    >
  >
) => apiPut<Booking>(`/bookings/${bookingId}`, data);
export const deleteBooking = (bookingId: string) => apiDelete<void>(`/bookings/${bookingId}`);

// ---------------------------------------------------------------------------
// Booking Cancellations
// ---------------------------------------------------------------------------

export type BookingCancellationStatus = "PENDING" | "APPROVED" | "REJECTED";
export interface BookingCancellation {
  id: string;
  booking_id: string;
  requested_by?: string | null;
  cancellation_reason: string;
  cancellation_reason_description?: string | null;
  cancellation_charge: number;
  status: BookingCancellationStatus;
  approved_by?: string | null;
  approved_at?: string | null;
  created_at?: string | null;
}
export const createBookingCancellation = (input: {
  booking_id: string;
  cancellation_reason: string;
  cancellation_reason_description?: string;
  cancellation_charge?: number;
  requested_by?: string;
}) => apiPost<BookingCancellation>("/booking-cancellations/", { cancellation_charge: 0, ...input });
export const listBookingCancellations = () => apiGet<BookingCancellation[]>("/booking-cancellations/");
export const getBookingCancellation = (cancellationId: string) => apiGet<BookingCancellation>(`/booking-cancellations/${cancellationId}`);
export const updateBookingCancellation = (
  cancellationId: string,
  data: Partial<Pick<BookingCancellation, "cancellation_reason" | "cancellation_reason_description" | "cancellation_charge" | "status" | "approved_by" | "approved_at">>
) => apiPut<BookingCancellation>(`/booking-cancellations/${cancellationId}`, data);
export const deleteBookingCancellation = (cancellationId: string) => apiDelete<void>(`/booking-cancellations/${cancellationId}`);

// ---------------------------------------------------------------------------
// Booking Refunds
// ---------------------------------------------------------------------------

export type BookingRefundStatus = "PENDING" | "PROCESSING" | "SUCCESS" | "FAILED";
export interface BookingRefund {
  id: string;
  booking_id: string;
  payment_refund_id?: string | null;
  refund_amount: number;
  refund_reason: string;
  refund_status: BookingRefundStatus;
  refund_reference?: string | null;
  approved_by?: string | null;
  approved_at?: string | null;
  refunded_at?: string | null;
  created_at: string;
}
export const createBookingRefund = (input: { booking_id: string; refund_amount: number; refund_reason: string; payment_refund_id?: string; refund_reference?: string }) =>
  apiPost<BookingRefund>("/booking-refunds/", input);
export const listBookingRefunds = () => apiGet<BookingRefund[]>("/booking-refunds/");
export const getBookingRefund = (refundId: string) => apiGet<BookingRefund>(`/booking-refunds/${refundId}`);
export const updateBookingRefund = (
  refundId: string,
  data: Partial<Pick<BookingRefund, "refund_status" | "refund_reference" | "approved_by" | "approved_at" | "refunded_at">>
) => apiPut<BookingRefund>(`/booking-refunds/${refundId}`, data);
export const deleteBookingRefund = (refundId: string) => apiDelete<void>(`/booking-refunds/${refundId}`);

// ---------------------------------------------------------------------------
// Booking Feedbacks
// ---------------------------------------------------------------------------

export interface BookingFeedback {
  id: string;
  booking_id: string;
  customer_id: string;
  rating: number;
  review_title?: string | null;
  review_text?: string | null;
  is_verified_booking?: boolean | null;
  is_published?: boolean | null;
  created_at: string;
  updated_at: string;
}
export const createBookingFeedback = (input: {
  booking_id: string;
  customer_id: string;
  rating: number;
  review_title?: string;
  review_text?: string;
  is_verified_booking?: boolean;
  is_published?: boolean;
}) => apiPost<BookingFeedback>("/booking-feedbacks/", input);
export const listBookingFeedbacks = () => apiGet<BookingFeedback[]>("/booking-feedbacks/");
export const getBookingFeedback = (feedbackId: string) => apiGet<BookingFeedback>(`/booking-feedbacks/${feedbackId}`);
export const updateBookingFeedback = (
  feedbackId: string,
  data: Partial<Pick<BookingFeedback, "rating" | "review_title" | "review_text" | "is_verified_booking" | "is_published">>
) => apiPut<BookingFeedback>(`/booking-feedbacks/${feedbackId}`, data);
export const deleteBookingFeedback = (feedbackId: string) => apiDelete<void>(`/booking-feedbacks/${feedbackId}`);

// ---------------------------------------------------------------------------
// Appointments — simpler, standalone (no tenant/store scoping, no payment link).
// ---------------------------------------------------------------------------

export interface Appointment {
  id: string;
  customer_name: string;
  customer_phone?: string | null;
  customer_email?: string | null;
  service_name: string;
  appointment_date: string;
  start_time: string;
  end_time: string;
  google_event_link?: string | null;
  created_at: string;
}
export const createAppointment = (input: {
  customer_name: string;
  service_name: string;
  appointment_date: string;
  start_time: string;
  end_time: string;
  customer_phone?: string;
  customer_email?: string;
}) => apiPost<Appointment>("/appointments/", input);
export const listAppointments = () => apiGet<Appointment[]>("/appointments/");
export const getAppointment = (appointmentId: string) => apiGet<Appointment>(`/appointments/${appointmentId}`);
export const updateAppointment = (appointmentId: string, data: { appointment_date: string; start_time: string; end_time: string }) =>
  apiPut<Appointment>(`/appointments/${appointmentId}`, data);
export const deleteAppointment = (appointmentId: string) => apiDelete<void>(`/appointments/${appointmentId}`);
