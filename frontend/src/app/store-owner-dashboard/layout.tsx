import { PageTransition } from "@/components/providers/page-transition";

export default function StoreOwnerDashboardLayout({ children }: { children: React.ReactNode }) {
  return <PageTransition>{children}</PageTransition>;
}
