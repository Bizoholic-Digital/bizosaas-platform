import React from 'react'
import Link from 'next/link'
import { 
  Facebook, 
  Twitter, 
  Instagram, 
  Linkedin, 
  Youtube,
  MapPin,
  Phone,
  Mail,
  Clock
} from 'lucide-react'

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white">
      {/* Main footer content */}
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-bizbook-primary text-white rounded-lg flex items-center justify-center font-bold">
                B
              </div>
              <div>
                <h2 className="text-xl font-bold">BizBook</h2>
                <p className="text-sm text-gray-400">Business Directory</p>
              </div>
            </div>
            <p className="text-gray-400 text-sm">
              Your trusted local business directory. Discover, connect, and grow with 
              businesses in your community.
            </p>
            <div className="flex space-x-4">
              <Link href="#" className="text-gray-400 hover:text-bizbook-secondary transition-colors">
                <Facebook className="w-5 h-5" />
              </Link>
              <Link href="#" className="text-gray-400 hover:text-bizbook-secondary transition-colors">
                <Twitter className="w-5 h-5" />
              </Link>
              <Link href="#" className="text-gray-400 hover:text-bizbook-secondary transition-colors">
                <Instagram className="w-5 h-5" />
              </Link>
              <Link href="#" className="text-gray-400 hover:text-bizbook-secondary transition-colors">
                <Linkedin className="w-5 h-5" />
              </Link>
              <Link href="#" className="text-gray-400 hover:text-bizbook-secondary transition-colors">
                <Youtube className="w-5 h-5" />
              </Link>
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/" className="text-gray-400 hover:text-white transition-colors">Home</Link></li>
              <li><Link href="/search" className="text-gray-400 hover:text-white transition-colors">Search Businesses</Link></li>
              <li><Link href="/categories" className="text-gray-400 hover:text-white transition-colors">Categories</Link></li>
              <li><Link href="/events" className="text-gray-400 hover:text-white transition-colors">Events</Link></li>
              <li><Link href="/products" className="text-gray-400 hover:text-white transition-colors">Products</Link></li>
              <li><Link href="/coupons" className="text-gray-400 hover:text-white transition-colors">Deals & Coupons</Link></li>
              <li><Link href="/blog" className="text-gray-400 hover:text-white transition-colors">Blog</Link></li>
              <li><Link href="/community" className="text-gray-400 hover:text-white transition-colors">Community</Link></li>
            </ul>
          </div>

          {/* Business Services */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">For Businesses</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/add-business" className="text-gray-400 hover:text-white transition-colors">Add Your Business</Link></li>
              <li><Link href="/claim-business" className="text-gray-400 hover:text-white transition-colors">Claim Your Business</Link></li>
              <li><Link href="/business-login" className="text-gray-400 hover:text-white transition-colors">Business Login</Link></li>
              <li><Link href="/premium" className="text-gray-400 hover:text-white transition-colors">Premium Listings</Link></li>
              <li><Link href="/advertising" className="text-gray-400 hover:text-white transition-colors">Advertising</Link></li>
              <li><Link href="/analytics" className="text-gray-400 hover:text-white transition-colors">Business Analytics</Link></li>
              <li><Link href="/api" className="text-gray-400 hover:text-white transition-colors">API Access</Link></li>
            </ul>
          </div>

          {/* Contact Info */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Contact Us</h3>
            <div className="space-y-3 text-sm">
              <div className="flex items-start space-x-2">
                <MapPin className="w-4 h-4 mt-0.5 text-bizbook-secondary flex-shrink-0" />
                <div>
                  <p className="text-gray-400">123 Business Street</p>
                  <p className="text-gray-400">Suite 456</p>
                  <p className="text-gray-400">City, State 12345</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <Phone className="w-4 h-4 text-bizbook-secondary" />
                <p className="text-gray-400">+1 (555) 123-4567</p>
              </div>
              <div className="flex items-center space-x-2">
                <Mail className="w-4 h-4 text-bizbook-secondary" />
                <p className="text-gray-400">info@bizbook.com</p>
              </div>
              <div className="flex items-start space-x-2">
                <Clock className="w-4 h-4 mt-0.5 text-bizbook-secondary flex-shrink-0" />
                <div>
                  <p className="text-gray-400">Mon - Fri: 9:00 AM - 6:00 PM</p>
                  <p className="text-gray-400">Sat: 10:00 AM - 4:00 PM</p>
                  <p className="text-gray-400">Sun: Closed</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom bar */}
      <div className="border-t border-gray-800">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="text-sm text-gray-400">
              © 2024 BizBook Business Directory. All rights reserved.
            </div>
            <div className="flex space-x-6 text-sm">
              <Link href="/privacy" className="text-gray-400 hover:text-white transition-colors">
                Privacy Policy
              </Link>
              <Link href="/terms" className="text-gray-400 hover:text-white transition-colors">
                Terms of Service
              </Link>
              <Link href="/support" className="text-gray-400 hover:text-white transition-colors">
                Support
              </Link>
              <Link href="/sitemap" className="text-gray-400 hover:text-white transition-colors">
                Sitemap
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer