"use client"
import { useState } from "react";
import Link from "next/link";
import { Zap, Phone, ArrowLeft } from "lucide-react";

export default function LoginPage() {
  const [phone, setPhone] = useState("");
  const [otp, setOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);

  const handleSendOtp = (e: React.FormEvent) => {
    e.preventDefault();
    // Mock OTP sending
    setOtpSent(true);
  };

  const handleVerifyOtp = (e: React.FormEvent) => {
    e.preventDefault();
    // Mock OTP verification
    alert("Login successful!");
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
          
          {!otpSent ? (
            <form onSubmit={handleSendOtp}>
              <div className="mb-6">
                <label className="block text-gray-700 mb-2">Phone Number</label>
                <div className="relative">
                  <div className="absolute left-4 top-1/2 -translate-y-1/2">
                    <Phone className="w-5 h-5 text-gray-400" />
                  </div>
                  <input
                    type="tel"
                    placeholder="Enter your phone number"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#5b4ef9] focus:border-transparent"
                    required
                  />
                </div>
                <p className="text-sm text-gray-500 mt-2">We'll send you an OTP to verify</p>
              </div>
              
              <button
                type="submit"
                className="w-full bg-[#5b4ef9] text-white py-3 rounded-lg hover:bg-[#4a3ee0] transition-colors"
              >
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
                  OTP sent to {phone}{" "}
                  <button
                    type="button"
                    onClick={() => setOtpSent(false)}
                    className="text-[#5b4ef9] hover:underline"
                  >
                    Change
                  </button>
                </p>
              </div>
              
              <button
                type="submit"
                className="w-full bg-[#5b4ef9] text-white py-3 rounded-lg hover:bg-[#4a3ee0] transition-colors mb-4"
              >
                Verify & Login
              </button>
              
              <button
                type="button"
                onClick={() => alert("OTP resent!")}
                className="w-full text-[#5b4ef9] py-2 hover:underline"
              >
                Resend OTP
              </button>
            </form>
          )}
          
          <div className="mt-8 text-center">
            <p className="text-gray-600 text-sm">
              Don't have an account?{" "}
              <a href="register" className="text-[#5b4ef9] hover:underline font-semibold">
                Sign up free
              </a>
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
