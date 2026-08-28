"use client";

import React, { useState, useRef, useEffect } from "react";

// ─── Types ────────────────────────────────────────────────────
type Step = "closed" | "form" | "otp" | "password" | "chat";
type MessageType = "text" | "image" | "audio" | "file";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  type: MessageType;
  fileName?: string;
  fileUrl?: string;
  timestamp: Date;
}

// ─── Mock AI replies ──────────────────────────────────────────
const AI_REPLIES = [
  "Hello! Welcome to Excellence. How can I help you today? 😊",
  "Great question! Our team is dedicated to providing the best solutions for your business.",
  "I&apos;d be happy to help you with that. Could you share more details?",
  "Absolutely! Excellence offers a wide range of premium products tailored to your needs.",
  "Thank you for reaching out! Is there anything else I can help you with?",
  "Our support team is available 24/7 to assist you. What would you like to know?",
];

// ─── Icons (inline SVG to avoid extra deps) ───────────────────
const SendIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
    <line x1="22" y1="2" x2="11" y2="13" /><polygon points="22 2 15 22 11 13 2 9 22 2" />
  </svg>
);
const CloseIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
    <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
  </svg>
);
const MinimizeIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
    <line x1="5" y1="12" x2="19" y2="12" />
  </svg>
);
const ChatIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-6 h-6">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
  </svg>
);
const AttachIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
    <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" />
  </svg>
);
const ImageIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
    <rect x="3" y="3" width="18" height="18" rx="2" /><circle cx="8.5" cy="8.5" r="1.5" />
    <polyline points="21 15 16 10 5 21" />
  </svg>
);
const MicIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
    <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
    <path d="M19 10v2a7 7 0 0 1-14 0v-2" /><line x1="12" y1="19" x2="12" y2="23" />
    <line x1="8" y1="23" x2="16" y2="23" />
  </svg>
);
const BotIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
    <rect x="3" y="11" width="18" height="10" rx="2" /><circle cx="12" cy="5" r="2" />
    <path d="M12 7v4" /><line x1="8" y1="16" x2="8" y2="16" /><line x1="16" y1="16" x2="16" y2="16" />
  </svg>
);
const EyeIcon = ({ show }: { show: boolean }) => show ? (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" />
  </svg>
) : (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
    <line x1="1" y1="1" x2="23" y2="23" />
  </svg>
);

// ─── Timestamp formatter ──────────────────────────────────────
function formatTime(d: Date) {
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

// ─── Typing Indicator ─────────────────────────────────────────
function TypingIndicator() {
  return (
    <div className="flex items-end gap-2 mb-3">
      <div className="w-7 h-7 rounded-full bg-purple-100 flex items-center justify-center flex-shrink-0">
        <BotIcon />
      </div>
      <div className="bg-white border border-gray-100 rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm">
        <div className="flex gap-1 items-center h-4">
          {[0, 1, 2].map((i) => (
            <span
              key={i}
              className="w-2 h-2 rounded-full bg-purple-400 inline-block"
              style={{ animation: `bounce 1.2s ease-in-out ${i * 0.2}s infinite` }}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── Input Field ──────────────────────────────────────────────
function FormInput({
  label, type = "text", value, onChange, placeholder, error, rightEl
}: {
  label: string; type?: string; value: string;
  onChange: (v: string) => void; placeholder?: string;
  error?: string; rightEl?: React.ReactNode;
}) {
  return (
    <div className="mb-3">
      <label className="block text-xs font-semibold text-gray-600 mb-1">{label}</label>
      <div className="relative">
        <input
          type={type}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className={`w-full px-3 py-2.5 text-sm rounded-xl border ${error ? "border-red-400 bg-red-50" : "border-gray-200 bg-gray-50"
            } focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent transition-all pr-${rightEl ? "10" : "3"}`}
        />
        {rightEl && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2">{rightEl}</div>
        )}
      </div>
      {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
    </div>
  );
}

// ─── OTP Input ────────────────────────────────────────────────
function OTPInput({ value, onChange }: { value: string[]; onChange: (v: string[]) => void }) {
  const refs = [useRef<HTMLInputElement>(null), useRef<HTMLInputElement>(null),
  useRef<HTMLInputElement>(null), useRef<HTMLInputElement>(null),
  useRef<HTMLInputElement>(null), useRef<HTMLInputElement>(null)];

  const handleChange = (i: number, v: string) => {
    if (!/^\d*$/.test(v)) return;
    const next = [...value];
    next[i] = v.slice(-1);
    onChange(next);
    if (v && i < 5) refs[i + 1].current?.focus();
  };

  const handleKeyDown = (i: number, e: React.KeyboardEvent) => {
    if (e.key === "Backspace" && !value[i] && i > 0) refs[i - 1].current?.focus();
  };

  return (
    <div className="flex gap-2 justify-center my-4">
      {[0, 1, 2, 3, 4, 5].map((i) => (
        <input
          key={i}
          ref={refs[i]}
          type="text"
          inputMode="numeric"
          maxLength={1}
          value={value[i] || ""}
          onChange={(e) => handleChange(i, e.target.value)}
          onKeyDown={(e) => handleKeyDown(i, e)}
          className="w-10 h-12 text-center text-lg font-bold border-2 rounded-xl border-gray-200 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200 transition-all bg-gray-50"
        />
      ))}
    </div>
  );
}

// ─── Message Bubble ───────────────────────────────────────────
function MessageBubble({ msg }: { msg: Message }) {
  const isUser = msg.role === "user";
  return (
    <div className={`flex items-end gap-2 mb-3 ${isUser ? "flex-row-reverse" : ""}`}>
      {!isUser && (
        <div className="w-7 h-7 rounded-full bg-purple-100 flex items-center justify-center flex-shrink-0">
          <BotIcon />
        </div>
      )}
      <div className={`max-w-[78%] ${isUser ? "items-end" : "items-start"} flex flex-col gap-1`}>
        <div
          className={`px-4 py-2.5 rounded-2xl text-sm shadow-sm ${isUser
            ? "bg-gradient-to-br from-purple-600 to-purple-700 text-white rounded-br-sm"
            : "bg-white border border-gray-100 text-gray-800 rounded-bl-sm"
            }`}
        >
          {msg.type === "image" && msg.fileUrl && (
            <img src={msg.fileUrl} alt="uploaded" className="max-w-full rounded-lg mb-1 max-h-32 object-cover" />
          )}
          {msg.type === "audio" && msg.fileUrl && (
            <audio controls src={msg.fileUrl} className="w-full max-w-[200px]" />
          )}
          {msg.type === "file" && (
            <div className="flex items-center gap-2 text-xs">
              <AttachIcon />
              <span className="underline">{msg.fileName}</span>
            </div>
          )}
          {msg.content && <p className="leading-relaxed">{msg.content}</p>}
        </div>
        <span className="text-[10px] text-gray-400 px-1">{formatTime(msg.timestamp)}</span>
      </div>
    </div>
  );
}

// ─── Main Widget ──────────────────────────────────────────────
export default function ChatWidget() {
  const [step, setStep] = useState<Step>("closed");
  const [minimized, setMinimized] = useState(false);
  const [isNew, setIsNew] = useState(true); // toggle to test both flows

  // Form state
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [otp, setOtp] = useState<string[]>(["", "", "", "", "", ""]);
  const [password, setPassword] = useState("");
  const [confirmPwd, setConfirmPwd] = useState("");
  const [showPwd, setShowPwd] = useState(false);
  const [skipPassword, setSkipPassword] = useState(false);
  const [formError, setFormError] = useState("");
  const [otpError, setOtpError] = useState("");
  const [_otpSent, setOtpSent] = useState(false);
  const [otpResendTimer, setOtpResendTimer] = useState(0);
  const [loading, setLoading] = useState(false);

  // Chat state
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [_userName, setUserName] = useState("");

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const imageInputRef = useRef<HTMLInputElement>(null);
  const audioInputRef = useRef<HTMLInputElement>(null);

  // Auto scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  // OTP resend timer
  useEffect(() => {
    if (otpResendTimer > 0) {
      const t = setTimeout(() => setOtpResendTimer((p) => p - 1), 1000);
      return () => clearTimeout(t);
    }
  }, [otpResendTimer]);

  // ── Form submit ──────────────────────────────────────────────
  const handleFormSubmit = () => {
    setFormError("");
    if (!name.trim()) return setFormError("Please enter your name.");
    if (!email.trim() || !/\S+@\S+\.\S+/.test(email)) return setFormError("Enter a valid email.");
    if (!phone.trim() || phone.length < 10) return setFormError("Enter a valid phone number.");

    setLoading(true);
    // Simulate API: check if user exists (static mock)
    setTimeout(() => {
      setLoading(false);
      setIsNew(phone === "9999999999" ? false : true); // mock: 9999999999 = existing user
      setOtpSent(true);
      setOtpResendTimer(30);
      setStep("otp");
    }, 1000);
  };

  // ── OTP submit ───────────────────────────────────────────────
  const handleOTPSubmit = () => {
    setOtpError("");
    const entered = otp.join("");
    if (entered.length < 6) return setOtpError("Please enter the complete 6-digit OTP.");

    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      // MOCK: any 6-digit otp works except "000000"
      if (entered === "000000") return setOtpError("Invalid OTP. Please try again.");

      setUserName(name);
      if (isNew) {
        setStep("password");
      } else {
        startChat();
      }
    }, 900);
  };

  // ── Password submit ──────────────────────────────────────────
  const handlePasswordSubmit = () => {
    if (!skipPassword) {
      if (password.length < 6) return setFormError("Password must be at least 6 characters.");
      if (password !== confirmPwd) return setFormError("Passwords do not match.");
    }
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      startChat();
    }, 700);
  };

  // ── Start chat ───────────────────────────────────────────────
  const startChat = () => {
    setStep("chat");
    const welcome: Message = {
      id: "welcome",
      role: "assistant",
      content: `Hi ${name}! 👋 Welcome to Excellence. I'm your AI assistant. How can I help you today?`,
      type: "text",
      timestamp: new Date(),
    };
    setMessages([welcome]);
  };

  // ── Send message ─────────────────────────────────────────────
  const sendMessage = (content: string, type: MessageType = "text", fileUrl?: string, fileName?: string) => {
    if (!content.trim() && !fileUrl) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
      type,
      fileUrl,
      fileName,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    // Simulate AI response
    const delay = 1000 + Math.random() * 1000;
    setTimeout(() => {
      setIsTyping(false);
      const reply = AI_REPLIES[Math.floor(Math.random() * AI_REPLIES.length)];
      const aiMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: reply,
        type: "text",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMsg]);
    }, delay);
  };

  // ── File handlers ────────────────────────────────────────────
  const handleFile = (file: File, type: MessageType) => {
    const url = URL.createObjectURL(file);
    const label = type === "image" ? "" : type === "audio" ? "" : file.name;
    sendMessage(label, type, url, file.name);
  };

  // ── Resend OTP ───────────────────────────────────────────────
  const resendOTP = () => {
    setOtp(["", "", "", "", "", ""]);
    setOtpError("");
    setOtpResendTimer(30);
  };

  // ── Open chat ────────────────────────────────────────────────
  const openChat = () => {
    setMinimized(false);
    if (step === "closed") setStep("form");
  };

  // ── Panel visibility ─────────────────────────────────────────
  const showPanel = step !== "closed" && !minimized;

  return (
    <>
      {/* Bounce keyframes */}
      <style>{`
        @keyframes bounce {
          0%, 60%, 100% { transform: translateY(0); }
          30% { transform: translateY(-6px); }
        }
        @keyframes slideUp {
          from { opacity: 0; transform: translateY(20px) scale(0.97); }
          to { opacity: 1; transform: translateY(0) scale(1); }
        }
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        .chat-panel { animation: slideUp 0.25s cubic-bezier(.4,0,.2,1); }
        .msg-in { animation: fadeIn 0.2s ease; }
      `}</style>

      {/* ── Floating button ── */}
      <button
        onClick={openChat}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-gradient-to-br from-purple-600 to-purple-800 text-white shadow-xl flex items-center justify-center hover:scale-110 active:scale-95 transition-transform"
        aria-label="Open chat"
      >
        {step !== "closed" && !minimized ? <CloseIcon /> : <ChatIcon />}
        {/* Unread dot */}
        {step === "closed" && (
          <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full border-2 border-white text-[9px] font-bold flex items-center justify-center text-white">1</span>
        )}
      </button>

      {/* ── Chat panel ── */}
      {showPanel && (
        <div
          className="chat-panel fixed bottom-24 right-6 z-50 w-[350px] max-w-[calc(100vw-24px)] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-gray-100"
          style={{ height: step === "chat" ? "520px" : "auto", maxHeight: "80vh" }}
        >
          {/* Header */}
          <div className="bg-gradient-to-r from-purple-600 to-purple-800 px-4 py-3 flex items-center justify-between flex-shrink-0">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-full bg-white/20 flex items-center justify-center">
                <BotIcon />
              </div>
              <div>
                <p className="text-white font-semibold text-sm leading-tight">Excellence AI</p>
                <div className="flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-green-400 inline-block" />
                  <span className="text-white/80 text-[10px]">Online • Replies instantly</span>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-1">
              <button
                onClick={() => setMinimized(true)}
                className="w-7 h-7 rounded-full hover:bg-white/20 flex items-center justify-center text-white transition-colors"
              >
                <MinimizeIcon />
              </button>
              <button
                onClick={() => { setStep("closed"); setMinimized(false); }}
                className="w-7 h-7 rounded-full hover:bg-white/20 flex items-center justify-center text-white transition-colors"
              >
                <CloseIcon />
              </button>
            </div>
          </div>

          {/* ── FORM STEP ── */}
          {step === "form" && (
            <div className="p-5 overflow-y-auto">
              <div className="mb-4">
                <h3 className="font-bold text-gray-800 text-base">Start a conversation</h3>
                <p className="text-xs text-gray-500 mt-0.5">Please fill in your details to continue</p>
              </div>
              <FormInput label="Full Name" value={name} onChange={setName} placeholder="John Doe" />
              <FormInput label="Email Address" type="email" value={email} onChange={setEmail} placeholder="you@example.com" />
              <FormInput label="Phone Number" type="tel" value={phone} onChange={setPhone} placeholder="+91 98765 43210" />
              {formError && (
                <div className="bg-red-50 border border-red-200 text-red-600 text-xs rounded-lg px-3 py-2 mb-3">
                  {formError}
                </div>
              )}
              <button
                onClick={handleFormSubmit}
                disabled={loading}
                className="w-full py-2.5 bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-xl text-sm font-semibold hover:from-purple-700 hover:to-purple-800 transition-all disabled:opacity-60 flex items-center justify-center gap-2"
              >
                {loading ? (
                  <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                  </svg>
                ) : "Send OTP →"}
              </button>
              <p className="text-[10px] text-gray-400 text-center mt-3">
                We&apos;ll send a one-time password to verify your number.
              </p>
            </div>
          )}

          {/* ── OTP STEP ── */}
          {step === "otp" && (
            <div className="p-5 overflow-y-auto">
              <button onClick={() => setStep("form")} className="text-xs text-purple-600 hover:underline mb-3 flex items-center gap-1">
                ← Back
              </button>
              <h3 className="font-bold text-gray-800 text-base">Verify your number</h3>
              <p className="text-xs text-gray-500 mt-1">
                {isNew ? "New account" : "Welcome back!"} — OTP sent to <span className="font-semibold text-gray-700">{phone}</span>
              </p>
              <OTPInput value={otp} onChange={setOtp} />
              {otpError && (
                <div className="bg-red-50 border border-red-200 text-red-600 text-xs rounded-lg px-3 py-2 mb-3 text-center">
                  {otpError}
                </div>
              )}
              <button
                onClick={handleOTPSubmit}
                disabled={loading}
                className="w-full py-2.5 bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-xl text-sm font-semibold hover:from-purple-700 hover:to-purple-800 transition-all disabled:opacity-60 flex items-center justify-center gap-2"
              >
                {loading ? (
                  <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                  </svg>
                ) : "Verify OTP"}
              </button>
              <div className="text-center mt-3">
                {otpResendTimer > 0 ? (
                  <p className="text-xs text-gray-400">Resend OTP in <span className="font-semibold text-gray-600">{otpResendTimer}s</span></p>
                ) : (
                  <button onClick={resendOTP} className="text-xs text-purple-600 hover:underline">
                    Resend OTP
                  </button>
                )}
              </div>
              <p className="text-[10px] text-gray-400 text-center mt-2">
                💡 Tip: Use <strong>000000</strong> to test wrong OTP, any other 6 digits to verify.
              </p>
            </div>
          )}

          {/* ── PASSWORD STEP (new users only) ── */}
          {step === "password" && (
            <div className="p-5 overflow-y-auto">
              <h3 className="font-bold text-gray-800 text-base">Set a password</h3>
              <p className="text-xs text-gray-500 mt-1 mb-4">Optional — you can skip and login via OTP anytime.</p>
              {!skipPassword && (
                <>
                  <FormInput
                    label="Password"
                    type={showPwd ? "text" : "password"}
                    value={password}
                    onChange={setPassword}
                    placeholder="Min. 6 characters"
                    rightEl={
                      <button onClick={() => setShowPwd((p) => !p)} className="text-gray-400 hover:text-gray-600">
                        <EyeIcon show={showPwd} />
                      </button>
                    }
                  />
                  <FormInput
                    label="Confirm Password"
                    type={showPwd ? "text" : "password"}
                    value={confirmPwd}
                    onChange={setConfirmPwd}
                    placeholder="Repeat password"
                  />
                </>
              )}
              {formError && (
                <div className="bg-red-50 border border-red-200 text-red-600 text-xs rounded-lg px-3 py-2 mb-3">
                  {formError}
                </div>
              )}
              <button
                onClick={handlePasswordSubmit}
                disabled={loading}
                className="w-full py-2.5 bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-xl text-sm font-semibold hover:from-purple-700 hover:to-purple-800 transition-all disabled:opacity-60 flex items-center justify-center gap-2"
              >
                {loading ? (
                  <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                  </svg>
                ) : skipPassword ? "Start Chatting →" : "Save & Start Chatting →"}
              </button>
              <button
                onClick={() => { setSkipPassword((p) => !p); setFormError(""); }}
                className="w-full text-xs text-gray-500 hover:text-purple-600 mt-2 underline transition-colors"
              >
                {skipPassword ? "Set a password instead" : "Skip — login via OTP next time"}
              </button>
            </div>
          )}

          {/* ── CHAT STEP ── */}
          {step === "chat" && (
            <>
              {/* Messages area */}
              <div className="flex-1 overflow-y-auto px-4 py-3 bg-gray-50 space-y-0">
                {messages.length === 0 && (
                  <div className="flex flex-col items-center justify-center h-full text-center py-10">
                    <div className="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center mb-3">
                      <BotIcon />
                    </div>
                    <p className="text-sm text-gray-500">No messages yet.<br />Start the conversation!</p>
                  </div>
                )}
                {messages.map((msg) => (
                  <div key={msg.id} className="msg-in">
                    <MessageBubble msg={msg} />
                  </div>
                ))}
                {isTyping && <TypingIndicator />}
                <div ref={messagesEndRef} />
              </div>

              {/* Input bar */}
              <div className="px-3 py-3 bg-white border-t border-gray-100 flex-shrink-0">
                <div className="flex items-end gap-2">
                  {/* Attachment buttons */}
                  <div className="flex gap-1 pb-0.5">
                    <button
                      onClick={() => imageInputRef.current?.click()}
                      className="w-8 h-8 rounded-full hover:bg-purple-50 text-gray-400 hover:text-purple-600 flex items-center justify-center transition-colors"
                      title="Send image"
                    >
                      <ImageIcon />
                    </button>
                    <button
                      onClick={() => audioInputRef.current?.click()}
                      className="w-8 h-8 rounded-full hover:bg-purple-50 text-gray-400 hover:text-purple-600 flex items-center justify-center transition-colors"
                      title="Send audio"
                    >
                      <MicIcon />
                    </button>
                    <button
                      onClick={() => fileInputRef.current?.click()}
                      className="w-8 h-8 rounded-full hover:bg-purple-50 text-gray-400 hover:text-purple-600 flex items-center justify-center transition-colors"
                      title="Attach file"
                    >
                      <AttachIcon />
                    </button>
                  </div>

                  {/* Text input */}
                  <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" && !e.shiftKey) {
                        e.preventDefault();
                        sendMessage(input);
                      }
                    }}
                    placeholder="Type a message..."
                    rows={1}
                    className="flex-1 resize-none text-sm bg-gray-50 border border-gray-200 rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent max-h-24 overflow-y-auto"
                  />

                  {/* Send */}
                  <button
                    onClick={() => sendMessage(input)}
                    disabled={!input.trim()}
                    className="w-9 h-9 rounded-full bg-gradient-to-br from-purple-600 to-purple-700 text-white flex items-center justify-center hover:from-purple-700 hover:to-purple-800 disabled:opacity-40 transition-all flex-shrink-0"
                  >
                    <SendIcon />
                  </button>
                </div>

                {/* Hidden file inputs */}
                <input ref={imageInputRef} type="file" accept="image/*" className="hidden"
                  onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0], "image")} />
                <input ref={audioInputRef} type="file" accept="audio/*" className="hidden"
                  onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0], "audio")} />
                <input ref={fileInputRef} type="file" className="hidden"
                  onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0], "file")} />
              </div>

              {/* Footer */}
              <div className="bg-white border-t border-gray-50 px-3 py-1.5 text-center flex-shrink-0">
                <p className="text-[10px] text-gray-400">Powered by <span className="font-semibold text-purple-600">Excellence AI</span> • Your data is secure 🔒</p>
              </div>
            </>
          )}
        </div>
      )}

      {/* ── Minimized pill ── */}
      {minimized && step !== "closed" && (
        <button
          onClick={() => setMinimized(false)}
          className="fixed bottom-24 right-6 z-50 bg-white border border-gray-200 shadow-lg rounded-full px-4 py-2 flex items-center gap-2 hover:shadow-xl transition-shadow text-sm font-medium text-gray-700"
        >
          <div className="w-2 h-2 rounded-full bg-green-400" />
          Excellence AI
          <span className="text-gray-400">▲</span>
        </button>
      )}
    </>
  );
}
