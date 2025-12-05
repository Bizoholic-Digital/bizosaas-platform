import { Metadata } from 'next'
import { MainHeader } from '@/components/layout/main-header'
import { Footer } from '@/components/footer'
import { Card, CardContent } from '@/components/ui/card'

export const metadata: Metadata = {
  title: 'Privacy Policy - BizoSaaS AI Marketing Platform',
  description: 'Our commitment to protecting your privacy and data. Learn how we collect, use, and safeguard your information.',
}

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-background">
      <MainHeader />
      
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold mb-8">Privacy Policy</h1>
          <p className="text-muted-foreground mb-8">
            Last updated: January 1, 2025
          </p>

          <Card className="mb-8">
            <CardContent className="p-8 prose prose-gray max-w-none dark:prose-invert">
              <h2>Introduction</h2>
              <p>
                BizoSaaS ("we," "our," or "us") is committed to protecting your privacy. This Privacy Policy 
                explains how we collect, use, disclose, and safeguard your information when you use our 
                AI-powered marketing automation platform and related services.
              </p>

              <h2>Information We Collect</h2>
              
              <h3>Information You Provide</h3>
              <ul>
                <li><strong>Account Information:</strong> Name, email address, company details, and payment information</li>
                <li><strong>Profile Data:</strong> Marketing preferences, business goals, and campaign objectives</li>
                <li><strong>Content:</strong> Marketing campaigns, customer data, and creative assets you upload</li>
                <li><strong>Communications:</strong> Messages you send to us through support channels</li>
              </ul>

              <h3>Information We Collect Automatically</h3>
              <ul>
                <li><strong>Usage Data:</strong> How you interact with our platform, features used, and time spent</li>
                <li><strong>Device Information:</strong> IP address, browser type, device characteristics</li>
                <li><strong>Performance Data:</strong> Campaign metrics, conversion rates, and engagement statistics</li>
                <li><strong>Cookies:</strong> Essential cookies for functionality and analytics cookies with your consent</li>
              </ul>

              <h2>How We Use Your Information</h2>
              <p>We use the information we collect to:</p>
              <ul>
                <li>Provide and improve our AI marketing platform</li>
                <li>Process payments and manage your account</li>
                <li>Deliver customer support and respond to inquiries</li>
                <li>Analyze usage patterns to enhance our services</li>
                <li>Send important updates about your account and our services</li>
                <li>Comply with legal obligations and protect our rights</li>
              </ul>

              <h2>AI and Machine Learning</h2>
              <p>
                Our AI agents analyze your marketing data to provide personalized recommendations and automation. 
                This includes:
              </p>
              <ul>
                <li>Campaign performance optimization</li>
                <li>Audience segmentation and targeting</li>
                <li>Content personalization suggestions</li>
                <li>Predictive analytics for better ROI</li>
              </ul>
              <p>
                All AI processing is done in compliance with data protection laws, and your data is never 
                used to train models that benefit other customers.
              </p>

              <h2>Information Sharing</h2>
              <p>We may share your information in the following circumstances:</p>
              
              <h3>With Your Consent</h3>
              <p>We share information with third parties when you explicitly authorize us to do so.</p>

              <h3>Service Providers</h3>
              <p>We work with trusted third-party service providers who help us operate our platform:</p>
              <ul>
                <li><strong>Cloud Infrastructure:</strong> AWS, Google Cloud for secure data storage</li>
                <li><strong>Payment Processing:</strong> Stripe for secure payment handling</li>
                <li><strong>Analytics:</strong> Privacy-focused analytics to improve our service</li>
                <li><strong>Communication:</strong> Email and messaging services for platform notifications</li>
              </ul>

              <h3>Legal Requirements</h3>
              <p>
                We may disclose information when required by law, to protect our rights, or to investigate 
                fraud or security issues.
              </p>

              <h2>Data Security</h2>
              <p>We implement industry-standard security measures to protect your information:</p>
              <ul>
                <li><strong>Encryption:</strong> All data is encrypted in transit and at rest</li>
                <li><strong>Access Controls:</strong> Strict access limitations on a need-to-know basis</li>
                <li><strong>Regular Audits:</strong> Ongoing security assessments and penetration testing</li>
                <li><strong>Compliance:</strong> SOC 2 Type II and GDPR compliant infrastructure</li>
              </ul>

              <h2>Data Retention</h2>
              <p>
                We retain your information for as long as your account is active or as needed to provide services. 
                When you delete your account, we will delete your personal data within 30 days, except where 
                required for legal compliance.
              </p>

              <h2>Your Rights and Choices</h2>
              <p>Depending on your location, you may have the following rights:</p>
              <ul>
                <li><strong>Access:</strong> Request a copy of your personal data</li>
                <li><strong>Correction:</strong> Update or correct inaccurate information</li>
                <li><strong>Deletion:</strong> Request deletion of your personal data</li>
                <li><strong>Portability:</strong> Export your data in a machine-readable format</li>
                <li><strong>Opt-out:</strong> Unsubscribe from marketing communications</li>
              </ul>
              <p>To exercise these rights, contact us at privacy@bizosaas.com</p>

              <h2>International Transfers</h2>
              <p>
                Your information may be processed in countries other than your own. We ensure adequate 
                protection through standard contractual clauses and other appropriate safeguards.
              </p>

              <h2>Children's Privacy</h2>
              <p>
                Our services are not intended for individuals under 16 years of age. We do not knowingly 
                collect personal information from children under 16.
              </p>

              <h2>California Privacy Rights</h2>
              <p>
                If you are a California resident, you have additional rights under the California Consumer 
                Privacy Act (CCPA), including the right to know, delete, and opt-out of the sale of personal information.
              </p>

              <h2>Updates to This Policy</h2>
              <p>
                We may update this Privacy Policy from time to time. We will notify you of material changes 
                via email or through our platform. Your continued use of our services after changes indicates 
                acceptance of the updated policy.
              </p>

              <h2>Contact Us</h2>
              <p>
                If you have questions about this Privacy Policy or our privacy practices, please contact us:
              </p>
              <ul>
                <li><strong>Email:</strong> privacy@bizosaas.com</li>
                <li><strong>Address:</strong> BizoSaaS, Inc., 1234 Innovation Drive, San Francisco, CA 94105</li>
                <li><strong>Phone:</strong> +1 (555) 123-4567</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
      
      <Footer />
    </div>
  )
}