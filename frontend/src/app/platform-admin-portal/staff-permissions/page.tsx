"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { AlertTriangle, ArrowLeft, Loader2, ShieldCheck, UserCog } from "lucide-react";

import { useRequireAuth } from "@/hooks/use-require-auth";
import {
  usePlatformPermissions,
  usePlatformRoles,
  useStoreStaffPermissions,
  useTogglePermissionGrant,
} from "@/hooks/use-platform";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";

/** Groups flat "namespace:action" permission codes into a matrix section per namespace. */
function groupByNamespace(codes: string[]): Map<string, string[]> {
  const groups = new Map<string, string[]>();
  for (const code of codes) {
    const [namespace] = code.split(":");
    if (!groups.has(namespace)) groups.set(namespace, []);
    groups.get(namespace)!.push(code);
  }
  return groups;
}

function isValidUuid(value: string): boolean {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value.trim());
}

export default function StaffPermissionsPage() {
  const { session, ready } = useRequireAuth();
  const [userId, setUserId] = useState("");
  const [storeId, setStoreId] = useState("");

  const validUserId = isValidUuid(userId) ? userId.trim() : null;
  const validStoreId = isValidUuid(storeId) ? storeId.trim() : null;

  const { data: roles, isLoading: rolesLoading } = usePlatformRoles();
  const { data: permissions, isLoading: permissionsLoading } = usePlatformPermissions();
  const { data: grants, isLoading: grantsLoading } = useStoreStaffPermissions(validUserId, validStoreId);
  const toggleGrant = useTogglePermissionGrant();

  const grouped = useMemo(() => groupByNamespace((permissions ?? []).map((p) => p.permissionCode)), [permissions]);
  const permissionByCode = useMemo(() => new Map((permissions ?? []).map((p) => [p.permissionCode, p])), [permissions]);
  const grantByPermissionId = useMemo(
    () => new Map((grants ?? []).map((g) => [g.permissionId, g])),
    [grants],
  );

  if (!ready) return null;
  const isPlatformRole = session?.role === "platform_owner" || session?.role === "store_owner";

  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#f7f5ff_100%)] text-slate-900">
      <header className="border-b border-slate-200 bg-white/85 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <div>
            <p className="text-xs uppercase tracking-[0.24em] text-slate-500">KarobarOne portal</p>
            <h1 className="mt-1 text-xl font-semibold text-slate-950">Staff & Permissions</h1>
          </div>
          <Link
            href="/platform-admin-portal"
            className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]"
          >
            <ArrowLeft className="size-4" />
            Dashboard
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
        {!isPlatformRole ? (
          <div className="flex flex-col items-center gap-3 rounded-3xl border border-amber-200 bg-amber-50 py-16 text-center">
            <AlertTriangle className="h-8 w-8 text-amber-500" />
            <p className="text-sm font-medium text-amber-900">
              This screen is restricted to platform owners and store owners.
            </p>
          </div>
        ) : (
          <>
            <div className="flex flex-col gap-1">
              <h2 className="text-3xl font-semibold tracking-tight">Store-staff permission matrix</h2>
              <p className="text-sm text-slate-500">
                Grant or revoke fine-grained permission overrides for a staff member on a specific store. Roles below are
                system-wide defaults; overrides here apply on top of a user's role for one store.
              </p>
            </div>

            <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
              <h3 className="text-sm font-semibold text-slate-900">System roles</h3>
              <div className="mt-3 flex flex-wrap gap-2">
                {rolesLoading && <Loader2 className="h-4 w-4 animate-spin text-slate-400" />}
                {roles?.map((role) => (
                  <Badge key={role.id} variant="outline" className="gap-1.5 border-slate-200 text-slate-600">
                    <UserCog className="h-3 w-3" />
                    {role.roleName}
                    {role.isSystemRole && <span className="text-slate-400">· system</span>}
                  </Badge>
                ))}
                {roles && roles.length === 0 && <p className="text-sm text-slate-400">No roles registered yet.</p>}
              </div>
            </section>

            <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
              <h3 className="text-sm font-semibold text-slate-900">Select staff member & store</h3>
              <div className="mt-3 grid gap-4 sm:grid-cols-2">
                <div>
                  <Label htmlFor="userId">User ID (UUID)</Label>
                  <Input
                    id="userId"
                    value={userId}
                    onChange={(e) => setUserId(e.target.value)}
                    placeholder="e.g. 3fa85f64-5717-4562-b3fc-2c963f66afa6"
                    className="mt-1.5"
                  />
                </div>
                <div>
                  <Label htmlFor="storeId">Store ID (UUID)</Label>
                  <Input
                    id="storeId"
                    value={storeId}
                    onChange={(e) => setStoreId(e.target.value)}
                    placeholder="e.g. 6c9a1e2b-...-8d3c1a9b0e11"
                    className="mt-1.5"
                  />
                </div>
              </div>
            </section>

            <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-slate-900">Permission grants</h3>
                {(permissionsLoading || grantsLoading) && <Loader2 className="h-4 w-4 animate-spin text-slate-400" />}
              </div>

              {!validUserId || !validStoreId ? (
                <p className="mt-4 text-sm text-slate-400">
                  Enter a valid user ID and store ID above to view and edit their permission matrix.
                </p>
              ) : (
                <div className="mt-4 space-y-6">
                  {Array.from(grouped.entries()).map(([namespace, codes]) => (
                    <div key={namespace}>
                      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">{namespace}</p>
                      <div className="mt-2 grid gap-2 sm:grid-cols-2">
                        {codes.map((code) => {
                          const permission = permissionByCode.get(code);
                          if (!permission) return null;
                          const existingGrant = grantByPermissionId.get(permission.id);
                          const checked = Boolean(existingGrant);
                          const isMutatingThis =
                            toggleGrant.isPending &&
                            toggleGrant.variables?.permissionId === permission.id &&
                            toggleGrant.variables?.userId === validUserId;

                          return (
                            <motion.label
                              key={code}
                              whileTap={{ scale: 0.98 }}
                              className="flex cursor-pointer items-center gap-3 rounded-xl border border-slate-100 bg-slate-50/60 px-3 py-2.5 transition hover:border-[#5b4ef9]/30"
                            >
                              <Checkbox
                                checked={checked}
                                disabled={isMutatingThis}
                                onCheckedChange={() =>
                                  toggleGrant.mutate({
                                    userId: validUserId,
                                    storeId: validStoreId,
                                    permissionId: permission.id,
                                    existingGrant,
                                  })
                                }
                              />
                              <div className="flex-1">
                                <p className="text-sm font-medium text-slate-800">{permission.permissionName}</p>
                                <p className="text-xs text-slate-400">{permission.permissionCode}</p>
                              </div>
                              {isMutatingThis && <Loader2 className="h-3.5 w-3.5 animate-spin text-slate-400" />}
                              {checked && !isMutatingThis && <ShieldCheck className="h-4 w-4 text-emerald-500" />}
                            </motion.label>
                          );
                        })}
                      </div>
                    </div>
                  ))}
                  {grouped.size === 0 && <p className="text-sm text-slate-400">No permissions registered yet.</p>}
                </div>
              )}
            </section>
          </>
        )}
      </main>
    </div>
  );
}
