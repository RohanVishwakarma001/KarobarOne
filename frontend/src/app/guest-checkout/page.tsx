import { CommerceShell } from "@/components/commerce/CommerceShell";
import { CheckoutForm } from "@/components/commerce/CheckoutForm";
export default function GuestCheckoutPage(){ return <CommerceShell title="Guest Checkout" eyebrow="Orders & Payments"><CheckoutForm guest /></CommerceShell>; }
