"use client";

import { createContext, useContext, useMemo, useState } from "react";

type CartSheetContextValue = {
  isOpen: boolean;
  open: () => void;
  close: () => void;
  toggle: () => void;
};

const CartSheetContext = createContext<CartSheetContextValue | null>(null);

export function CartSheetProvider({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  const value = useMemo<CartSheetContextValue>(
    () => ({
      isOpen,
      open: () => setIsOpen(true),
      close: () => setIsOpen(false),
      toggle: () => setIsOpen((v) => !v),
    }),
    [isOpen],
  );
  return <CartSheetContext.Provider value={value}>{children}</CartSheetContext.Provider>;
}

export function useCartSheet(): CartSheetContextValue {
  const ctx = useContext(CartSheetContext);
  if (!ctx) throw new Error("useCartSheet must be used within a CartSheetProvider");
  return ctx;
}
