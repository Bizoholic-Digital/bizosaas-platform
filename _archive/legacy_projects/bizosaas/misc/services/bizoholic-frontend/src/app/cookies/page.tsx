import { Metadata } from 'next'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'

export const metadata: Metadata = {
  title: 'Cookie Policy | Bizoholic',
  description: 'Learn about how Bizoholic uses cookies and similar tracking technologies.',
}

export default function CookiesPage() {
  return (
    <>
      <Navigation />
      <main className="min-h-screen bg-white">
        <div className="container py-24">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-4xl font-bold text-gray-900 mb-8">Cookie Policy</h1>
            <p className="text-gray-600 mb-8">Last updated: {new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}</p>

            <div className="prose prose-lg max-w-none">
              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">1. What Are Cookies</h2>
                <p className="text-gray-700 mb-4">
                  Cookies are small text files that are placed on your computer or mobile device when you visit a website. They are widely used to make websites work more efficiently and provide information to website owners.
                </p>
                <p className="text-gray-700">
                  Cookies set by the website owner (in this case, Bizoholic) are called &quot;first-party cookies.&quot; Cookies set by parties other than the website owner are called &quot;third-party cookies.&quot;
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">2. How We Use Cookies</h2>
                <p className="text-gray-700 mb-4">
                  Bizoholic uses cookies to enhance your experience on our website, understand how you use our services, and improve our offerings. We use both first-party and third-party cookies for several purposes.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">3. Types of Cookies We Use</h2>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">3.1 Essential Cookies</h3>
                <p className="text-gray-700 mb-4">
                  These cookies are necessary for the website to function properly. They enable core functionality such as security, network management, and accessibility. You cannot opt out of essential cookies.
                </p>
                <div className="bg-gray-50 p-4 rounded-lg mb-4">
                  <p className="text-gray-700 mb-2"><strong>Examples:</strong></p>
                  <ul className="list-disc list-inside text-gray-700 space-y-1">
                    <li>Session cookies for authentication</li>
                    <li>Security cookies to prevent fraud</li>
                    <li>Load balancing cookies</li>
                  </ul>
                </div>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">3.2 Performance and Analytics Cookies</h3>
                <p className="text-gray-700 mb-4">
                  These cookies help us understand how visitors interact with our website by collecting and reporting information anonymously. This helps us improve our website and services.
                </p>
                <div className="bg-gray-50 p-4 rounded-lg mb-4">
                  <p className="text-gray-700 mb-2"><strong>Examples:</strong></p>
                  <ul className="list-disc list-inside text-gray-700 space-y-1">
                    <li>Google Analytics cookies (traffic and behavior analysis)</li>
                    <li>Performance monitoring cookies</li>
                    <li>Error tracking cookies</li>
                    <li>Page load time measurement</li>
                  </ul>
                </div>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">3.3 Functionality Cookies</h3>
                <p className="text-gray-700 mb-4">
                  These cookies allow the website to remember choices you make (such as your username, language, or region) and provide enhanced, personalized features.
                </p>
                <div className="bg-gray-50 p-4 rounded-lg mb-4">
                  <p className="text-gray-700 mb-2"><strong>Examples:</strong></p>
                  <ul className="list-disc list-inside text-gray-700 space-y-1">
                    <li>Language preference cookies</li>
                    <li>Theme/display preference cookies</li>
                    <li>Remember me functionality</li>
                    <li>Video player preferences</li>
                  </ul>
                </div>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">3.4 Targeting and Advertising Cookies</h3>
                <p className="text-gray-700 mb-4">
                  These cookies are used to deliver advertisements more relevant to you and your interests. They are also used to limit the number of times you see an advertisement and help measure the effectiveness of advertising campaigns.
                </p>
                <div className="bg-gray-50 p-4 rounded-lg mb-4">
                  <p className="text-gray-700 mb-2"><strong>Examples:</strong></p>
                  <ul className="list-disc list-inside text-gray-700 space-y-1">
                    <li>Google Ads cookies</li>
                    <li>Facebook Pixel</li>
                    <li>LinkedIn Insight Tag</li>
                    <li>Retargeting cookies</li>
                  </ul>
                </div>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">3.5 Social Media Cookies</h3>
                <p className="text-gray-700 mb-4">
                  These cookies are set by social media services that we have added to the site to enable you to share our content with your friends and networks.
                </p>
                <div className="bg-gray-50 p-4 rounded-lg mb-4">
                  <p className="text-gray-700 mb-2"><strong>Examples:</strong></p>
                  <ul className="list-disc list-inside text-gray-700 space-y-1">
                    <li>Social sharing buttons</li>
                    <li>Embedded social media content</li>
                    <li>Social login functionality</li>
                  </ul>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">4. Third-Party Cookies</h2>
                <p className="text-gray-700 mb-4">
                  In addition to our own cookies, we may use various third-party cookies to report usage statistics of our services and deliver advertisements:
                </p>

                <div className="space-y-4">
                  <div className="border-l-4 border-primary-500 pl-4">
                    <h4 className="font-semibold text-gray-800 mb-2">Google Analytics</h4>
                    <p className="text-gray-700 mb-2">
                      We use Google Analytics to track and analyze website traffic and user behavior.
                    </p>
                    <p className="text-sm text-gray-600">
                      Learn more: <a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">Google Privacy Policy</a>
                    </p>
                  </div>

                  <div className="border-l-4 border-primary-500 pl-4">
                    <h4 className="font-semibold text-gray-800 mb-2">Google Ads</h4>
                    <p className="text-gray-700 mb-2">
                      We use Google Ads for advertising and remarketing campaigns.
                    </p>
                    <p className="text-sm text-gray-600">
                      Learn more: <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">Google Ads Privacy</a>
                    </p>
                  </div>

                  <div className="border-l-4 border-primary-500 pl-4">
                    <h4 className="font-semibold text-gray-800 mb-2">Facebook Pixel</h4>
                    <p className="text-gray-700 mb-2">
                      We use Facebook Pixel to track conversions and create custom audiences.
                    </p>
                    <p className="text-sm text-gray-600">
                      Learn more: <a href="https://www.facebook.com/privacy/explanation" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">Facebook Data Policy</a>
                    </p>
                  </div>

                  <div className="border-l-4 border-primary-500 pl-4">
                    <h4 className="font-semibold text-gray-800 mb-2">LinkedIn Insight Tag</h4>
                    <p className="text-gray-700 mb-2">
                      We use LinkedIn Insight Tag for conversion tracking and audience targeting.
                    </p>
                    <p className="text-sm text-gray-600">
                      Learn more: <a href="https://www.linkedin.com/legal/privacy-policy" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">LinkedIn Privacy Policy</a>
                    </p>
                  </div>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">5. Cookie Duration</h2>
                <p className="text-gray-700 mb-4">
                  Cookies can be either &quot;session cookies&quot; or &quot;persistent cookies&quot;:
                </p>

                <div className="bg-gray-50 p-4 rounded-lg mb-4">
                  <h4 className="font-semibold text-gray-800 mb-2">Session Cookies</h4>
                  <p className="text-gray-700">
                    These cookies are temporary and are deleted when you close your browser. They help us track your actions during a single browsing session.
                  </p>
                </div>

                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-gray-800 mb-2">Persistent Cookies</h4>
                  <p className="text-gray-700">
                    These cookies remain on your device for a set period (ranging from days to years) and are activated each time you visit our website. They help us remember your preferences and actions across multiple visits.
                  </p>
                </div>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">6. Managing Cookies</h2>
                <p className="text-gray-700 mb-4">
                  You have the right to decide whether to accept or reject cookies. You can exercise your cookie preferences through several methods:
                </p>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">6.1 Browser Settings</h3>
                <p className="text-gray-700 mb-4">
                  Most web browsers allow you to control cookies through their settings. You can set your browser to:
                </p>
                <ul className="list-disc list-inside text-gray-700 mb-4 space-y-2">
                  <li>Block all cookies</li>
                  <li>Block third-party cookies only</li>
                  <li>Clear all cookies when you close the browser</li>
                  <li>Notify you when a cookie is set</li>
                </ul>

                <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-4">
                  <p className="text-sm text-gray-700">
                    <strong>Note:</strong> If you block cookies, some features of our website may not function properly, and your user experience may be affected.
                  </p>
                </div>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">6.2 Browser-Specific Instructions</h3>
                <div className="space-y-2 mb-4">
                  <p className="text-gray-700">
                    <strong>Chrome:</strong> <a href="https://support.google.com/chrome/answer/95647" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">Cookie settings in Chrome</a>
                  </p>
                  <p className="text-gray-700">
                    <strong>Firefox:</strong> <a href="https://support.mozilla.org/en-US/kb/cookies-information-websites-store-on-your-computer" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">Cookie settings in Firefox</a>
                  </p>
                  <p className="text-gray-700">
                    <strong>Safari:</strong> <a href="https://support.apple.com/guide/safari/manage-cookies-sfri11471/mac" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">Cookie settings in Safari</a>
                  </p>
                  <p className="text-gray-700">
                    <strong>Edge:</strong> <a href="https://support.microsoft.com/en-us/microsoft-edge/delete-cookies-in-microsoft-edge-63947406-40ac-c3b8-57b9-2a946a29ae09" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">Cookie settings in Edge</a>
                  </p>
                </div>

                <h3 className="text-xl font-semibold text-gray-800 mb-3">6.3 Opt-Out Tools</h3>
                <p className="text-gray-700 mb-4">
                  You can opt out of targeted advertising cookies through these industry tools:
                </p>
                <ul className="list-disc list-inside text-gray-700 mb-4 space-y-2">
                  <li><a href="http://optout.networkadvertising.org/" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">Network Advertising Initiative (NAI)</a></li>
                  <li><a href="http://optout.aboutads.info/" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">Digital Advertising Alliance (DAA)</a></li>
                  <li><a href="https://www.youronlinechoices.com/" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">European Interactive Digital Advertising Alliance (EDAA)</a></li>
                </ul>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">7. Do Not Track Signals</h2>
                <p className="text-gray-700 mb-4">
                  Some browsers include a &quot;Do Not Track&quot; (DNT) feature that signals to websites that you do not want your online activities tracked. Currently, there is no universal standard for how DNT signals should be interpreted. We do not currently respond to DNT signals.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">8. Mobile Device Identifiers</h2>
                <p className="text-gray-700 mb-4">
                  When you use our mobile applications, we may use mobile device identifiers (such as Apple&apos;s IDFA or Google&apos;s Advertising ID) for similar purposes as cookies. You can control these through your device settings:
                </p>
                <ul className="list-disc list-inside text-gray-700 mb-4 space-y-2">
                  <li><strong>iOS:</strong> Settings → Privacy → Advertising → Limit Ad Tracking</li>
                  <li><strong>Android:</strong> Settings → Google → Ads → Opt out of Ads Personalization</li>
                </ul>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">9. Updates to This Cookie Policy</h2>
                <p className="text-gray-700 mb-4">
                  We may update this Cookie Policy from time to time to reflect changes in our practices or for operational, legal, or regulatory reasons. We will notify you of any material changes by posting the new Cookie Policy on this page and updating the &quot;Last updated&quot; date.
                </p>
                <p className="text-gray-700">
                  We encourage you to review this Cookie Policy periodically to stay informed about our use of cookies.
                </p>
              </section>

              <section className="mb-8">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">10. More Information</h2>
                <p className="text-gray-700 mb-4">
                  For more information about how we handle your personal data, please see our <a href="/privacy" className="text-primary-600 hover:underline">Privacy Policy</a>.
                </p>
                <p className="text-gray-700 mb-4">
                  If you have any questions about our use of cookies, please contact us:
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
