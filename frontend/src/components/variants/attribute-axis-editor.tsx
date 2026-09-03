"use client";

import { useState } from "react";
import { AnimatePresence, Reorder, motion } from "framer-motion";
import { Plus, Wand2, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { springs, useReducedMotion } from "@/lib/motion";

export type AttributeAxis = {
  id: string;
  name: string;
  values: string[];
};

/** Cartesian product of every axis's values, e.g. Size:[S,M] x Color:[Red,Blue] -> 4 combinations. */
export function generateCombinations(axes: AttributeAxis[]): Record<string, string>[] {
  const usable = axes.filter((a) => a.name.trim() && a.values.length > 0);
  if (usable.length === 0) return [];
  return usable.reduce<Record<string, string>[]>(
    (acc, axis) =>
      acc.flatMap((combo) => axis.values.map((value) => ({ ...combo, [axis.name.trim()]: value }))),
    [{}],
  );
}

export function AttributeAxisEditor({
  axes,
  onAxesChange,
  onGenerate,
}: {
  axes: AttributeAxis[];
  onAxesChange: (axes: AttributeAxis[]) => void;
  onGenerate: (combinations: Record<string, string>[]) => void;
}) {
  const [nameDraft, setNameDraft] = useState("");
  const [valuesDraft, setValuesDraft] = useState("");

  const addAxis = () => {
    const name = nameDraft.trim();
    const values = Array.from(
      new Set(
        valuesDraft
          .split(",")
          .map((v) => v.trim())
          .filter(Boolean),
      ),
    );
    if (!name || values.length === 0) return;
    onAxesChange([...axes, { id: crypto.randomUUID(), name, values }]);
    setNameDraft("");
    setValuesDraft("");
  };

  const removeAxis = (id: string) => onAxesChange(axes.filter((a) => a.id !== id));

  const reorderAxisValues = (axisId: string, nextValues: string[]) =>
    onAxesChange(axes.map((a) => (a.id === axisId ? { ...a, values: nextValues } : a)));

  const reducedMotion = useReducedMotion();
  const combinationCount = generateCombinations(axes).length;

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold text-slate-900">Options</h3>
          <p className="text-xs text-slate-500">Add each option axis (Size, Color, Material...) with its values.</p>
        </div>
      </div>

      <div className="mt-4 space-y-2">
        <AnimatePresence initial={false}>
          {axes.map((axis) => (
            <motion.div
              key={axis.id}
              layout
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.18 }}
              className="flex items-center gap-3 overflow-hidden rounded-xl border border-slate-100 bg-slate-50/60 px-3 py-2.5"
            >
              <span className="shrink-0 text-sm font-medium text-slate-700">{axis.name}</span>
              {/* Drag to reorder — this order feeds generateCombinations(), so it's not just cosmetic: it's the order variant rows come out in. */}
              <Reorder.Group
                as="div"
                axis="x"
                values={axis.values}
                onReorder={(next) => reorderAxisValues(axis.id, next)}
                className="flex flex-1 flex-wrap gap-1.5"
              >
                {axis.values.map((v) => (
                  <Reorder.Item
                    key={v}
                    value={v}
                    as="span"
                    whileDrag={reducedMotion ? undefined : { scale: 1.08, boxShadow: "0 6px 16px -4px rgba(15,23,42,0.25)" }}
                    transition={springs.snappy}
                    className="cursor-grab rounded-full bg-white px-2.5 py-0.5 text-xs font-medium text-slate-600 ring-1 ring-slate-200 active:cursor-grabbing"
                  >
                    {v}
                  </Reorder.Item>
                ))}
              </Reorder.Group>
              <button
                type="button"
                onClick={() => removeAxis(axis.id)}
                className="shrink-0 rounded-full p-1 text-slate-400 hover:bg-slate-200 hover:text-slate-600"
              >
                <X className="h-3.5 w-3.5" />
                <span className="sr-only">Remove {axis.name}</span>
              </button>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      <div className="mt-4 flex flex-col gap-2 sm:flex-row">
        <Input
          placeholder="Axis name (e.g. Size)"
          value={nameDraft}
          onChange={(e) => setNameDraft(e.target.value)}
          className="sm:w-40"
        />
        <Input
          placeholder="Values, comma-separated (e.g. S, M, L)"
          value={valuesDraft}
          onChange={(e) => setValuesDraft(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              addAxis();
            }
          }}
          className="flex-1"
        />
        <Button type="button" variant="outline" onClick={addAxis} disabled={!nameDraft.trim() || !valuesDraft.trim()}>
          <Plus className="h-4 w-4" />
          Add axis
        </Button>
      </div>

      <div className="mt-4 flex items-center justify-between border-t border-slate-100 pt-4">
        <p className="text-xs text-slate-500">
          {combinationCount > 0
            ? `${combinationCount} combination${combinationCount === 1 ? "" : "s"} will be generated`
            : "Add at least one axis with values"}
        </p>
        <Button
          type="button"
          onClick={() => onGenerate(generateCombinations(axes))}
          disabled={combinationCount === 0}
          className="bg-[#5b4ef9] hover:bg-[#4a3ee0]"
        >
          <Wand2 className="h-4 w-4" />
          Generate variants
        </Button>
      </div>
    </div>
  );
}
