"use client";

import { useEffect, useState } from "react";
import { Tag } from "lucide-react";
import { type Offer, listOffers } from "@/lib/api/github";

function describeDiscount(offer: Offer) {
  return offer.discount_type === "PERCENTAGE" ? `${offer.discount_value}% off` : `₹${offer.discount_value.toLocaleString("en-IN")} off`;
}

/** Renders nothing until active offers are loaded, and nothing at all if there are none — this is a banner, not a page section. */
export function OffersBanner() {
  const [offers, setOffers] = useState<Offer[] | null>(null);

  useEffect(() => {
    let cancelled = false;
    listOffers()
      .then((all) => {
        if (cancelled) return;
        const now = Date.now();
        setOffers(
          all.filter((o) => o.is_active !== false && new Date(o.starts_at).getTime() <= now && now <= new Date(o.ends_at).getTime())
        );
      })
      .catch(() => {
        if (!cancelled) setOffers([]);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (!offers || offers.length === 0) return null;

  return (
    <div className="border-b border-[#5b4ef9]/15 bg-[#5b4ef9]/5">
      <div className="mx-auto flex max-w-7xl gap-3 overflow-x-auto px-6 py-3">
        {offers.map((offer) => (
          <div
            key={offer.id}
            className="flex shrink-0 items-center gap-2 rounded-full border border-[#5b4ef9]/20 bg-white px-3 py-1.5 text-xs font-medium text-gray-700"
          >
            <Tag className="h-3.5 w-3.5 text-[#5b4ef9]" />
            <span className="font-semibold text-[#5b4ef9]">{offer.offer_code}</span>
            <span>{describeDiscount(offer)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
