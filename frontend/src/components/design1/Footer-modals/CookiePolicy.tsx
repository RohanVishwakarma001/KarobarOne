import { X } from "lucide-react";

interface CookiePolicyModalProps {
  onClose: () => void;
}

export default function CookiePolicyModal({ onClose }: CookiePolicyModalProps) {
  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="bg-white text-gray-900 rounded-lg max-w-3xl w-full max-h-[85vh] overflow-y-auto relative">
        <div className="sticky top-0 bg-white border-b px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold">Cookie Policy</h2>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full">
            <X size={20} />
          </button>
        </div>

        <div className="px-6 py-4 space-y-4 text-sm leading-relaxed text-gray-700">
          <p className="text-gray-500">Last Updated: [LAST_UPDATED_DATE]</p>
          <p>
            This Cookie Policy explains how [BUSINESS_NAME] (&quot;Company&quot;, &quot;we&quot;, &quot;our&quot;, or &quot;us&quot;) uses cookies and similar technologies when you visit or interact with [WEBSITE_URL] (&quot;Platform&quot;).
          </p>
          <p>
            This Cookie Policy should be read together with our Privacy Policy and Terms &amp; Conditions.
          </p>
          <p>
            By continuing to use the Platform, you consent to the use of cookies and similar technologies as described in this Policy, subject to any preferences you may set through available cookie management tools.
          </p>

          <h3 className="font-semibold text-base text-gray-900">1. What Are Cookies?</h3>
          <p>
            Cookies are small text files stored on your device when you visit a website.
          </p>
          <p>
            Cookies help websites function efficiently, remember user preferences, improve user experience, analyze website performance, enhance security, personalize content, and support advertising and marketing activities.
          </p>
          <p>
            Cookies may be stored by us or by authorized third-party service providers integrated with the Platform.
          </p>

          <h3 className="font-semibold text-base text-gray-900">2. What Technologies Do We Use?</h3>
          <p>In addition to cookies, we may use:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>Pixels</li>
            <li>Tracking scripts</li>
            <li>Tags</li>
            <li>Beacons</li>
            <li>Local storage technologies</li>
            <li>SDKs (Software Development Kits)</li>
            <li>Device identifiers</li>
            <li>Session storage</li>
            <li>Browser storage mechanisms</li>
            <li>Mobile application tracking technologies</li>
          </ul>
          <p>
            References to &quot;cookies&quot; in this Policy include these similar technologies unless stated otherwise.
          </p>

          <h3 className="font-semibold text-base text-gray-900">3. Types of Cookies We Use</h3>
          <p className="font-medium text-gray-900">Essential Cookies</p>
          <p>These cookies are necessary for the Platform to function properly. They may be used to:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>Maintain user sessions</li>
            <li>Enable login functionality</li>
            <li>Process transactions</li>
            <li>Maintain shopping carts</li>
            <li>Prevent fraud</li>
            <li>Provide security protections</li>
            <li>Load website features</li>
            <li>Support account management</li>
          </ul>
          <p>Without these cookies, certain Platform features may not function correctly.</p>

          <p className="font-medium text-gray-900">Functional Cookies</p>
          <p>These cookies help remember user preferences and settings. Examples include:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>Language preferences</li>
            <li>Location preferences</li>
            <li>Login preferences</li>
            <li>Saved carts</li>
            <li>User interface settings</li>
            <li>Accessibility settings</li>
          </ul>
          <p>These cookies improve convenience and user experience.</p>

          <p className="font-medium text-gray-900">Analytics and Performance Cookies</p>
          <p>These cookies help us understand how users interact with the Platform. Information collected may include:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>Pages visited</li>
            <li>Time spent on pages</li>
            <li>User journeys</li>
            <li>Device information</li>
            <li>Browser information</li>
            <li>Website performance metrics</li>
            <li>Error tracking information</li>
            <li>Traffic sources</li>
          </ul>
          <p>Analytics providers may include:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>Google Analytics</li>
            <li>Microsoft Clarity</li>
            <li>Hotjar</li>
            <li>Similar analytics providers</li>
          </ul>

          <p className="font-medium text-gray-900">Advertising and Marketing Cookies</p>
          <p>These cookies help us deliver relevant advertisements and measure advertising performance. These cookies may be used to:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>Show personalized advertisements</li>
            <li>Measure advertising effectiveness</li>
            <li>Build audience segments</li>
            <li>Conduct remarketing campaigns</li>
            <li>Track conversions</li>
            <li>Analyze marketing performance</li>
          </ul>
          <p>Advertising platforms may include:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>Google Ads</li>
            <li>Meta Advertising Platforms</li>
            <li>YouTube Advertising</li>
            <li>LinkedIn Advertising</li>
            <li>Other advertising providers</li>
          </ul>

          <p className="font-medium text-gray-900">Social Media Cookies</p>
          <p>
            Social media cookies may be used when users interact with social sharing features, social logins, embedded content, or social media integrations. These cookies may be set by:
          </p>
          <ul className="list-disc pl-6 space-y-1">
            <li>Facebook</li>
            <li>Instagram</li>
            <li>LinkedIn</li>
            <li>YouTube</li>
            <li>Google</li>
            <li>Other social media platforms</li>
          </ul>
          <p>Use of these services may be subject to the privacy policies of those providers.</p>

          <p className="font-medium text-gray-900">Payment and Transaction Cookies</p>
          <p>Payment-related cookies may be used to:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>Facilitate secure transactions</li>
            <li>Prevent fraud</li>
            <li>Verify payment sessions</li>
            <li>Process checkout activities</li>
            <li>Maintain transaction integrity</li>
          </ul>
          <p>These cookies may be associated with third-party payment service providers.</p>

          <p className="font-medium text-gray-900">Customer Support Cookies</p>
          <p>Customer support technologies may be used to:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>Operate chat systems</li>
            <li>Manage support requests</li>
            <li>Improve customer service</li>
            <li>Store communication preferences</li>
            <li>Maintain support sessions</li>
          </ul>

          <h3 className="font-semibold text-base text-gray-900">4. Information Collected Through Cookies</h3>
          <p>Depending on the cookies used, information collected may include:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>IP address</li>
            <li>Device identifiers</li>
            <li>Browser type</li>
            <li>Operating system</li>
            <li>Geographic region</li>
            <li>Website activity</li>
            <li>Session information</li>
            <li>Shopping activity</li>
            <li>Product interactions</li>
            <li>Referral sources</li>
            <li>Advertising interactions</li>
            <li>Purchase activity</li>
            <li>User preferences</li>
          </ul>
          <p>The information collected may be linked with information described in our Privacy Policy.</p>

          <h3 className="font-semibold text-base text-gray-900">5. Third-Party Cookies</h3>
          <p>Certain cookies may be placed by third-party providers integrated with the Platform. Such providers may include:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>Analytics providers</li>
            <li>Payment processors</li>
            <li>Advertising platforms</li>
            <li>Shipping partners</li>
            <li>CRM systems</li>
            <li>Marketing automation providers</li>
            <li>Customer support providers</li>
            <li>Social media platforms</li>
          </ul>
          <p>We do not control third-party cookies and recommend reviewing the privacy policies of those providers.</p>

          <h3 className="font-semibold text-base text-gray-900">6. How We Use Cookie Information</h3>
          <p>Cookie data may be used for purposes including:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>Operating the Platform</li>
            <li>Improving website performance</li>
            <li>Enhancing security</li>
            <li>Personalizing user experiences</li>
            <li>Measuring traffic</li>
            <li>Analyzing customer behavior</li>
            <li>Supporting marketing campaigns</li>
            <li>Processing transactions</li>
            <li>Preventing fraud</li>
            <li>Providing customer support</li>
            <li>Improving products and services</li>
          </ul>

          <h3 className="font-semibold text-base text-gray-900">7. Managing Cookies</h3>
          <p>Most browsers allow users to:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>View stored cookies</li>
            <li>Delete cookies</li>
            <li>Block cookies</li>
            <li>Restrict certain cookies</li>
            <li>Configure cookie preferences</li>
          </ul>
          <p>Browser settings differ by provider and device.</p>
          <p>Disabling certain cookies may affect Platform functionality and user experience.</p>

          <h3 className="font-semibold text-base text-gray-900">8. Mobile Applications</h3>
          <p>Where the Company provides mobile applications, similar technologies may be used to collect information relating to:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>App usage</li>
            <li>Device identifiers</li>
            <li>Crash reports</li>
            <li>Session activity</li>
            <li>Performance analytics</li>
            <li>Marketing attribution</li>
          </ul>
          <p>Users may manage permissions through device settings where available.</p>

          <h3 className="font-semibold text-base text-gray-900">9. Data Retention</h3>
          <p>Cookie retention periods vary depending on the type of cookie used.</p>
          <p>
            Some cookies expire automatically when a browsing session ends, while others may remain stored for longer periods until deleted or expired.
          </p>
          <p>Retention periods may vary based on operational, security, analytics, and legal requirements.</p>

          <h3 className="font-semibold text-base text-gray-900">10. Changes to This Cookie Policy</h3>
          <p>We reserve the right to modify, update, amend, or replace this Cookie Policy at any time.</p>
          <p>Updated versions shall become effective upon publication on the Platform.</p>
          <p>Continued use of the Platform after publication of updated versions constitutes acceptance of the revised Policy.</p>

          <h3 className="font-semibold text-base text-gray-900">11. Contact Information</h3>
          <p>For questions regarding this Cookie Policy, please contact:</p>
          <p>
            [BUSINESS_NAME]<br />
            Email: [SUPPORT_EMAIL]<br />
            Phone: [SUPPORT_PHONE]<br />
            Website: [WEBSITE_URL]<br />
            Address: [REGISTERED_ADDRESS]
          </p>
        </div>

        <div className="sticky bottom-0 bg-white border-t px-6 py-3 flex justify-end">
          <button
            onClick={onClose}
            className="bg-gray-900 text-white px-4 py-2 rounded-md hover:bg-gray-800 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}