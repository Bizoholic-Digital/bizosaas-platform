import { Metadata } from 'next'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'

export const metadata: Metadata = {
  title: 'Terms of Service | Bizoholic',
  description: 'Read the terms and conditions for using Bizoholic services.',
}

export default function TermsPage() {
  return (
    <>
      <Navigation />
      <main className="min-h-screen bg-white">
        <div className="container py-24">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-4xl font-bold text-gray-900 mb-8">Terms of Service</h1>
            <p className="text-gray-600 mb-8">Last updated: {new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}</p>

            <div className="prose prose-lg max-w-none">
              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">1. Agreement to Terms</h2>
                <p className="text-gray-700 mb-4">
                  By accessing or using Bizoholic&apos;s website and services (&quot;Services&quot;), you agree to be bound by these Terms of Service (&quot;Terms&quot;). If you disagree with any part of these terms, you may not access our Services.
                </p>
                <p className="text-gray-700">
                  These Terms apply to all visitors, users, and others who access or use the Services.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">2. Use of Services</h2>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">2.1 Eligibility</h3>
                <p className="text-gray-700 mb-4">
                  You must be at least 18 years old and capable of forming a binding contract to use our Services. By using our Services, you represent and warrant that you meet these requirements.
                </p>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">2.2 Account Registration</h3>
                <p className="text-gray-700 mb-4">
                  To access certain features of our Services, you may be required to register for an account. You agree to:
                </p>
                <ul className="list-disc list-inside text-gray-700 mb-4 space-y-2">
                  <li>Provide accurate, current, and complete information</li>
                  <li>Maintain and promptly update your account information</li>
                  <li>Maintain the security of your password and account</li>
                  <li>Accept all responsibility for activities under your account</li>
                  <li>Notify us immediately of any unauthorized use</li>
                </ul>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">2.3 Acceptable Use</h3>
                <p className="text-gray-700 mb-4">
                  You agree not to:
                </p>
                <ul className="list-disc list-inside text-gray-700 mb-4 space-y-2">
                  <li>Use the Services for any illegal purpose or in violation of any laws</li>
                  <li>Violate or infringe upon the rights of others</li>
                  <li>Transmit any viruses, malware, or harmful code</li>
                  <li>Attempt to gain unauthorized access to any part of the Services</li>
                  <li>Interfere with or disrupt the Services or servers</li>
                  <li>Engage in any automated use of the system without our permission</li>
                  <li>Impersonate any person or entity</li>
                  <li>Harass, abuse, or harm another person</li>
                </ul>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">3. Services and Deliverables</h2>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">3.1 Service Description</h3>
                <p className="text-gray-700 mb-4">
                  Bizoholic provides AI-powered digital marketing services including but not limited to:
                </p>
                <ul className="list-disc list-inside text-gray-700 mb-4 space-y-2">
                  <li>Search Engine Optimization (SEO)</li>
                  <li>Pay-Per-Click (PPC) Advertising Management</li>
                  <li>Social Media Marketing</li>
                  <li>Content Marketing and Copywriting</li>
                  <li>Email Marketing Automation</li>
                  <li>Web Design and Development</li>
                  <li>Conversion Rate Optimization</li>
                  <li>Marketing Analytics and Reporting</li>
                </ul>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">3.2 Service Modifications</h3>
                <p className="text-gray-700 mb-4">
                  We reserve the right to modify, suspend, or discontinue any part of our Services at any time with or without notice. We will not be liable to you or any third party for any modification, suspension, or discontinuation of the Services.
                </p>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">3.3 Performance Standards</h3>
                <p className="text-gray-700 mb-4">
                  While we strive to provide excellent results, we cannot guarantee specific outcomes such as search engine rankings, traffic levels, or conversion rates. Marketing results depend on many factors beyond our control.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">4. Payment and Billing</h2>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">4.1 Fees</h3>
                <p className="text-gray-700 mb-4">
                  You agree to pay all fees associated with your chosen service plan. All fees are in U.S. dollars unless otherwise stated. Fees are subject to change with 30 days&apos; notice.
                </p>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">4.2 Payment Terms</h3>
                <p className="text-gray-700 mb-4">
                  Payment is due according to the terms specified in your service agreement. Late payments may result in suspension or termination of services and may incur late fees.
                </p>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">4.3 Refund Policy</h3>
                <p className="text-gray-700 mb-4">
                  Refunds are provided on a case-by-case basis at our sole discretion. Setup fees and completed work are generally non-refundable. Monthly subscriptions may be canceled with appropriate notice as specified in your service agreement.
                </p>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">4.4 Auto-Renewal</h3>
                <p className="text-gray-700 mb-4">
                  Subscription services automatically renew at the end of each billing period unless you cancel before the renewal date. You authorize us to charge your payment method for renewal fees.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">5. Intellectual Property</h2>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">5.1 Our Intellectual Property</h3>
                <p className="text-gray-700 mb-4">
                  The Services and all content, features, and functionality are owned by Bizoholic and are protected by copyright, trademark, and other intellectual property laws. You may not reproduce, distribute, modify, or create derivative works without our express written permission.
                </p>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">5.2 Your Content</h3>
                <p className="text-gray-700 mb-4">
                  You retain ownership of content you provide to us. By providing content, you grant us a worldwide, non-exclusive, royalty-free license to use, reproduce, modify, and distribute your content solely for the purpose of providing our Services.
                </p>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">5.3 Work Product</h3>
                <p className="text-gray-700 mb-4">
                  Upon full payment, you will own the rights to deliverables created specifically for you, subject to our retention of underlying methodologies, processes, and pre-existing materials.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">6. Confidentiality</h2>
                <p className="text-gray-700 mb-4">
                  Both parties agree to maintain the confidentiality of any proprietary or confidential information disclosed during the course of our relationship. This obligation continues for three (3) years after termination of services.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">7. Warranties and Disclaimers</h2>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">7.1 Our Warranties</h3>
                <p className="text-gray-700 mb-4">
                  We warrant that we will perform our Services in a professional and workmanlike manner consistent with industry standards.
                </p>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">7.2 Disclaimers</h3>
                <p className="text-gray-700 mb-4 uppercase">
                  THE SERVICES ARE PROVIDED &quot;AS IS&quot; AND &quot;AS AVAILABLE&quot; WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT. WE DO NOT WARRANT THAT THE SERVICES WILL BE UNINTERRUPTED, TIMELY, SECURE, OR ERROR-FREE.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">8. Limitation of Liability</h2>
                <p className="text-gray-700 mb-4 uppercase">
                  TO THE MAXIMUM EXTENT PERMITTED BY LAW, BIZOHOLIC SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, OR ANY LOSS OF PROFITS OR REVENUES, WHETHER INCURRED DIRECTLY OR INDIRECTLY, OR ANY LOSS OF DATA, USE, GOODWILL, OR OTHER INTANGIBLE LOSSES.
                </p>
                <p className="text-gray-700 mb-4">
                  Our total liability shall not exceed the amount you paid us in the twelve (12) months preceding the event giving rise to liability.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">9. Indemnification</h2>
                <p className="text-gray-700 mb-4">
                  You agree to indemnify, defend, and hold harmless Bizoholic from any claims, damages, losses, liabilities, and expenses (including attorney fees) arising out of your use of the Services, your violation of these Terms, or your violation of any rights of another party.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">10. Termination</h2>
                <p className="text-gray-700 mb-4">
                  Either party may terminate services with written notice as specified in your service agreement. We may terminate or suspend your account immediately, without prior notice, for cause including breach of these Terms.
                </p>
                <p className="text-gray-700 mb-4">
                  Upon termination, your right to use the Services will immediately cease. Provisions that by their nature should survive termination shall survive, including intellectual property rights, warranty disclaimers, and limitations of liability.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">11. Dispute Resolution</h2>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">11.1 Informal Resolution</h3>
                <p className="text-gray-700 mb-4">
                  Before filing a claim, you agree to contact us to attempt to resolve the dispute informally by sending written notice to legal@bizoholic.com.
                </p>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">11.2 Arbitration</h3>
                <p className="text-gray-700 mb-4">
                  Any dispute arising out of or relating to these Terms or the Services shall be resolved through binding arbitration in accordance with the rules of the American Arbitration Association.
                </p>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">11.3 Class Action Waiver</h3>
                <p className="text-gray-700 mb-4">
                  You agree that any arbitration or legal proceeding shall be conducted on an individual basis and not in a class, consolidated, or representative action.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">12. Governing Law</h2>
                <p className="text-gray-700 mb-4">
                  These Terms shall be governed by and construed in accordance with the laws of the State of California, United States, without regard to its conflict of law provisions.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">13. Changes to Terms</h2>
                <p className="text-gray-700 mb-4">
                  We reserve the right to modify these Terms at any time. We will notify you of any material changes by posting the new Terms on this page and updating the &quot;Last updated&quot; date. Your continued use of the Services after any changes constitutes acceptance of the new Terms.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">14. Severability</h2>
                <p className="text-gray-700 mb-4">
                  If any provision of these Terms is found to be unenforceable or invalid, that provision shall be limited or eliminated to the minimum extent necessary, and the remaining provisions shall remain in full force and effect.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">15. Entire Agreement</h2>
                <p className="text-gray-700 mb-4">
                  These Terms, together with any service agreements you have entered into with us, constitute the entire agreement between you and Bizoholic regarding the Services and supersede all prior agreements.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">16. Contact Information</h2>
                <p className="text-gray-700 mb-4">
                  For questions about these Terms, please contact us:
                </p>
                <div className="bg-gray-50 p-6 rounded-lg">
                  <p className="text-gray-700 mb-2"><strong>Email:</strong> legal@bizoholic.com</p>
                  <p className="text-gray-700 mb-2"><strong>Phone:</strong> +1 (555) 123-4567</p>
                  <p className="text-gray-700 mb-2"><strong>Address:</strong> Bizoholic Digital Marketing</p>
                  <p className="text-gray-700 ml-16">San Francisco, CA</p>
                  <p className="text-gray-700 ml-16">United States</p>
                </div>
              </section>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
