"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { UserPlus } from "lucide-react";

import { AnimatedDialog } from "./animated-dialog";
import { AnimatedButton } from "@/components/ui/animated-button";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { customerCreateSchema, type CustomerCreateFormValues } from "@/lib/validation/customers";
import { CUSTOMER_STATUSES } from "@/lib/api/customers";
import { useCreateCustomer } from "@/hooks/use-customers";

const DEFAULT_VALUES: CustomerCreateFormValues = {
  firstName: "",
  lastName: undefined,
  email: "",
  mobile: "",
  status: "ACTIVE",
  isGuestCustomer: false,
  isEmailVerified: false,
  isMobileVerified: false,
  password: undefined,
};

export function CreateCustomerDialog({
  open,
  onOpenChange,
  tenantId,
  storeId,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  tenantId: string;
  storeId: string;
}) {
  const form = useForm<CustomerCreateFormValues>({
    resolver: zodResolver(customerCreateSchema),
    defaultValues: DEFAULT_VALUES,
  });
  const createCustomer = useCreateCustomer(tenantId);

  useEffect(() => {
    if (open) form.reset(DEFAULT_VALUES);
  }, [open, form]);

  const onSubmit = form.handleSubmit(async (values) => {
    try {
      await createCustomer.mutateAsync({
        tenantId,
        storeId,
        firstName: values.firstName,
        lastName: values.lastName,
        email: values.email,
        mobile: values.mobile,
        status: values.status,
        isGuestCustomer: values.isGuestCustomer,
        password: values.password,
      });
      onOpenChange(false);
    } catch {
      // Toasted by useCreateCustomer's onError; keep the dialog open so the user can retry.
    }
  });

  return (
    <AnimatedDialog
      open={open}
      onOpenChange={onOpenChange}
      title="Add customer"
      description="Creates a profile in this store — the customer can register themselves later using the same email or mobile."
    >
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
                    <Input placeholder="Aditi" {...field} />
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
                    <Input placeholder="Sharma" {...field} value={field.value ?? ""} />
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
                  <Input type="email" placeholder="aditi@example.com" {...field} />
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
                    <Input placeholder="9876543210" {...field} />
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

          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Password (optional)</FormLabel>
                <FormControl>
                  <Input type="password" placeholder="Leave blank to invite them to set one later" {...field} value={field.value ?? ""} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="isGuestCustomer"
            render={({ field }) => (
              <FormItem className="flex flex-row items-center justify-between rounded-xl border border-slate-200 px-3.5 py-3">
                <div>
                  <Label htmlFor="isGuestCustomer">Guest customer</Label>
                  <p className="text-xs text-slate-500">No login — created for a one-off order or booking.</p>
                </div>
                <FormControl>
                  <Switch id="isGuestCustomer" checked={field.value} onCheckedChange={field.onChange} />
                </FormControl>
              </FormItem>
            )}
          />

          <div className="flex justify-end gap-2 pt-2">
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <AnimatedButton
              type="submit"
              status={createCustomer.status}
              icon={<UserPlus className="h-4 w-4" />}
              label="Add customer"
              loadingLabel="Adding…"
              successLabel="Added"
              className="bg-[#5b4ef9] hover:bg-[#4a3ee0]"
            />
          </div>
        </form>
      </Form>
    </AnimatedDialog>
  );
}
