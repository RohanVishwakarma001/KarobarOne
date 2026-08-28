export interface RazorpaySuccessResponse {
  razorpay_order_id: string;
  razorpay_payment_id: string;
  razorpay_signature: string;
}

interface RazorpayOptions {
  key: string;
  amount: number;
  currency: string;
  order_id: string;
  name: string;
  description?: string;
  prefill?: { name?: string; email?: string; contact?: string };
  theme?: { color?: string };
  handler: (response: RazorpaySuccessResponse) => void;
  modal?: { ondismiss?: () => void };
}

interface RazorpayCheckout {
  open(): void;
}

declare global {
  interface Window {
    Razorpay?: new (options: RazorpayOptions) => RazorpayCheckout;
  }
}

function loadScript(src: string): Promise<void> {
  return new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${src}"]`)) return resolve();
    const script = document.createElement("script");
    script.src = src;
    script.async = true;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Could not load the payment gateway. Check your connection."));
    document.body.appendChild(script);
  });
}

/** Opens Razorpay Checkout and resolves with the success payload, or rejects if the user cancels/it fails. */
export async function openRazorpayCheckout(options: Omit<RazorpayOptions, "handler" | "modal">): Promise<RazorpaySuccessResponse> {
  await loadScript("https://checkout.razorpay.com/v1/checkout.js");
  if (!window.Razorpay) throw new Error("Payment gateway failed to initialize.");

  return new Promise((resolve, reject) => {
    const rzp = new window.Razorpay!({
      ...options,
      handler: (response) => resolve(response),
      modal: { ondismiss: () => reject(new Error("Payment was cancelled.")) },
    });
    rzp.open();
  });
}
