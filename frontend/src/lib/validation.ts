export function isValidPhone(phone: string): boolean {
  const cleaned = phone.replace(/[\s-]/g, "")
  return /^(\+91)?[6-9]\d{9}$/.test(cleaned)
}

export function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

export function isValidGST(gst: string): boolean {
  return /^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/.test(gst.toUpperCase())
}

export function isValidPAN(pan: string): boolean {
  return /^[A-Z]{5}\d{4}[A-Z]{1}$/.test(pan.toUpperCase())
}

export function isValidBusinessName(name: string): boolean {
  return name.trim().length > 0 && name.length <= 100
}