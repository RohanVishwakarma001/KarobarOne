"use client";

import { Trash2 } from "lucide-react";
import { AnimatedDialog } from "./animated-dialog";
import { AnimatedButton } from "@/components/ui/animated-button";
import { Button } from "@/components/ui/button";
import { useDeleteCustomer } from "@/hooks/use-customers";
import type { CustomerResponse } from "@/lib/api/customers";

export function DeleteCustomerDialog({
  open,
  onOpenChange,
  tenantId,
  customer,
  onDeleted,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  tenantId: string;
  customer: CustomerResponse;
  onDeleted?: () => void;
}) {
  const deleteCustomer = useDeleteCustomer(tenantId);

  const handleConfirm = async () => {
    try {
      await deleteCustomer.mutateAsync(customer.id);
      // Let the button's success checkmark actually be seen before the
      // dialog vanishes out from under it — closing instantly would cut the
      // morph off mid-animation.
      setTimeout(() => {
        onOpenChange(false);
        onDeleted?.();
      }, 550);
    } catch {
      // Toasted by useDeleteCustomer's onError; the button's own shake plays either way.
    }
  };

  return (
    <AnimatedDialog
      open={open}
      onOpenChange={onOpenChange}
      title="Delete this customer?"
      description={`${customer.firstName} ${customer.lastName ?? ""} (${customer.customerCode}) will be moved to trash and can be restored later.`}
      className="max-w-sm"
    >
      <div className="flex justify-end gap-2 pt-2">
        <Button type="button" variant="outline" onClick={() => onOpenChange(false)} disabled={deleteCustomer.isPending}>
          Cancel
        </Button>
        <AnimatedButton
          type="button"
          variant="destructive"
          status={deleteCustomer.status}
          icon={<Trash2 className="h-4 w-4" />}
          label="Delete"
          loadingLabel="Deleting…"
          successLabel="Deleted"
          onClick={handleConfirm}
        />
      </div>
    </AnimatedDialog>
  );
}
