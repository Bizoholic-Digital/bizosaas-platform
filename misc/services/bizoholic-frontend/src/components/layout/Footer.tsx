'use client'

import Link from 'next/link'
import Image from 'next/image'
import { Mail, Phone, MapPin } from 'lucide-react'

export default function Footer() {
  const navigation = {
    services: [
      { name: 'SEO Optimization', href: '/services/seo-optimization' },
      { name: 'PPC Management', href: '/services/ppc-management' },
      { name: 'Social Media Marketing', href: '/services/social-media' },
      { name: 'Content Marketing', href: '/services/content-marketing' },
    ],
    company: [
      { name: 'About Us', href: '/about' },
      { name: 'Contact', href: '/contact' },
      { name: 'Careers', href: '/careers' },
      { name: 'Blog', href: '/blog' },
    ],
    support: [
      { name: 'Help Center', href: '/support' },
      { name: 'Documentation', href: '/docs' },
      { name: 'Client Portal', href: 'http://localhost:3005' },
      { name: 'Status Page', href: '/status' },
    ],
    legal: [
      { name: 'Privacy Policy', href: '/privacy' },
      { name: 'Terms of Service', href: '/terms' },
      { name: 'Cookie Policy', href: '/cookies' },
    ],
  }

  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="container py-12">
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
          {/* Company info */}
          <div className="lg:col-span-2">
            <Link href="/" className="inline-block mb-6">
              <Image
                src="/Bizoholic_Digital_-_Color-transparent.png"
                alt="Bizoholic"
                width={150}
                height={40}
                className="h-10 w-auto filter brightness-0 invert"
              />
            </Link>
            <p className="text-gray-400 mb-6 max-w-md">
              Transform your marketing with AI automation. Get 75% cost savings, 
              ROI within 7 days, and setup in 15 minutes.
            </p>
            
            {/* Contact info */}
            <div className="space-y-3">
              <div className="flex items-center">
                <Mail className="h-5 w-5 mr-3 text-primary-400" />
                <span>hello@bizoholic.com</span>
              </div>
              <div className="flex items-center">
                <Phone className="h-5 w-5 mr-3 text-primary-400" />
                <span>+1 (555) 123-4567</span>
              </div>
              <div className="flex items-center">
                <MapPin className="h-5 w-5 mr-3 text-primary-400" />
                <span>San Francisco, CA</span>
              </div>
            </div>
          </div>

          {/* Navigation links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Services</h3>
            <ul className="space-y-3">
              {navigation.services.map((item) => (
                <li key={item.name}>
                  <Link 
                    href={item.href}
                    className="hover:text-primary-400 transition-colors"
                  >
                    {item.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-4">Company</h3>
            <ul className="space-y-3">
              {navigation.company.map((item) => (
                <li key={item.name}>
                  <Link 
                    href={item.href}
                    className="hover:text-primary-400 transition-colors"
                  >
                    {item.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-4">Support</h3>
            <ul className="space-y-3">
              {navigation.support.map((item) => (
                <li key={item.name}>
                  <Link 
                    href={item.href}
                    className="hover:text-primary-400 transition-colors"
                    {...(item.name === 'Client Portal' ? { target: '_blank', rel: 'noopener noreferrer' } : {})}
                  >
                    {item.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom section */}
        <div className="border-t border-gray-800 mt-12 pt-8">
          <div className="flex flex-col lg:flex-row justify-between items-center">
            <div className="text-gray-400 text-sm mb-4 lg:mb-0">
              © {new Date().getFullYear()} Bizoholic. All rights reserved.
            </div>
            <div className="flex space-x-6">
              {navigation.legal.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="text-gray-400 hover:text-primary-400 text-sm transition-colors"
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}