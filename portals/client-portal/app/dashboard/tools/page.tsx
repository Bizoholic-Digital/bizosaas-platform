import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ExternalLink } from "lucide-react"

const recommendedTools = [
    {
        category: "Email Marketing",
        tools: [
            {
                name: "Mailchimp",
                description: "All-in-one marketing platform for small business.",
                link: "https://mailchimp.com", // Placeholder for affiliate link
                recommended: true
            },
            {
                name: "ConvertKit",
                description: "The go-to marketing hub for creators.",
                link: "https://convertkit.com", // Placeholder for affiliate link
                recommended: false
            }
        ]
    },
    {
        category: "SEO & Analytics",
        tools: [
            {
                name: "SEMrush",
                description: "Online visibility management and content marketing SaaS platform.",
                link: "https://semrush.com", // Placeholder for affiliate link
                recommended: true
            },
            {
                name: "Ahrefs",
                description: "SEO tools & resources to grow your search traffic.",
                link: "https://ahrefs.com", // Placeholder for affiliate link
                recommended: false
            }
        ]
    },
    {
        category: "Hosting & Infrastructure",
        tools: [
            {
                name: "Hostinger",
                description: "Premium web hosting & domain registration.",
                link: "https://hostinger.com", // Placeholder for affiliate link
                recommended: true
            },
            {
                name: "Kinsta",
                description: "Premium managed WordPress hosting.",
                link: "https://kinsta.com", // Placeholder for affiliate link
                recommended: false
            }
        ]
    }
]

export default function ToolsPage() {
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Recommended Tools</h2>
                    <p className="text-muted-foreground">
                        Curated list of best-in-class tools to grow your business.
                    </p>
                </div>
            </div>

            <div className="space-y-8">
                {recommendedTools.map((category) => (
                    <div key={category.category}>
                        <h3 className="text-xl font-semibold mb-4">{category.category}</h3>
                        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                            {category.tools.map((tool) => (
                                <Card key={tool.name} className={tool.recommended ? "border-blue-500 shadow-md" : ""}>
                                    <CardHeader>
                                        <div className="flex justify-between items-start">
                                            <CardTitle className="text-lg">{tool.name}</CardTitle>
                                            {tool.recommended && (
                                                <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded dark:bg-blue-900 dark:text-blue-300">
                                                    Recommended
                                                </span>
                                            )}
                                        </div>
                                        <CardDescription>{tool.description}</CardDescription>
                                    </CardHeader>
                                    <CardContent>
                                        <Button className="w-full" variant="outline" asChild>
                                            <a href={tool.link} target="_blank" rel="noopener noreferrer">
                                                Visit Website <ExternalLink className="ml-2 h-4 w-4" />
                                            </a>
                                        </Button>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}
