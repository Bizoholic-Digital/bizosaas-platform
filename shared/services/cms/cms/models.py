from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site
from wagtail.models import Page, Site as WagtailSite
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.api import APIField
from wagtail.snippets.models import register_snippet
from wagtail.contrib.settings.models import BaseGenericSetting as BaseSetting, register_setting
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
import json

# Custom blocks for marketing content
class CallToActionBlock(blocks.StructBlock):
    """CTA block for marketing pages"""
    title = blocks.CharBlock(max_length=100)
    description = blocks.TextBlock(required=False)
    button_text = blocks.CharBlock(max_length=50)
    button_url = blocks.URLBlock()
    button_style = blocks.ChoiceBlock(
        choices=[
            ('primary', 'Primary'),
            ('secondary', 'Secondary'),
            ('outline', 'Outline'),
        ],
        default='primary'
    )
    
    class Meta:
        template = 'cms/blocks/cta_block.html'
        icon = 'pick'
        label = 'Call to Action'

class FeatureBlock(blocks.StructBlock):
    """Feature highlight block"""
    icon = ImageChooserBlock(required=False)
    title = blocks.CharBlock(max_length=100)
    description = blocks.TextBlock()
    
    class Meta:
        template = 'cms/blocks/feature_block.html'
        icon = 'list-ul'
        label = 'Feature'

class TestimonialBlock(blocks.StructBlock):
    """Customer testimonial block"""
    quote = blocks.TextBlock()
    author_name = blocks.CharBlock(max_length=100)
    author_title = blocks.CharBlock(max_length=100, required=False)
    author_company = blocks.CharBlock(max_length=100, required=False)
    author_image = ImageChooserBlock(required=False)
    rating = blocks.IntegerBlock(min_value=1, max_value=5, default=5)
    
    class Meta:
        template = 'cms/blocks/testimonial_block.html'
        icon = 'openquote'
        label = 'Testimonial'

class StatsBlock(blocks.StructBlock):
    """Statistics/metrics block"""
    stat_number = blocks.CharBlock(max_length=20)
    stat_label = blocks.CharBlock(max_length=50)
    stat_description = blocks.TextBlock(required=False)
    
    class Meta:
        template = 'cms/blocks/stats_block.html'
        icon = 'snippet'
        label = 'Statistic'

class PricingBlock(blocks.StructBlock):
    """Pricing plan block"""
    plan_name = blocks.CharBlock(max_length=100)
    price = blocks.CharBlock(max_length=20)
    price_period = blocks.CharBlock(max_length=20, default='month')
    features = blocks.ListBlock(blocks.CharBlock(max_length=100))
    is_popular = blocks.BooleanBlock(default=False, required=False)
    cta_text = blocks.CharBlock(max_length=50, default='Get Started')
    cta_url = blocks.URLBlock()
    
    class Meta:
        template = 'cms/blocks/pricing_block.html'
        icon = 'form'
        label = 'Pricing Plan'

# Tenant model for multi-tenancy with Site-based isolation
@register_snippet
class Tenant(ClusterableModel):
    """Tenant model for multi-tenant CMS with Wagtail Site integration"""
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100, unique=True)
    subdomain = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # BizOSaaS integration
    bizosaas_tenant_id = models.CharField(max_length=50, unique=True)
    api_settings = models.JSONField(default=dict, blank=True)
    
    # Wagtail Site integration for proper multi-tenant isolation
    wagtail_site = models.OneToOneField(
        WagtailSite,
        on_delete=models.CASCADE,
        related_name='tenant',
        null=True,
        blank=True,
        help_text="Associated Wagtail Site for this tenant"
    )
    
    # Tenant-specific settings
    theme_settings = models.JSONField(
        default=dict,
        blank=True,
        help_text="Theme and branding settings for this tenant"
    )
    
    seo_settings = models.JSONField(
        default=dict,
        blank=True,
        help_text="SEO settings specific to this tenant"
    )
    
    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('bizosaas_tenant_id'),
            FieldPanel('is_active'),
        ], heading="Basic Information"),
        MultiFieldPanel([
            FieldPanel('domain'),
            FieldPanel('subdomain'),
            FieldPanel('wagtail_site'),
        ], heading="Domain & Site Configuration"),
        MultiFieldPanel([
            FieldPanel('theme_settings'),
            FieldPanel('seo_settings'),
            FieldPanel('api_settings'),
        ], heading="Configuration Settings", classname="collapsible"),
    ]
    
    def __str__(self):
        return f"{self.name} ({self.bizosaas_tenant_id})"
    
    def save(self, *args, **kwargs):
        """Override save to auto-create Wagtail Site if needed"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Auto-create Wagtail Site for new tenants
        if is_new and not self.wagtail_site:
            self.create_wagtail_site()
    
    def create_wagtail_site(self):
        """Create a new Wagtail Site for this tenant"""
        try:
            # Create Wagtail Site
            site = WagtailSite.objects.create(
                hostname=self.domain,
                port=80,
                site_name=self.name,
                is_default_site=False
            )
            
            # Link to tenant
            self.wagtail_site = site
            self.save(update_fields=['wagtail_site'])
            
            # Create root page for this tenant
            self.create_tenant_root_page()
            
            return site
        except Exception as e:
            # Log error but don't fail tenant creation
            print(f"Failed to create Wagtail site for tenant {self.name}: {e}")
            return None
    
    def create_tenant_root_page(self):
        """Create root page structure for this tenant"""
        if not self.wagtail_site:
            return
        
        try:
            # Get or create a root page for this tenant
            from wagtail.models import Page
            
            # Find the Wagtail root page
            root_page = Page.get_first_root_node()
            
            # Create tenant-specific root page
            tenant_root = Page(
                title=f"{self.name} - Home",
                slug=f"tenant-{self.subdomain}",
                content_type_id=Page.get_content_type().pk,
            )
            
            root_page.add_child(instance=tenant_root)
            
            # Set as site root
            self.wagtail_site.root_page = tenant_root
            self.wagtail_site.save(update_fields=['root_page'])
            
            return tenant_root
            
        except Exception as e:
            print(f"Failed to create root page for tenant {self.name}: {e}")
            return None
    
    def get_site_pages(self):
        """Get all pages belonging to this tenant's site"""
        if not self.wagtail_site or not self.wagtail_site.root_page:
            return Page.objects.none()
        
        return self.wagtail_site.root_page.get_descendants(inclusive=True)
    
    @property
    def full_domain(self):
        """Get the full domain including subdomain if applicable"""
        if self.subdomain and self.subdomain != 'www':
            return f"{self.subdomain}.{self.domain}"
        return self.domain
    
    class Meta:
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'

# Base page with tenant support
class TenantAwarePage(Page):
    """Base page model with tenant awareness"""
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        related_name='pages',
        null=True,
        blank=True
    )
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        # Auto-assign tenant based on site or context
        if not self.tenant and hasattr(self, '_current_tenant'):
            self.tenant = self._current_tenant
        super().save(*args, **kwargs)

# Landing page for marketing campaigns
class LandingPage(TenantAwarePage):
    """Marketing landing page"""
    # Override tenant field with unique related_name
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        related_name='landing_pages',
        null=True,
        blank=True
    )
    
    subtitle = models.CharField(max_length=200, blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # A/B testing support
    variant_name = models.CharField(max_length=50, blank=True, default='A')
    is_control = models.BooleanField(default=True)
    
    # Campaign integration
    campaign_id = models.CharField(max_length=100, blank=True)
    conversion_goals = models.JSONField(default=list, blank=True)
    
    # Content blocks
    content_blocks = StreamField([
        ('heading', blocks.CharBlock(max_length=100)),
        ('paragraph', blocks.TextBlock()),
        ('image', ImageChooserBlock()),
        ('cta', CallToActionBlock()),
        ('features', blocks.ListBlock(FeatureBlock())),
        ('testimonials', blocks.ListBlock(TestimonialBlock())),
        ('stats', blocks.ListBlock(StatsBlock())),
        ('pricing', blocks.ListBlock(PricingBlock())),
        ('html', blocks.RawHTMLBlock()),
    ], blank=True)
    
    # SEO and tracking
    meta_description = models.TextField(max_length=300, blank=True)
    tracking_codes = models.JSONField(default=dict, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('hero_image'),
        FieldPanel('content_blocks'),
    ]
    
    promote_panels = Page.promote_panels + [
        FieldPanel('meta_description'),
        MultiFieldPanel([
            FieldPanel('variant_name'),
            FieldPanel('is_control'),
            FieldPanel('campaign_id'),
        ], heading='A/B Testing & Campaign'),
    ]
    
    api_fields = [
        APIField('subtitle'),
        APIField('hero_image'),
        APIField('content_blocks'),
        APIField('variant_name'),
        APIField('campaign_id'),
        APIField('tenant'),
    ]
    
    class Meta:
        verbose_name = 'Landing Page'
        verbose_name_plural = 'Landing Pages'

# Marketing campaign page
class CampaignPage(TenantAwarePage):
    """Page for marketing campaigns"""
    # Override tenant field with unique related_name
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        related_name='campaign_pages',
        null=True,
        blank=True
    )
    
    campaign_type = models.CharField(
        max_length=50,
        choices=[
            ('email', 'Email Campaign'),
            ('social', 'Social Media'),
            ('ppc', 'Pay-Per-Click'),
            ('content', 'Content Marketing'),
            ('seo', 'SEO Campaign'),
        ]
    )
    
    # Campaign details
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    target_audience = models.JSONField(default=dict, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Content
    campaign_description = RichTextField(blank=True)
    assets = StreamField([
        ('image', ImageChooserBlock()),
        ('video_embed', blocks.URLBlock()),
        ('copy_text', blocks.TextBlock()),
        ('cta', CallToActionBlock()),
    ], blank=True)
    
    # Performance tracking
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    spend = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    content_panels = Page.content_panels + [
        FieldPanel('campaign_type'),
        FieldPanel('campaign_description'),
        FieldPanel('assets'),
        MultiFieldPanel([
            FieldPanel('start_date'),
            FieldPanel('end_date'),
            FieldPanel('budget'),
        ], heading='Campaign Schedule & Budget'),
    ]
    
    api_fields = [
        APIField('campaign_type'),
        APIField('start_date'),
        APIField('end_date'),
        APIField('target_audience'),
        APIField('budget'),
        APIField('assets'),
        APIField('impressions'),
        APIField('clicks'),
        APIField('conversions'),
        APIField('spend'),
        APIField('tenant'),
    ]
    
    def ctr(self):
        """Calculate click-through rate"""
        if self.impressions > 0:
            return (self.clicks / self.impressions) * 100
        return 0
    
    def conversion_rate(self):
        """Calculate conversion rate"""
        if self.clicks > 0:
            return (self.conversions / self.clicks) * 100
        return 0
    
    class Meta:
        verbose_name = 'Campaign Page'
        verbose_name_plural = 'Campaign Pages'

# Blog/Content page
class ContentPage(TenantAwarePage):
    """Content marketing page (blog posts, articles)"""
    # Override tenant field with unique related_name
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        related_name='content_pages',
        null=True,
        blank=True
    )
    
    author = models.CharField(max_length=100, blank=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # Content
    excerpt = models.TextField(max_length=300, blank=True)
    body = StreamField([
        ('heading', blocks.CharBlock(max_length=100)),
        ('paragraph', blocks.TextBlock()),
        ('image', ImageChooserBlock()),
        ('quote', blocks.BlockQuoteBlock()),
        ('code', blocks.TextBlock()),
        ('cta', CallToActionBlock()),
    ], blank=True)
    
    # SEO
    keywords = models.CharField(max_length=300, blank=True)
    reading_time = models.IntegerField(default=5)  # minutes
    
    # Social sharing
    social_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('author'),
        FieldPanel('publish_date'),
        FieldPanel('featured_image'),
        FieldPanel('excerpt'),
        FieldPanel('body'),
    ]
    
    promote_panels = Page.promote_panels + [
        FieldPanel('keywords'),
        FieldPanel('reading_time'),
        FieldPanel('social_image'),
    ]
    
    api_fields = [
        APIField('author'),
        APIField('publish_date'),
        APIField('featured_image'),
        APIField('excerpt'),
        APIField('body'),
        APIField('keywords'),
        APIField('reading_time'),
        APIField('tenant'),
    ]
    
    class Meta:
        verbose_name = 'Content Page'
        verbose_name_plural = 'Content Pages'

# Service page for BizOSaaS services
class ServicePage(TenantAwarePage):
    """Service description page"""
    # Override tenant field with unique related_name
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        related_name='service_pages',
        null=True,
        blank=True
    )
    
    # Service details
    service_description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    badge = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=100, blank=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    # Pricing
    price_data = models.JSONField(default=dict, blank=True)
    
    # Content blocks
    content_blocks = StreamField([
        ('heading', blocks.CharBlock(max_length=100)),
        ('paragraph', blocks.TextBlock()),
        ('image', ImageChooserBlock()),
        ('features', blocks.ListBlock(FeatureBlock())),
        ('pricing', blocks.ListBlock(PricingBlock())),
        ('testimonials', blocks.ListBlock(TestimonialBlock())),
        ('cta', CallToActionBlock()),
        ('html', blocks.RawHTMLBlock()),
    ], blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('service_description'),
        FieldPanel('icon'),
        FieldPanel('badge'),
        FieldPanel('category'),
        FieldPanel('featured'),
        FieldPanel('order'),
        FieldPanel('price_data'),
        FieldPanel('content_blocks'),
    ]
    
    api_fields = [
        APIField('service_description'),
        APIField('icon'),
        APIField('badge'),
        APIField('category'),
        APIField('featured'),
        APIField('order'),
        APIField('price_data'),
        APIField('content_blocks'),
        APIField('tenant'),
    ]
    
    class Meta:
        verbose_name = 'Service Page'
        verbose_name_plural = 'Service Pages'

# Team member page
@register_snippet
class TeamMember(ClusterableModel):
    """Team member profile"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    
    # Multi-tenant support
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='team_members',
        null=True,
        blank=True
    )
    
    panels = [
        FieldPanel('name'),
        FieldPanel('position'),
        FieldPanel('bio'),
        FieldPanel('photo'),
        FieldPanel('email'),
        FieldPanel('linkedin'),
        FieldPanel('twitter'),
        FieldPanel('tenant'),
    ]
    
    def __str__(self):
        return f"{self.name} - {self.position}"
    
    class Meta:
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

# Client testimonial snippet
@register_snippet
class ClientTestimonial(ClusterableModel):
    """Client testimonial"""
    client_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    testimonial = models.TextField()
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    featured = models.BooleanField(default=False)
    
    # Multi-tenant support
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='testimonials',
        null=True,
        blank=True
    )
    
    panels = [
        FieldPanel('client_name'),
        FieldPanel('company'),
        FieldPanel('position'),
        FieldPanel('testimonial'),
        FieldPanel('photo'),
        FieldPanel('rating'),
        FieldPanel('featured'),
        FieldPanel('tenant'),
    ]
    
    def __str__(self):
        return f"{self.client_name} - {self.company}"
    
    class Meta:
        verbose_name = 'Client Testimonial'
        verbose_name_plural = 'Client Testimonials'

# Bizoholic Marketing Homepage
class BizoholicHomePage(Page):
    """Main homepage for Bizoholic marketing website"""
    
    # Hero section
    hero_title = models.CharField(
        max_length=200, 
        default="AI-Powered Marketing Automation"
    )
    hero_subtitle = models.TextField(
        max_length=500,
        default="Transform your marketing with AI automation. Get 75% cost savings, ROI within 7 days, and setup in 15 minutes. The smartest marketing platform for small businesses."
    )
    hero_cta_text = models.CharField(max_length=50, default="Get Started Free")
    hero_cta_url = models.CharField(max_length=200, default="/contact")
    
    # Features section
    features_title = models.CharField(
        max_length=100, 
        default="Why Choose Bizoholic?"
    )
    features_content = StreamField([
        ('feature', FeatureBlock()),
    ], blank=True)
    
    # Stats section
    stats_content = StreamField([
        ('stat', StatsBlock()),
    ], blank=True)
    
    # Additional sections
    extra_content = StreamField([
        ('heading', blocks.CharBlock(max_length=100)),
        ('paragraph', blocks.TextBlock()),
        ('image', ImageChooserBlock()),
        ('cta', CallToActionBlock()),
        ('features', blocks.ListBlock(FeatureBlock())),
        ('testimonials', blocks.ListBlock(TestimonialBlock())),
        ('stats', blocks.ListBlock(StatsBlock())),
        ('pricing', blocks.ListBlock(PricingBlock())),
        ('html', blocks.RawHTMLBlock()),
    ], blank=True)
    
    # Service status monitoring
    show_service_status = models.BooleanField(
        default=True,
        help_text="Show service status monitoring section"
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_cta_text'),
            FieldPanel('hero_cta_url'),
        ], heading="Hero Section"),
        MultiFieldPanel([
            FieldPanel('features_title'),
            FieldPanel('features_content'),
        ], heading="Features Section"),
        FieldPanel('stats_content'),
        FieldPanel('extra_content'),
        FieldPanel('show_service_status'),
    ]
    
    api_fields = [
        APIField('hero_title'),
        APIField('hero_subtitle'),
        APIField('hero_cta_text'),
        APIField('hero_cta_url'),
        APIField('features_title'),
        APIField('features_content'),
        APIField('stats_content'),
        APIField('extra_content'),
        APIField('show_service_status'),
    ]
    
    # Limit to one instance
    max_count = 1
    
    class Meta:
        verbose_name = 'Bizoholic Homepage'
        verbose_name_plural = 'Bizoholic Homepage'

# FAQ page
class FAQPage(TenantAwarePage):
    """FAQ and Help content page"""
    # Override tenant field with unique related_name
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        related_name='faq_pages',
        null=True,
        blank=True
    )
    
    category = models.CharField(max_length=100, blank=True)
    
    # FAQ content blocks
    faq_content = StreamField([
        ('faq_section', blocks.StructBlock([
            ('section_title', blocks.CharBlock(max_length=100)),
            ('faqs', blocks.ListBlock(blocks.StructBlock([
                ('question', blocks.CharBlock(max_length=200)),
                ('answer', blocks.TextBlock()),
            ]))),
        ])),
        ('content_block', blocks.StructBlock([
            ('title', blocks.CharBlock(max_length=100)),
            ('content', blocks.TextBlock()),
        ])),
    ], blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('category'),
        FieldPanel('faq_content'),
    ]
    
    api_fields = [
        APIField('category'),
        APIField('faq_content'),
        APIField('tenant'),
    ]
    
    class Meta:
        verbose_name = 'FAQ Page'
        verbose_name_plural = 'FAQ Pages'

# AI Content Management
@register_snippet
class AIContentTemplate(ClusterableModel):
    """AI-generated content templates"""
    name = models.CharField(max_length=100)
    content_type = models.CharField(
        max_length=50,
        choices=[
            ('blog_post', 'Blog Post'),
            ('landing_page', 'Landing Page'),
            ('service_page', 'Service Page'),
            ('email_template', 'Email Template'),
        ]
    )
    template_content = models.TextField()
    ai_prompt = models.TextField(blank=True)
    variables = models.JSONField(default=dict, blank=True)
    
    # Multi-tenant support
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='ai_templates',
        null=True,
        blank=True
    )
    
    panels = [
        FieldPanel('name'),
        FieldPanel('content_type'),
        FieldPanel('template_content'),
        FieldPanel('ai_prompt'),
        FieldPanel('variables'),
        FieldPanel('tenant'),
    ]
    
    def __str__(self):
        return f"{self.name} ({self.content_type})"
    
    class Meta:
        verbose_name = 'AI Content Template'
        verbose_name_plural = 'AI Content Templates'


# Site-wide settings for branding and configuration
@register_setting
class SiteSettings(BaseSetting):
    """Site-wide settings for branding, logos, navigation, and global configurations"""
    
    # Logo and Branding
    site_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Main site logo (recommended: PNG with transparent background)'
    )
    
    site_logo_height = models.IntegerField(
        default=32,
        help_text='Logo height in pixels (width will auto-adjust)'
    )
    
    favicon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Site favicon (recommended: 32x32px PNG or ICO)'
    )
    
    # Brand Colors
    primary_color = models.CharField(
        max_length=7,
        default='#0ea5e9',
        help_text='Primary brand color (hex format: #000000)'
    )
    
    secondary_color = models.CharField(
        max_length=7,
        default='#64748b',
        help_text='Secondary brand color (hex format: #000000)'
    )
    
    # Typography
    heading_font = models.CharField(
        max_length=100,
        default='Inter, sans-serif',
        help_text='Font family for headings'
    )
    
    body_font = models.CharField(
        max_length=100,
        default='Inter, sans-serif',
        help_text='Font family for body text'
    )
    
    # Navigation
    show_site_name = models.BooleanField(
        default=False,
        help_text='Show site name next to logo (recommended: False for logo-only branding)'
    )
    
    site_name = models.CharField(
        max_length=100,
        default='Bizoholic',
        help_text='Site name (used for alt text and when show_site_name is enabled)'
    )
    
    # Contact Information
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    
    # Social Media
    twitter_url = models.URLField(blank=True, help_text='Twitter/X profile URL')
    linkedin_url = models.URLField(blank=True, help_text='LinkedIn profile URL')
    facebook_url = models.URLField(blank=True, help_text='Facebook profile URL')
    youtube_url = models.URLField(blank=True, help_text='YouTube channel URL')
    
    # Analytics and Tracking
    google_analytics_id = models.CharField(
        max_length=20,
        blank=True,
        help_text='Google Analytics tracking ID (GA4)'
    )
    
    facebook_pixel_id = models.CharField(
        max_length=20,
        blank=True,
        help_text='Facebook Pixel ID'
    )
    
    # Footer Settings
    footer_text = models.TextField(
        blank=True,
        help_text='Custom footer text or copyright notice'
    )
    
    panels = [
        MultiFieldPanel([
            FieldPanel('site_logo'),
            FieldPanel('site_logo_height'),
            FieldPanel('favicon'),
            FieldPanel('show_site_name'),
            FieldPanel('site_name'),
        ], heading="Logo & Branding"),
        
        MultiFieldPanel([
            FieldPanel('primary_color'),
            FieldPanel('secondary_color'),
            FieldPanel('heading_font'),
            FieldPanel('body_font'),
        ], heading="Colors & Typography"),
        
        MultiFieldPanel([
            FieldPanel('contact_email'),
            FieldPanel('contact_phone'),
        ], heading="Contact Information"),
        
        MultiFieldPanel([
            FieldPanel('twitter_url'),
            FieldPanel('linkedin_url'),
            FieldPanel('facebook_url'),
            FieldPanel('youtube_url'),
        ], heading="Social Media"),
        
        MultiFieldPanel([
            FieldPanel('google_analytics_id'),
            FieldPanel('facebook_pixel_id'),
        ], heading="Analytics & Tracking"),
        
        MultiFieldPanel([
            FieldPanel('footer_text'),
        ], heading="Footer Settings"),
    ]
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'