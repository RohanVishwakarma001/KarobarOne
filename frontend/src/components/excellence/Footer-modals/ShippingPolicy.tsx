import { X } from "lucide-react";

interface ShippingPolicyModalProps {
  onClose: () => void;
}

export default function ShippingPolicyModal({ onClose }: ShippingPolicyModalProps) {
  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="bg-white text-gray-900 rounded-lg max-w-3xl w-full max-h-[85vh] overflow-y-auto relative">
        <div className="sticky top-0 bg-white border-b px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold">Shipping Policy</h2>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full">
            <X size={20} />
          </button>
        </div>

        <div className="px-6 py-4 space-y-4 text-sm leading-relaxed text-gray-700">
          <p className="text-gray-500">Last Updated: [LAST_UPDATED_DATE]</p>
          <p>Thank you for shopping with [BRAND_NAME].</p>
          <p>
            This Shipping Policy explains how orders are processed, shipped, delivered, tracked, and managed when you purchase products through [WEBSITE_URL] (&quot;Platform&quot;).
          </p>
          <p>By placing an order on the Platform, you agree to the terms outlined in this Shipping Policy.</p>

          <h3 className="font-semibold text-base text-gray-900">1. Order Processing</h3>
          <p>
            Orders are generally processed after successful payment confirmation and completion of applicable verification checks.
          </p>
          <p>
            Order processing typically takes [ORDER_PROCESSING_TIME] unless otherwise specified on the product page.
          </p>
          <p>
            Orders placed on weekends, public holidays, or non-business days may be processed on the next working day.
          </p>
          <p>
            In certain circumstances, processing may take longer due to high order volumes, inventory verification, product customization requirements, operational constraints, or events beyond our reasonable control.
          </p>

          <h3 className="font-semibold text-base text-gray-900">2. Shipping Coverage</h3>
          <p>
            We currently ship products to locations within [SHIPPING_COVERAGE_AREA].
          </p>
          <p>
            Certain products may not be available for delivery to all locations due to logistics restrictions, regulatory limitations, serviceability constraints, or operational considerations.
          </p>
          <p>
            We reserve the right to refuse shipment to locations that are not serviceable through our logistics network.
          </p>

          <h3 className="font-semibold text-base text-gray-900">3. Shipping Partners</h3>
          <p>Orders may be delivered through one or more authorized logistics and shipping partners including:</p>
          <p>[SHIPPING_PARTNER_NAME]</p>
          <p>
            The selection of shipping partners is determined by factors such as delivery location, serviceability, package dimensions, delivery timelines, and operational requirements.
          </p>
          <p>We reserve the right to change shipping partners without prior notice.</p>

          <h3 className="font-semibold text-base text-gray-900">4. Shipping Charges</h3>
          <p>
            Shipping charges, if applicable, shall be displayed during checkout before order confirmation.
          </p>
          <p>Shipping fees may vary based on:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>Delivery location</li>
            <li>Product category</li>
            <li>Weight or dimensions</li>
            <li>Order value</li>
            <li>Delivery method</li>
            <li>Promotional offers</li>
          </ul>
          <p>Any applicable shipping charges shall be payable by the customer unless otherwise specified.</p>
          <p>Free shipping promotions, where offered, shall remain subject to eligibility criteria and promotional terms.</p>

          <h3 className="font-semibold text-base text-gray-900">5. Estimated Delivery Timelines</h3>
          <p>Estimated delivery timelines are provided for informational purposes only.</p>
          <p>
            Typical delivery timelines may range from [ESTIMATED_DELIVERY_TIME] depending on the destination, product availability, courier operations, and external factors.
          </p>
          <p>Actual delivery dates may vary and are not guaranteed unless expressly stated otherwise.</p>

          <h3 className="font-semibold text-base text-gray-900">6. Order Tracking</h3>
          <p>
            Where available, shipment tracking details will be provided through email, SMS, WhatsApp, customer account dashboards, or other communication channels.
          </p>
          <p>
            Tracking information becomes available after the shipment has been handed over to the logistics provider and updated in the courier system.
          </p>
          <p>Customers are encouraged to monitor shipment progress using the provided tracking information.</p>

          <h3 className="font-semibold text-base text-gray-900">7. Delivery Attempts</h3>
          <p>
            Delivery partners may attempt delivery multiple times in accordance with their operational policies.
          </p>
          <p>
            If delivery cannot be completed due to incorrect addresses, recipient unavailability, refusal to accept delivery, inability to contact the recipient, or other customer-related issues, the shipment may be returned to us.
          </p>
          <p>Additional shipping or re-delivery charges may apply where applicable.</p>

          <h3 className="font-semibold text-base text-gray-900">8. Customer Responsibilities</h3>
          <p>
            Customers are responsible for providing complete and accurate delivery information, including recipient name, address, contact number, postal code, landmark details, and other necessary delivery information.
          </p>
          <p>
            We shall not be responsible for delays, failed deliveries, losses, or additional charges resulting from inaccurate, incomplete, or incorrect shipping information provided by the customer.
          </p>

          <h3 className="font-semibold text-base text-gray-900">9. Delayed Deliveries</h3>
          <p>
            While we make reasonable efforts to ensure timely delivery, delays may occur due to factors beyond our control, including:
          </p>
          <p>
            Weather conditions, natural disasters, transportation disruptions, public holidays, government restrictions, customs inspections, strikes, civil disturbances, pandemics, courier operational issues, remote delivery locations, or force majeure events.
          </p>
          <p>The Company shall not be liable for delivery delays arising from such circumstances.</p>

          <h3 className="font-semibold text-base text-gray-900">10. Damaged Packages</h3>
          <p>Customers are advised to inspect packages at the time of delivery.</p>
          <p>If a package appears visibly damaged, tampered with, opened, or otherwise compromised, customers should:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>Refuse delivery where appropriate; or</li>
            <li>
              Immediately notify us at [SUPPORT_EMAIL] within [DAMAGE_REPORTING_PERIOD] of receiving the shipment.
            </li>
          </ul>
          <p>Claims submitted after the specified reporting period may not be eligible for review.</p>

          <h3 className="font-semibold text-base text-gray-900">11. Lost Shipments</h3>
          <p>
            If a shipment is reported lost by the logistics provider or fails to reach the customer within a reasonable timeframe, we will investigate the matter with the shipping partner.
          </p>
          <p>
            Resolution may include replacement, re-shipment, refund, store credit, or another appropriate remedy in accordance with our applicable policies and the findings of the investigation.
          </p>

          <h3 className="font-semibold text-base text-gray-900">12. Split Shipments</h3>
          <p>
            Where an order contains multiple products, we reserve the right to ship products separately based on inventory availability, warehouse locations, packaging requirements, or operational considerations.
          </p>
          <p>Customers may therefore receive multiple shipments for a single order.</p>

          <h3 className="font-semibold text-base text-gray-900">13. Delivery Acceptance</h3>
          <p>
            Upon successful delivery to the address provided during checkout, responsibility for the shipment shall transfer to the customer.
          </p>
          <p>Proof of delivery maintained by the shipping partner may be used to establish successful delivery.</p>

          <h3 className="font-semibold text-base text-gray-900">14. International Shipping</h3>
          <p>[INTERNATIONAL_SHIPPING_CLAUSE]</p>

          <h3 className="font-semibold text-base text-gray-900">15. Force Majeure</h3>
          <p>
            The Company shall not be responsible for shipping delays, interruptions, failures, or losses caused by events beyond reasonable control, including natural disasters, government actions, transportation disruptions, labor disputes, pandemics, cyber incidents, or similar events.
          </p>

          <h3 className="font-semibold text-base text-gray-900">16. Changes to this Shipping Policy</h3>
          <p>We reserve the right to modify, amend, update, or replace this Shipping Policy at any time.</p>
          <p>Updated versions shall become effective upon publication on the Platform.</p>
          <p>Customers are encouraged to review this Shipping Policy periodically.</p>

          <h3 className="font-semibold text-base text-gray-900">17. Contact Information</h3>
          <p>For shipping-related enquiries, customers may contact:</p>
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