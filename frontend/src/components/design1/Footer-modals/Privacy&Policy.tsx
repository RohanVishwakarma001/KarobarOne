import { X } from "lucide-react";

interface PrivacyPolicyModalProps {
  onClose: () => void;
}

export default function PrivacyPolicyModal({ onClose }: PrivacyPolicyModalProps) {
  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="bg-white text-gray-900 rounded-lg max-w-3xl w-full max-h-[85vh] overflow-y-auto relative">
        <div className="sticky top-0 bg-white border-b px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold">Privacy Policy</h2>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full">
            <X size={20} />
          </button>
        </div>

        <div className="px-6 py-4 space-y-4 text-sm leading-relaxed text-gray-700">
          <p className="text-gray-500">Last Updated: [LAST_UPDATED_DATE]</p>
          <p>
            Welcome to [BRAND_NAME] (&quot;Company&quot;, &quot;we&quot;, &quot;our&quot;, or &quot;us&quot;). This Privacy Policy explains how we collect, use, process, store, share, and protect information when you access or use our website, mobile application, products, or services available through [WEBSITE_URL] (&quot;Platform&quot;). By accessing or using the Platform, you acknowledge that you have read and understood this Privacy Policy and agree to the practices described herein.
          </p>

          <h3 className="font-semibold text-base text-gray-900">1. Company Information</h3>
          <p>
            The Platform is owned and operated by [BUSINESS_NAME], legally registered as [LEGAL_NAME], having its registered office at [REGISTERED_ADDRESS].
          </p>
          <p>
            For customer support, you may contact us at [SUPPORT_EMAIL] or [SUPPORT_PHONE]. Our GST Registration Number is [GST_NUMBER].
          </p>
          <p>
            For all privacy-related requests, corrections, complaints, or data deletion requests, users may contact us at [PRIVACY_CONTACT_EMAIL].
          </p>

          <h3 className="font-semibold text-base text-gray-900">2. Information We Collect</h3>
          <p>
            In order to provide our services efficiently, we may collect certain personal, transactional, technical, and operational information from users. This may include your name, email address, mobile number, billing address, shipping address, company name, GST details, account credentials, authentication records, order history, payment status, invoice details, customer service interactions, and communication preferences.
          </p>
          <p>
            We may also collect technical information such as IP address, browser type, operating system, device identifiers, session information, website activity, approximate location information, and other analytics-related data generated through your interaction with the Platform.
          </p>
          <p>
            Where permitted by law and user consent, we may collect marketing-related information to understand preferences, improve customer experience, and communicate relevant offers and updates.
          </p>

          <h3 className="font-semibold text-base text-gray-900">3. How Information Is Collected</h3>
          <p>
            Information may be collected when you create an account, place an order, subscribe to newsletters, submit enquiries, communicate with customer support, participate in promotional campaigns, use our mobile application, interact with advertisements, or browse our Platform.
          </p>
          <p>
            Certain information may also be collected automatically through cookies, tracking technologies, analytics platforms, advertising networks, and authorized third-party integrations used to operate and improve the Platform.
          </p>

          <h3 className="font-semibold text-base text-gray-900">4. Purpose of Collection and Use</h3>
          <p>
            The information collected by us is used for operating the Platform, processing orders, facilitating payments, delivering products, providing customer support, managing returns and refunds, preventing fraud, improving website performance, conducting analytics, communicating with customers, complying with legal obligations, and maintaining business records.
          </p>
          <p>
            Where permitted by applicable laws, we may also use information for marketing, promotional campaigns, customer engagement, product recommendations, and service improvement initiatives.
          </p>

          <h3 className="font-semibold text-base text-gray-900">5. Payment Processing</h3>
          <p>
            Payments made through the Platform may be processed by authorized third-party payment processors. We do not store complete credit card details, debit card details, banking credentials, UPI PINs, or other sensitive payment authentication information on our servers.
          </p>
          <p>
            Payment transactions are handled directly by payment service providers that maintain their own privacy, security, and compliance standards. Users are encouraged to review the privacy policies of such providers before completing any transaction.
          </p>

          <h3 className="font-semibold text-base text-gray-900">6. Shipping and Order Fulfilment</h3>
          <p>
            To facilitate order processing and delivery, we may share relevant customer information with logistics and shipping service providers, including [SHIPPING_PARTNER_NAME].
          </p>
          <p>
            Such information may include the customer&apos;s name, contact number, delivery address, order details, and shipment-related information necessary to complete order fulfilment, provide shipment tracking, manage returns, and deliver customer support services.
          </p>

          <h3 className="font-semibold text-base text-gray-900">7. Marketing Communications</h3>
          <p>
            From time to time, we may send transactional messages, service notifications, order updates, promotional emails, SMS communications, WhatsApp messages, push notifications, and marketing content relating to our products and services.
          </p>
          <p>
            Users may opt out of promotional communications at any time by following the unsubscribe instructions provided in such communications or by contacting us through [SUPPORT_EMAIL]. However, transactional communications relating to orders, payments, security, and account management may continue to be sent where necessary.
          </p>

          <h3 className="font-semibold text-base text-gray-900">8. Cookies and Tracking Technologies</h3>
          <p>
            The Platform uses cookies and similar technologies to enhance functionality, improve user experience, understand visitor behavior, measure advertising effectiveness, and support security operations.
          </p>
          <p>
            These technologies may be used for authentication, cart management, analytics, performance monitoring, personalization, advertising, remarketing, and audience measurement purposes. We may also use services provided by third-party analytics and advertising platforms, including Google Analytics, Google Ads, Meta advertising services, and other authorized technology partners.
          </p>
          <p>
            Users may modify browser settings to manage or disable cookies. However, certain Platform features may not function properly if cookies are disabled.
          </p>

          <h3 className="font-semibold text-base text-gray-900">9. Third-Party Service Providers</h3>
          <p>
            We may engage third-party service providers to assist with website hosting, cloud infrastructure, payment processing, shipping and logistics, analytics, marketing automation, customer support, communication services, security monitoring, and other operational activities.
          </p>
          <p>
            Such service providers may access information only to the extent necessary to perform services on our behalf and are expected to maintain appropriate confidentiality and security standards.
          </p>

          <h3 className="font-semibold text-base text-gray-900">10. Data Storage and Security</h3>
          <p>
            We implement reasonable technical, organizational, and administrative measures to safeguard personal information against unauthorized access, disclosure, alteration, loss, misuse, or destruction.
          </p>
          <p>
            Information may be stored on cloud-based infrastructure, managed hosting environments, third-party business systems, or other authorized storage facilities located within or outside India. While we strive to maintain appropriate security measures, no method of electronic transmission or storage can be guaranteed to be completely secure.
          </p>

          <h3 className="font-semibold text-base text-gray-900">11. Data Retention</h3>
          <p>
            Personal information will be retained for as long as reasonably necessary to provide services, maintain business records, comply with legal requirements, resolve disputes, prevent fraud, enforce agreements, and protect legitimate business interests.
          </p>
          <p>
            Where required by law, certain information may continue to be retained even after a user account has been closed or deleted.
          </p>

          <h3 className="font-semibold text-base text-gray-900">12. User Rights and Requests</h3>
          <p>
            Users who wish to access, correct, update, delete, or otherwise manage their personal information may submit a request to [PRIVACY_CONTACT_EMAIL].
          </p>
          <p>
            We may require reasonable identity verification before processing such requests. Requests will be reviewed and addressed in accordance with applicable laws and operational requirements.
          </p>

          <h3 className="font-semibold text-base text-gray-900">13. Children&apos;s Privacy</h3>
          <p>
            The Platform is intended for individuals who meet the minimum age requirement of [MINIMUM_AGE_REQUIREMENT] years.
          </p>
          <p>
            If we become aware that personal information has been collected from a child without appropriate authorization or legal basis, we may take reasonable steps to delete such information. Parents or legal guardians who believe that a child has provided information through the Platform may contact us for assistance.
          </p>

          <h3 className="font-semibold text-base text-gray-900">14. Legal Compliance</h3>
          <p>
            This Privacy Policy is intended to comply with applicable Indian laws and regulations, including the Digital Personal Data Protection Act, 2023, the Information Technology Act, 2000, relevant rules framed thereunder, and applicable consumer protection and eCommerce regulations.
          </p>

          <h3 className="font-semibold text-base text-gray-900">15. Cross-Border Data Transfers</h3>
          <p>
            Certain technology providers, infrastructure partners, or service providers engaged by us may process or store information on servers located outside India. By using the Platform, users acknowledge and consent to such processing where necessary for providing services, subject to reasonable safeguards and applicable legal requirements.
          </p>

          <h3 className="font-semibold text-base text-gray-900">16. Grievance Officer</h3>
          <p>
            In accordance with applicable laws, privacy-related complaints, concerns, or grievances may be addressed to:
          </p>
          <p>
            Grievance Officer: [GRIEVANCE_OFFICER_NAME]<br />
            Email: [GRIEVANCE_OFFICER_EMAIL]<br />
            Phone: [GRIEVANCE_OFFICER_PHONE]<br />
            Address: [GRIEVANCE_OFFICER_ADDRESS]
          </p>

          <h3 className="font-semibold text-base text-gray-900">17. Changes to this Privacy Policy</h3>
          <p>
            We reserve the right to update, amend, or modify this Privacy Policy from time to time. Any changes will become effective upon publication of the revised version on the Platform. Users are encouraged to review this Privacy Policy periodically to remain informed about how information is handled.
          </p>

          <h3 className="font-semibold text-base text-gray-900">18. Contact Us</h3>
          <p>
            If you have any questions regarding this Privacy Policy or our data handling practices, please contact:<br />
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