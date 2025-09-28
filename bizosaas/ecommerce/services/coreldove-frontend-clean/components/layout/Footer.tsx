'use client'

import Link from 'next/link'
import Image from 'next/image'
import { 
  Facebook, 
  Twitter, 
  Instagram, 
  Youtube, 
  Mail,
  Phone,
  MapPin,
  CreditCard,
  Truck,
  Shield,
  Headphones
} from 'lucide-react'

export default function Footer() {
  const footerLinks = {
    shop: [
      { name: 'All Products', href: '/catalog' },
      { name: 'Categories', href: '/categories' },
      { name: 'New Arrivals', href: '/catalog?sort=newest' },
      { name: 'Best Sellers', href: '/catalog?sort=popular' },
      { name: 'Sale Items', href: '/catalog?filter=sale' },
    ],
    support: [
      { name: 'Contact Us', href: '/contact' },
      { name: 'FAQ', href: '/faq' },
      { name: 'Shipping Info', href: '/shipping' },
      { name: 'Returns', href: '/returns' },
      { name: 'Size Guide', href: '/size-guide' },
    ],
    company: [
      { name: 'About Us', href: '/about' },
      { name: 'Careers', href: '/careers' },
      { name: 'Press', href: '/press' },
      { name: 'AI Technology', href: '/ai-technology' },
      { name: 'Affiliate Program', href: '/affiliate' },
    ],
    legal: [
      { name: 'Privacy Policy', href: '/privacy' },
      { name: 'Terms of Service', href: '/terms' },
      { name: 'Cookie Policy', href: '/cookies' },
      { name: 'GDPR', href: '/gdpr' },
      { name: 'Accessibility', href: '/accessibility' },
    ]
  }

  const socialLinks = [
    { name: 'Facebook', icon: Facebook, href: 'https://facebook.com/coreldove' },
    { name: 'Twitter', icon: Twitter, href: 'https://twitter.com/coreldove' },
    { name: 'Instagram', icon: Instagram, href: 'https://instagram.com/coreldove' },
    { name: 'YouTube', icon: Youtube, href: 'https://youtube.com/coreldove' },
  ]

  const features = [
    {
      icon: Truck,
      title: 'Free Shipping',
      description: 'On orders over $50'
    },
    {
      icon: Shield,
      title: 'Secure Payment',
      description: 'SSL encrypted checkout'
    },
    {
      icon: Headphones,
      title: '24/7 Support',
      description: 'Always here to help'
    },
    {
      icon: CreditCard,
      title: 'Easy Returns',
      description: '30-day return policy'
    }
  ]

  return (
    <footer className="bg-gray-900 text-white">
      {/* Features Bar */}
      <div className="border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {features.map((feature) => (
              <div key={feature.title} className="flex items-center space-x-3">
                <div className="flex-shrink-0">
                  <feature.icon className="h-6 w-6 text-coreldove-red" />
                </div>
                <div>
                  <div className="font-semibold text-sm">{feature.title}</div>
                  <div className="text-gray-400 text-xs">{feature.description}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Main Footer */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-8">
          {/* Brand Column */}
          <div className="lg:col-span-2">
            <Link href="/" className="flex items-center mb-4">
              <Image
                src="/coreldove-logo-white.png"
                alt="CoreLDove"
                width={150}
                height={60}
                className="h-12 w-auto"
              />
            </Link>
            <p className="text-gray-400 mb-4 max-w-sm">
              AI-powered e-commerce platform delivering premium products with intelligent curation and exceptional customer service.
            </p>
            
            {/* Contact Info */}
            <div className="space-y-2 text-sm text-gray-400">
              <div className="flex items-center space-x-2">
                <Mail className="h-4 w-4" />
                <span>support@coreldove.com</span>
              </div>
              <div className="flex items-center space-x-2">
                <Phone className="h-4 w-4" />
                <span>1-800-CORELDOVE</span>
              </div>
              <div className="flex items-center space-x-2">
                <MapPin className="h-4 w-4" />
                <span>San Francisco, CA</span>
              </div>
            </div>

            {/* Social Links */}
            <div className="flex space-x-4 mt-6">
              {socialLinks.map((social) => (
                <a
                  key={social.name}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-coreldove-red transition-colors"
                >
                  <social.icon className="h-5 w-5" />
                </a>
              ))}
            </div>
          </div>

          {/* Shop Links */}
          <div>
            <h3 className="font-semibold mb-4">Shop</h3>
            <ul className="space-y-2">
              {footerLinks.shop.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-gray-400 hover:text-white text-sm transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Support Links */}
          <div>
            <h3 className="font-semibold mb-4">Support</h3>
            <ul className="space-y-2">
              {footerLinks.support.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-gray-400 hover:text-white text-sm transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company Links */}
          <div>
            <h3 className="font-semibold mb-4">Company</h3>
            <ul className="space-y-2">
              {footerLinks.company.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-gray-400 hover:text-white text-sm transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal Links */}
          <div>
            <h3 className="font-semibold mb-4">Legal</h3>
            <ul className="space-y-2">
              {footerLinks.legal.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-gray-400 hover:text-white text-sm transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Newsletter Signup */}
      <div className="border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="mb-4 md:mb-0">
              <h3 className="font-semibold mb-2">Stay Updated</h3>
              <p className="text-gray-400 text-sm">Get the latest products and AI insights delivered to your inbox.</p>
            </div>
            <form className="flex w-full md:w-auto">
              <input
                type="email"
                placeholder="Enter your email"
                className="px-4 py-2 bg-gray-800 border border-gray-700 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-coreldove-red focus:border-transparent w-full md:w-64"
              />
              <button
                type="submit"
                className="px-6 py-2 bg-coreldove-red hover:bg-red-700 rounded-r-lg font-semibold transition-colors"
              >
                Subscribe
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between text-sm text-gray-400">
            <div className="mb-4 md:mb-0">
              © 2024 CoreLDove Inc. All rights reserved. | Powered by AI & Saleor
            </div>
            <div className="flex items-center space-x-4">
              <span>Payment Methods:</span>
              <div className="flex space-x-2">
                <div className="w-8 h-5 bg-gray-700 rounded flex items-center justify-center text-xs">
                  💳
                </div>
                <div className="w-8 h-5 bg-gray-700 rounded flex items-center justify-center text-xs">
                  🏦
                </div>
                <div className="w-8 h-5 bg-gray-700 rounded flex items-center justify-center text-xs">
                  💰
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}