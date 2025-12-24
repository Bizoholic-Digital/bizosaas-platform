'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Eye, EyeOff, Mail, Lock, User, Building, ArrowRight } from 'lucide-react'

export default function SignupPage() {
    const router = useRouter()
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: '',
        companyName: '',
        agreeToTerms: false,
    })
    const [showPassword, setShowPassword] = useState(false)
    const [showConfirmPassword, setShowConfirmPassword] = useState(false)
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [success, setSuccess] = useState(false)

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value, type, checked } = e.target
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }))
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError(null)

        // Validation
        if (!formData.firstName || !formData.lastName || !formData.email || !formData.password) {
            setError('Please fill in all required fields')
            return
        }

        if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match')
            return
        }

        if (formData.password.length < 8) {
            setError('Password must be at least 8 characters long')
            return
        }

        if (!formData.agreeToTerms) {
            setError('You must agree to the Terms of Service and Privacy Policy')
            return
        }

        setIsLoading(true)

        try {
            const response = await fetch('/api/auth/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    firstName: formData.firstName,
                    lastName: formData.lastName,
                    email: formData.email,
                    password: formData.password,
                    companyName: formData.companyName,
                }),
            })

            const data = await response.json()

            if (!response.ok) {
                throw new Error(data.error || 'Signup failed')
            }

            setSuccess(true)
            setTimeout(() => {
                router.push('/login?message=Account created successfully. Please sign in.')
            }, 2000)
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Signup failed. Please try again.')
        } finally {
            setIsLoading(false)
        }
    }

    if (success) {
        return (
            <div className=\"min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950\">
                < div className =\"max-w-md w-full mx-4\">
                    < div className =\"bg-white dark:bg-gray-900 rounded-2xl shadow-2xl p-8 text-center space-y-4 border border-gray-200 dark:border-gray-800\">
                        < div className =\"w-16 h-16 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center mx-auto\">
                            < svg className =\"w-8 h-8 text-green-600 dark:text-green-400\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\">
                                < path strokeLinecap =\"round\" strokeLinejoin=\"round\" strokeWidth={2} d=\"M5 13l4 4L19 7\" />
                            </svg >
                        </div >
            <h2 className=\"text-2xl font-bold text-gray-900 dark:text-white\">Account Created!</h2>
                < p className =\"text-gray-600 dark:text-gray-400\">
                            Your account has been created successfully.Redirecting to login...
                        </p >
                    </div >
                </div >
            </div >
        )
    }

    return (
        <div className=\"min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950 py-12\">
            < div className =\"max-w-md w-full mx-4\">
                < div className =\"bg-white dark:bg-gray-900 rounded-2xl shadow-2xl p-8 space-y-6 border border-gray-200 dark:border-gray-800\">
    {/* Header */ }
    <div className=\"text-center space-y-2\">
        < h2 className =\"text-3xl font-bold text-gray-900 dark:text-white\">
                            Create Account
                        </h2 >
        <p className=\"text-sm text-gray-600 dark:text-gray-400\">
                            Join BizOSaaS and start building
                        </p >
                    </div >

        {/* Error Message */ }
    {
        error && (
            <div className=\"bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4\">
                < p className =\"text-sm text-red-700 dark:text-red-400\">{error}</p>
                        </div >
                    )
    }

    {/* Signup Form */ }
    <form onSubmit={handleSubmit} className=\"space-y-4\">
    {/* Name Fields */ }
    <div className=\"grid grid-cols-2 gap-4\">
        < div className =\"space-y-2\">
            < label htmlFor =\"firstName\" className=\"text-sm font-medium text-gray-700 dark:text-gray-300\">
                                    First Name *
                                </label >
        <div className=\"relative\">
            < User className =\"absolute left-3 top-3 h-4 w-4 text-gray-400\" />
                < input
    id =\"firstName\"
    name =\"firstName\"
    type =\"text\"
    required
    value = { formData.firstName }
    onChange = { handleChange }
    className =\"w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-800 dark:text-white\"
    placeholder =\"John\"
        />
                                </div >
                            </div >
        <div className=\"space-y-2\">
            < label htmlFor =\"lastName\" className=\"text-sm font-medium text-gray-700 dark:text-gray-300\">
                                    Last Name *
                                </label >
        <div className=\"relative\">
            < User className =\"absolute left-3 top-3 h-4 w-4 text-gray-400\" />
                < input
    id =\"lastName\"
    name =\"lastName\"
    type =\"text\"
    required
    value = { formData.lastName }
    onChange = { handleChange }
    className =\"w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-800 dark:text-white\"
    placeholder =\"Doe\"
        />
                                </div >
                            </div >
                        </div >

        {/* Email */ }
        < div className =\"space-y-2\">
            < label htmlFor =\"email\" className=\"text-sm font-medium text-gray-700 dark:text-gray-300\">
                                Email Address *
                            </label >
        <div className=\"relative\">
            < Mail className =\"absolute left-3 top-3 h-4 w-4 text-gray-400\" />
                < input
    id =\"email\"
    name =\"email\"
    type =\"email\"
    required
    value = { formData.email }
    onChange = { handleChange }
    className =\"w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-800 dark:text-white\"
    placeholder =\"john@example.com\"
        />
                            </div >
                        </div >

        {/* Company Name (Optional) */ }
        < div className =\"space-y-2\">
            < label htmlFor =\"companyName\" className=\"text-sm font-medium text-gray-700 dark:text-gray-300\">
                                Company Name(Optional)
                            </label >
        <div className=\"relative\">
            < Building className =\"absolute left-3 top-3 h-4 w-4 text-gray-400\" />
                < input
    id =\"companyName\"
    name =\"companyName\"
    type =\"text\"
    value = { formData.companyName }
    onChange = { handleChange }
    className =\"w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-800 dark:text-white\"
    placeholder =\"Acme Inc.\"
        />
                            </div >
                        </div >

        {/* Password */ }
        < div className =\"space-y-2\">
            < label htmlFor =\"password\" className=\"text-sm font-medium text-gray-700 dark:text-gray-300\">
    Password *
                            </label >
        <div className=\"relative\">
            < Lock className =\"absolute left-3 top-3 h-4 w-4 text-gray-400\" />
                < input
    id =\"password\"
    name =\"password\"
    type = { showPassword? 'text': 'password' }
    required
    value = { formData.password }
    onChange = { handleChange }
    className =\"w-full pl-10 pr-12 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-800 dark:text-white\"
    placeholder =\"••••••••\"
        />
        <button
            type=\"button\"
    onClick = {() => setShowPassword(!showPassword)
}
className =\"absolute right-3 top-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300\"
    >
{
    showPassword?<EyeOff className =\"h-4 w-4\" /> : <Eye className=\"h-4 w-4\" />}
                                </button>
                            </div >
    <p className=\"text-xs text-gray-500\">Minimum 8 characters</p>
                        </div >

    {/* Confirm Password */ }
    < div className =\"space-y-2\">
        < label htmlFor =\"confirmPassword\" className=\"text-sm font-medium text-gray-700 dark:text-gray-300\">
                                Confirm Password *
                            </label >
    <div className=\"relative\">
        < Lock className =\"absolute left-3 top-3 h-4 w-4 text-gray-400\" />
            < input
id =\"confirmPassword\"
name =\"confirmPassword\"
type = { showConfirmPassword? 'text': 'password' }
required
value = { formData.confirmPassword }
onChange = { handleChange }
className =\"w-full pl-10 pr-12 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-800 dark:text-white\"
placeholder =\"••••••••\"
    />
    <button
        type=\"button\"
onClick = {() => setShowConfirmPassword(!showConfirmPassword)}
className =\"absolute right-3 top-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300\"
    >
{
    showConfirmPassword?<EyeOff className =\"h-4 w-4\" /> : <Eye className=\"h-4 w-4\" />}
                                </button>
                            </div >
                        </div >

    {/* Terms Checkbox */ }
    < div className =\"flex items-start space-x-2\">
        < input
id =\"agreeToTerms\"
name =\"agreeToTerms\"
type =\"checkbox\"
checked = { formData.agreeToTerms }
onChange = { handleChange }
className =\"mt-1 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500\"
    />
    <label htmlFor=\"agreeToTerms\" className=\"text-sm text-gray-600 dark:text-gray-400\">
                                I agree to the{ ' ' }
<a href=\"/terms\" className=\"text-blue-600 dark:text-blue-400 hover:underline\">
                                    Terms of Service
                                </a > { ' '}
                                and{ ' ' }
<a href=\"/privacy\" className=\"text-blue-600 dark:text-blue-400 hover:underline\">
                                    Privacy Policy
                                </a >
                            </label >
                        </div >

    {/* Submit Button */ }
    < button
type =\"submit\"
className =\"w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center\"
disabled = { isLoading }
    >
{
    isLoading?(
                                <>
    <div className=\"h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent mr-2\" />
                                    Creating Account...
                                </>
                            ) : (
    <>
        Create Account
        <ArrowRight className=\"ml-2 h-4 w-4\" />
    </>
)}
                        </button >
                    </form >

    {/* Footer */ }
    < div className =\"pt-4 border-t border-gray-200 dark:border-gray-800 text-center\">
        < p className =\"text-sm text-gray-600 dark:text-gray-400\">
                            Already have an account ? { ' '}
    < a href =\"/login\" className=\"text-blue-600 dark:text-blue-400 hover:underline font-semibold\">
                                Sign In
                            </a >
                        </p >
                    </div >
                </div >
            </div >
        </div >
    )
}
