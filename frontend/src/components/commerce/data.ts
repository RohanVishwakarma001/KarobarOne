export const products = [
  { id: 1, name: "Premium Cotton Shirt", variant: "Blue · M", price: 1299, qty: 2, image: "PS" },
  { id: 2, name: "Everyday Sneakers", variant: "White · 9", price: 2499, qty: 1, image: "SN" },
];

export const orders = [
  { id: "KO-10482", date: "08 Aug 2026", items: 3, amount: 5097, status: "Delivered" },
  { id: "KO-10471", date: "04 Aug 2026", items: 1, amount: 1299, status: "Processing" },
  { id: "KO-10455", date: "29 Jul 2026", items: 2, amount: 3598, status: "Shipped" },
  { id: "KO-10421", date: "22 Jul 2026", items: 1, amount: 899, status: "Cancelled" },
];

export const payments = [
  { id: "PAY-78431", order: "KO-10482", date: "08 Aug 2026", method: "UPI", amount: 5097, status: "Paid" },
  { id: "PAY-78395", order: "KO-10471", date: "04 Aug 2026", method: "Card", amount: 1299, status: "Paid" },
  { id: "PAY-78120", order: "KO-10455", date: "29 Jul 2026", method: "Net Banking", amount: 3598, status: "Refunded" },
];

export const money = (value: number) => `₹${value.toLocaleString("en-IN")}`;
