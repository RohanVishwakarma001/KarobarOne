"use client";

import { useState } from "react";
import * as DialogPrimitive from "@radix-ui/react-dialog";
import { AnimatePresence, motion } from "framer-motion";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2, MapPin, Monitor, Plus, Star, Trash2, X } from "lucide-react";

import { useCustomerAddresses, useCustomerSessions, useCreateAddress, useUpdateAddress, useDeleteAddress } from "@/hooks/use-addresses";
import { useUpdateCustomer } from "@/hooks/use-customers";
import { addressFormSchema, type AddressFormValues } from "@/lib/validation/addresses";
import type { AddressResponse, AddressType } from "@/lib/api/addresses";
import type { CustomerResponse } from "@/lib/api/customers";
import { AnimatedButton } from "@/components/ui/animated-button";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Skeleton } from "@/components/ui/skeleton";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { cn } from "@/lib/utils";
import { useReducedMotion } from "@/lib/motion";

const EMPTY_ADDRESS: AddressFormValues = {
  addressType: "SHIPPING",
  fullName: "",
  mobile: "",
  addressLine1: "",
  city: "",
  state: "",
  postalCode: "",
  isDefault: false,
};

function AddressCard({ address, onEdit, onDelete, deleting }: { address: AddressResponse; onEdit: () => void; onDelete: () => void; deleting: boolean }) {
  return (
    <motion.div layout initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="rounded-2xl border border-slate-200 p-3.5">
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2">
          <span
            className={cn(
              "rounded-full px-2 py-0.5 text-[11px] font-medium",
              address.addressType === "BILLING" ? "bg-indigo-50 text-indigo-600" : "bg-emerald-50 text-emerald-600",
            )}
          >
            {address.addressType === "BILLING" ? "Billing" : "Shipping"}
          </span>
          {address.isDefault && (
            <span className="inline-flex items-center gap-1 rounded-full bg-amber-50 px-2 py-0.5 text-[11px] font-medium text-amber-600">
              <Star className="h-2.5 w-2.5 fill-current" /> Default
            </span>
          )}
        </div>
        <div className="flex gap-1">
          <button type="button" onClick={onEdit} className="rounded-full p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-600">
            <MapPin className="h-3.5 w-3.5" />
          </button>
          <button type="button" onClick={onDelete} disabled={deleting} className="rounded-full p-1 text-slate-400 hover:bg-red-50 hover:text-red-500">
            {deleting ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Trash2 className="h-3.5 w-3.5" />}
          </button>
        </div>
      </div>
      <p className="mt-2 text-sm font-medium text-slate-800">{address.fullName}</p>
      <p className="text-xs text-slate-500">
        {address.addressLine1}, {address.city}, {address.state} {address.postalCode}
      </p>
      <p className="text-xs text-slate-400">{address.mobile}</p>
    </motion.div>
  );
}

export function AddressManagerSheet({
  open,
  onOpenChange,
  customer,
  tenantId,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  customer: CustomerResponse;
  tenantId: string;
}) {
  const reducedMotion = useReducedMotion();
  const addressesQuery = useCustomerAddresses(customer.id);
  const sessionsQuery = useCustomerSessions(customer.id);
  const createAddress = useCreateAddress(customer.id);
  const updateAddressMutation = useUpdateAddress(customer.id);
  const deleteAddress = useDeleteAddress(customer.id);
  const updateCustomer = useUpdateCustomer(tenantId);

  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const form = useForm<AddressFormValues>({ resolver: zodResolver(addressFormSchema), defaultValues: EMPTY_ADDRESS });

  const startAdd = () => {
    setEditingId(null);
    form.reset(EMPTY_ADDRESS);
    setShowForm(true);
  };

  const startEdit = (address: AddressResponse) => {
    setEditingId(address.id);
    form.reset({
      addressType: address.addressType,
      fullName: address.fullName,
      mobile: address.mobile,
      addressLine1: address.addressLine1,
      addressLine2: address.addressLine2 ?? undefined,
      landmark: address.landmark ?? undefined,
      city: address.city,
      state: address.state,
      postalCode: address.postalCode,
      isDefault: address.isDefault,
    });
    setShowForm(true);
  };

  const onSubmit = form.handleSubmit(async (values) => {
    const payload = {
      addressType: values.addressType,
      fullName: values.fullName,
      mobile: values.mobile,
      addressLine1: values.addressLine1,
      addressLine2: values.addressLine2,
      landmark: values.landmark,
      city: values.city,
      state: values.state,
      postalCode: values.postalCode,
      isDefault: values.isDefault,
    };
    try {
      if (editingId) {
        await updateAddressMutation.mutateAsync({ addressId: editingId, input: payload });
      } else {
        await createAddress.mutateAsync(payload);
      }
      setShowForm(false);
    } catch {
      // toasted by the mutation hooks
    }
  });

  const handleDelete = async (addressId: string) => {
    setDeletingId(addressId);
    try {
      await deleteAddress.mutateAsync(addressId);
    } finally {
      setDeletingId(null);
    }
  };

  const toggleAccountStatus = () => {
    updateCustomer.mutate({
      customerId: customer.id,
      input: { status: customer.status === "ACTIVE" ? "INACTIVE" : "ACTIVE" },
    });
  };

  const addresses = addressesQuery.data ?? [];
  const activeSessions = (sessionsQuery.data ?? []).filter((s) => s.isActive);

  return (
    <DialogPrimitive.Root open={open} onOpenChange={onOpenChange}>
      <AnimatePresence>
        {open && (
          <DialogPrimitive.Portal forceMount>
            <DialogPrimitive.Overlay asChild forceMount>
              <motion.div className="fixed inset-0 z-50 bg-slate-950/40" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.15 }} />
            </DialogPrimitive.Overlay>
            <DialogPrimitive.Content asChild forceMount onOpenAutoFocus={(e) => e.preventDefault()}>
              <motion.div
                className="fixed right-0 top-0 z-50 flex h-full w-full max-w-lg flex-col bg-white shadow-2xl"
                initial={reducedMotion ? { opacity: 0 } : { x: "100%" }}
                animate={reducedMotion ? { opacity: 1 } : { x: 0 }}
                exit={reducedMotion ? { opacity: 0 } : { x: "100%" }}
                transition={{ type: "spring", stiffness: 380, damping: 36 }}
              >
                <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4">
                  <div>
                    <DialogPrimitive.Title className="text-lg font-semibold text-slate-900">
                      {customer.firstName} {customer.lastName ?? ""}
                    </DialogPrimitive.Title>
                    <p className="text-xs text-slate-400">{customer.email}</p>
                  </div>
                  <DialogPrimitive.Close className="rounded-full p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-600">
                    <X className="h-4 w-4" />
                  </DialogPrimitive.Close>
                </div>

                <div className="flex-1 space-y-6 overflow-y-auto px-5 py-5">
                  <div className="flex items-center justify-between rounded-2xl border border-slate-100 bg-slate-50/60 px-4 py-3">
                    <div>
                      <p className="text-sm font-medium text-slate-800">Account active</p>
                      <p className="text-xs text-slate-400">Inactive customers can't sign in or check out.</p>
                    </div>
                    <Switch checked={customer.status === "ACTIVE"} onCheckedChange={toggleAccountStatus} disabled={updateCustomer.isPending} />
                  </div>

                  <section>
                    <div className="mb-3 flex items-center justify-between">
                      <h3 className="text-sm font-semibold text-slate-900">Addresses</h3>
                      <Button type="button" size="sm" variant="outline" onClick={startAdd}>
                        <Plus className="h-3.5 w-3.5" /> Add
                      </Button>
                    </div>

                    {showForm && (
                      <Form {...form}>
                        <form onSubmit={onSubmit} className="mb-4 space-y-3 rounded-2xl border border-slate-200 p-4">
                          <div className="grid grid-cols-2 gap-3">
                            <FormField
                              control={form.control}
                              name="addressType"
                              render={({ field }) => (
                                <FormItem>
                                  <FormLabel>Type</FormLabel>
                                  <Select value={field.value} onValueChange={(v) => field.onChange(v as AddressType)}>
                                    <FormControl>
                                      <SelectTrigger>
                                        <SelectValue />
                                      </SelectTrigger>
                                    </FormControl>
                                    <SelectContent>
                                      <SelectItem value="SHIPPING">Shipping</SelectItem>
                                      <SelectItem value="BILLING">Billing</SelectItem>
                                    </SelectContent>
                                  </Select>
                                  <FormMessage />
                                </FormItem>
                              )}
                            />
                            <FormField
                              control={form.control}
                              name="mobile"
                              render={({ field }) => (
                                <FormItem>
                                  <FormLabel>Mobile</FormLabel>
                                  <FormControl>
                                    <Input {...field} placeholder="9876543210" />
                                  </FormControl>
                                  <FormMessage />
                                </FormItem>
                              )}
                            />
                          </div>
                          <FormField
                            control={form.control}
                            name="fullName"
                            render={({ field }) => (
                              <FormItem>
                                <FormLabel>Full name</FormLabel>
                                <FormControl>
                                  <Input {...field} />
                                </FormControl>
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                          <FormField
                            control={form.control}
                            name="addressLine1"
                            render={({ field }) => (
                              <FormItem>
                                <FormLabel>Address</FormLabel>
                                <FormControl>
                                  <Input {...field} />
                                </FormControl>
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                          <div className="grid grid-cols-3 gap-3">
                            <FormField
                              control={form.control}
                              name="city"
                              render={({ field }) => (
                                <FormItem>
                                  <FormLabel>City</FormLabel>
                                  <FormControl>
                                    <Input {...field} />
                                  </FormControl>
                                  <FormMessage />
                                </FormItem>
                              )}
                            />
                            <FormField
                              control={form.control}
                              name="state"
                              render={({ field }) => (
                                <FormItem>
                                  <FormLabel>State</FormLabel>
                                  <FormControl>
                                    <Input {...field} />
                                  </FormControl>
                                  <FormMessage />
                                </FormItem>
                              )}
                            />
                            <FormField
                              control={form.control}
                              name="postalCode"
                              render={({ field }) => (
                                <FormItem>
                                  <FormLabel>Postal code</FormLabel>
                                  <FormControl>
                                    <Input {...field} />
                                  </FormControl>
                                  <FormMessage />
                                </FormItem>
                              )}
                            />
                          </div>
                          <FormField
                            control={form.control}
                            name="isDefault"
                            render={({ field }) => (
                              <FormItem className="flex flex-row items-center justify-between rounded-xl border border-slate-100 px-3.5 py-2.5">
                                <Label htmlFor="isDefault" className="text-xs">
                                  Set as default for this type
                                </Label>
                                <FormControl>
                                  <Switch id="isDefault" checked={field.value} onCheckedChange={field.onChange} />
                                </FormControl>
                              </FormItem>
                            )}
                          />
                          <div className="flex justify-end gap-2">
                            <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                              Cancel
                            </Button>
                            <AnimatedButton
                              type="submit"
                              status={editingId ? updateAddressMutation.status : createAddress.status}
                              label={editingId ? "Save" : "Add address"}
                              loadingLabel="Saving…"
                              successLabel="Saved"
                              className="bg-[#5b4ef9] hover:bg-[#4a3ee0]"
                            />
                          </div>
                        </form>
                      </Form>
                    )}

                    {addressesQuery.isLoading && (
                      <div className="space-y-2">
                        <Skeleton className="h-24 w-full rounded-2xl" />
                        <Skeleton className="h-24 w-full rounded-2xl" />
                      </div>
                    )}

                    {!addressesQuery.isLoading && addresses.length === 0 && !showForm && (
                      <p className="rounded-2xl border border-dashed border-slate-200 py-8 text-center text-sm text-slate-400">No addresses yet.</p>
                    )}

                    <AnimatePresence mode="popLayout" initial={false}>
                      <div className="space-y-2">
                        {addresses.map((address) => (
                          <AddressCard
                            key={address.id}
                            address={address}
                            onEdit={() => startEdit(address)}
                            onDelete={() => handleDelete(address.id)}
                            deleting={deletingId === address.id}
                          />
                        ))}
                      </div>
                    </AnimatePresence>
                  </section>

                  <section>
                    <h3 className="mb-3 flex items-center gap-1.5 text-sm font-semibold text-slate-900">
                      <Monitor className="h-3.5 w-3.5" /> Active sessions
                    </h3>
                    {sessionsQuery.isLoading && <Skeleton className="h-12 w-full rounded-xl" />}
                    {!sessionsQuery.isLoading && activeSessions.length === 0 && <p className="text-sm text-slate-400">No active sessions.</p>}
                    <ul className="space-y-2">
                      {activeSessions.map((session) => (
                        <li key={session.id} className="rounded-xl border border-slate-100 bg-slate-50/60 px-3.5 py-2.5 text-xs text-slate-500">
                          <p className="truncate font-medium text-slate-700">{session.userAgent ?? "Unknown device"}</p>
                          <p>
                            {session.ipAddress ?? "Unknown IP"} · since {new Date(session.loginAt).toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" })}
                          </p>
                        </li>
                      ))}
                    </ul>
                  </section>
                </div>
              </motion.div>
            </DialogPrimitive.Content>
          </DialogPrimitive.Portal>
        )}
      </AnimatePresence>
    </DialogPrimitive.Root>
  );
}
