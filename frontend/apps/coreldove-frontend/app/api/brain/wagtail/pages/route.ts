/**
 * Wagtail CMS Pages API Route - Dynamic Content Management
 * Connects to Wagtail CMS via Brain API for manageable page content
 */

import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const slug = searchParams.get('slug')
    const type = searchParams.get('type') || 'page'
    
    // Build the Wagtail API URL
    let wagtailPath = '/api/v2/pages/'
    if (slug) {
      wagtailPath += `?slug=${slug}&type=${type}&fields=*`
    } else {
      wagtailPath += `?type=${type}&fields=*`
    }

    // Call Wagtail CMS via Brain API
    const response = await fetch(`${BRAIN_API_URL}/api/brain/wagtail${wagtailPath}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3012',
      },
    })

    if (response.ok) {
      const data = await response.json()
      return NextResponse.json(data)
    } else {
      console.error('Failed to fetch from Wagtail CMS:', response.status)
      
      // Fallback page content for development/testing
      const fallbackPages = {
        meta: { total_count: 6 },
        items: [
          {
            id: 1,
            title: 'Privacy Policy',
            slug: 'privacy',
            content: `
              <div class="privacy-policy">
                <p class="text-lg text-muted-foreground mb-8">At CorelDove, we are committed to protecting your privacy and ensuring that your personal information is handled in a safe and responsible manner. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our website or use our services.</p>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Information We Collect</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Personal Information</h3>
                <p>We may collect personal information that you provide directly to us, including:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li><strong>Contact Information:</strong> Name, email address, phone number, mailing address</li>
                  <li><strong>Account Information:</strong> Username, password, preferences, and account settings</li>
                  <li><strong>Purchase Information:</strong> Billing address, shipping address, payment method details</li>
                  <li><strong>Communication:</strong> Messages, feedback, reviews, and customer service inquiries</li>
                  <li><strong>Marketing Preferences:</strong> Subscription preferences and communication choices</li>
                </ul>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Automatically Collected Information</h3>
                <p>When you visit our website, we automatically collect certain information about your device and usage patterns:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li><strong>Technical Information:</strong> IP address, browser type, operating system, device identifiers</li>
                  <li><strong>Usage Data:</strong> Pages visited, time spent on pages, click-through rates, search terms</li>
                  <li><strong>Cookies and Tracking:</strong> Session cookies, persistent cookies, web beacons, and similar technologies</li>
                  <li><strong>Location Data:</strong> General geographic location based on IP address</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">How We Use Your Information</h2>
                
                <p>We use the information we collect for various business purposes, including:</p>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Service Provision</h3>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Processing and fulfilling your orders and transactions</li>
                  <li>Creating and managing your account</li>
                  <li>Providing customer support and responding to inquiries</li>
                  <li>Delivering products and services you request</li>
                  <li>Processing payments and managing billing</li>
                </ul>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Communication and Marketing</h3>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Sending order confirmations, shipping notifications, and account updates</li>
                  <li>Providing promotional materials and marketing communications (with your consent)</li>
                  <li>Conducting surveys and gathering feedback</li>
                  <li>Sending newsletters and product announcements</li>
                </ul>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Improvement and Analytics</h3>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Analyzing website usage patterns and user behavior</li>
                  <li>Improving our products, services, and website functionality</li>
                  <li>Conducting research and development</li>
                  <li>Personalizing your shopping experience and recommendations</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Information Sharing and Disclosure</h2>
                
                <p>We do not sell, trade, or rent your personal information to third parties. However, we may share your information in the following circumstances:</p>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Service Providers</h3>
                <p>We may share information with trusted third-party service providers who assist us in:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Payment processing and fraud prevention</li>
                  <li>Shipping and logistics</li>
                  <li>Email marketing and communication services</li>
                  <li>Website hosting and technical support</li>
                  <li>Analytics and data analysis</li>
                </ul>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Legal Requirements</h3>
                <p>We may disclose your information when required by law or in response to:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Valid legal requests from government authorities</li>
                  <li>Court orders, subpoenas, or other legal processes</li>
                  <li>Protecting our rights, property, or safety</li>
                  <li>Investigating fraud or security issues</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Data Security</h2>
                
                <p>We implement appropriate technical and organizational security measures to protect your personal information:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li><strong>Encryption:</strong> SSL/TLS encryption for data transmission</li>
                  <li><strong>Access Controls:</strong> Limited access to personal information on a need-to-know basis</li>
                  <li><strong>Regular Updates:</strong> Security patches and system updates</li>
                  <li><strong>Monitoring:</strong> Continuous monitoring for security breaches</li>
                  <li><strong>Data Backup:</strong> Regular backups with secure storage</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Your Rights and Choices</h2>
                
                <p>You have certain rights regarding your personal information:</p>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Access and Control</h3>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li><strong>Access:</strong> Request access to your personal information</li>
                  <li><strong>Correction:</strong> Update or correct inaccurate information</li>
                  <li><strong>Deletion:</strong> Request deletion of your personal information</li>
                  <li><strong>Portability:</strong> Request a copy of your data in a portable format</li>
                  <li><strong>Restriction:</strong> Limit how we process your information</li>
                </ul>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Marketing Communications</h3>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Unsubscribe from promotional emails using the unsubscribe link</li>
                  <li>Update your communication preferences in your account settings</li>
                  <li>Contact us directly to opt out of marketing communications</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Cookies and Tracking Technologies</h2>
                
                <p>Our website uses cookies and similar tracking technologies to enhance your browsing experience:</p>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Types of Cookies</h3>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li><strong>Essential Cookies:</strong> Required for basic website functionality</li>
                  <li><strong>Performance Cookies:</strong> Help us understand how visitors use our website</li>
                  <li><strong>Functional Cookies:</strong> Remember your preferences and settings</li>
                  <li><strong>Marketing Cookies:</strong> Used to deliver relevant advertisements</li>
                </ul>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Managing Cookies</h3>
                <p>You can control cookies through your browser settings. Note that disabling certain cookies may affect website functionality.</p>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">International Data Transfers</h2>
                
                <p>Your information may be transferred to and stored in countries other than your own. We ensure appropriate safeguards are in place for international transfers, including:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Adequacy decisions by relevant data protection authorities</li>
                  <li>Standard contractual clauses approved by regulatory bodies</li>
                  <li>Binding corporate rules and certification mechanisms</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Children's Privacy</h2>
                
                <p>Our services are not intended for children under 13 years of age. We do not knowingly collect personal information from children under 13. If we become aware that we have collected information from a child under 13, we will take steps to delete such information.</p>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Changes to This Privacy Policy</h2>
                
                <p>We may update this Privacy Policy from time to time to reflect changes in our practices or applicable laws. We will:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Post the updated policy on our website</li>
                  <li>Update the "Last Updated" date</li>
                  <li>Notify you of significant changes via email or website notice</li>
                  <li>Obtain your consent for material changes where required by law</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Contact Information</h2>
                
                <p>If you have any questions, concerns, or requests regarding this Privacy Policy or our data practices, please contact us:</p>
                
                <div class="bg-muted p-6 rounded-lg mt-4">
                  <h3 class="text-lg font-medium mb-3">Privacy Officer</h3>
                  <p><strong>Email:</strong> privacy@coreldove.com</p>
                  <p><strong>Phone:</strong> 1-800-CORELDOVE (1-800-267-3536)</p>
                  <p><strong>Mail:</strong> CorelDove Privacy Department<br>
                     123 Commerce Street<br>
                     Business District, BD 12345<br>
                     United States</p>
                  <p class="mt-3"><strong>Response Time:</strong> We will respond to your privacy inquiries within 30 days of receipt.</p>
                </div>
                
                <p class="text-sm text-muted-foreground mt-8 p-4 bg-muted/50 rounded">
                  <strong>Last Updated:</strong> December 2024<br>
                  This Privacy Policy is effective as of the date last updated and applies to all information collected by CorelDove.
                </p>
              </div>
            `,
            meta: {
              seo_title: 'Privacy Policy - CorelDove | Data Protection & Security',
              search_description: 'Learn about CorelDove\'s comprehensive privacy practices, data protection measures, and how we safeguard your personal information. Your privacy is our priority.'
            }
          },
          {
            id: 2,
            title: 'Terms of Service',
            slug: 'terms',
            content: `
              <div class="terms-of-service">
                <p class="text-lg text-muted-foreground mb-8">Welcome to CorelDove. These Terms of Service ("Terms") govern your use of our website, products, and services. By accessing or using CorelDove, you agree to be bound by these Terms. Please read them carefully.</p>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">1. Acceptance of Terms</h2>
                
                <p>By accessing, browsing, or using the CorelDove website or services, you acknowledge that you have read, understood, and agree to be bound by these Terms and our Privacy Policy. If you do not agree to these Terms, please do not use our services.</p>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Modifications to Terms</h3>
                <p>We reserve the right to modify these Terms at any time. Changes will be effective immediately upon posting on our website. Your continued use of our services after any modifications constitutes acceptance of the updated Terms.</p>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">2. Description of Services</h2>
                
                <p>CorelDove provides an e-commerce platform offering:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Online product catalog and shopping experience</li>
                  <li>Secure payment processing and order management</li>
                  <li>Customer account management and order tracking</li>
                  <li>Customer support and assistance services</li>
                  <li>Product recommendations and personalized content</li>
                  <li>Shipping and delivery coordination</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">3. User Accounts and Registration</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Account Creation</h3>
                <p>To access certain features of our services, you may need to create an account. You agree to:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Provide accurate, current, and complete information during registration</li>
                  <li>Maintain and update your account information as necessary</li>
                  <li>Keep your password secure and confidential</li>
                  <li>Notify us immediately of any unauthorized use of your account</li>
                  <li>Accept responsibility for all activities under your account</li>
                </ul>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Account Security</h3>
                <p>You are solely responsible for maintaining the confidentiality of your account credentials. CorelDove will not be liable for any loss or damage arising from unauthorized use of your account.</p>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">4. Use License and Restrictions</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Permitted Use</h3>
                <p>Subject to these Terms, we grant you a limited, non-exclusive, non-transferable license to:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Access and use our website for personal, non-commercial purposes</li>
                  <li>Browse and purchase products through our platform</li>
                  <li>Create and manage your user account</li>
                  <li>Use our customer support services</li>
                </ul>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Prohibited Activities</h3>
                <p>You agree not to:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Use our services for any illegal or unauthorized purpose</li>
                  <li>Violate any applicable laws or regulations</li>
                  <li>Infringe upon intellectual property rights of others</li>
                  <li>Transmit harmful, threatening, or defamatory content</li>
                  <li>Attempt to gain unauthorized access to our systems</li>
                  <li>Use automated tools to access or scrape our website</li>
                  <li>Interfere with the proper functioning of our services</li>
                  <li>Impersonate any person or entity</li>
                  <li>Collect personal information about other users</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">5. Products and Pricing</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Product Information</h3>
                <p>We strive to provide accurate product descriptions, images, and pricing. However:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Product information may not always be completely accurate or current</li>
                  <li>Colors and images may vary from actual products due to display differences</li>
                  <li>We reserve the right to correct errors in product information</li>
                  <li>Product availability is subject to change without notice</li>
                </ul>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Pricing and Payment</h3>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>All prices are subject to change without notice</li>
                  <li>Prices are displayed in USD unless otherwise indicated</li>
                  <li>Additional taxes, shipping, and handling fees may apply</li>
                  <li>We reserve the right to refuse or cancel orders for any reason</li>
                  <li>Payment must be received before order processing</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">6. Orders and Purchasing</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Order Process</h3>
                <p>When you place an order through our website:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Your order constitutes an offer to purchase products</li>
                  <li>We reserve the right to accept or decline your order</li>
                  <li>Order confirmation does not guarantee product availability</li>
                  <li>We will notify you if products become unavailable</li>
                  <li>Incorrect pricing errors may result in order cancellation</li>
                </ul>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Payment Terms</h3>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Payment is due at the time of order placement</li>
                  <li>We accept major credit cards, PayPal, and other specified payment methods</li>
                  <li>Your payment information must be accurate and current</li>
                  <li>You authorize us to charge your payment method for the total order amount</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">7. Shipping and Delivery</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Shipping Policy</h3>
                <p>Our shipping terms include:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Shipping costs are calculated based on destination and product weight</li>
                  <li>Delivery times are estimates and not guaranteed</li>
                  <li>Risk of loss transfers to you upon delivery</li>
                  <li>We are not responsible for delays caused by carriers</li>
                  <li>International shipping may be subject to customs duties</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">8. Returns and Refunds</h2>
                
                <p>Please refer to our detailed Return Policy for complete information. In summary:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Returns must be initiated within 30 days of delivery</li>
                  <li>Products must be in original condition and packaging</li>
                  <li>Return shipping costs may apply</li>
                  <li>Refunds will be processed to the original payment method</li>
                  <li>Some items may not be eligible for return</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">9. Intellectual Property Rights</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Our Content</h3>
                <p>All content on our website, including text, graphics, logos, images, and software, is the property of CorelDove or our licensors and is protected by copyright, trademark, and other intellectual property laws.</p>
                
                <h3 class="text-xl font-medium mt-6 mb-3">User Content</h3>
                <p>By submitting content to our website (reviews, comments, etc.), you grant us a non-exclusive, royalty-free license to use, modify, and display such content in connection with our services.</p>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">10. Privacy and Data Protection</h2>
                
                <p>Your privacy is important to us. Please review our Privacy Policy to understand how we collect, use, and protect your information. By using our services, you consent to our data practices as described in our Privacy Policy.</p>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">11. Disclaimers and Limitations</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Service Availability</h3>
                <p>Our services are provided "as is" and "as available." We do not guarantee:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Uninterrupted or error-free service</li>
                  <li>Complete accuracy of all information</li>
                  <li>Compatibility with all devices or browsers</li>
                  <li>Freedom from viruses or harmful components</li>
                </ul>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Limitation of Liability</h3>
                <p>To the maximum extent permitted by law, CorelDove shall not be liable for any indirect, incidental, special, consequential, or punitive damages arising from your use of our services.</p>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">12. Indemnification</h2>
                
                <p>You agree to indemnify and hold harmless CorelDove, its officers, directors, employees, and agents from any claims, damages, losses, or expenses arising from:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Your use of our services</li>
                  <li>Your violation of these Terms</li>
                  <li>Your violation of any rights of others</li>
                  <li>Any content you submit or share through our services</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">13. Termination</h2>
                
                <p>We may terminate or suspend your account and access to our services at any time, with or without notice, for any reason, including violation of these Terms. Upon termination:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Your right to use our services will cease immediately</li>
                  <li>We may delete your account and associated data</li>
                  <li>Outstanding orders may be cancelled or fulfilled at our discretion</li>
                  <li>Provisions that should survive termination will remain in effect</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">14. Governing Law and Dispute Resolution</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Governing Law</h3>
                <p>These Terms are governed by and construed in accordance with the laws of the State of [State] and federal laws of the United States, without regard to conflict of law principles.</p>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Dispute Resolution</h3>
                <p>Any disputes arising from these Terms or your use of our services will be resolved through:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Good faith negotiation between the parties</li>
                  <li>Binding arbitration if negotiation fails</li>
                  <li>Appropriate courts in [Jurisdiction] for certain matters</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">15. Miscellaneous</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Entire Agreement</h3>
                <p>These Terms, together with our Privacy Policy and any other legal notices, constitute the entire agreement between you and CorelDove regarding your use of our services.</p>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Severability</h3>
                <p>If any provision of these Terms is found to be unenforceable, the remaining provisions will remain in full force and effect.</p>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Waiver</h3>
                <p>Our failure to enforce any provision of these Terms does not constitute a waiver of that provision or any other provision.</p>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">16. Contact Information</h2>
                
                <p>If you have questions about these Terms of Service, please contact us:</p>
                
                <div class="bg-muted p-6 rounded-lg mt-4">
                  <h3 class="text-lg font-medium mb-3">Legal Department</h3>
                  <p><strong>Email:</strong> legal@coreldove.com</p>
                  <p><strong>Phone:</strong> 1-800-CORELDOVE (1-800-267-3536)</p>
                  <p><strong>Mail:</strong> CorelDove Legal Department<br>
                     123 Commerce Street<br>
                     Business District, BD 12345<br>
                     United States</p>
                  <p class="mt-3"><strong>Business Hours:</strong> Monday - Friday, 9:00 AM - 5:00 PM EST</p>
                </div>
                
                <p class="text-sm text-muted-foreground mt-8 p-4 bg-muted/50 rounded">
                  <strong>Last Updated:</strong> December 2024<br>
                  These Terms of Service are effective as of the date last updated and supersede all prior agreements.
                </p>
              </div>
            `,
            meta: {
              seo_title: 'Terms of Service - CorelDove | Legal Terms & Conditions',
              search_description: 'Read CorelDove\'s comprehensive terms of service, user agreements, and legal policies governing your use of our e-commerce platform and services.'
            }
          },
          {
            id: 3,
            title: 'Shipping Information',
            slug: 'shipping',
            content: `
              <div class="shipping-information">
                <p class="text-lg text-muted-foreground mb-8">CorelDove is committed to getting your orders to you quickly and safely. We offer multiple shipping options to meet your needs, whether you need standard delivery or expedited shipping.</p>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Shipping Options & Rates</h2>
                
                <div class="grid md:grid-cols-3 gap-6 mt-6">
                  <div class="bg-muted p-6 rounded-lg">
                    <h3 class="text-xl font-medium mb-3">📦 Standard Shipping</h3>
                    <p class="text-2xl font-bold text-primary mb-2">FREE</p>
                    <p class="text-sm text-muted-foreground mb-3">On orders over $50</p>
                    <ul class="text-sm space-y-1">
                      <li>• 3-5 business days</li>
                      <li>• $4.99 for orders under $50</li>
                      <li>• Package tracking included</li>
                      <li>• Signature not required</li>
                    </ul>
                  </div>
                  
                  <div class="bg-muted p-6 rounded-lg">
                    <h3 class="text-xl font-medium mb-3">⚡ Express Shipping</h3>
                    <p class="text-2xl font-bold text-primary mb-2">$9.99</p>
                    <p class="text-sm text-muted-foreground mb-3">All orders</p>
                    <ul class="text-sm space-y-1">
                      <li>• 1-2 business days</li>
                      <li>• Priority handling</li>
                      <li>• Real-time tracking</li>
                      <li>• Insurance included</li>
                    </ul>
                  </div>
                  
                  <div class="bg-muted p-6 rounded-lg">
                    <h3 class="text-xl font-medium mb-3">🚀 Overnight Shipping</h3>
                    <p class="text-2xl font-bold text-primary mb-2">$19.99</p>
                    <p class="text-sm text-muted-foreground mb-3">Next business day</p>
                    <ul class="text-sm space-y-1">
                      <li>• Next business day delivery</li>
                      <li>• Guaranteed by 10:30 AM</li>
                      <li>• Signature required</li>
                      <li>• Full insurance coverage</li>
                    </ul>
                  </div>
                </div>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Processing Time</h2>
                
                <div class="bg-blue-50 border border-blue-200 p-6 rounded-lg">
                  <h3 class="text-lg font-medium mb-3">📋 Order Processing Schedule</h3>
                  <ul class="space-y-2">
                    <li>• <strong>Orders placed before 2:00 PM EST:</strong> Same day processing</li>
                    <li>• <strong>Orders placed after 2:00 PM EST:</strong> Next business day processing</li>
                    <li>• <strong>Weekend orders:</strong> Processed on Monday</li>
                    <li>• <strong>Holiday orders:</strong> Processed on next business day</li>
                  </ul>
                  <p class="text-sm text-muted-foreground mt-4">Processing time is separate from shipping time. Orders typically ship within 1-2 business days of processing.</p>
                </div>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">International Shipping</h2>
                
                <p>We're proud to serve customers worldwide with shipping to over 50 countries:</p>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Available Countries</h3>
                <div class="grid md:grid-cols-2 gap-6 mt-4">
                  <div>
                    <h4 class="font-medium mb-2">🌍 Europe (5-10 business days)</h4>
                    <p class="text-sm text-muted-foreground">United Kingdom, Germany, France, Italy, Spain, Netherlands, Belgium, Austria, Sweden, Norway, Denmark</p>
                  </div>
                  <div>
                    <h4 class="font-medium mb-2">🌏 Asia-Pacific (7-14 business days)</h4>
                    <p class="text-sm text-muted-foreground">Australia, Japan, Singapore, South Korea, Hong Kong, New Zealand, Taiwan, Malaysia</p>
                  </div>
                  <div>
                    <h4 class="font-medium mb-2">🌎 Americas (3-8 business days)</h4>
                    <p class="text-sm text-muted-foreground">Canada, Mexico, Brazil, Argentina, Chile, Colombia</p>
                  </div>
                  <div>
                    <h4 class="font-medium mb-2">🌍 Other Regions (10-21 business days)</h4>
                    <p class="text-sm text-muted-foreground">South Africa, Israel, UAE, Saudi Arabia, India, Thailand</p>
                  </div>
                </div>
                
                <h3 class="text-xl font-medium mt-6 mb-3">International Shipping Rates</h3>
                <div class="overflow-x-auto">
                  <table class="w-full border-collapse border border-gray-300 mt-4">
                    <thead>
                      <tr class="bg-muted">
                        <th class="border border-gray-300 p-3 text-left">Region</th>
                        <th class="border border-gray-300 p-3 text-left">Standard</th>
                        <th class="border border-gray-300 p-3 text-left">Express</th>
                        <th class="border border-gray-300 p-3 text-left">Delivery Time</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td class="border border-gray-300 p-3">Canada</td>
                        <td class="border border-gray-300 p-3">$12.99</td>
                        <td class="border border-gray-300 p-3">$24.99</td>
                        <td class="border border-gray-300 p-3">3-8 days</td>
                      </tr>
                      <tr class="bg-muted/20">
                        <td class="border border-gray-300 p-3">Europe</td>
                        <td class="border border-gray-300 p-3">$19.99</td>
                        <td class="border border-gray-300 p-3">$39.99</td>
                        <td class="border border-gray-300 p-3">5-10 days</td>
                      </tr>
                      <tr>
                        <td class="border border-gray-300 p-3">Asia-Pacific</td>
                        <td class="border border-gray-300 p-3">$24.99</td>
                        <td class="border border-gray-300 p-3">$49.99</td>
                        <td class="border border-gray-300 p-3">7-14 days</td>
                      </tr>
                      <tr class="bg-muted/20">
                        <td class="border border-gray-300 p-3">Other Regions</td>
                        <td class="border border-gray-300 p-3">$29.99</td>
                        <td class="border border-gray-300 p-3">$59.99</td>
                        <td class="border border-gray-300 p-3">10-21 days</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Important International Notes</h3>
                <div class="bg-yellow-50 border border-yellow-200 p-6 rounded-lg">
                  <ul class="space-y-2">
                    <li>• <strong>Customs & Duties:</strong> Additional fees may apply based on your country's import regulations</li>
                    <li>• <strong>Restricted Items:</strong> Some products may not be available for international shipping</li>
                    <li>• <strong>Address Accuracy:</strong> Please ensure your address is complete and accurate to avoid delays</li>
                    <li>• <strong>Tracking:</strong> International tracking may have limited visibility in some regions</li>
                  </ul>
                </div>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Package Tracking</h2>
                
                <p>Stay informed about your order every step of the way:</p>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Tracking Information</h3>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li><strong>Email Notifications:</strong> Tracking number sent via email once your order ships</li>
                  <li><strong>Real-time Updates:</strong> Track your package status 24/7 on our website</li>
                  <li><strong>SMS Alerts:</strong> Optional text message updates for delivery notifications</li>
                  <li><strong>Account Dashboard:</strong> View all your order tracking information in one place</li>
                  <li><strong>Delivery Confirmation:</strong> Photo confirmation upon delivery (where available)</li>
                </ul>
                
                <h3 class="text-xl font-medium mt-6 mb-3">How to Track Your Order</h3>
                <div class="grid md:grid-cols-2 gap-6 mt-4">
                  <div class="bg-muted p-6 rounded-lg">
                    <h4 class="font-medium mb-3">🔗 Track Online</h4>
                    <ol class="text-sm space-y-2">
                      <li>1. Visit our tracking page</li>
                      <li>2. Enter your order number or tracking number</li>
                      <li>3. View real-time status updates</li>
                      <li>4. Get estimated delivery time</li>
                    </ol>
                  </div>
                  <div class="bg-muted p-6 rounded-lg">
                    <h4 class="font-medium mb-3">📱 Track via Email/SMS</h4>
                    <ol class="text-sm space-y-2">
                      <li>1. Check your email for shipping confirmation</li>
                      <li>2. Click the tracking link provided</li>
                      <li>3. Enable SMS notifications if desired</li>
                      <li>4. Receive updates on your phone</li>
                    </ol>
                  </div>
                </div>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Delivery Information</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Delivery Requirements</h3>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li><strong>Address Accuracy:</strong> Ensure your delivery address is complete and correct</li>
                  <li><strong>Availability:</strong> Someone should be available to receive the package</li>
                  <li><strong>Secure Location:</strong> Choose a safe delivery location if you won't be home</li>
                  <li><strong>ID Verification:</strong> Some packages may require ID verification upon delivery</li>
                </ul>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Delivery Attempts</h3>
                <div class="bg-muted p-6 rounded-lg">
                  <p>If you're not available for delivery:</p>
                  <ul class="mt-3 space-y-2">
                    <li>• <strong>First Attempt:</strong> Package left at secure location or neighbor (if safe)</li>
                    <li>• <strong>Second Attempt:</strong> Delivery notice left with pickup instructions</li>
                    <li>• <strong>Third Attempt:</strong> Package held at local carrier facility for pickup</li>
                    <li>• <strong>Final Notice:</strong> Package returned to sender after 7 days</li>
                  </ul>
                </div>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Special Shipping Services</h2>
                
                <div class="grid md:grid-cols-2 gap-6 mt-6">
                  <div class="bg-muted p-6 rounded-lg">
                    <h3 class="text-lg font-medium mb-3">🎁 Gift Wrapping</h3>
                    <p class="text-sm mb-3">Make your gift extra special with our professional gift wrapping service.</p>
                    <ul class="text-sm space-y-1">
                      <li>• Premium wrapping paper</li>
                      <li>• Decorative ribbon and bow</li>
                      <li>• Personalized gift message</li>
                      <li>• Additional $4.99 per item</li>
                    </ul>
                  </div>
                  
                  <div class="bg-muted p-6 rounded-lg">
                    <h3 class="text-lg font-medium mb-3">📅 Scheduled Delivery</h3>
                    <p class="text-sm mb-3">Choose a specific delivery date that works for you.</p>
                    <ul class="text-sm space-y-1">
                      <li>• Select preferred delivery date</li>
                      <li>• Available for express shipping</li>
                      <li>• Subject to carrier availability</li>
                      <li>• Additional $7.99 fee</li>
                    </ul>
                  </div>
                </div>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Shipping Policies</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Order Modifications</h3>
                <div class="bg-red-50 border border-red-200 p-6 rounded-lg">
                  <p class="mb-3">Once an order is placed, modifications may not be possible due to our quick processing times:</p>
                  <ul class="space-y-2">
                    <li>• <strong>Address Changes:</strong> Contact us within 1 hour of placing your order</li>
                    <li>• <strong>Shipping Method:</strong> Changes may be possible before processing</li>
                    <li>• <strong>Order Cancellation:</strong> Must be requested before shipment</li>
                    <li>• <strong>Emergency Contact:</strong> Call 1-800-CORELDOVE for urgent requests</li>
                  </ul>
                </div>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Damaged or Lost Packages</h3>
                <p>We take full responsibility for packages until they reach you safely:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li><strong>Damaged Items:</strong> Full replacement or refund for items damaged during shipping</li>
                  <li><strong>Lost Packages:</strong> Investigation initiated after expected delivery date</li>
                  <li><strong>Claims Process:</strong> We handle all carrier claims on your behalf</li>
                  <li><strong>Resolution Time:</strong> Most issues resolved within 3-5 business days</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Contact Shipping Support</h2>
                
                <p>Need help with your shipment? Our shipping support team is here to help:</p>
                
                <div class="bg-muted p-6 rounded-lg mt-4">
                  <h3 class="text-lg font-medium mb-3">Shipping Support Team</h3>
                  <p><strong>Email:</strong> shipping@coreldove.com</p>
                  <p><strong>Phone:</strong> 1-800-CORELDOVE (1-800-267-3536)</p>
                  <p><strong>Live Chat:</strong> Available on our website 24/7</p>
                  <p class="mt-3"><strong>Support Hours:</strong> Monday - Friday, 8:00 AM - 8:00 PM EST<br>
                     Saturday - Sunday, 10:00 AM - 6:00 PM EST</p>
                </div>
                
                <p class="text-sm text-muted-foreground mt-8 p-4 bg-muted/50 rounded">
                  <strong>Last Updated:</strong> December 2024<br>
                  Shipping information and rates are subject to change. Current rates apply at checkout.
                </p>
              </div>
            `,
            meta: {
              seo_title: 'Shipping Information - CorelDove | Fast & Reliable Delivery',
              search_description: 'Comprehensive shipping information for CorelDove orders. Learn about delivery options, international shipping, tracking, and our commitment to fast, secure delivery.'
            }
          },
          {
            id: 4,
            title: 'Returns & Exchanges',
            slug: 'returns',
            content: `
              <div class="returns-exchanges">
                <p class="text-lg text-muted-foreground mb-8">At CorelDove, your satisfaction is our top priority. We stand behind every product we sell and want you to be completely happy with your purchase. Our comprehensive returns and exchanges policy ensures a hassle-free experience.</p>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Our Return Promise</h2>
                
                <div class="bg-green-50 border border-green-200 p-6 rounded-lg mb-6">
                  <h3 class="text-lg font-medium mb-3">✅ 30-Day Satisfaction Guarantee</h3>
                  <p>We offer a full <strong>30-day return window</strong> from the date of delivery. If you're not completely satisfied with your purchase, we'll make it right with a full refund or exchange.</p>
                </div>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Return Policy</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Eligible Items</h3>
                <p>Most items purchased from CorelDove can be returned within 30 days of delivery:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li><strong>New, unused items</strong> in original packaging</li>
                  <li><strong>Items with original tags</strong> and labels attached</li>
                  <li><strong>Electronics</strong> in original condition with all accessories</li>
                  <li><strong>Clothing and accessories</strong> unworn with tags</li>
                  <li><strong>Home goods</strong> in resalable condition</li>
                </ul>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Non-Returnable Items</h3>
                <p>For health and safety reasons, certain items cannot be returned:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li>Personal care items (opened cosmetics, toiletries)</li>
                  <li>Underwear and intimate apparel</li>
                  <li>Custom or personalized items</li>
                  <li>Perishable goods and food items</li>
                  <li>Digital downloads and software</li>
                  <li>Final sale or clearance items</li>
                  <li>Items damaged by misuse or normal wear</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">How to Return Items</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Step-by-Step Return Process</h3>
                
                <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
                  <div class="bg-muted p-4 rounded-lg text-center">
                    <div class="text-2xl font-bold text-primary mb-2">1</div>
                    <h4 class="font-medium mb-2">Initiate Return</h4>
                    <p class="text-sm">Contact our customer service or use your account dashboard to start a return</p>
                  </div>
                  
                  <div class="bg-muted p-4 rounded-lg text-center">
                    <div class="text-2xl font-bold text-primary mb-2">2</div>
                    <h4 class="font-medium mb-2">Get Authorization</h4>
                    <p class="text-sm">Receive your Return Authorization (RA) number and prepaid shipping label</p>
                  </div>
                  
                  <div class="bg-muted p-4 rounded-lg text-center">
                    <div class="text-2xl font-bold text-primary mb-2">3</div>
                    <h4 class="font-medium mb-2">Package Securely</h4>
                    <p class="text-sm">Pack items in original packaging with all accessories and documentation</p>
                  </div>
                  
                  <div class="bg-muted p-4 rounded-lg text-center">
                    <div class="text-2xl font-bold text-primary mb-2">4</div>
                    <h4 class="font-medium mb-2">Ship & Track</h4>
                    <p class="text-sm">Drop off at any authorized shipping location and track your return</p>
                  </div>
                </div>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Return Methods</h3>
                
                <div class="grid md:grid-cols-2 gap-6 mt-4">
                  <div class="bg-muted p-6 rounded-lg">
                    <h4 class="font-medium mb-3">🌐 Online Return Portal</h4>
                    <ol class="text-sm space-y-2">
                      <li>1. Log into your CorelDove account</li>
                      <li>2. Go to "Order History" → "Return Items"</li>
                      <li>3. Select items and reason for return</li>
                      <li>4. Print prepaid shipping label</li>
                      <li>5. Drop off at any UPS/FedEx location</li>
                    </ol>
                  </div>
                  
                  <div class="bg-muted p-6 rounded-lg">
                    <h4 class="font-medium mb-3">📞 Phone Support</h4>
                    <ol class="text-sm space-y-2">
                      <li>1. Call 1-800-CORELDOVE</li>
                      <li>2. Provide order number and return details</li>
                      <li>3. Receive RA number via email</li>
                      <li>4. Use provided shipping label</li>
                      <li>5. Get confirmation once shipped</li>
                    </ol>
                  </div>
                </div>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Exchanges</h2>
                
                <p>We make exchanges simple and convenient:</p>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Free Exchange Options</h3>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li><strong>Size Exchanges:</strong> Different size of the same item</li>
                  <li><strong>Color Exchanges:</strong> Different color of the same item</li>
                  <li><strong>Style Exchanges:</strong> Different style within same product category</li>
                  <li><strong>Defective Items:</strong> Replacement for damaged or defective products</li>
                </ul>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Exchange Process</h3>
                <div class="bg-blue-50 border border-blue-200 p-6 rounded-lg">
                  <ol class="space-y-3">
                    <li><strong>Choose Exchange Type:</strong> Select whether you want same item in different size/color or a different item</li>
                    <li><strong>Send Original Item:</strong> Use the return process above to send back the original item</li>
                    <li><strong>Automatic Processing:</strong> We'll ship your replacement as soon as we receive the return</li>
                    <li><strong>Price Adjustments:</strong> If there's a price difference, we'll charge or refund accordingly</li>
                  </ol>
                </div>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Exchange Timeline</h3>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li><strong>Processing:</strong> 1-2 business days after we receive your return</li>
                  <li><strong>Shipping:</strong> 2-5 business days for standard shipping</li>
                  <li><strong>Express Option:</strong> 1-2 business day shipping available for urgent exchanges</li>
                  <li><strong>Total Time:</strong> Typically 5-7 business days from return to delivery</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Refund Information</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Refund Timeline</h3>
                <div class="overflow-x-auto">
                  <table class="w-full border-collapse border border-gray-300 mt-4">
                    <thead>
                      <tr class="bg-muted">
                        <th class="border border-gray-300 p-3 text-left">Payment Method</th>
                        <th class="border border-gray-300 p-3 text-left">Processing Time</th>
                        <th class="border border-gray-300 p-3 text-left">Total Timeline</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td class="border border-gray-300 p-3">Credit/Debit Card</td>
                        <td class="border border-gray-300 p-3">3-5 business days</td>
                        <td class="border border-gray-300 p-3">5-10 business days</td>
                      </tr>
                      <tr class="bg-muted/20">
                        <td class="border border-gray-300 p-3">PayPal</td>
                        <td class="border border-gray-300 p-3">1-2 business days</td>
                        <td class="border border-gray-300 p-3">3-7 business days</td>
                      </tr>
                      <tr>
                        <td class="border border-gray-300 p-3">Gift Card</td>
                        <td class="border border-gray-300 p-3">Same day</td>
                        <td class="border border-gray-300 p-3">Instant</td>
                      </tr>
                      <tr class="bg-muted/20">
                        <td class="border border-gray-300 p-3">Store Credit</td>
                        <td class="border border-gray-300 p-3">Same day</td>
                        <td class="border border-gray-300 p-3">Instant</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Refund Amount</h3>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li><strong>Full Purchase Price:</strong> You'll receive a refund for the full amount paid</li>
                  <li><strong>Original Shipping:</strong> Free if return is due to our error, otherwise shipping charges are non-refundable</li>
                  <li><strong>Return Shipping:</strong> Free with our prepaid label</li>
                  <li><strong>Taxes:</strong> All applicable taxes will be refunded</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Special Circumstances</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Damaged or Defective Items</h3>
                <div class="bg-red-50 border border-red-200 p-6 rounded-lg">
                  <p class="mb-3">If you receive a damaged or defective item:</p>
                  <ul class="space-y-2">
                    <li>• <strong>Contact us immediately:</strong> Report within 48 hours of delivery</li>
                    <li>• <strong>Priority processing:</strong> Expedited replacement or refund</li>
                    <li>• <strong>No return required:</strong> Keep the item if it's safe and we'll send a replacement</li>
                    <li>• <strong>Full compensation:</strong> Complete refund including all shipping costs</li>
                  </ul>
                </div>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Wrong Item Received</h3>
                <div class="bg-yellow-50 border border-yellow-200 p-6 rounded-lg">
                  <p class="mb-3">If we sent you the wrong item:</p>
                  <ul class="space-y-2">
                    <li>• <strong>Our mistake, our cost:</strong> Free return shipping and expedited replacement</li>
                    <li>• <strong>Keep or return:</strong> You can keep the wrong item as a courtesy (value under $25)</li>
                    <li>• <strong>Priority shipping:</strong> Correct item shipped via express delivery</li>
                    <li>• <strong>Compensation:</strong> Store credit for the inconvenience</li>
                  </ul>
                </div>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Holiday Returns</h3>
                <p>Extended return policy during holiday seasons:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li><strong>Extended Window:</strong> Items purchased Nov 1 - Dec 31 can be returned until Jan 31</li>
                  <li><strong>Gift Receipts:</strong> Recipients can return gifts without original purchaser information</li>
                  <li><strong>Gift Cards:</strong> Option to issue store credit instead of refund to original payment method</li>
                </ul>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Return Shipping</h2>
                
                <h3 class="text-xl font-medium mt-6 mb-3">Prepaid Shipping Labels</h3>
                <p>We make returns convenient with free shipping:</p>
                <ul class="list-disc pl-6 mt-3 space-y-2">
                  <li><strong>Free Return Labels:</strong> Provided with every return authorization</li>
                  <li><strong>Multiple Carriers:</strong> UPS, FedEx, USPS options available</li>
                  <li><strong>Drop-off Locations:</strong> Over 40,000 locations nationwide</li>
                  <li><strong>Pickup Service:</strong> Schedule pickup from your home or office</li>
                  <li><strong>Tracking Included:</strong> Monitor your return every step of the way</li>
                </ul>
                
                <h3 class="text-xl font-medium mt-6 mb-3">International Returns</h3>
                <div class="bg-muted p-6 rounded-lg">
                  <p class="mb-3">For international customers:</p>
                  <ul class="space-y-2">
                    <li>• <strong>Return shipping:</strong> Calculated based on destination</li>
                    <li>• <strong>Customs duties:</strong> May apply for return shipments</li>
                    <li>• <strong>Processing time:</strong> 10-15 business days for international returns</li>
                    <li>• <strong>Currency conversion:</strong> Refunds processed in original currency</li>
                  </ul>
                </div>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Customer Support</h2>
                
                <p>Our dedicated returns team is here to help make your experience smooth and hassle-free:</p>
                
                <div class="bg-muted p-6 rounded-lg mt-4">
                  <h3 class="text-lg font-medium mb-3">Returns Support Team</h3>
                  <p><strong>Email:</strong> returns@coreldove.com</p>
                  <p><strong>Phone:</strong> 1-800-CORELDOVE (1-800-267-3536)</p>
                  <p><strong>Live Chat:</strong> Available on our website 24/7</p>
                  <p><strong>Response Time:</strong> Same-day response for all return inquiries</p>
                  <p class="mt-3"><strong>Support Hours:</strong> Monday - Friday, 7:00 AM - 10:00 PM EST<br>
                     Saturday - Sunday, 9:00 AM - 8:00 PM EST</p>
                </div>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Tips for Smooth Returns</h2>
                
                <div class="grid md:grid-cols-2 gap-6 mt-6">
                  <div class="bg-green-50 border border-green-200 p-6 rounded-lg">
                    <h3 class="text-lg font-medium mb-3">📦 Packaging Tips</h3>
                    <ul class="text-sm space-y-2">
                      <li>• Use original packaging when possible</li>
                      <li>• Include all accessories and documentation</li>
                      <li>• Pack securely to prevent damage</li>
                      <li>• Include packing slip or RA number</li>
                      <li>• Take photos before shipping</li>
                    </ul>
                  </div>
                  
                  <div class="bg-blue-50 border border-blue-200 p-6 rounded-lg">
                    <h3 class="text-lg font-medium mb-3">⚡ Quick Processing</h3>
                    <ul class="text-sm space-y-2">
                      <li>• Start returns within 30 days</li>
                      <li>• Use online return portal for fastest service</li>
                      <li>• Keep tracking numbers for reference</li>
                      <li>• Monitor email for updates</li>
                      <li>• Contact support with any questions</li>
                    </ul>
                  </div>
                </div>
                
                <p class="text-sm text-muted-foreground mt-8 p-4 bg-muted/50 rounded">
                  <strong>Last Updated:</strong> December 2024<br>
                  Return policy terms are subject to change. Current terms apply to all purchases made after the effective date.
                </p>
              </div>
            `,
            meta: {
              seo_title: 'Returns & Exchanges - CorelDove | 30-Day Satisfaction Guarantee',
              search_description: 'Hassle-free returns and exchanges at CorelDove. 30-day satisfaction guarantee, free return shipping, and dedicated support team. Learn about our comprehensive return policy.'
            }
          },
          {
            id: 5,
            title: 'Help Center',
            slug: 'help',
            content: `
              <div class="help-center">
                <p class="text-lg text-muted-foreground mb-8">Welcome to the CorelDove Help Center! We're here to assist you with any questions or concerns you may have. Browse our comprehensive FAQ section below or contact our support team directly.</p>
                
                <div class="grid md:grid-cols-3 gap-6 mb-8">
                  <div class="bg-blue-50 border border-blue-200 p-6 rounded-lg text-center">
                    <div class="text-4xl mb-3">📞</div>
                    <h3 class="text-lg font-medium mb-2">Phone Support</h3>
                    <p class="text-sm text-muted-foreground mb-3">Speak with our experts</p>
                    <p class="font-medium">1-800-CORELDOVE</p>
                    <p class="text-sm">(1-800-267-3536)</p>
                  </div>
                  
                  <div class="bg-green-50 border border-green-200 p-6 rounded-lg text-center">
                    <div class="text-4xl mb-3">💬</div>
                    <h3 class="text-lg font-medium mb-2">Live Chat</h3>
                    <p class="text-sm text-muted-foreground mb-3">Instant support online</p>
                    <p class="font-medium">Available 24/7</p>
                    <p class="text-sm">Click chat button</p>
                  </div>
                  
                  <div class="bg-purple-50 border border-purple-200 p-6 rounded-lg text-center">
                    <div class="text-4xl mb-3">📧</div>
                    <h3 class="text-lg font-medium mb-2">Email Support</h3>
                    <p class="text-sm text-muted-foreground mb-3">Written assistance</p>
                    <p class="font-medium">support@coreldove.com</p>
                    <p class="text-sm">Response within 2 hours</p>
                  </div>
                </div>
                
                <h2 class="text-2xl font-semibold mt-8 mb-6">Frequently Asked Questions</h2>
                
                <div class="space-y-6">
                  <h3 class="text-xl font-medium mt-6 mb-4">🛒 Ordering & Payment</h3>
                  
                  <div class="border-l-4 border-blue-500 pl-4">
                    <h4 class="font-medium mb-2">How do I place an order?</h4>
                    <p class="text-muted-foreground">Simply browse our products, add items to your cart, and proceed to checkout. You can shop as a guest or create an account for faster future orders and order tracking.</p>
                  </div>
                  
                  <div class="border-l-4 border-blue-500 pl-4">
                    <h4 class="font-medium mb-2">What payment methods do you accept?</h4>
                    <p class="text-muted-foreground">We accept all major credit cards (Visa, MasterCard, American Express, Discover), PayPal, Apple Pay, Google Pay, and digital payment methods. All payments are processed securely with SSL encryption.</p>
                  </div>
                  
                  <div class="border-l-4 border-blue-500 pl-4">
                    <h4 class="font-medium mb-2">Can I modify or cancel my order?</h4>
                    <p class="text-muted-foreground">Orders can be modified or cancelled within 1 hour of placement. After this window, orders enter our fulfillment process. Contact us immediately at 1-800-CORELDOVE if you need to make changes.</p>
                  </div>
                  
                  <div class="border-l-4 border-blue-500 pl-4">
                    <h4 class="font-medium mb-2">Do you offer discounts or promotions?</h4>
                    <p class="text-muted-foreground">Yes! Sign up for our newsletter to receive exclusive offers, seasonal sales notifications, and early access to new products. We also offer bulk discounts for large orders.</p>
                  </div>
                  
                  <h3 class="text-xl font-medium mt-8 mb-4">📦 Shipping & Delivery</h3>
                  
                  <div class="border-l-4 border-green-500 pl-4">
                    <h4 class="font-medium mb-2">How do I track my order?</h4>
                    <p class="text-muted-foreground">Once your order ships, you'll receive a tracking email with your tracking number and direct link to track your package. You can also track orders in your account dashboard under "My Orders".</p>
                  </div>
                  
                  <div class="border-l-4 border-green-500 pl-4">
                    <h4 class="font-medium mb-2">What are your shipping options?</h4>
                    <p class="text-muted-foreground">We offer Standard (3-5 days, FREE over $50), Express (1-2 days, $9.99), and Overnight ($19.99) shipping. International shipping is available to most countries with delivery times varying by location.</p>
                  </div>
                  
                  <div class="border-l-4 border-green-500 pl-4">
                    <h4 class="font-medium mb-2">Do you ship internationally?</h4>
                    <p class="text-muted-foreground">Yes! We ship to over 200 countries worldwide. International shipping costs and delivery times vary by destination. Customers are responsible for any customs duties or taxes.</p>
                  </div>
                  
                  <div class="border-l-4 border-green-500 pl-4">
                    <h4 class="font-medium mb-2">What if my package is lost or damaged?</h4>
                    <p class="text-muted-foreground">All shipments are fully insured. If your package is lost in transit or arrives damaged, contact us immediately. We'll investigate with the carrier and provide a replacement or full refund promptly.</p>
                  </div>
                  
                  <h3 class="text-xl font-medium mt-8 mb-4">🔄 Returns & Exchanges</h3>
                  
                  <div class="border-l-4 border-orange-500 pl-4">
                    <h4 class="font-medium mb-2">What is your return policy?</h4>
                    <p class="text-muted-foreground">We offer a 30-day satisfaction guarantee. Items can be returned in original condition for a full refund. We provide free return shipping labels for most returns within the US.</p>
                  </div>
                  
                  <div class="border-l-4 border-orange-500 pl-4">
                    <h4 class="font-medium mb-2">How do I start a return?</h4>
                    <p class="text-muted-foreground">Log into your account and go to "My Orders" to start a return, or contact our support team. We'll email you a prepaid return label and detailed instructions.</p>
                  </div>
                  
                  <div class="border-l-4 border-orange-500 pl-4">
                    <h4 class="font-medium mb-2">How long do refunds take?</h4>
                    <p class="text-muted-foreground">Refunds are processed within 1-2 business days of receiving your return. Depending on your payment method, it may take 3-7 business days for the refund to appear in your account.</p>
                  </div>
                  
                  <div class="border-l-4 border-orange-500 pl-4">
                    <h4 class="font-medium mb-2">Can I exchange items instead of returning?</h4>
                    <p class="text-muted-foreground">Absolutely! Exchanges are processed faster than returns and refunds. Simply specify the desired replacement item when initiating your return, and we'll send the exchange once we receive your return.</p>
                  </div>
                  
                  <h3 class="text-xl font-medium mt-8 mb-4">👕 Products & Sizing</h3>
                  
                  <div class="border-l-4 border-purple-500 pl-4">
                    <h4 class="font-medium mb-2">Do you offer size guides?</h4>
                    <p class="text-muted-foreground">Yes! Detailed size guides with measurements are available on every product page. Click the "Size Guide" link near the size selection. We also offer virtual fitting tools for select items.</p>
                  </div>
                  
                  <div class="border-l-4 border-purple-500 pl-4">
                    <h4 class="font-medium mb-2">Are your products authentic?</h4>
                    <p class="text-muted-foreground">All products sold on CorelDove are 100% authentic and sourced directly from authorized manufacturers and distributors. We guarantee the authenticity of every item.</p>
                  </div>
                  
                  <div class="border-l-4 border-purple-500 pl-4">
                    <h4 class="font-medium mb-2">How do I care for my products?</h4>
                    <p class="text-muted-foreground">Care instructions are provided with each product and on the product detail pages. For specific care questions, our customer service team can provide detailed guidance.</p>
                  </div>
                  
                  <div class="border-l-4 border-purple-500 pl-4">
                    <h4 class="font-medium mb-2">Do you restock sold-out items?</h4>
                    <p class="text-muted-foreground">We regularly restock popular items. You can sign up for restock notifications on any sold-out product page, and we'll email you when it's available again.</p>
                  </div>
                  
                  <h3 class="text-xl font-medium mt-8 mb-4">👤 Account & Privacy</h3>
                  
                  <div class="border-l-4 border-red-500 pl-4">
                    <h4 class="font-medium mb-2">How do I create an account?</h4>
                    <p class="text-muted-foreground">Click "Sign Up" at the top of any page, or create an account during checkout. Having an account allows you to track orders, save favorites, and checkout faster on future orders.</p>
                  </div>
                  
                  <div class="border-l-4 border-red-500 pl-4">
                    <h4 class="font-medium mb-2">How do I reset my password?</h4>
                    <p class="text-muted-foreground">Click "Forgot Password" on the login page, enter your email address, and we'll send you a secure password reset link. The link is valid for 24 hours.</p>
                  </div>
                  
                  <div class="border-l-4 border-red-500 pl-4">
                    <h4 class="font-medium mb-2">Is my personal information secure?</h4>
                    <p class="text-muted-foreground">Absolutely. We use industry-standard SSL encryption to protect your data, and we never share your personal information with third parties without your consent. Read our full Privacy Policy for details.</p>
                  </div>
                  
                  <div class="border-l-4 border-red-500 pl-4">
                    <h4 class="font-medium mb-2">How do I unsubscribe from emails?</h4>
                    <p class="text-muted-foreground">You can unsubscribe from marketing emails by clicking the unsubscribe link at the bottom of any email, or by updating your email preferences in your account settings.</p>
                  </div>
                </div>
                
                <div class="bg-muted p-8 rounded-lg mt-12">
                  <h2 class="text-2xl font-semibold mb-6">Still Need Help?</h2>
                  
                  <div class="grid md:grid-cols-2 gap-8">
                    <div>
                      <h3 class="text-lg font-medium mb-4">📞 Phone Support</h3>
                      <p class="mb-3"><strong>Toll-Free:</strong> 1-800-CORELDOVE (1-800-267-3536)</p>
                      <p class="mb-3"><strong>International:</strong> +1-555-CORELDOVE (+1-555-267-3536)</p>
                      <p class="text-sm text-muted-foreground">
                        <strong>Hours:</strong><br>
                        Monday - Friday: 6:00 AM - 10:00 PM EST<br>
                        Saturday - Sunday: 8:00 AM - 8:00 PM EST<br>
                        Holiday hours may vary
                      </p>
                    </div>
                    
                    <div>
                      <h3 class="text-lg font-medium mb-4">💬 Digital Support</h3>
                      <p class="mb-3"><strong>Email:</strong> support@coreldove.com</p>
                      <p class="mb-3"><strong>Live Chat:</strong> Available 24/7 on our website</p>
                      <p class="mb-3"><strong>Social Media:</strong> @CorelDove on Twitter, Instagram, Facebook</p>
                      <p class="text-sm text-muted-foreground">
                        <strong>Response Times:</strong><br>
                        Email: Within 2 hours during business hours<br>
                        Live Chat: Immediate<br>
                        Social Media: Within 4 hours
                      </p>
                    </div>
                  </div>
                  
                  <div class="mt-8 p-6 bg-blue-50 border border-blue-200 rounded-lg">
                    <h3 class="text-lg font-medium mb-3">🚨 Urgent Issues</h3>
                    <p class="text-sm">For urgent matters such as fraudulent charges, security concerns, or time-sensitive order issues, please call our priority support line: <strong>1-800-URGENT1</strong> (1-800-874-3681) available 24/7.</p>
                  </div>
                </div>
                
                <div class="text-center mt-12 p-6 bg-gradient-to-r from-red-50 to-pink-50 rounded-lg border border-red-200">
                  <h3 class="text-xl font-medium mb-3">💝 We Value Your Feedback</h3>
                  <p class="text-muted-foreground mb-4">Help us improve by sharing your experience. Your feedback helps us serve you better!</p>
                  <div class="flex gap-4 justify-center">
                    <a href="mailto:feedback@coreldove.com" class="inline-flex items-center px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors">
                      Send Feedback
                    </a>
                    <a href="/survey" class="inline-flex items-center px-4 py-2 border border-red-500 text-red-500 rounded-md hover:bg-red-50 transition-colors">
                      Take Survey
                    </a>
                  </div>
                </div>
              </div>
            `,
            meta: {
              seo_title: 'Help Center - CorelDove | Customer Support & FAQ',
              search_description: 'Get comprehensive help with CorelDove orders, shipping, returns, payments, and account management. 24/7 support via phone, chat, and email with detailed FAQs.'
            }
          },
          {
            id: 6,
            title: 'Refund Policy',
            slug: 'refund',
            content: `
              <div class="refund-policy">
                <p class="text-lg text-muted-foreground mb-8">At CorelDove, we stand behind every purchase with our comprehensive refund policy. Your satisfaction is our priority, and we're committed to making the refund process as smooth and transparent as possible.</p>
                
                <div class="bg-green-50 border border-green-200 p-6 rounded-lg mb-8">
                  <h2 class="text-xl font-medium mb-3">💚 Our Refund Promise</h2>
                  <p class="mb-4">We offer a <strong>30-day satisfaction guarantee</strong> on all purchases. If you're not completely satisfied with your order, we'll make it right with a full refund, no questions asked.</p>
                  <ul class="list-disc pl-6 space-y-1 text-sm">
                    <li>Full refunds processed within 1-2 business days</li>
                    <li>Free return shipping labels provided</li>
                    <li>No restocking fees on standard returns</li>
                    <li>Dedicated refund support team available</li>
                  </ul>
                </div>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Refund Eligibility</h2>
                
                <div class="grid md:grid-cols-2 gap-6 mb-8">
                  <div class="bg-muted p-6 rounded-lg">
                    <h3 class="text-lg font-medium mb-3 text-green-600">✅ Eligible for Full Refund</h3>
                    <ul class="space-y-2 text-sm">
                      <li>• Items in original, unused condition</li>
                      <li>• Original packaging and tags intact</li>
                      <li>• Returned within 30 days of delivery</li>
                      <li>• Standard retail products</li>
                      <li>• Items purchased at full price</li>
                      <li>• Defective or damaged items</li>
                      <li>• Items that don't match description</li>
                    </ul>
                  </div>
                  
                  <div class="bg-muted p-6 rounded-lg">
                    <h3 class="text-lg font-medium mb-3 text-red-600">❌ Non-Refundable Items</h3>
                    <ul class="space-y-2 text-sm">
                      <li>• Personalized or custom-made items</li>
                      <li>• Final sale or clearance items</li>
                      <li>• Digital downloads after access</li>
                      <li>• Intimate apparel and swimwear</li>
                      <li>• Items damaged by normal wear</li>
                      <li>• Gift cards and store credit</li>
                      <li>• Items returned after 30 days</li>
                    </ul>
                  </div>
                </div>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">How to Request a Refund</h2>
                
                <div class="space-y-6">
                  <div class="flex items-start space-x-4">
                    <div class="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-medium text-sm">1</div>
                    <div>
                      <h3 class="text-lg font-medium mb-2">Start Your Refund Request</h3>
                      <p class="text-muted-foreground mb-3">Log into your account and go to "My Orders" or contact our support team directly.</p>
                      <div class="flex gap-2 flex-wrap">
                        <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">Account Dashboard</span>
                        <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">Call 1-800-CORELDOVE</span>
                        <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">Email refunds@coreldove.com</span>
                      </div>
                    </div>
                  </div>
                  
                  <div class="flex items-start space-x-4">
                    <div class="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-medium text-sm">2</div>
                    <div>
                      <h3 class="text-lg font-medium mb-2">Provide Order Information</h3>
                      <p class="text-muted-foreground mb-3">We'll need your order number, reason for return, and preferred refund method.</p>
                      <ul class="list-disc pl-6 text-sm text-muted-foreground space-y-1">
                        <li>Order number (found in confirmation email)</li>
                        <li>Item(s) you wish to return</li>
                        <li>Reason for return (optional but helpful)</li>
                        <li>Photos if item is defective/damaged</li>
                      </ul>
                    </div>
                  </div>
                  
                  <div class="flex items-start space-x-4">
                    <div class="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-medium text-sm">3</div>
                    <div>
                      <h3 class="text-lg font-medium mb-2">Receive Return Label</h3>
                      <p class="text-muted-foreground mb-3">We'll email you a prepaid return shipping label and packaging instructions within 2 hours.</p>
                      <div class="bg-yellow-50 border border-yellow-200 p-3 rounded text-sm">
                        <strong>Pro Tip:</strong> Keep your return tracking number for reference. We'll notify you once we receive your return.
                      </div>
                    </div>
                  </div>
                  
                  <div class="flex items-start space-x-4">
                    <div class="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-medium text-sm">4</div>
                    <div>
                      <h3 class="text-lg font-medium mb-2">Pack and Ship</h3>
                      <p class="text-muted-foreground mb-3">Securely package your item(s) with all original materials and attach the return label.</p>
                      <ul class="list-disc pl-6 text-sm text-muted-foreground space-y-1">
                        <li>Include all original packaging and tags</li>
                        <li>Pack securely to prevent damage in transit</li>
                        <li>Drop off at any shipping location or schedule pickup</li>
                        <li>Keep tracking receipt until refund is processed</li>
                      </ul>
                    </div>
                  </div>
                  
                  <div class="flex items-start space-x-4">
                    <div class="flex-shrink-0 w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center font-medium text-sm">5</div>
                    <div>
                      <h3 class="text-lg font-medium mb-2">Receive Your Refund</h3>
                      <p class="text-muted-foreground">Your refund will be processed within 1-2 business days of receiving your return.</p>
                    </div>
                  </div>
                </div>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Refund Methods & Processing Times</h2>
                
                <div class="overflow-x-auto">
                  <table class="w-full border-collapse border border-gray-300 rounded-lg overflow-hidden">
                    <thead class="bg-muted">
                      <tr>
                        <th class="border border-gray-300 px-4 py-3 text-left font-medium">Payment Method</th>
                        <th class="border border-gray-300 px-4 py-3 text-left font-medium">Refund Method</th>
                        <th class="border border-gray-300 px-4 py-3 text-left font-medium">Processing Time</th>
                        <th class="border border-gray-300 px-4 py-3 text-left font-medium">Notes</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td class="border border-gray-300 px-4 py-3">Credit Card</td>
                        <td class="border border-gray-300 px-4 py-3">Original credit card</td>
                        <td class="border border-gray-300 px-4 py-3">3-5 business days</td>
                        <td class="border border-gray-300 px-4 py-3">May take 1-2 billing cycles to appear</td>
                      </tr>
                      <tr class="bg-muted/50">
                        <td class="border border-gray-300 px-4 py-3">Debit Card</td>
                        <td class="border border-gray-300 px-4 py-3">Original debit card</td>
                        <td class="border border-gray-300 px-4 py-3">3-7 business days</td>
                        <td class="border border-gray-300 px-4 py-3">Depends on your bank's processing</td>
                      </tr>
                      <tr>
                        <td class="border border-gray-300 px-4 py-3">PayPal</td>
                        <td class="border border-gray-300 px-4 py-3">PayPal account</td>
                        <td class="border border-gray-300 px-4 py-3">1-2 business days</td>
                        <td class="border border-gray-300 px-4 py-3">Fastest refund method</td>
                      </tr>
                      <tr class="bg-muted/50">
                        <td class="border border-gray-300 px-4 py-3">Apple Pay / Google Pay</td>
                        <td class="border border-gray-300 px-4 py-3">Original card linked</td>
                        <td class="border border-gray-300 px-4 py-3">3-5 business days</td>
                        <td class="border border-gray-300 px-4 py-3">Same as underlying card method</td>
                      </tr>
                      <tr>
                        <td class="border border-gray-300 px-4 py-3">Bank Transfer</td>
                        <td class="border border-gray-300 px-4 py-3">Original bank account</td>
                        <td class="border border-gray-300 px-4 py-3">5-7 business days</td>
                        <td class="border border-gray-300 px-4 py-3">International transfers may take longer</td>
                      </tr>
                      <tr class="bg-muted/50">
                        <td class="border border-gray-300 px-4 py-3">Store Credit</td>
                        <td class="border border-gray-300 px-4 py-3">CorelDove credit</td>
                        <td class="border border-gray-300 px-4 py-3">Immediate</td>
                        <td class="border border-gray-300 px-4 py-3">110% value, never expires</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">Special Refund Situations</h2>
                
                <div class="space-y-6">
                  <div class="border-l-4 border-red-500 pl-4">
                    <h3 class="text-lg font-medium mb-2">🔧 Defective or Damaged Items</h3>
                    <p class="text-muted-foreground mb-3">If your item arrives defective or damaged, we'll provide an immediate full refund plus shipping costs.</p>
                    <ul class="list-disc pl-6 text-sm text-muted-foreground space-y-1">
                      <li>No return shipping required for defective items</li>
                      <li>Full refund including original shipping costs</li>
                      <li>Optional replacement at no extra cost</li>
                      <li>Expedited processing within 24 hours</li>
                    </ul>
                  </div>
                  
                  <div class="border-l-4 border-blue-500 pl-4">
                    <h3 class="text-lg font-medium mb-2">🚚 Wrong Item Shipped</h3>
                    <p class="text-muted-foreground mb-3">If we sent you the wrong item, we'll cover all costs and provide expedited resolution.</p>
                    <ul class="list-disc pl-6 text-sm text-muted-foreground space-y-1">
                      <li>Keep the wrong item until replacement arrives</li>
                      <li>Free expedited shipping for correct item</li>
                      <li>Prepaid return label for wrong item</li>
                      <li>Full refund if correct item is unavailable</li>
                    </ul>
                  </div>
                  
                  <div class="border-l-4 border-green-500 pl-4">
                    <h3 class="text-lg font-medium mb-2">🎁 Gift Refunds</h3>
                    <p class="text-muted-foreground mb-3">Gift recipients can return items without the original purchaser's involvement.</p>
                    <ul class="list-disc pl-6 text-sm text-muted-foreground space-y-1">
                      <li>Gift receipts enable easy returns</li>
                      <li>Refund issued as store credit or gift card</li>
                      <li>Original purchaser can request cash refund</li>
                      <li>Extended 45-day return window for gifts</li>
                    </ul>
                  </div>
                  
                  <div class="border-l-4 border-purple-500 pl-4">
                    <h3 class="text-lg font-medium mb-2">💳 Card No Longer Valid</h3>
                    <p class="text-muted-foreground mb-3">If your original payment method is no longer valid, we offer alternative refund options.</p>
                    <ul class="list-disc pl-6 text-sm text-muted-foreground space-y-1">
                      <li>Store credit for immediate use</li>
                      <li>Check mailed to billing address</li>
                      <li>Bank transfer to verified account</li>
                      <li>PayPal transfer with verification</li>
                    </ul>
                  </div>
                </div>
                
                <h2 class="text-2xl font-semibold mt-8 mb-4">International Refunds</h2>
                
                <div class="bg-blue-50 border border-blue-200 p-6 rounded-lg">
                  <h3 class="text-lg font-medium mb-3">🌍 Global Refund Support</h3>
                  <p class="mb-4">We provide refunds to customers worldwide with consideration for international shipping and customs.</p>
                  
                  <div class="grid md:grid-cols-2 gap-6">
                    <div>
                      <h4 class="font-medium mb-2">Return Shipping</h4>
                      <ul class="text-sm space-y-1">
                        <li>• Free return labels within US and Canada</li>
                        <li>• International returns: customer pays initial shipping</li>
                        <li>• We reimburse return shipping costs upon receipt</li>
                        <li>• Express return options available</li>
                      </ul>
                    </div>
                    
                    <div>
                      <h4 class="font-medium mb-2">Customs & Duties</h4>
                      <ul class="text-sm space-y-1">
                        <li>• We refund customs duties paid on returned items</li>
                        <li>• Provide customs documentation for returns</li>
                        <li>• Work with local customs offices</li>
                        <li>• Extended processing time for international returns</li>
                      </ul>
                    </div>
                  </div>
                </div>
                
                <div class="bg-muted p-8 rounded-lg mt-12">
                  <h2 class="text-2xl font-semibold mb-6">Refund Support Team</h2>
                  
                  <div class="grid md:grid-cols-3 gap-6">
                    <div class="text-center">
                      <div class="text-4xl mb-3">📞</div>
                      <h3 class="text-lg font-medium mb-2">Phone Support</h3>
                      <p class="text-sm text-muted-foreground mb-3">Dedicated refund specialists</p>
                      <p class="font-medium">1-800-REFUNDS</p>
                      <p class="text-sm">(1-800-733-8637)</p>
                      <p class="text-xs text-muted-foreground mt-2">Monday-Friday: 7 AM - 9 PM EST<br>Saturday-Sunday: 9 AM - 6 PM EST</p>
                    </div>
                    
                    <div class="text-center">
                      <div class="text-4xl mb-3">📧</div>
                      <h3 class="text-lg font-medium mb-2">Email Support</h3>
                      <p class="text-sm text-muted-foreground mb-3">Fast email assistance</p>
                      <p class="font-medium">refunds@coreldove.com</p>
                      <p class="text-sm">Response in 1-2 hours</p>
                      <p class="text-xs text-muted-foreground mt-2">Include order number for faster service</p>
                    </div>
                    
                    <div class="text-center">
                      <div class="text-4xl mb-3">💬</div>
                      <h3 class="text-lg font-medium mb-2">Live Chat</h3>
                      <p class="text-sm text-muted-foreground mb-3">Instant refund assistance</p>
                      <p class="font-medium">Available 24/7</p>
                      <p class="text-sm">Click chat icon</p>
                      <p class="text-xs text-muted-foreground mt-2">Priority queue for refund requests</p>
                    </div>
                  </div>
                  
                  <div class="mt-8 p-6 bg-green-50 border border-green-200 rounded-lg text-center">
                    <h3 class="text-lg font-medium mb-3">💯 Satisfaction Guarantee</h3>
                    <p class="text-sm">Not satisfied with our refund process? Contact our management team at <strong>escalations@coreldove.com</strong> and we'll make it right. Your satisfaction is our commitment.</p>
                  </div>
                </div>
                
                <div class="text-sm text-muted-foreground mt-8 p-4 bg-muted/50 rounded">
                  <strong>Last Updated:</strong> December 2024<br>
                  This Refund Policy is effective as of the date last updated and supersedes all prior refund policies. We reserve the right to update this policy at any time, with changes taking effect immediately upon posting on our website.
                </div>
              </div>
            `,
            meta: {
              seo_title: 'Refund Policy - CorelDove | 30-Day Money Back Guarantee',
              search_description: 'Comprehensive refund policy with 30-day satisfaction guarantee, fast processing, multiple refund methods, and dedicated support team. Easy returns and full refunds at CorelDove.'
            }
          }
        ]
      }
      
      if (slug) {
        const page = fallbackPages.items.find(p => p.slug === slug)
        return NextResponse.json({
          meta: { total_count: page ? 1 : 0 },
          items: page ? [page] : []
        })
      }
      
      return NextResponse.json(fallbackPages)
    }
  } catch (error) {
    console.error('Error in Wagtail pages API:', error)
    return NextResponse.json(
      { error: 'Failed to fetch page content' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Forward to Wagtail CMS via Brain API for page creation/updates
    const response = await fetch(`${BRAIN_API_URL}/api/brain/wagtail/api/v2/pages/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3012',
      },
      body: JSON.stringify(body)
    })

    if (response.ok) {
      const data = await response.json()
      return NextResponse.json(data)
    } else {
      const error = await response.text()
      return NextResponse.json(
        { error: 'Failed to create/update page', details: error },
        { status: response.status }
      )
    }
  } catch (error) {
    console.error('Error creating/updating page:', error)
    return NextResponse.json(
      { error: 'Failed to create/update page' },
      { status: 500 }
    )
  }
}