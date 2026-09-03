"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  Activity,
  AlertTriangle,
  ArrowLeft,
  Building2,
  Check,
  Cpu,
  Loader2,
  ShieldCheck,
  Sparkles,
  Users2,
} from "lucide-react";

import { useRequireAuth } from "@/hooks/use-require-auth";
import { usePlatformPlans, usePlatformTenants, useTenantPlan, useChangeTenantPlan } from "@/hooks/use-platform";
import type { Plan, TenantCompact } from "@/lib/api/platform";
import { AnimatedDialog } from "@/components/customers/animated-dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { springs } from "@/lib/motion";

const PAGE_SIZE = 20;

function formatINR(value: string | number): string {
  const n = typeof value === "string" ? Number(value) : value;
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(n);
}

function StatCard({
  label,
  value,
  icon,
  delay,
}: {
  label: string;
  value: string | number;
  icon: React.ReactNode;
  delay: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.3 }}
      whileHover={{ scale: 1.02, boxShadow: "0 12px 32px -8px rgba(91,78,249,0.25)" }}
      className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-4"
    >
      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#5b4ef9]/10 text-[#5b4ef9]">
        {icon}
      </div>
      <div>
        <p className="text-xs font-medium uppercase tracking-[0.18em] text-slate-500">{label}</p>
        <p className="mt-1 text-2xl font-semibold text-slate-900">{value}</p>
      </div>
    </motion.div>
  );
}

function PlanCard({ plan, index }: { plan: Plan; index: number }) {
  const isFree = plan.planCode === "FREE";
  const isEnterprise = plan.planCode === "ENTERPRISE";
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.08 * index, ...springs.gentle }}
      whileHover={{ y: -4 }}
      className={`relative flex flex-col rounded-3xl border p-6 ${
        isEnterprise ? "border-[#5b4ef9] bg-[#5b4ef9]/[0.03] shadow-lg shadow-[#5b4ef9]/10" : "border-slate-200 bg-white"
      }`}
    >
      {isEnterprise && (
        <span className="absolute -top-3 right-6 rounded-full bg-[#5b4ef9] px-3 py-1 text-xs font-semibold text-white">
          Best value
        </span>
      )}
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">{plan.planCode}</p>
      <h3 className="mt-1 text-xl font-semibold text-slate-900">{plan.planName}</h3>
      <p className="mt-4 flex items-baseline gap-1">
        <span className="text-3xl font-bold text-slate-900">{isFree ? "Free" : formatINR(plan.monthlyPrice)}</span>
        {!isFree && <span className="text-sm text-slate-500">/month</span>}
      </p>
      <p className="mt-1 text-sm text-slate-500">{plan.transactionCommissionPercent}% commission per order</p>

      <ul className="mt-5 flex-1 space-y-2">
        {plan.features.length === 0 && <li className="text-sm text-slate-400">No feature overrides configured.</li>}
        {plan.features.map((f) => (
          <li key={f.id} className="flex items-start gap-2 text-sm text-slate-600">
            <Check className="mt-0.5 h-4 w-4 shrink-0 text-emerald-500" />
            <span>{f.featureName}</span>
          </li>
        ))}
      </ul>

      <Badge variant={plan.isActive ? "default" : "secondary"} className={plan.isActive ? "mt-5 w-fit bg-emerald-600" : "mt-5 w-fit"}>
        {plan.isActive ? "Open for signups" : "Closed"}
      </Badge>
    </motion.div>
  );
}

function TenantPlanCell({ tenantId, plans }: { tenantId: string; plans: Plan[] }) {
  const { data: mapping, isLoading } = useTenantPlan(tenantId);
  if (isLoading) return <Loader2 className="h-3.5 w-3.5 animate-spin text-slate-400" />;
  if (!mapping) return <span className="text-xs text-slate-400">No plan assigned</span>;
  const plan = mapping.plan ?? plans.find((p) => p.id === mapping.planId);
  return (
    <Badge variant="outline" className="border-[#5b4ef9]/30 text-[#5b4ef9]">
      {plan?.planName ?? mapping.planId.slice(0, 8)}
    </Badge>
  );
}

function ChangePlanDialog({
  tenant,
  plans,
  open,
  onOpenChange,
}: {
  tenant: TenantCompact;
  plans: Plan[];
  open: boolean;
  onOpenChange: (open: boolean) => void;
}) {
  const { data: mapping } = useTenantPlan(open ? tenant.id : null);
  const changePlan = useChangeTenantPlan();
  const [pendingPlanId, setPendingPlanId] = useState<string | null>(null);

  const currentPlanCode = mapping?.plan?.planCode ?? plans.find((p) => p.id === mapping?.planId)?.planCode;
  const tierOrder = ["FREE", "PRO", "ENTERPRISE"];

  return (
    <AnimatedDialog
      open={open}
      onOpenChange={onOpenChange}
      title={`Change plan — ${tenant.businessName}`}
      description={mapping ? `Currently on ${mapping.plan?.planName ?? "an assigned plan"}.` : "This tenant has no plan yet."}
    >
      <div className="grid gap-3 sm:grid-cols-3">
        {plans.map((plan) => {
          const isCurrent = plan.id === mapping?.planId;
          const currentIdx = tierOrder.indexOf(currentPlanCode ?? "FREE");
          const targetIdx = tierOrder.indexOf(plan.planCode);
          const direction: "upgrade" | "downgrade" = targetIdx >= currentIdx ? "upgrade" : "downgrade";
          const isPending = changePlan.isPending && pendingPlanId === plan.id;

          return (
            <button
              key={plan.id}
              type="button"
              disabled={isCurrent || changePlan.isPending}
              onClick={() => {
                setPendingPlanId(plan.id);
                changePlan.mutate(
                  { tenantId: tenant.id, planId: plan.id, hasExistingPlan: Boolean(mapping), direction },
                  { onSuccess: () => onOpenChange(false) },
                );
              }}
              className={`flex flex-col items-start rounded-2xl border p-4 text-left transition ${
                isCurrent
                  ? "border-[#5b4ef9] bg-[#5b4ef9]/5"
                  : "border-slate-200 hover:border-[#5b4ef9]/40 hover:bg-slate-50 disabled:opacity-50"
              }`}
            >
              <p className="text-sm font-semibold text-slate-900">{plan.planName}</p>
              <p className="mt-1 text-xs text-slate-500">
                {plan.planCode === "FREE" ? "Free" : formatINR(plan.monthlyPrice) + "/mo"} · {plan.transactionCommissionPercent}%
              </p>
              {isCurrent ? (
                <span className="mt-3 text-xs font-medium text-[#5b4ef9]">Current plan</span>
              ) : (
                <span className="mt-3 inline-flex items-center gap-1 text-xs font-medium text-slate-500">
                  {isPending && <Loader2 className="h-3 w-3 animate-spin" />}
                  {direction === "upgrade" ? "Upgrade to this" : "Downgrade to this"}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </AnimatedDialog>
  );
}

export default function PlatformAdminPortalPage() {
  const { session, ready } = useRequireAuth();
  const [changePlanTenant, setChangePlanTenant] = useState<TenantCompact | null>(null);

  const { data: plansData, isLoading: plansLoading } = usePlatformPlans();
  const { data: tenantsData, isLoading: tenantsLoading, isError, refetch } = usePlatformTenants({
    skip: 0,
    limit: PAGE_SIZE,
  });

  const plans = useMemo(() => plansData?.items ?? [], [plansData]);
  const tenants = useMemo(() => tenantsData?.items ?? [], [tenantsData]);
  const activeCount = useMemo(() => tenants.filter((t) => t.isActive).length, [tenants]);

  if (!ready) return null;

  const isPlatformRole = session?.role === "platform_owner" || session?.role === "platform_staff";

  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#f7f5ff_100%)] text-slate-900">
      <header className="border-b border-slate-200 bg-white/85 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <div>
            <p className="text-xs uppercase tracking-[0.24em] text-slate-500">KarobarOne portal</p>
            <h1 className="mt-1 text-xl font-semibold text-slate-950">Platform Admin Portal</h1>
          </div>
          <nav className="flex items-center gap-2">
            <Link
              href="/platform-admin-portal/staff-permissions"
              className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]"
            >
              <ShieldCheck className="size-4" />
              Staff & Permissions
            </Link>
            <Link
              href="/platform-admin-portal/seo-ai"
              className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]"
            >
              <Sparkles className="size-4" />
              SEO & AI
            </Link>
            <Link
              href="/platform-admin-portal/system-health"
              className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]"
            >
              <Activity className="size-4" />
              System Health
            </Link>
            <Link
              href="/"
              className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]"
            >
              <ArrowLeft className="size-4" />
              Home
            </Link>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
        {!isPlatformRole ? (
          <div className="flex flex-col items-center gap-3 rounded-3xl border border-amber-200 bg-amber-50 py-16 text-center">
            <AlertTriangle className="h-8 w-8 text-amber-500" />
            <p className="text-sm font-medium text-amber-900">
              This dashboard is restricted to platform owners and platform staff.
            </p>
          </div>
        ) : (
          <>
            <div className="flex flex-col gap-1">
              <h2 className="text-3xl font-semibold tracking-tight">Tenants & subscription plans</h2>
              <p className="text-sm text-slate-500">Platform-wide tenant overview and plan tier management.</p>
            </div>

            <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3">
              <StatCard label="Total tenants" value={tenantsData?.total ?? 0} icon={<Building2 className="h-5 w-5" />} delay={0} />
              <StatCard label="Active (this page)" value={activeCount} icon={<Users2 className="h-5 w-5" />} delay={0.05} />
              <StatCard label="Plan tiers" value={plans.length} icon={<Cpu className="h-5 w-5" />} delay={0.1} />
            </div>

            <section className="mt-8">
              <h3 className="text-lg font-semibold text-slate-900">Subscription plan tiers</h3>
              {plansLoading ? (
                <div className="mt-4 grid gap-4 sm:grid-cols-3">
                  {[0, 1, 2].map((i) => (
                    <div key={i} className="h-64 animate-pulse rounded-3xl border border-slate-200 bg-slate-100" />
                  ))}
                </div>
              ) : (
                <div className="mt-4 grid gap-4 sm:grid-cols-3">
                  {plans.map((plan, i) => (
                    <PlanCard key={plan.id} plan={plan} index={i} />
                  ))}
                </div>
              )}
            </section>

            <section className="mt-8 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-slate-900">Tenants</h3>
                {tenantsLoading && <Loader2 className="h-4 w-4 animate-spin text-slate-400" />}
              </div>

              <div className="mt-4 overflow-hidden rounded-2xl border border-slate-100">
                <Table>
                  <TableHeader>
                    <TableRow className="bg-slate-50/80 hover:bg-slate-50/80">
                      <TableHead>Business</TableHead>
                      <TableHead>Location</TableHead>
                      <TableHead>Type</TableHead>
                      <TableHead>Plan</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {isError && (
                      <TableRow className="hover:bg-transparent">
                        <TableCell colSpan={6} className="p-0">
                          <div className="flex flex-col items-center gap-3 py-14 text-center">
                            <AlertTriangle className="h-7 w-7 text-red-400" />
                            <p className="text-sm font-medium text-slate-700">Couldn't load tenants.</p>
                            <Button variant="outline" size="sm" onClick={() => refetch()}>
                              Try again
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    )}

                    {!isError && !tenantsLoading && tenants.length === 0 && (
                      <TableRow className="hover:bg-transparent">
                        <TableCell colSpan={6} className="py-14 text-center text-sm text-slate-500">
                          No tenants registered yet.
                        </TableCell>
                      </TableRow>
                    )}

                    {!isError &&
                      tenants.map((tenant, i) => (
                        <motion.tr
                          key={tenant.id}
                          initial={{ opacity: 0, y: 6 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: Math.min(i, 8) * 0.03, duration: 0.18 }}
                          className="border-b border-slate-100 transition-colors last:border-0 hover:bg-slate-50"
                        >
                          <TableCell>
                            <p className="font-medium text-slate-900">{tenant.businessName}</p>
                            <p className="text-xs text-slate-400">{tenant.email}</p>
                          </TableCell>
                          <TableCell className="text-sm text-slate-600">
                            {tenant.city}, {tenant.state}
                          </TableCell>
                          <TableCell className="text-sm text-slate-600">{tenant.businessType}</TableCell>
                          <TableCell>
                            <TenantPlanCell tenantId={tenant.id} plans={plans} />
                          </TableCell>
                          <TableCell>
                            <Badge variant={tenant.isActive ? "default" : "secondary"} className={tenant.isActive ? "bg-emerald-600" : ""}>
                              {tenant.isActive ? "Active" : "Inactive"}
                            </Badge>
                          </TableCell>
                          <TableCell className="text-right">
                            <Button variant="outline" size="sm" onClick={() => setChangePlanTenant(tenant)}>
                              Change plan
                            </Button>
                          </TableCell>
                        </motion.tr>
                      ))}
                  </TableBody>
                </Table>
              </div>
            </section>
          </>
        )}
      </main>

      {changePlanTenant && (
        <ChangePlanDialog
          tenant={changePlanTenant}
          plans={plans}
          open={Boolean(changePlanTenant)}
          onOpenChange={(open) => !open && setChangePlanTenant(null)}
        />
      )}
    </div>
  );
}
