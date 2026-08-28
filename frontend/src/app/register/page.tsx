"use client"
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { toast } from "sonner";
import { motion, AnimatePresence } from "framer-motion";
import {
  Zap,
  ArrowLeft,
  User,
  Mail,
  Phone,
  Lock,
  CheckCircle2,
  Loader2,
} from "lucide-react";
import { ApiError } from "@/lib/api/coreClient";
import { register, verifyRegister } from "@/lib/api/auth";
import { saveSession } from "@/lib/auth/session";

interface FormData {
  firstName: string;
  lastName: string;
  email: string;
  mobile: string;
  password: string;
  confirmPassword: string;
}

const initialFormData: FormData = {
  firstName: "",
  lastName: "",
  email: "",
  mobile: "",
  password: "",
  confirmPassword: "",
};

const STEPS = [
  { id: 1, label: "Account" },
  { id: 2, label: "Verify" },
];

export default function RegisterPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [errors, setErrors] = useState<Partial<Record<keyof FormData, string>>>({});
  const [submitting, setSubmitting] = useState(false);
  const [otpId, setOtpId] = useState<string | null>(null);
  const [otp, setOtp] = useState("");

  const updateField = (field: keyof FormData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) setErrors((prev) => ({ ...prev, [field]: undefined }));
  };

  const validateAccountStep = (): boolean => {
    const newErrors: Partial<Record<keyof FormData, string>> = {};

    if (!formData.firstName.trim()) newErrors.firstName = "First name is required";
    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = "Enter a valid email";
    }
    if (!formData.mobile.trim()) newErrors.mobile = "Mobile number is required";
    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 8) {
      newErrors.password = "Minimum 8 characters";
    }
    if (formData.confirmPassword !== formData.password) {
      newErrors.confirmPassword = "Passwords do not match";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleCreateAccount = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateAccountStep()) return;
    setSubmitting(true);
    try {
      const res = await register({
        firstName: formData.firstName.trim(),
        lastName: formData.lastName.trim() || undefined,
        email: formData.email.trim(),
        mobile: formData.mobile.trim(),
        password: formData.password,
      });
      setOtpId(res.otpId);
      toast.success(res.message);
      setStep(2);
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Could not create your account.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!otpId) return;
    setSubmitting(true);
    try {
      const tokens = await verifyRegister(otpId, otp);
      saveSession(tokens);
      toast.success("Account verified! Let's set up your business.");
      router.push("/onboarding/business");
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Incorrect or expired OTP.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen relative flex items-center justify-center p-6 overflow-hidden bg-gradient-to-br from-[#5b4ef9] to-[#4a3ee0]">
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
            <p className="text-white/70">Set up your KarobarOne login</p>
          </div>

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

          <AnimatePresence mode="wait">
            {step === 1 && (
              <motion.form
                key="step1"
                onSubmit={handleCreateAccount}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.2 }}
                className="space-y-4"
              >
                <div className="grid grid-cols-2 gap-3">
                  <Field
                    icon={<User className="w-5 h-5 text-white/60" />}
                    label="First Name"
                    placeholder="First name"
                    value={formData.firstName}
                    onChange={(v) => updateField("firstName", v)}
                    error={errors.firstName}
                  />
                  <Field
                    label="Last Name"
                    placeholder="Last name"
                    value={formData.lastName}
                    onChange={(v) => updateField("lastName", v)}
                  />
                </div>
                <Field
                  icon={<Mail className="w-5 h-5 text-white/60" />}
                  label="Email"
                  type="email"
                  placeholder="you@business.com"
                  value={formData.email}
                  onChange={(v) => updateField("email", v)}
                  error={errors.email}
                />
                <Field
                  icon={<Phone className="w-5 h-5 text-white/60" />}
                  label="Mobile"
                  placeholder="+91XXXXXXXXXX"
                  value={formData.mobile}
                  onChange={(v) => updateField("mobile", v)}
                  error={errors.mobile}
                />
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

                <button
                  type="submit"
                  disabled={submitting}
                  className="w-full flex items-center justify-center gap-2 bg-white text-[#5b4ef9] py-3 rounded-lg font-semibold hover:bg-white/90 transition-colors disabled:opacity-60"
                >
                  {submitting && <Loader2 className="w-4 h-4 animate-spin" />}
                  Create Account
                </button>
              </motion.form>
            )}

            {step === 2 && (
              <motion.form
                key="step2"
                onSubmit={handleVerify}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.2 }}
                className="space-y-4"
              >
                <p className="text-white/70 text-sm text-center">
                  We emailed a 6-digit code to {formData.email}
                </p>
                <input
                  type="text"
                  placeholder="Enter 6-digit OTP"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  maxLength={6}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-white/50 text-center text-2xl tracking-widest"
                  required
                />
                <button
                  type="submit"
                  disabled={submitting}
                  className="w-full flex items-center justify-center gap-2 bg-white text-[#5b4ef9] py-3 rounded-lg font-semibold hover:bg-white/90 transition-colors disabled:opacity-60"
                >
                  {submitting && <Loader2 className="w-4 h-4 animate-spin" />}
                  Verify & Continue
                </button>
                <button
                  type="button"
                  onClick={() => setStep(1)}
                  className="w-full text-white/70 py-2 hover:underline text-sm"
                >
                  Back to account details
                </button>
              </motion.form>
            )}
          </AnimatePresence>

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
