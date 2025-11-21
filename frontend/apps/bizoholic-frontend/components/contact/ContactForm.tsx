'use client'

import { useState } from 'react'
import { ArrowRight, Bot, Clock, CheckCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { useToast } from '@/hooks/use-toast'

interface ContactFormData {
  firstName: string
  lastName: string
  email: string
  company: string
  phone: string
  message: string
}

interface ContactFormProps {
  className?: string
}

export function ContactForm({ className }: ContactFormProps) {
  const [formData, setFormData] = useState<ContactFormData>({
    firstName: '',
    lastName: '',
    email: '',
    company: '',
    phone: '',
    message: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const { toast } = useToast()

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!formData.firstName || !formData.lastName || !formData.email || !formData.message) {
      toast({
        title: 'Missing Information',
        description: 'Please fill in all required fields.',
        variant: 'destructive',
      })
      return
    }

    setIsSubmitting(true)

    try {
      // Submit to CRM/AI agent endpoint
      const response = await fetch('/api/contact/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          timestamp: new Date().toISOString(),
          source: 'contact-form',
          utm_source: typeof window !== 'undefined' ? window.location.search : '',
        }),
      })

      if (response.ok) {
        const result = await response.json()
        
        toast({
          title: 'Message Sent Successfully!',
          description: 'Our AI marketing experts will review your inquiry and respond within 24 hours.',
        })
        
        setIsSubmitted(true)
        
        // Reset form
        setFormData({
          firstName: '',
          lastName: '',
          email: '',
          company: '',
          phone: '',
          message: ''
        })
      } else {
        throw new Error('Failed to submit form')
      }
    } catch (error) {
      console.error('Contact form error:', error)
      
      // Fallback: Try to send via email or store locally
      try {
        // Store in localStorage as backup
        const leads = JSON.parse(localStorage.getItem('contact_leads') || '[]')
        leads.push({
          ...formData,
          timestamp: new Date().toISOString(),
          id: Date.now().toString(),
        })
        localStorage.setItem('contact_leads', JSON.stringify(leads))
        
        toast({
          title: 'Message Received',
          description: 'Your message has been saved. We\'ll contact you within 24 hours.',
        })
        
        setIsSubmitted(true)
      } catch (backupError) {
        toast({
          title: 'Submission Failed',
          description: 'There was an issue submitting your form. Please try again or contact us directly.',
          variant: 'destructive',
        })
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isSubmitted) {
    return (
      <Card className={className}>
        <CardContent className="text-center py-12">
          <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-6" />
          <h3 className="text-2xl font-bold mb-4">Thank You!</h3>
          <p className="text-muted-foreground mb-6">
            Your message has been submitted successfully. Our AI marketing experts 
            will analyze your inquiry and respond with personalized recommendations within 24 hours.
          </p>
          <Button 
            onClick={() => setIsSubmitted(false)}
            variant="outline"
          >
            Send Another Message
          </Button>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className={className}>
      <div className="mb-8">
        <h2 className="text-3xl md:text-4xl font-bold mb-6">
          Send us a <span className="text-primary">Message</span>
        </h2>
        <p className="text-lg text-muted-foreground mb-8">
          Not sure which consultation type is right for you? Send us a message 
          and we'll recommend the best approach for your specific needs.
        </p>
        
        <div className="space-y-6">
          <div className="flex items-start gap-4">
            <Bot className="h-6 w-6 text-primary mt-1" />
            <div>
              <h3 className="font-semibold mb-2">AI-Powered Response</h3>
              <p className="text-muted-foreground">
                Our AI assistant will analyze your message and connect you 
                with the right expert within 24 hours.
              </p>
            </div>
          </div>
          
          <div className="flex items-start gap-4">
            <Clock className="h-6 w-6 text-primary mt-1" />
            <div>
              <h3 className="font-semibold mb-2">Quick Response</h3>
              <p className="text-muted-foreground">
                Most inquiries receive a personalized response within 4 business hours.
              </p>
            </div>
          </div>
        </div>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle>Contact Form</CardTitle>
          <CardDescription>
            Tell us about your business and marketing challenges
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <Input 
                name="firstName"
                placeholder="First Name *" 
                value={formData.firstName}
                onChange={handleInputChange}
                required
                disabled={isSubmitting}
              />
              <Input 
                name="lastName"
                placeholder="Last Name *" 
                value={formData.lastName}
                onChange={handleInputChange}
                required
                disabled={isSubmitting}
              />
            </div>
            <Input 
              name="email"
              type="email" 
              placeholder="Email Address *" 
              value={formData.email}
              onChange={handleInputChange}
              required
              disabled={isSubmitting}
            />
            <Input 
              name="company"
              placeholder="Company Name" 
              value={formData.company}
              onChange={handleInputChange}
              disabled={isSubmitting}
            />
            <Input 
              name="phone"
              placeholder="Phone Number (Optional)" 
              value={formData.phone}
              onChange={handleInputChange}
              disabled={isSubmitting}
            />
            <Textarea 
              name="message"
              placeholder="Tell us about your business and marketing goals... *" 
              rows={4}
              value={formData.message}
              onChange={handleInputChange}
              required
              disabled={isSubmitting}
            />
            <Button 
              type="submit" 
              className="w-full" 
              size="lg" 
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-background border-t-transparent mr-2" />
                  Sending Message...
                </>
              ) : (
                <>
                  Send Message
                  <ArrowRight className="ml-2 h-4 w-4" />
                </>
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}