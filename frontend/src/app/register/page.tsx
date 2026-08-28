"use client"
import { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import {
  Zap,
  ArrowLeft,
  Building2,
  User,
  Mail,
  MapPin,
  Lock,
  CheckCircle2,
  ChevronRight,
  ChevronLeft,
} from "lucide-react";

interface FormData {
  businessName: string;
  businessCategory: string;
  businessType: string;
  ownerName: string;
  email: string;
  city: string;
  state: string;
  password: string;
  confirmPassword: string;
  agreedToTerms: boolean;
}

const initialFormData: FormData = {
  businessName: "",
  businessCategory: "",
  businessType: "",
  ownerName: "",
  email: "",
  city: "",
  state: "",
  password: "",
  confirmPassword: "",
  agreedToTerms: false,
};

const STEPS = [
  { id: 1, label: "Business" },
  { id: 2, label: "Contact" },
  { id: 3, label: "Account" },
  { id: 4, label: "Confirm" },
];

export default function RegisterPage() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [errors, setErrors] = useState<Partial<Record<keyof FormData, string>>>({});

  const updateField = (field: keyof FormData, value: string | boolean) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) setErrors((prev) => ({ ...prev, [field]: undefined }));
  };

  const validateStep = (): boolean => {
    const newErrors: Partial<Record<keyof FormData, string>> = {};

    if (step === 1) {
      if (!formData.businessName.trim()) newErrors.businessName = "Business name is required";
      if (!formData.businessCategory.trim()) newErrors.businessCategory = "Select a category";
      if (!formData.businessType.trim()) newErrors.businessType = "Select a business type";
    }

    if (step === 2) {
      if (!formData.ownerName.trim()) newErrors.ownerName = "Owner name is required";
      if (!formData.email.trim()) {
        newErrors.email = "Email is required";
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
        newErrors.email = "Enter a valid email";
      }
      if (!formData.city.trim()) newErrors.city = "City is required";
      if (!formData.state.trim()) newErrors.state = "State is required";
    }

    if (step === 3) {
      if (!formData.password) {
        newErrors.password = "Password is required";
      } else if (formData.password.length < 8) {
        newErrors.password = "Minimum 8 characters";
      }
      if (formData.confirmPassword !== formData.password) {
        newErrors.confirmPassword = "Passwords do not match";
      }
    }

    if (step === 4) {
      if (!formData.agreedToTerms) newErrors.agreedToTerms = "You must accept the terms";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleNext = () => {
    if (validateStep()) setStep((s) => Math.min(s + 1, STEPS.length));
  };

  const handleBack = () => setStep((s) => Math.max(s - 1, 1));

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateStep()) return;
    // Mock registration submit
    alert("Registration successful!");
  };

  return (
    <div className="min-h-screen relative flex items-center justify-center p-6 overflow-hidden bg-gradient-to-br from-[#5b4ef9] to-[#4a3ee0]">
      {/* Ambient glow blobs for glassmorphism depth */}
      <div className="absolute -top-24 -left-24 w-96 h-96 bg-white/20 rounded-full blur-3xl" />
      <div className="absolute -bottom-24 -right-24 w-96 h-96 bg-[#4a3ee0]/40 rounded-full blur-3xl" />

      <div className="w-full max-w-md relative z-10">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-white mb-6 hover:text-white/80 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Home
        </Link>

        <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-8 shadow-2xl">
          <div className="flex items-center justify-center gap-3 mb-6">
            <div className="bg-[#5b4ef9] p-2 rounded-lg">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-semibold text-white">KarobarOne</span>
          </div>

          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-white mb-2">Create Account</h1>
            <p className="text-white/70">Register your business in a few steps</p>
          </div>

          {/* Progress bar */}
          <div className="flex items-center justify-between mb-8">
            {STEPS.map((s, idx) => (
              <div key={s.id} className="flex items-center flex-1">
                <div className="flex flex-col items-center gap-1">
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold transition-colors ${
                      step > s.id
                        ? "bg-white text-[#5b4ef9]"
                        : step === s.id
                        ? "bg-white text-[#5b4ef9] ring-4 ring-white/30"
                        : "bg-white/20 text-white/60"
                    }`}
                  >
                    {step > s.id ? <CheckCircle2 className="w-4 h-4" /> : s.id}
                  </div>
                  <span className="text-[10px] text-white/70">{s.label}</span>
                </div>
                {idx < STEPS.length - 1 && (
                  <div
                    className={`h-0.5 flex-1 mx-1 mb-4 transition-colors ${
                      step > s.id ? "bg-white" : "bg-white/20"
                    }`}
                  />
                )}
              </div>
            ))}
          </div>

          <form onSubmit={handleSubmit}>
            <AnimatePresence mode="wait">
              {step === 1 && (
                <motion.div
                  key="step1"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.2 }}
                  className="space-y-4"
                >
                  <Field
                    icon={<Building2 className="w-5 h-5 text-white/60" />}
                    label="Business Name"
                    placeholder="Enter your business name"
                    value={formData.businessName}
                    onChange={(v) => updateField("businessName", v)}
                    error={errors.businessName}
                  />

                  <div>
                    <label className="block text-white/80 mb-2 text-sm">Business Category</label>
                    <select
                      value={formData.businessCategory}
                      onChange={(e) => updateField("businessCategory", e.target.value)}
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-white/50 [&>option]:text-gray-900"
                    >
                      <option value="">Select category</option>
                      <option value="retail">Retail</option>
                      <option value="services">Services</option>
                      <option value="restaurant">Restaurant / Food</option>
                      <option value="manufacturing">Manufacturing</option>
                      <option value="other">Other</option>
                    </select>
                    {errors.businessCategory && (
                      <p className="text-red-200 text-xs mt-1">{errors.businessCategory}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-white/80 mb-2 text-sm">Business Type</label>
                    <select
                      value={formData.businessType}
                      onChange={(e) => updateField("businessType", e.target.value)}
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-white/50 [&>option]:text-gray-900"
                    >
                      <option value="">Select business type</option>
                      <option value="individual">Individual / Proprietorship</option>
                      <option value="partnership">Partnership</option>
                      <option value="pvt-ltd">Private Limited</option>
                    </select>
                    {errors.businessType && (
                      <p className="text-red-200 text-xs mt-1">{errors.businessType}</p>
                    )}
                  </div>
                </motion.div>
              )}

              {step === 2 && (
                <motion.div
                  key="step2"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.2 }}
                  className="space-y-4"
                >
                  <Field
                    icon={<User className="w-5 h-5 text-white/60" />}
                    label="Owner Name"
                    placeholder="Enter owner's full name"
                    value={formData.ownerName}
                    onChange={(v) => updateField("ownerName", v)}
                    error={errors.ownerName}
                  />
                  <Field
                    icon={<Mail className="w-5 h-5 text-white/60" />}
                    label="Email"
                    type="email"
                    placeholder="you@business.com"
                    value={formData.email}
                    onChange={(v) => updateField("email", v)}
                    error={errors.email}
                  />
                  <div className="grid grid-cols-2 gap-3">
                    <Field
                      icon={<MapPin className="w-5 h-5 text-white/60" />}
                      label="City"
                      placeholder="City"
                      value={formData.city}
                      onChange={(v) => updateField("city", v)}
                      error={errors.city}
                    />
                    <Field
                      label="State"
                      placeholder="State"
                      value={formData.state}
                      onChange={(v) => updateField("state", v)}
                      error={errors.state}
                    />
                  </div>
                </motion.div>
              )}

              {step === 3 && (
                <motion.div
                  key="step3"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.2 }}
                  className="space-y-4"
                >
                  <Field
                    icon={<Lock className="w-5 h-5 text-white/60" />}
                    label="Password"
                    type="password"
                    placeholder="Minimum 8 characters"
                    value={formData.password}
                    onChange={(v) => updateField("password", v)}
                    error={errors.password}
                  />
                  <Field
                    icon={<Lock className="w-5 h-5 text-white/60" />}
                    label="Confirm Password"
                    type="password"
                    placeholder="Re-enter password"
                    value={formData.confirmPassword}
                    onChange={(v) => updateField("confirmPassword", v)}
                    error={errors.confirmPassword}
                  />
                </motion.div>
              )}

              {step === 4 && (
                <motion.div
                  key="step4"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.2 }}
                  className="space-y-4"
                >
                  <div className="bg-white/10 border border-white/20 rounded-lg p-4 space-y-2 text-sm text-white/90">
                    <SummaryRow label="Business" value={formData.businessName} />
                    <SummaryRow label="Category" value={formData.businessCategory} />
                    <SummaryRow label="Owner" value={formData.ownerName} />
                    <SummaryRow label="Email" value={formData.email} />
                    <SummaryRow label="Location" value={`${formData.city}, ${formData.state}`} />
                  </div>

                  <label className="flex items-start gap-2 text-sm text-white/80">
                    <input
                      type="checkbox"
                      checked={formData.agreedToTerms}
                      onChange={(e) => updateField("agreedToTerms", e.target.checked)}
                      className="mt-1"
                    />
                    <span>
                      I agree to the{" "}
                      <a href="#" className="underline hover:text-white">
                        Terms of Service
                      </a>{" "}
                      and{" "}
                      <a href="#" className="underline hover:text-white">
                        Privacy Policy
                      </a>
                    </span>
                  </label>
                  {errors.agreedToTerms && (
                    <p className="text-red-200 text-xs">{errors.agreedToTerms}</p>
                  )}
                </motion.div>
              )}
            </AnimatePresence>

            <div className="flex gap-3 mt-8">
              {step > 1 && (
                <button
                  type="button"
                  onClick={handleBack}
                  className="flex items-center justify-center gap-1 flex-1 bg-white/10 border border-white/20 text-white py-3 rounded-lg hover:bg-white/20 transition-colors"
                >
                  <ChevronLeft className="w-4 h-4" />
                  Back
                </button>
              )}

              {step < STEPS.length ? (
                <button
                  type="button"
                  onClick={handleNext}
                  className="flex items-center justify-center gap-1 flex-1 bg-white text-[#5b4ef9] py-3 rounded-lg font-semibold hover:bg-white/90 transition-colors"
                >
                  Next
                  <ChevronRight className="w-4 h-4" />
                </button>
              ) : (
                <button
                  type="submit"
                  className="flex-1 bg-white text-[#5b4ef9] py-3 rounded-lg font-semibold hover:bg-white/90 transition-colors"
                >
                  Create Account
                </button>
              )}
            </div>
          </form>

          <div className="mt-6 text-center">
            <p className="text-white/70 text-sm">
              Already have an account?{" "}
              <Link href="/login" className="text-white hover:underline font-semibold">
                Login
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function Field({
  icon,
  label,
  placeholder,
  value,
  onChange,
  error,
  type = "text",
}: {
  icon?: React.ReactNode;
  label: string;
  placeholder: string;
  value: string;
  onChange: (v: string) => void;
  error?: string;
  type?: string;
}) {
  return (
    <div>
      <label className="block text-white/80 mb-2 text-sm">{label}</label>
      <div className="relative">
        {icon && <div className="absolute left-4 top-1/2 -translate-y-1/2">{icon}</div>}
        <input
          type={type}
          placeholder={placeholder}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className={`w-full ${
            icon ? "pl-12" : "pl-4"
          } pr-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-white/50`}
        />
      </div>
      {error && <p className="text-red-200 text-xs mt-1">{error}</p>}
    </div>
  );
}

function SummaryRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between">
      <span className="text-white/60">{label}</span>
      <span className="font-medium">{value || "—"}</span>
    </div>
  );
}