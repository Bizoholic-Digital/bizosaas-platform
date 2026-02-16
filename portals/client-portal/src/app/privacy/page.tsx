import { Metadata } from 'next'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'

export const metadata: Metadata = {
  title: 'Privacy Policy | Bizoholic',
  description: 'Learn how Bizoholic collects, uses, and protects your personal information.',
}

export default function PrivacyPage() {
  return (
    <>
      <Navigation />
      <main className="min-h-screen bg-white">
        <div className="container py-24">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-4xl font-bold text-gray-900 mb-8">Privacy Policy</h1>
            <p className="text-gray-600 mb-8">Last updated: {new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}</p>

            <div className="prose prose-lg max-w-none">
              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">1. Introduction</h2>
                <p className="text-gray-700 mb-4">
                  Bizoholic (&quot;we,&quot; &quot;our,&quot; or &quot;us&quot;) is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our website or use our services.
                </p>
                <p className="text-gray-700">
                  Please read this privacy policy carefully. If you do not agree with the terms of this privacy policy, please do not access the site or use our services.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">2. Information We Collect</h2>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">2.1 Personal Information</h3>
                <p className="text-gray-700 mb-4">
                  We may collect personal information that you voluntarily provide to us when you:
                </p>
                <ul className="list-disc list-inside text-gray-700 mb-4 space-y-2">
                  <li>Register for an account</li>
                  <li>Submit a contact form</li>
                  <li>Subscribe to our newsletter</li>
                  <li>Request a quote or consultation</li>
                  <li>Participate in surveys or promotions</li>
                </ul>
                <p className="text-gray-700 mb-4">
                  This information may include: name, email address, phone number, company name, job title, billing address, and payment information.
                </p>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">2.2 Automatically Collected Information</h3>
                <p className="text-gray-700 mb-4">
                  When you visit our website, we automatically collect certain information about your device and usage patterns, including:
                </p>
                <ul className="list-disc list-inside text-gray-700 mb-4 space-y-2">
                  <li>IP address and location data</li>
                  <li>Browser type and version</li>
                  <li>Operating system</li>
                  <li>Referring website</li>
                  <li>Pages viewed and time spent on pages</li>
                  <li>Click-through patterns and browsing behavior</li>
                </ul>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">3. How We Use Your Information</h2>
                <p className="text-gray-700 mb-4">
                  We use the information we collect for the following purposes:
                </p>
                <ul className="list-disc list-inside text-gray-700 mb-4 space-y-2">
                  <li>To provide, maintain, and improve our services</li>
                  <li>To process your transactions and manage your account</li>
                  <li>To communicate with you about services, updates, and promotional offers</li>
                  <li>To respond to your inquiries and provide customer support</li>
                  <li>To analyze usage patterns and optimize user experience</li>
                  <li>To detect, prevent, and address technical issues or fraudulent activity</li>
                  <li>To comply with legal obligations and enforce our terms of service</li>
                </ul>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">4. Sharing Your Information</h2>
                <p className="text-gray-700 mb-4">
                  We may share your information in the following circumstances:
                </p>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">4.1 Service Providers</h3>
                <p className="text-gray-700 mb-4">
                  We may share your information with third-party service providers who perform services on our behalf, such as payment processing, data analysis, email delivery, hosting services, and customer service.
                </p>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">4.2 Business Transfers</h3>
                <p className="text-gray-700 mb-4">
                  If we are involved in a merger, acquisition, or sale of assets, your information may be transferred as part of that transaction.
                </p>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">4.3 Legal Requirements</h3>
                <p className="text-gray-700 mb-4">
                  We may disclose your information if required to do so by law or in response to valid requests by public authorities.
                </p>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">4.4 With Your Consent</h3>
                <p className="text-gray-700 mb-4">
                  We may share your information for any other purpose with your explicit consent.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">5. Cookies and Tracking Technologies</h2>
                <p className="text-gray-700 mb-4">
                  We use cookies and similar tracking technologies to track activity on our website and store certain information. You can instruct your browser to refuse all cookies or to indicate when a cookie is being sent. However, if you do not accept cookies, you may not be able to use some portions of our website.
                </p>
                <p className="text-gray-700 mb-4">
                  For more information about our use of cookies, please see our <a href="/cookies" className="text-primary-600 hover:underline">Cookie Policy</a>.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">6. Data Security</h2>
                <p className="text-gray-700 mb-4">
                  We implement appropriate technical and organizational security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction. These measures include:
                </p>
                <ul className="list-disc list-inside text-gray-700 mb-4 space-y-2">
                  <li>Encryption of data in transit and at rest</li>
                  <li>Regular security assessments and vulnerability testing</li>
                  <li>Access controls and authentication mechanisms</li>
                  <li>Employee training on data protection practices</li>
                  <li>Incident response procedures</li>
                </ul>
                <p className="text-gray-700">
                  However, no method of transmission over the Internet or electronic storage is 100% secure, and we cannot guarantee absolute security.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">7. Your Privacy Rights</h2>
                <p className="text-gray-700 mb-4">
                  Depending on your location, you may have certain rights regarding your personal information:
                </p>
                <ul className="list-disc list-inside text-gray-700 mb-4 space-y-2">
                  <li><strong>Access:</strong> Request access to your personal information</li>
                  <li><strong>Correction:</strong> Request correction of inaccurate information</li>
                  <li><strong>Deletion:</strong> Request deletion of your personal information</li>
                  <li><strong>Portability:</strong> Request a copy of your data in a structured format</li>
                  <li><strong>Objection:</strong> Object to processing of your personal information</li>
                  <li><strong>Restriction:</strong> Request restriction of processing</li>
                  <li><strong>Withdrawal:</strong> Withdraw consent at any time</li>
                </ul>
                <p className="text-gray-700">
                  To exercise these rights, please contact us at privacy@bizoholic.com.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">8. Data Retention</h2>
                <p className="text-gray-700 mb-4">
                  We retain your personal information only for as long as necessary to fulfill the purposes outlined in this Privacy Policy, unless a longer retention period is required or permitted by law. When we no longer need your information, we will securely delete or anonymize it.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">9. Third-Party Links</h2>
                <p className="text-gray-700 mb-4">
                  Our website may contain links to third-party websites. We are not responsible for the privacy practices of these websites. We encourage you to review the privacy policies of any third-party sites you visit.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">10. Children&apos;s Privacy</h2>
                <p className="text-gray-700 mb-4">
                  Our services are not intended for children under the age of 16. We do not knowingly collect personal information from children under 16. If you become aware that a child has provided us with personal information, please contact us immediately.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">11. International Data Transfers</h2>
                <p className="text-gray-700 mb-4">
                  Your information may be transferred to and maintained on computers located outside of your state, province, country, or other governmental jurisdiction where data protection laws may differ. We will take appropriate measures to ensure your information receives adequate protection.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">12. Changes to This Privacy Policy</h2>
                <p className="text-gray-700 mb-4">
                  We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and updating the &quot;Last updated&quot; date. You are advised to review this Privacy Policy periodically for any changes.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">13. Contact Us</h2>
                <p className="text-gray-700 mb-4">
                  If you have any questions about this Privacy Policy or our data practices, please contact us:
                </p>
                <div className="bg-gray-50 p-6 rounded-lg">
                  <p className="text-gray-700 mb-2"><strong>Email:</strong> privacy@bizoholic.com</p>
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
