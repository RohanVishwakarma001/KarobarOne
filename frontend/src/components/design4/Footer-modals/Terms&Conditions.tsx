import { X } from "lucide-react";

interface TermsConditionsModalProps {
  onClose: () => void;
}

export default function TermsConditionsModal({ onClose }: TermsConditionsModalProps) {
  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="bg-white text-gray-900 rounded-lg max-w-3xl w-full max-h-[85vh] overflow-y-auto relative">
        <div className="sticky top-0 bg-white border-b px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold">Terms and Conditions</h2>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full">
            <X size={20} />
          </button>
        </div>

        <div className="px-6 py-4 space-y-4 text-sm leading-relaxed text-gray-700">
          <p className="text-gray-500">Last Updated: [LAST_UPDATED_DATE]</p>
          <p>
            Welcome to [BRAND_NAME]. These Terms and Conditions (&quot;Terms&quot;) govern your access to and use of the website, mobile application, products, services, content, and related features available through [WEBSITE_URL] (&quot;Platform&quot;).
          </p>
          <p>
            The Platform is owned and operated by [BUSINESS_NAME], legally operating as [LEGAL_NAME].
          </p>
          <p>
            By accessing, browsing, registering on, or purchasing from the Platform, you acknowledge that you have read, understood, and agreed to be bound by these Terms and all applicable laws and regulations.
          </p>
          <p>
            If you do not agree with these Terms, you must discontinue use of the Platform.
          </p>

          <h3 className="font-semibold text-base text-gray-900">1. Eligibility</h3>
          <p>
            The Platform is intended for individuals who are at least [MINIMUM_AGE_REQUIREMENT] years of age and are legally capable of entering into binding contracts under applicable laws.
          </p>
          <p>
            By using the Platform, you represent and warrant that you satisfy these eligibility requirements.
          </p>

          <h3 className="font-semibold text-base text-gray-900">2. Account Registration</h3>
          <p>
            Certain features of the Platform may require account registration.
          </p>
          <p>
            Users may register through email authentication, mobile verification, OTP authentication, social login providers, or other methods made available by the Company.
          </p>
          <p>
            You are responsible for maintaining the confidentiality of your account credentials and for all activities conducted through your account.
          </p>
          <p>
            You agree to provide accurate, complete, and updated information at all times.
          </p>
          <p>
            The Company reserves the right to suspend, restrict, or terminate accounts that contain inaccurate information, violate these Terms, or engage in suspicious activities.
          </p>

          <h3 className="font-semibold text-base text-gray-900">3. Products and Services</h3>
          <p>
            The Company makes reasonable efforts to display products, descriptions, specifications, images, pricing, and availability information accurately.
          </p>
          <p>
            However, actual product appearance, color, packaging, specifications, or features may vary due to manufacturing updates, display settings, or other factors.
          </p>
          <p>
            The Company reserves the right to modify, discontinue, replace, or update products, services, offers, pricing, and specifications without prior notice.
          </p>

          <h3 className="font-semibold text-base text-gray-900">4. Pricing and Payments</h3>
          <p>
            All prices displayed on the Platform are stated in Indian Rupees (INR) unless otherwise specified.
          </p>
          <p>
            Applicable taxes, shipping charges, handling fees, convenience charges, and other charges may be added during checkout where applicable.
          </p>
          <p>
            Payments may be processed through authorized third-party payment processors and banking partners.
          </p>
          <p>
            The Company does not store complete payment credentials such as card numbers, CVV details, UPI PINs, banking passwords, or similar authentication information.
          </p>
          <p>
            The Company reserves the right to refuse, cancel, or hold any transaction suspected of fraud, unauthorized activity, pricing errors, or legal violations.
          </p>

          <h3 className="font-semibold text-base text-gray-900">5. Order Acceptance</h3>
          <p>
            Placing an order on the Platform constitutes an offer to purchase products.
          </p>
          <p>
            Order confirmation does not guarantee order acceptance.
          </p>
          <p>
            The Company reserves the right to accept, reject, cancel, or limit any order at its sole discretion, including but not limited to circumstances involving inventory shortages, pricing errors, suspected fraud, payment verification failures, legal restrictions, or operational limitations.
          </p>
          <p>
            In cases where payment has already been received for a cancelled order, refunds shall be processed in accordance with the applicable Refund Policy.
          </p>

          <h3 className="font-semibold text-base text-gray-900">6. Shipping and Delivery</h3>
          <p>
            Products may be shipped through authorized logistics and delivery partners, including [SHIPPING_PARTNER_NAME].
          </p>
          <p>
            Estimated delivery timelines are provided for convenience only and are not guaranteed unless expressly stated otherwise.
          </p>
          <p>
            Delivery delays may occur due to weather conditions, transportation disruptions, public holidays, government actions, force majeure events, remote serviceability areas, or other circumstances beyond the Company&apos;s control.
          </p>
          <p>
            Risk of loss and ownership of products shall transfer to the customer in accordance with applicable laws and the Company&apos;s shipping policies.
          </p>

          <h3 className="font-semibold text-base text-gray-900">7. Returns, Refunds, and Cancellations</h3>
          <p>
            Returns, refunds, exchanges, replacements, and order cancellations shall be governed by the Company&apos;s separate Refund and Cancellation Policy available on the Platform.
          </p>
          <p>
            By placing an order, you agree to the terms of the applicable refund, return, replacement, exchange, and cancellation policies.
          </p>

          <h3 className="font-semibold text-base text-gray-900">8. User Conduct</h3>
          <p>Users agree not to:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>Violate any applicable law or regulation.</li>
            <li>Use the Platform for unlawful purposes.</li>
            <li>Impersonate another individual or entity.</li>
            <li>Interfere with Platform operations.</li>
            <li>Attempt unauthorized access to systems or accounts.</li>
            <li>Introduce malicious software, malware, or harmful code.</li>
            <li>Manipulate reviews, ratings, promotions, or transactions.</li>
            <li>Engage in fraudulent, abusive, or deceptive activities.</li>
          </ul>
          <p>
            The Company reserves the right to investigate and take appropriate action against violations.
          </p>

          <h3 className="font-semibold text-base text-gray-900">9. Intellectual Property</h3>
          <p>
            All content available on the Platform, including text, graphics, logos, images, videos, software, trademarks, designs, databases, source code, user interfaces, and branding materials, is owned by or licensed to the Company and is protected under applicable intellectual property laws.
          </p>
          <p>
            Users may not reproduce, distribute, modify, publish, transmit, reverse engineer, or commercially exploit any content without prior written authorization.
          </p>

          <h3 className="font-semibold text-base text-gray-900">10. Promotional Offers</h3>
          <p>
            The Company may provide discounts, coupons, promotional campaigns, loyalty rewards, referral programs, or special offers from time to time.
          </p>
          <p>
            Such promotions may be modified, suspended, withdrawn, or cancelled at any time without prior notice.
          </p>
          <p>Additional terms may apply to specific promotions.</p>

          <h3 className="font-semibold text-base text-gray-900">11. User Generated Content</h3>
          <p>
            Where the Platform permits reviews, ratings, testimonials, comments, photographs, videos, feedback, or other user submissions, users grant the Company a non-exclusive, royalty-free, worldwide license to use, reproduce, display, publish, modify, and distribute such content for lawful business purposes.
          </p>
          <p>
            The Company reserves the right to remove content that violates applicable laws, these Terms, or community standards.
          </p>

          <h3 className="font-semibold text-base text-gray-900">12. Third-Party Services</h3>
          <p>
            The Platform may contain integrations, services, content, links, advertisements, payment systems, analytics tools, or features operated by third parties.
          </p>
          <p>
            The Company does not control and is not responsible for the policies, practices, availability, content, or actions of third-party providers.
          </p>
          <p>
            Use of third-party services remains subject to the terms and policies of such providers.
          </p>

          <h3 className="font-semibold text-base text-gray-900">13. Privacy</h3>
          <p>
            Collection and processing of personal information shall be governed by the Privacy Policy available on the Platform.
          </p>
          <p>
            By using the Platform, you consent to the collection, processing, and use of information in accordance with the Privacy Policy.
          </p>

          <h3 className="font-semibold text-base text-gray-900">14. Disclaimer of Warranties</h3>
          <p>
            The Platform, products, services, content, and related materials are provided on an &quot;as is&quot; and &quot;as available&quot; basis.
          </p>
          <p>
            To the maximum extent permitted by law, the Company disclaims all warranties, representations, and guarantees, whether express or implied, including warranties relating to merchantability, fitness for a particular purpose, non-infringement, uninterrupted availability, or error-free operation.
          </p>
          <p>
            Nothing in these Terms shall exclude rights that cannot legally be excluded under applicable consumer protection laws.
          </p>

          <h3 className="font-semibold text-base text-gray-900">15. Limitation of Liability</h3>
          <p>
            To the fullest extent permitted by applicable law, the Company, its directors, officers, employees, affiliates, suppliers, partners, and representatives shall not be liable for any indirect, incidental, special, consequential, exemplary, or punitive damages arising from or related to the use of the Platform, products, services, or transactions.
          </p>
          <p>
            The Company&apos;s aggregate liability for any claim shall not exceed the amount actually paid by the customer for the specific product giving rise to the claim, unless otherwise required by law.
          </p>

          <h3 className="font-semibold text-base text-gray-900">16. Indemnification</h3>
          <p>
            You agree to indemnify, defend, and hold harmless the Company and its affiliates from any claims, losses, damages, liabilities, penalties, expenses, or costs arising from your violation of these Terms, misuse of the Platform, infringement of third-party rights, or violation of applicable laws.
          </p>

          <h3 className="font-semibold text-base text-gray-900">17. Force Majeure</h3>
          <p>
            The Company shall not be liable for delays, interruptions, failures, or inability to perform obligations caused by events beyond its reasonable control, including natural disasters, government actions, pandemics, strikes, labor disputes, internet outages, cyberattacks, transportation disruptions, or similar events.
          </p>

          <h3 className="font-semibold text-base text-gray-900">18. Suspension and Termination</h3>
          <p>
            The Company may suspend, restrict, or terminate access to the Platform without prior notice where it reasonably believes that a user has violated these Terms, engaged in unlawful activities, created security risks, or otherwise acted contrary to the interests of the Company or other users.
          </p>

          <h3 className="font-semibold text-base text-gray-900">19. Governing Law and Jurisdiction</h3>
          <p>
            These Terms shall be governed by and interpreted in accordance with the laws of India.
          </p>
          <p>
            Any disputes arising from or relating to these Terms, the Platform, or transactions conducted through the Platform shall be subject to the exclusive jurisdiction of the courts located in [JURISDICTION_CITY].
          </p>

          <h3 className="font-semibold text-base text-gray-900">20. Grievance Officer</h3>
          <p>For complaints, concerns, or grievances relating to the Platform, users may contact:</p>
          <p>
            Grievance Officer: [GRIEVANCE_OFFICER_NAME]<br />
            Email: [GRIEVANCE_OFFICER_EMAIL]<br />
            Phone: [GRIEVANCE_OFFICER_PHONE]<br />
            Address: [GRIEVANCE_OFFICER_ADDRESS]
          </p>

          <h3 className="font-semibold text-base text-gray-900">21. Changes to Terms</h3>
          <p>
            The Company reserves the right to modify, amend, replace, or update these Terms at any time.
          </p>
          <p>
            Updated versions shall become effective upon publication on the Platform.
          </p>
          <p>
            Continued use of the Platform following such updates constitutes acceptance of the revised Terms.
          </p>

          <h3 className="font-semibold text-base text-gray-900">22. Contact Information</h3>
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