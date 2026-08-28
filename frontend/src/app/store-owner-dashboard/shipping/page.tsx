"use client";

import { useEffect, useMemo, useState } from "react";
import { toast } from "sonner";
import { Loader2, Plus, Truck } from "lucide-react";
import { AdminShell } from "@/components/commerce/AdminShell";
import {
  ApiError,
  type ShippingPartner,
  type ShippingProfile,
  type ShippingZone,
  type ShippingRate,
  createShippingPartner,
  listShippingPartners,
  createShippingProfile,
  listShippingProfiles,
  createShippingZone,
  listShippingZones,
  createShippingRate,
  listShippingRates,
} from "@/lib/api/github";

type Tab = "partners" | "profiles" | "zones" | "rates";
const TABS: { id: Tab; label: string }[] = [
  { id: "partners", label: "Partners" },
  { id: "profiles", label: "Profiles" },
  { id: "zones", label: "Zones" },
  { id: "rates", label: "Rates" },
];

const inputCls = "rounded-lg border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-[#5b4ef9]";
const cardCls = "mb-6 grid gap-3 rounded-2xl border border-slate-200 bg-white p-5 sm:grid-cols-2 lg:grid-cols-4";
const tableWrapCls = "overflow-hidden rounded-2xl border border-slate-200 bg-white";
const thCls = "border-b border-slate-200 px-5 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500";
const tdCls = "px-5 py-3 text-sm";

export default function ShippingManagementPage() {
  const [tab, setTab] = useState<Tab>("partners");

  const [partners, setPartners] = useState<ShippingPartner[]>([]);
  const [profiles, setProfiles] = useState<ShippingProfile[]>([]);
  const [zones, setZones] = useState<ShippingZone[]>([]);
  const [rates, setRates] = useState<ShippingRate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = () => {
    setLoading(true);
    setError(null);
    Promise.all([listShippingPartners(), listShippingProfiles(), listShippingZones(), listShippingRates()])
      .then(([p, pr, z, r]) => {
        setPartners(p);
        setProfiles(pr);
        setZones(z);
        setRates(r);
      })
      .catch((e) => setError(e instanceof ApiError ? e.message : "Could not load shipping configuration."))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  return (
    <AdminShell title="Shipping Management" badge="SH">
      <div className="mb-5 flex flex-wrap gap-2">
        {TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`rounded-full px-4 py-2 text-sm font-medium transition ${tab === t.id ? "bg-[#5b4ef9] text-white" : "border border-slate-200 bg-white text-slate-600 hover:border-[#5b4ef9]/30"}`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {loading && (
        <div className="flex items-center justify-center gap-2 rounded-2xl border border-slate-200 bg-white px-6 py-16 text-sm text-slate-500">
          <Loader2 className="h-4 w-4 animate-spin" /> Loading shipping configuration…
        </div>
      )}
      {!loading && error && <div className="rounded-2xl border border-slate-200 bg-white px-6 py-16 text-center font-medium text-red-600">{error}</div>}

      {!loading && !error && tab === "partners" && <PartnersSection partners={partners} onCreated={load} />}
      {!loading && !error && tab === "profiles" && <ProfilesSection profiles={profiles} onCreated={load} />}
      {!loading && !error && tab === "zones" && <ZonesSection zones={zones} onCreated={load} />}
      {!loading && !error && tab === "rates" && <RatesSection rates={rates} profiles={profiles} zones={zones} onCreated={load} />}
    </AdminShell>
  );
}

function EmptyState({ label }: { label: string }) {
  return (
    <div className="px-6 py-16 text-center">
      <Truck className="mx-auto h-8 w-8 text-slate-300" />
      <p className="mt-4 font-medium">{label}</p>
    </div>
  );
}

function PartnersSection({ partners, onCreated }: { partners: ShippingPartner[]; onCreated: () => void }) {
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [website, setWebsite] = useState("");

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!code.trim() || !name.trim()) {
      toast.error("Partner code and name are required.");
      return;
    }
    setSaving(true);
    try {
      await createShippingPartner({ partner_code: code.trim(), partner_name: name.trim(), website_url: website.trim() || undefined });
      toast.success("Shipping partner added.");
      setCode("");
      setName("");
      setWebsite("");
      setShowForm(false);
      onCreated();
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not add partner.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <section>
      <div className="mb-4 flex items-center justify-between">
        <p className="text-sm text-slate-600">Courier partners this store ships with.</p>
        <button onClick={() => setShowForm((v) => !v)} className="inline-flex items-center gap-2 rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white hover:bg-[#4a3ee0]">
          <Plus className="h-4 w-4" /> New partner
        </button>
      </div>
      {showForm && (
        <form onSubmit={handleCreate} className={cardCls}>
          <input className={inputCls} placeholder="Partner code" value={code} onChange={(e) => setCode(e.target.value)} />
          <input className={inputCls} placeholder="Partner name" value={name} onChange={(e) => setName(e.target.value)} />
          <input className={inputCls} placeholder="Website URL (optional)" value={website} onChange={(e) => setWebsite(e.target.value)} />
          <div className="flex gap-2">
            <button disabled={saving} type="submit" className="rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white disabled:opacity-60">
              {saving ? "Saving…" : "Add"}
            </button>
            <button type="button" onClick={() => setShowForm(false)} className="rounded-lg px-4 py-2 text-sm text-slate-500">
              Cancel
            </button>
          </div>
        </form>
      )}
      <div className={tableWrapCls}>
        {partners.length === 0 ? (
          <EmptyState label="No shipping partners yet" />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50">
                <tr>
                  {["Code", "Name", "API enabled", "Active"].map((h) => (
                    <th key={h} className={thCls}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {partners.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-50/70">
                    <td className={tdCls + " font-medium"}>{p.partner_code}</td>
                    <td className={tdCls}>{p.partner_name}</td>
                    <td className={tdCls}>{p.api_enabled ? "Yes" : "No"}</td>
                    <td className={tdCls}>{p.is_active ? "Yes" : "No"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
}

function ProfilesSection({ profiles, onCreated }: { profiles: ShippingProfile[]; onCreated: () => void }) {
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [threshold, setThreshold] = useState("");

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim()) {
      toast.error("Profile name is required.");
      return;
    }
    setSaving(true);
    try {
      await createShippingProfile({ profile_name: name.trim(), description: description.trim() || undefined, free_shipping_threshold: threshold ? Number(threshold) : undefined });
      toast.success("Shipping profile created.");
      setName("");
      setDescription("");
      setThreshold("");
      setShowForm(false);
      onCreated();
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not create profile.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <section>
      <div className="mb-4 flex items-center justify-between">
        <p className="text-sm text-slate-600">Shipping profiles group rates and free-shipping thresholds.</p>
        <button onClick={() => setShowForm((v) => !v)} className="inline-flex items-center gap-2 rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white hover:bg-[#4a3ee0]">
          <Plus className="h-4 w-4" /> New profile
        </button>
      </div>
      {showForm && (
        <form onSubmit={handleCreate} className={cardCls}>
          <input className={inputCls} placeholder="Profile name" value={name} onChange={(e) => setName(e.target.value)} />
          <input className={inputCls} placeholder="Description (optional)" value={description} onChange={(e) => setDescription(e.target.value)} />
          <input type="number" step="0.01" className={inputCls} placeholder="Free shipping threshold (optional)" value={threshold} onChange={(e) => setThreshold(e.target.value)} />
          <div className="flex gap-2">
            <button disabled={saving} type="submit" className="rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white disabled:opacity-60">
              {saving ? "Saving…" : "Create"}
            </button>
            <button type="button" onClick={() => setShowForm(false)} className="rounded-lg px-4 py-2 text-sm text-slate-500">
              Cancel
            </button>
          </div>
        </form>
      )}
      <div className={tableWrapCls}>
        {profiles.length === 0 ? (
          <EmptyState label="No shipping profiles yet" />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50">
                <tr>
                  {["Name", "Description", "Free shipping over", "Active"].map((h) => (
                    <th key={h} className={thCls}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {profiles.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-50/70">
                    <td className={tdCls + " font-medium"}>{p.profile_name}</td>
                    <td className={tdCls + " text-slate-600"}>{p.description ?? "—"}</td>
                    <td className={tdCls + " text-slate-600"}>{p.free_shipping_threshold != null ? `₹${p.free_shipping_threshold.toLocaleString("en-IN")}` : "—"}</td>
                    <td className={tdCls}>{p.is_active ? "Yes" : "No"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
}

function ZonesSection({ zones, onCreated }: { zones: ShippingZone[]; onCreated: () => void }) {
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [name, setName] = useState("");
  const [code, setCode] = useState("");
  const [country, setCountry] = useState("India");
  const [state, setState] = useState("");
  const [city, setCity] = useState("");

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim() || !code.trim() || !country.trim() || !state.trim() || !city.trim()) {
      toast.error("Zone name, code, country, state, and city are required.");
      return;
    }
    setSaving(true);
    try {
      await createShippingZone({ zone_name: name.trim(), zone_code: code.trim(), country: country.trim(), state: state.trim(), city: city.trim() });
      toast.success("Shipping zone created.");
      setName("");
      setCode("");
      setState("");
      setCity("");
      setShowForm(false);
      onCreated();
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not create zone.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <section>
      <div className="mb-4 flex items-center justify-between">
        <p className="text-sm text-slate-600">Geographic zones used for shipping-rate calculation.</p>
        <button onClick={() => setShowForm((v) => !v)} className="inline-flex items-center gap-2 rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white hover:bg-[#4a3ee0]">
          <Plus className="h-4 w-4" /> New zone
        </button>
      </div>
      {showForm && (
        <form onSubmit={handleCreate} className={cardCls}>
          <input className={inputCls} placeholder="Zone name" value={name} onChange={(e) => setName(e.target.value)} />
          <input className={inputCls} placeholder="Zone code" value={code} onChange={(e) => setCode(e.target.value)} />
          <input className={inputCls} placeholder="Country" value={country} onChange={(e) => setCountry(e.target.value)} />
          <input className={inputCls} placeholder="State" value={state} onChange={(e) => setState(e.target.value)} />
          <input className={inputCls} placeholder="City" value={city} onChange={(e) => setCity(e.target.value)} />
          <div className="flex gap-2">
            <button disabled={saving} type="submit" className="rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white disabled:opacity-60">
              {saving ? "Saving…" : "Create"}
            </button>
            <button type="button" onClick={() => setShowForm(false)} className="rounded-lg px-4 py-2 text-sm text-slate-500">
              Cancel
            </button>
          </div>
        </form>
      )}
      <div className={tableWrapCls}>
        {zones.length === 0 ? (
          <EmptyState label="No shipping zones yet" />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50">
                <tr>
                  {["Zone", "Code", "Location", "Active"].map((h) => (
                    <th key={h} className={thCls}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {zones.map((z) => (
                  <tr key={z.id} className="hover:bg-slate-50/70">
                    <td className={tdCls + " font-medium"}>{z.zone_name}</td>
                    <td className={tdCls + " text-slate-600"}>{z.zone_code}</td>
                    <td className={tdCls + " text-slate-600"}>{[z.city, z.state, z.country].filter(Boolean).join(", ")}</td>
                    <td className={tdCls}>{z.is_active ? "Yes" : "No"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
}

function RatesSection({
  rates,
  profiles,
  zones,
  onCreated,
}: {
  rates: ShippingRate[];
  profiles: ShippingProfile[];
  zones: ShippingZone[];
  onCreated: () => void;
}) {
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [profileId, setProfileId] = useState("");
  const [zoneId, setZoneId] = useState("");
  const [minWeight, setMinWeight] = useState("");
  const [maxWeight, setMaxWeight] = useState("");
  const [charge, setCharge] = useState("");
  const [daysMin, setDaysMin] = useState("");
  const [daysMax, setDaysMax] = useState("");

  const profileName = useMemo(() => new Map(profiles.map((p) => [p.id, p.profile_name])), [profiles]);
  const zoneName = useMemo(() => new Map(zones.map((z) => [z.id, z.zone_name])), [zones]);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!profileId || !zoneId || !minWeight || !maxWeight || !charge || !daysMin || !daysMax) {
      toast.error("All rate fields are required.");
      return;
    }
    setSaving(true);
    try {
      await createShippingRate({
        shipping_profile_id: profileId,
        shipping_zone_id: zoneId,
        minimum_weight: Number(minWeight),
        maximum_weight: Number(maxWeight),
        shipping_charge: Number(charge),
        estimated_days_min: Number(daysMin),
        estimated_days_max: Number(daysMax),
      });
      toast.success("Shipping rate created.");
      setMinWeight("");
      setMaxWeight("");
      setCharge("");
      setDaysMin("");
      setDaysMax("");
      setShowForm(false);
      onCreated();
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : "Could not create rate.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <section>
      <div className="mb-4 flex items-center justify-between">
        <p className="text-sm text-slate-600">Rates by weight band, per profile/zone combination.</p>
        <button
          onClick={() => setShowForm((v) => !v)}
          disabled={profiles.length === 0 || zones.length === 0}
          className="inline-flex items-center gap-2 rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white hover:bg-[#4a3ee0] disabled:opacity-40"
        >
          <Plus className="h-4 w-4" /> New rate
        </button>
      </div>
      {(profiles.length === 0 || zones.length === 0) && (
        <p className="mb-4 text-xs text-amber-600">Create at least one shipping profile and zone before adding a rate.</p>
      )}
      {showForm && (
        <form onSubmit={handleCreate} className={cardCls}>
          <select className={inputCls} value={profileId} onChange={(e) => setProfileId(e.target.value)}>
            <option value="">Select profile</option>
            {profiles.map((p) => (
              <option key={p.id} value={p.id}>{p.profile_name}</option>
            ))}
          </select>
          <select className={inputCls} value={zoneId} onChange={(e) => setZoneId(e.target.value)}>
            <option value="">Select zone</option>
            {zones.map((z) => (
              <option key={z.id} value={z.id}>{z.zone_name}</option>
            ))}
          </select>
          <input type="number" step="0.01" className={inputCls} placeholder="Min weight (kg)" value={minWeight} onChange={(e) => setMinWeight(e.target.value)} />
          <input type="number" step="0.01" className={inputCls} placeholder="Max weight (kg)" value={maxWeight} onChange={(e) => setMaxWeight(e.target.value)} />
          <input type="number" step="0.01" className={inputCls} placeholder="Shipping charge" value={charge} onChange={(e) => setCharge(e.target.value)} />
          <input type="number" className={inputCls} placeholder="Min delivery days" value={daysMin} onChange={(e) => setDaysMin(e.target.value)} />
          <input type="number" className={inputCls} placeholder="Max delivery days" value={daysMax} onChange={(e) => setDaysMax(e.target.value)} />
          <div className="flex gap-2">
            <button disabled={saving} type="submit" className="rounded-lg bg-[#5b4ef9] px-4 py-2 text-sm font-medium text-white disabled:opacity-60">
              {saving ? "Saving…" : "Create"}
            </button>
            <button type="button" onClick={() => setShowForm(false)} className="rounded-lg px-4 py-2 text-sm text-slate-500">
              Cancel
            </button>
          </div>
        </form>
      )}
      <div className={tableWrapCls}>
        {rates.length === 0 ? (
          <EmptyState label="No shipping rates yet" />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50">
                <tr>
                  {["Profile", "Zone", "Weight band", "Charge", "Delivery"].map((h) => (
                    <th key={h} className={thCls}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {rates.map((r) => (
                  <tr key={r.id} className="hover:bg-slate-50/70">
                    <td className={tdCls + " font-medium"}>{profileName.get(r.shipping_profile_id) ?? r.shipping_profile_id.slice(0, 8)}</td>
                    <td className={tdCls + " text-slate-600"}>{zoneName.get(r.shipping_zone_id) ?? r.shipping_zone_id.slice(0, 8)}</td>
                    <td className={tdCls + " text-slate-600"}>{r.minimum_weight}–{r.maximum_weight} kg</td>
                    <td className={tdCls}>₹{r.shipping_charge.toLocaleString("en-IN")}</td>
                    <td className={tdCls + " text-slate-600"}>{r.estimated_days_min}–{r.estimated_days_max} days</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
}
