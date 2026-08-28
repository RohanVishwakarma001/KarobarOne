import { Construction } from "lucide-react";

export default function UnderMaintenancePage() {
  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center px-6">
      <Construction className="w-16 h-16 text-[#5b4ef9] mb-6" />
      <h1 className="text-3xl font-semibold mb-3 text-center">
        Page Under Maintenance
      </h1>
      <p className="text-gray-400 text-center max-w-md">
        We&apos;re working on this page. Please check back soon.
      </p>
    </div>
  );
}
