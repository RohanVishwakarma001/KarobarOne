"use client"
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { toast } from "sonner";
import { Zap, Mail, Lock, ArrowLeft, Loader2 } from "lucide-react";
import { ApiError } from "@/lib/api/coreClient";
import { login, verifyLogin } from "@/lib/api/auth";
import { saveSession, getSession } from "@/lib/auth/session";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [otpId, setOtpId] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSendOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await login(email, password);
      setOtpId(res.otpId);
      toast.success(res.message);
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Could not log in. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleVerifyOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!otpId) return;
    setSubmitting(true);
    try {
      const tokens = await verifyLogin(otpId, otp);
      saveSession(tokens);
      const session = getSession();
      toast.success("Logged in successfully.");
      router.push(session?.tenantId ? "/store-owner-dashboard" : "/onboarding/business");
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Incorrect or expired OTP.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#5b4ef9] to-[#4a3ee0] flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-white mb-8 hover:text-white/80 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Home
        </Link>

        <div className="bg-white rounded-2xl p-8 shadow-2xl">
          <div className="flex items-center justify-center gap-3 mb-8">
            <div className="bg-[#5b4ef9] p-2 rounded-lg">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-semibold text-gray-900">KarobarOne</span>
          </div>

          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome Back</h1>
            <p className="text-gray-600">Login to access your dashboard</p>
          </div>

          {!otpId ? (
            <form onSubmit={handleSendOtp}>
              <div className="mb-4">
                <label className="block text-gray-700 mb-2">Email</label>
                <div className="relative">
                  <div className="absolute left-4 top-1/2 -translate-y-1/2">
                    <Mail className="w-5 h-5 text-gray-400" />
                  </div>
                  <input
                    type="email"
                    placeholder="you@business.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#5b4ef9] focus:border-transparent"
                    required
                  />
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-gray-700 mb-2">Password</label>
                <div className="relative">
                  <div className="absolute left-4 top-1/2 -translate-y-1/2">
                    <Lock className="w-5 h-5 text-gray-400" />
                  </div>
                  <input
                    type="password"
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#5b4ef9] focus:border-transparent"
                    required
                  />
                </div>
                <p className="text-sm text-gray-500 mt-2">We'll email you an OTP to confirm it's you</p>
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full flex items-center justify-center gap-2 bg-[#5b4ef9] text-white py-3 rounded-lg hover:bg-[#4a3ee0] transition-colors disabled:opacity-60"
              >
                {submitting && <Loader2 className="w-4 h-4 animate-spin" />}
                Send OTP
              </button>
            </form>
          ) : (
            <form onSubmit={handleVerifyOtp}>
              <div className="mb-6">
                <label className="block text-gray-700 mb-2">Enter OTP</label>
                <input
                  type="text"
                  placeholder="Enter 6-digit OTP"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  maxLength={6}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#5b4ef9] focus:border-transparent text-center text-2xl tracking-widest"
                  required
                />
                <p className="text-sm text-gray-500 mt-2">
                  OTP sent to {email}{" "}
                  <button
                    type="button"
                    onClick={() => setOtpId(null)}
                    className="text-[#5b4ef9] hover:underline"
                  >
                    Change
                  </button>
                </p>
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full flex items-center justify-center gap-2 bg-[#5b4ef9] text-white py-3 rounded-lg hover:bg-[#4a3ee0] transition-colors mb-4 disabled:opacity-60"
              >
                {submitting && <Loader2 className="w-4 h-4 animate-spin" />}
                Verify & Login
              </button>

              <button
                type="button"
                onClick={handleSendOtp}
                className="w-full text-[#5b4ef9] py-2 hover:underline"
              >
                Resend OTP
              </button>
            </form>
          )}

          <div className="mt-8 text-center">
            <p className="text-gray-600 text-sm">
              Don't have an account?{" "}
              <Link href="/register" className="text-[#5b4ef9] hover:underline font-semibold">
                Sign up free
              </Link>
            </p>
          </div>
        </div>

        <p className="text-white text-center text-sm mt-6">
          By continuing, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  );
}
