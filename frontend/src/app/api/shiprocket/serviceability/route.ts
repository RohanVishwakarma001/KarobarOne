import { NextRequest, NextResponse } from "next/server";
import { GITHUB_API_BASE_URL } from "@/lib/api/config";
import { httpGetWithBody } from "@/lib/server/httpGetWithBody";

// Browser fetch() can't send a body on GET; this route proxies the call server-side.
// See lib/server/httpGetWithBody.ts for why.
export async function POST(req: NextRequest) {
  const body = await req.json();
  const { status, data } = await httpGetWithBody(`${GITHUB_API_BASE_URL}/shiprocket/serviceability`, body);
  return NextResponse.json(data, { status });
}
