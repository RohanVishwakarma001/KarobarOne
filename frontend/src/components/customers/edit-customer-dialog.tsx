"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Save } from "lucide-react";

import { AnimatedDialog } from "./animated-dialog";
import { AnimatedButton } from "@/components/ui/animated-button";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { customerUpdateSchema, type CustomerUpdateFormValues } from "@/lib/validation/customers";
import { CUSTOMER_STATUSES, type CustomerResponse } from "@/lib/api/customers";
import { useUpdateCustomer } from "@/hooks/use-customers";

function toFormValues(customer: CustomerResponse): CustomerUpdateFormValues {
  return {
    firstName: customer.firstName,
    lastName: customer.lastName ?? undefined,
    email: customer.email,
    mobile: customer.mobile,
    status: customer.status,
    isGuestCustomer: customer.isGuestCustomer,
    isEmailVerified: customer.isEmailVerified,
    isMobileVerified: customer.isMobileVerified,
  };
}

export function EditCustomerDialog({
  open,
  onOpenChange,
  tenantId,
  customer,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  tenantId: string;
  customer: CustomerResponse;
}) {
  const form = useForm<CustomerUpdateFormValues>({
    resolver: zodResolver(customerUpdateSchema),
    defaultValues: toFormValues(customer),
  });
  const updateCustomer = useUpdateCustomer(tenantId);

  useEffect(() => {
    if (open) form.reset(toFormValues(customer));
  }, [open, customer, form]);

  const onSubmit = form.handleSubmit(async (values) => {
    try {
      await updateCustomer.mutateAsync({ customerId: customer.id, input: values });
      onOpenChange(false);
    } catch {
      // Toasted by useUpdateCustomer's onError; keep the dialog open so the user can retry.
    }
  });

  return (
    <AnimatedDialog open={open} onOpenChange={onOpenChange} title="Edit customer" description={customer.customerCode}>
      <Form {...form}>
        <form onSubmit={onSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <FormField
              control={form.control}
              name="firstName"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>First name</FormLabel>
                  <FormControl>
                    <Input {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="lastName"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Last name</FormLabel>
                  <FormControl>
                    <Input {...field} value={field.value ?? ""} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input type="email" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <div className="grid grid-cols-2 gap-3">
            <FormField
              control={form.control}
              name="mobile"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Mobile</FormLabel>
                  <FormControl>
                    <Input {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="status"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Status</FormLabel>
                  <Select value={field.value} onValueChange={field.onChange}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {CUSTOMER_STATUSES.map((s) => (
                        <SelectItem key={s} value={s}>
                          {s.charAt(0) + s.slice(1).toLowerCase()}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          <div className="grid grid-cols-1 gap-2 sm:grid-cols-3">
            <FormField
              control={form.control}
              name="isGuestCustomer"
              render={({ field }) => (
                <FormItem className="flex flex-row items-center justify-between rounded-xl border border-slate-200 px-3.5 py-3 sm:flex-col sm:items-start sm:gap-2">
                  <Label htmlFor="isGuestCustomer" className="text-xs">Guest</Label>
                  <FormControl>
                    <Switch id="isGuestCustomer" checked={field.value} onCheckedChange={field.onChange} />
                  </FormControl>
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="isEmailVerified"
              render={({ field }) => (
                <FormItem className="flex flex-row items-center justify-between rounded-xl border border-slate-200 px-3.5 py-3 sm:flex-col sm:items-start sm:gap-2">
                  <Label htmlFor="isEmailVerified" className="text-xs">Email verified</Label>
                  <FormControl>
                    <Switch id="isEmailVerified" checked={field.value} onCheckedChange={field.onChange} />
                  </FormControl>
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="isMobileVerified"
              render={({ field }) => (
                <FormItem className="flex flex-row items-center justify-between rounded-xl border border-slate-200 px-3.5 py-3 sm:flex-col sm:items-start sm:gap-2">
                  <Label htmlFor="isMobileVerified" className="text-xs">Mobile verified</Label>
                  <FormControl>
                    <Switch id="isMobileVerified" checked={field.value} onCheckedChange={field.onChange} />
                  </FormControl>
                </FormItem>
              )}
            />
          </div>

          <div className="flex justify-end gap-2 pt-2">
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <AnimatedButton
              type="submit"
              status={updateCustomer.status}
              icon={<Save className="h-4 w-4" />}
              label="Save changes"
              loadingLabel="Saving…"
              successLabel="Saved"
              className="bg-[#5b4ef9] hover:bg-[#4a3ee0]"
            />
          </div>
        </form>
      </Form>
    </AnimatedDialog>
  );
}
