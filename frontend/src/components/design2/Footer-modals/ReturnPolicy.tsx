import { useState } from "react";
import { X } from "lucide-react";

interface ReturnPolicyModalProps {
  onClose: () => void;
}

type TabType = "physical" | "digital";

export default function ReturnPolicyModal({ onClose }: ReturnPolicyModalProps) {
  const [activeTab, setActiveTab] = useState<TabType>("physical");

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="bg-white text-gray-900 rounded-lg max-w-3xl w-full max-h-[85vh] overflow-y-auto relative">
        <div className="sticky top-0 bg-white border-b px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold">Return Policy</h2>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full">
            <X size={20} />
          </button>
        </div>

        <div className="sticky top-[65px] bg-white border-b px-6 flex gap-1 z-10">
          <button
            onClick={() => setActiveTab("physical")}
            className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
              activeTab === "physical"
                ? "border-gray-900 text-gray-900"
                : "border-transparent text-gray-500 hover:text-gray-700"
            }`}
          >
            Physical Products
          </button>
          <button
            onClick={() => setActiveTab("digital")}
            className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
              activeTab === "digital"
                ? "border-gray-900 text-gray-900"
                : "border-transparent text-gray-500 hover:text-gray-700"
            }`}
          >
            Digital Products
          </button>
        </div>

        {activeTab === "physical" && (
          <div className="px-6 py-4 space-y-4 text-sm leading-relaxed text-gray-700">
            <p className="text-gray-500">Last Updated: [LAST_UPDATED_DATE]</p>
            <p>Thank you for shopping with [BRAND_NAME].</p>
            <p>
              We strive to ensure customer satisfaction with every purchase. This Return, Refund, Replacement and Exchange Policy explains the conditions under which products purchased through [WEBSITE_URL] (&quot;Platform&quot;) may be returned, replaced, exchanged, cancelled, or refunded.
            </p>
            <p>By placing an order on the Platform, you agree to this Policy.</p>

            <h3 className="font-semibold text-base text-gray-900">1. Applicability</h3>
            <p>
              This Policy applies to purchases made through the Platform unless otherwise specified on the product page, during checkout, or through separate written communication.
            </p>
            <p>
              Certain products, categories, promotional items, customized products, or special-order items may be subject to different return conditions.
            </p>

            <h3 className="font-semibold text-base text-gray-900">2. Return Eligibility</h3>
            <p>Customers may request a return if:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>The product received is damaged.</li>
              <li>The product received is defective.</li>
              <li>The wrong product was delivered.</li>
              <li>The product received is materially different from the product ordered.</li>
              <li>The product qualifies for return under the specific conditions displayed on the product page.</li>
            </ul>
            <p>
              Return requests must be submitted within [RETURN_REQUEST_WINDOW] from the date of delivery.
            </p>
            <p>
              The product must be returned in its original condition together with original packaging, labels, accessories, manuals, warranty cards, complimentary items, and any other items received with the shipment.
            </p>

            <h3 className="font-semibold text-base text-gray-900">3. Products Not Eligible for Return</h3>
            <p>Unless required by applicable law, the following products may not be eligible for return:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Customized or personalized products.</li>
              <li>Made-to-order products.</li>
              <li>Perishable products.</li>
              <li>Consumable products.</li>
              <li>Products damaged due to misuse or improper handling.</li>
              <li>Products showing signs of use beyond reasonable inspection.</li>
              <li>Products without original packaging.</li>
              <li>Products missing accessories or components.</li>
              <li>Hygiene-sensitive products.</li>
              <li>Digital products, downloadable products, or digital activation codes.</li>
              <li>Gift cards, vouchers, or promotional credits.</li>
              <li>Products specifically marked as non-returnable.</li>
            </ul>
            <p>Additional non-returnable categories may be identified on individual product pages.</p>

            <h3 className="font-semibold text-base text-gray-900">4. Return Request Procedure</h3>
            <p>To initiate a return request, customers must contact:</p>
            <p>
              Email: [SUPPORT_EMAIL]<br />
              Phone: [SUPPORT_PHONE]
            </p>
            <p>Customers may be required to provide:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Order number</li>
              <li>Product details</li>
              <li>Description of the issue</li>
              <li>Photographs of the product</li>
              <li>Photographs of the packaging</li>
              <li>Unboxing video, where applicable</li>
              <li>Any other information reasonably required for verification</li>
            </ul>
            <p>Submission of a return request does not automatically guarantee approval.</p>

            <h3 className="font-semibold text-base text-gray-900">5. Return Verification</h3>
            <p>All return requests are subject to verification and approval.</p>
            <p>The Company reserves the right to inspect returned products and determine eligibility based on:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Product condition</li>
              <li>Packaging condition</li>
              <li>Supporting evidence provided</li>
              <li>Internal review findings</li>
              <li>Courier investigation findings</li>
              <li>Applicable policy conditions</li>
            </ul>
            <p>Return requests may be approved, partially approved, or rejected.</p>

            <h3 className="font-semibold text-base text-gray-900">6. Reverse Pickup</h3>
            <p>
              Where reverse pickup services are available, the Company may arrange collection of approved return shipments through authorized logistics partners.
            </p>
            <p>Availability of reverse pickup services depends on serviceability and operational feasibility.</p>
            <p>
              In locations where reverse pickup is unavailable, customers may be required to self-ship products to the address communicated by the Company.
            </p>

            <h3 className="font-semibold text-base text-gray-900">7. Replacement Policy</h3>
            <p>Eligible products may qualify for replacement where:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Products arrive damaged.</li>
              <li>Products arrive defective.</li>
              <li>Incorrect products are delivered.</li>
              <li>Manufacturing defects are identified within the applicable period.</li>
            </ul>
            <p>Replacement requests shall remain subject to stock availability and verification.</p>
            <p>
              Where replacement inventory is unavailable, the Company may offer an exchange, store credit, refund, or another suitable resolution.
            </p>

            <h3 className="font-semibold text-base text-gray-900">8. Exchange Policy</h3>
            <p>
              Where exchanges are offered, customers may exchange eligible products in accordance with the conditions specified on the relevant product pages.
            </p>
            <p>
              Exchange eligibility, exchange windows, available variants, and exchange procedures may vary by product category.
            </p>
            <p>Additional charges may apply where the replacement product has a higher value than the original product.</p>

            <h3 className="font-semibold text-base text-gray-900">9. Refund Policy</h3>
            <p>Approved refunds may be processed under circumstances including:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Approved returns.</li>
              <li>Cancelled orders.</li>
              <li>Unavailable inventory.</li>
              <li>Failed deliveries.</li>
              <li>Duplicate payments.</li>
              <li>Verified payment failures.</li>
              <li>Other circumstances approved by the Company.</li>
            </ul>
            <p>Refunds shall be issued using one or more of the following methods:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Original payment method</li>
              <li>Bank transfer</li>
              <li>Store credit</li>
              <li>Wallet credit</li>
              <li>Promotional credit</li>
            </ul>
            <p>The refund method shall be determined by the Company in accordance with operational and regulatory requirements.</p>

            <h3 className="font-semibold text-base text-gray-900">10. Refund Processing Time</h3>
            <p>
              Approved refunds are generally initiated within [REFUND_PROCESSING_PERIOD] after approval.
            </p>
            <p>Actual credit timelines may depend on:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Payment gateway processing</li>
              <li>Banking systems</li>
              <li>Financial institutions</li>
              <li>Card networks</li>
              <li>UPI providers</li>
              <li>Regulatory requirements</li>
            </ul>
            <p>The Company shall not be responsible for delays caused by external payment systems.</p>

            <h3 className="font-semibold text-base text-gray-900">11. Damaged, Defective or Incorrect Products</h3>
            <p>
              Customers must report damaged, defective, missing, tampered, or incorrect products within [DAMAGE_REPORTING_PERIOD] after delivery.
            </p>
            <p>
              Customers may be required to provide supporting evidence, including photographs, videos, packaging details, courier labels, and other information reasonably requested during the investigation process.
            </p>
            <p>
              Failure to report within the prescribed period may affect eligibility for replacement, return, exchange, or refund.
            </p>

            <h3 className="font-semibold text-base text-gray-900">12. Order Cancellation</h3>
            <p>Order cancellation requests may be accepted before shipment confirmation.</p>
            <p>
              Once an order has been shipped, cancellation may not be possible unless otherwise required by law or expressly approved by the Company.
            </p>
            <p>Refunds for approved cancellations shall be processed in accordance with this Policy.</p>

            <h3 className="font-semibold text-base text-gray-900">13. Refused Deliveries</h3>
            <p>If a customer refuses delivery without a valid reason, the Company reserves the right to:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Deduct shipping charges;</li>
              <li>Deduct reverse logistics charges;</li>
              <li>Deduct handling fees; or</li>
              <li>Reject refund requests where permitted by law.</li>
            </ul>

            <h3 className="font-semibold text-base text-gray-900">14. Fraud Prevention</h3>
            <p>
              The Company reserves the right to deny returns, refunds, replacements, exchanges, or cancellations where it reasonably suspects:
            </p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Fraudulent activity;</li>
              <li>Abuse of policies;</li>
              <li>False claims;</li>
              <li>Repeated misuse of return privileges;</li>
              <li>Product tampering;</li>
              <li>Abuse of promotional programs.</li>
            </ul>

            <h3 className="font-semibold text-base text-gray-900">15. Limitation of Liability</h3>
            <p>
              To the maximum extent permitted by law, the Company&apos;s liability relating to any return, refund, replacement, exchange, or cancellation shall not exceed the purchase price paid for the affected product.
            </p>

            <h3 className="font-semibold text-base text-gray-900">16. Changes to this Policy</h3>
            <p>The Company reserves the right to modify, update, amend, or replace this Policy at any time.</p>
            <p>Updated versions shall become effective upon publication on the Platform.</p>
            <p>Customers are encouraged to review this Policy periodically.</p>

            <h3 className="font-semibold text-base text-gray-900">17. Contact Information</h3>
            <p>For return, refund, replacement, exchange, or cancellation enquiries, please contact:</p>
            <p>
              [BUSINESS_NAME]<br />
              Email: [SUPPORT_EMAIL]<br />
              Phone: [SUPPORT_PHONE]<br />
              Website: [WEBSITE_URL]<br />
              Address: [REGISTERED_ADDRESS]
            </p>
          </div>
        )}

        {activeTab === "digital" && (
          <div className="px-6 py-4 space-y-4 text-sm leading-relaxed text-gray-700">
            <p className="text-gray-500">Last Updated: [LAST_UPDATED_DATE]</p>
            <p>Thank you for purchasing digital products from [BRAND_NAME] through [WEBSITE_URL] (&quot;Platform&quot;).</p>
            <p>
              This Refund and Cancellation Policy governs the purchase, delivery, cancellation, replacement, access, and refund eligibility of all digital products sold through the Platform.
            </p>
            <p>By purchasing any digital product, you acknowledge and agree to this Policy.</p>

            <h3 className="font-semibold text-base text-gray-900">1. Nature of Digital Products</h3>
            <p>
              The products offered through the Platform may include digital downloads, software, source code, templates, digital documents, design assets, educational content, memberships, subscriptions, licenses, digital tools, digital services, or other electronically delivered products.
            </p>
            <p>
              As digital products are delivered electronically and cannot generally be physically returned, different refund conditions apply compared to physical products.
            </p>

            <h3 className="font-semibold text-base text-gray-900">2. No Return Policy</h3>
            <p>
              Digital products cannot be returned once access has been granted, a download link has been issued, content has been accessed, a license key has been delivered, or the product has otherwise been made available to the customer.
            </p>
            <p>Accordingly, return requests are generally not accepted.</p>

            <h3 className="font-semibold text-base text-gray-900">3. Cancellation Policy</h3>
            <p>
              Orders may be cancelled only before digital delivery, account activation, license generation, content access, subscription activation, or download availability.
            </p>
            <p>Once delivery or access has occurred, cancellation requests may not be accepted.</p>

            <h3 className="font-semibold text-base text-gray-900">4. Non-Refundable Situations</h3>
            <p>Unless otherwise required by applicable law, refunds shall generally not be issued in the following circumstances:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Change of mind.</li>
              <li>Accidental purchase.</li>
              <li>Failure to read product descriptions.</li>
              <li>Lack of technical knowledge.</li>
              <li>Incompatibility with systems not listed as supported.</li>
              <li>Failure to meet customer expectations where the product matches its description.</li>
              <li>Partial use of digital content.</li>
              <li>Failure to use purchased access.</li>
              <li>Subscription non-usage.</li>
              <li>Customer device issues.</li>
              <li>Customer internet connectivity issues.</li>
              <li>Customer software configuration issues.</li>
              <li>Customer failure to download products within the allowed period.</li>
              <li>Customer violation of licensing terms.</li>
            </ul>

            <h3 className="font-semibold text-base text-gray-900">5. Eligible Refund Situations</h3>
            <p>Refund requests may be considered under circumstances including:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Duplicate payments.</li>
              <li>Verified payment processing errors.</li>
              <li>Failure of product delivery due to technical issues attributable to the Company.</li>
              <li>Product materially different from its published description.</li>
              <li>Corrupted files that cannot reasonably be repaired or replaced.</li>
              <li>License activation failures that cannot reasonably be resolved.</li>
              <li>Subscription access failures caused solely by the Company.</li>
              <li>Other circumstances approved by the Company at its sole discretion.</li>
            </ul>
            <p>Refund approval remains subject to verification and investigation.</p>

            <h3 className="font-semibold text-base text-gray-900">6. Technical Support and Resolution First</h3>
            <p>
              Before a refund request is approved, customers may be required to cooperate in reasonable troubleshooting procedures.
            </p>
            <p>Such procedures may include:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Installation assistance</li>
              <li>Configuration support</li>
              <li>Account verification</li>
              <li>Technical diagnostics</li>
              <li>Error verification</li>
              <li>License validation</li>
              <li>Access verification</li>
            </ul>
            <p>
              Where a technical issue can reasonably be resolved, the Company may offer correction, replacement, updated files, renewed access, account restoration, or technical assistance instead of a refund.
            </p>

            <h3 className="font-semibold text-base text-gray-900">7. Digital Product Delivery</h3>
            <p>Digital products may be delivered through one or more of the following methods:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Download links</li>
              <li>Customer dashboards</li>
              <li>Email delivery</li>
              <li>Membership portals</li>
              <li>Learning management systems</li>
              <li>SaaS platforms</li>
              <li>API access</li>
              <li>Cloud storage systems</li>
              <li>License key generation systems</li>
            </ul>
            <p>
              Successful generation of access credentials, delivery of download links, activation of subscriptions, or creation of customer access records may be treated as proof of delivery.
            </p>

            <h3 className="font-semibold text-base text-gray-900">8. License Keys and Activation Codes</h3>
            <p>
              Where digital products include software licenses, activation keys, API credentials, or similar access mechanisms, such credentials are considered delivered immediately upon issuance.
            </p>
            <p>Once issued, refunds may not be available except where activation defects cannot reasonably be resolved.</p>

            <h3 className="font-semibold text-base text-gray-900">9. Subscription Products</h3>
            <p>Subscription-based products may automatically renew if the customer has agreed to recurring billing.</p>
            <p>Customers are responsible for cancelling subscriptions before the next billing cycle if they do not wish to continue.</p>
            <p>
              Fees already charged for active billing periods are generally non-refundable unless required by law or expressly stated otherwise.
            </p>

            <h3 className="font-semibold text-base text-gray-900">10. Educational Content and Online Courses</h3>
            <p>
              Where the Platform provides educational content, recorded training, workshops, learning programs, certifications, coaching material, or online courses, refunds may be restricted once content access has been granted.
            </p>
            <p>
              Progress tracking, content access logs, login records, downloads, video views, or course activity may be used to determine eligibility.
            </p>

            <h3 className="font-semibold text-base text-gray-900">11. Source Code, Templates and Digital Assets</h3>
            <p>
              Products including source code, website templates, mobile application templates, software components, plugins, design files, graphics, databases, documentation, and other intellectual property are generally non-refundable after delivery.
            </p>
            <p>Exceptions may apply where files are materially defective and cannot reasonably be corrected.</p>

            <h3 className="font-semibold text-base text-gray-900">12. Refund Request Procedure</h3>
            <p>Customers seeking a refund must contact:</p>
            <p>
              Email: [SUPPORT_EMAIL]<br />
              Phone: [SUPPORT_PHONE]
            </p>
            <p>The request should include:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Order number</li>
              <li>Registered email address</li>
              <li>Product name</li>
              <li>Description of the issue</li>
              <li>Supporting screenshots</li>
              <li>Error messages where applicable</li>
              <li>Any other information reasonably requested</li>
            </ul>
            <p>Submission of a request does not guarantee approval.</p>

            <h3 className="font-semibold text-base text-gray-900">13. Refund Processing</h3>
            <p>
              Approved refunds are generally initiated within [REFUND_PROCESSING_PERIOD] after approval.
            </p>
            <p>Actual credit timelines may depend on:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Payment gateways</li>
              <li>Banking systems</li>
              <li>UPI networks</li>
              <li>Card issuers</li>
              <li>Financial institutions</li>
            </ul>
            <p>The Company shall not be responsible for delays caused by external financial systems.</p>

            <h3 className="font-semibold text-base text-gray-900">14. Fraud Prevention</h3>
            <p>The Company reserves the right to deny refunds where it reasonably suspects:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Unauthorized transactions</li>
              <li>Payment disputes made in bad faith</li>
              <li>Abuse of refund policies</li>
              <li>Multiple refund requests</li>
              <li>Product misuse</li>
              <li>Intellectual property theft</li>
              <li>Unauthorized distribution</li>
              <li>Violation of licensing terms</li>
            </ul>

            <h3 className="font-semibold text-base text-gray-900">15. Chargebacks</h3>
            <p>Customers are encouraged to contact the Company before initiating chargebacks or payment disputes.</p>
            <p>
              The Company reserves the right to provide transaction records, access logs, download records, activation logs, communication history, and related evidence in response to chargeback investigations.
            </p>

            <h3 className="font-semibold text-base text-gray-900">16. Limitation of Liability</h3>
            <p>
              To the maximum extent permitted by law, the Company&apos;s liability relating to digital products shall not exceed the amount actually paid by the customer for the affected product.
            </p>

            <h3 className="font-semibold text-base text-gray-900">17. Changes to this Policy</h3>
            <p>The Company reserves the right to modify, amend, replace, or update this Policy at any time.</p>
            <p>Updated versions shall become effective upon publication on the Platform.</p>

            <h3 className="font-semibold text-base text-gray-900">18. Contact Information</h3>
            <p>
              [BUSINESS_NAME]<br />
              Email: [SUPPORT_EMAIL]<br />
              Phone: [SUPPORT_PHONE]<br />
              Website: [WEBSITE_URL]<br />
              Address: [REGISTERED_ADDRESS]
            </p>
          </div>
        )}

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