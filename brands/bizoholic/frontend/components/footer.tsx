"use client"

import Link from "next/link";
import Image from "next/image";
import { Bot } from "lucide-react";
import { usePlatform } from "@/lib/platform-config";
import { useNavigation } from "@/hooks/use-navigation";

export function Footer() {
  const { platform, config } = usePlatform();
  const { services, loading } = useNavigation();

  return (
    <footer className="border-t bg-muted/30">
      <div className="container py-12">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <Image
                src={config.logo}
                alt={`${config.name} Logo`}
                width={120}
                height={40}
                className="h-10 w-auto"
                quality={100}
                style={{ objectFit: 'contain' }}
              />
            </div>
            <p className="text-sm text-muted-foreground mb-4">
              {config.description} - revolutionizing businesses with cutting-edge technology and autonomous solutions.
            </p>
            <p className="text-xs text-muted-foreground">
              Powered by AI-first principles
            </p>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Agency Services</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              {loading ? (
                <li>Loading...</li>
              ) : services.length > 0 ? (
                services.slice(0, 5).map((service, index) => (
                  <li key={index}>
                    <Link href={service.href} className="hover:text-foreground transition-colors">
                      {service.title}
                    </Link>
                  </li>
                ))
              ) : (
                <>
                  <li><Link href="/services" className="hover:text-foreground transition-colors">Digital Marketing</Link></li>
                  <li><Link href="/services" className="hover:text-foreground transition-colors">Business Strategy</Link></li>
                  <li><Link href="/services" className="hover:text-foreground transition-colors">AI Consulting</Link></li>
                  <li><Link href="/services" className="hover:text-foreground transition-colors">Campaign Management</Link></li>
                </>
              )}
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-4">BizoSaaS Platform</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link href="/bizosaas" className="hover:text-foreground transition-colors">Platform Overview</Link></li>
              <li><Link href="http://localhost:3003/register" className="hover:text-foreground transition-colors">Start Free Trial</Link></li>
              <li><Link href="/demo" className="hover:text-foreground transition-colors">Request Demo</Link></li>
              <li><Link href="/pricing" className="hover:text-foreground transition-colors">Pricing</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Company</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link href="/about" className="hover:text-foreground transition-colors">About Us</Link></li>
              <li><Link href="/blog" className="hover:text-foreground transition-colors">Blog</Link></li>
              <li><Link href="/contact" className="hover:text-foreground transition-colors">Contact</Link></li>
              <li><Link href="/careers" className="hover:text-foreground transition-colors">Careers</Link></li>
            </ul>
          </div>
        </div>

        <div className="border-t mt-12 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-muted-foreground">
              &copy; 2025 {config.name}. All rights reserved. Built with AI-first principles.
            </p>
            <div className="flex items-center gap-6 text-sm text-muted-foreground">
              <Link href="/privacy" className="hover:text-foreground transition-colors">Privacy Policy</Link>
              <Link href="/terms" className="hover:text-foreground transition-colors">Terms of Service</Link>
              <Link href="/status" className="hover:text-foreground transition-colors">Status</Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}