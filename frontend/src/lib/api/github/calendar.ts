import { apiGet } from "../client";

/**
 * Google Calendar-style OAuth stub for the Bookings module (store-owner side —
 * connects the store's calendar so appointments/bookings can sync). ⚠️ The
 * callback route returns the raw OAuth access token directly in the response
 * body — treat it as sensitive and never log it.
 */
export const checkCalendarStatus = () => apiGet<{ message: string }>("/calendar/");
export const getCalendarLoginUrl = () => apiGet<{ auth_url: string }>("/calendar/login");
export const completeCalendarAuth = (code: string) =>
  apiGet<{ message: string; access_token?: string }>(`/calendar/callback?code=${encodeURIComponent(code)}`);
