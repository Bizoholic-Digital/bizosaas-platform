from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock

class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

# --- Thrillring Gaming Models ---

class ThrillringHomePage(Page):
    """homepage for the Thrillring gaming portal."""
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    subpage_types = ['home.GamePage', 'home.NewsArticlePage', 'home.EventPage', 'home.LeaderboardPage']

class GamePage(Page):
    """Profile page for a specific game."""
    genre = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    release_date = models.DateField("Release Date")
    rating = models.DecimalField(max_digits=3, decimal_places=1, help_text="Rating out of 10")
    
    description = RichTextField()
    
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    gallery = StreamField([
        ('image', ImageChooserBlock()),
        ('caption', blocks.CharBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('genre'),
            FieldPanel('platform'),
            FieldPanel('release_date'),
            FieldPanel('rating'),
        ], heading="Game Info"),
        FieldPanel('description'),
        FieldPanel('cover_image'),
        FieldPanel('gallery'),
    ]

class NewsArticlePage(Page):
    """Gaming news article."""
    date = models.DateField("Post date")
    author = models.CharField(max_length=255)
    intro = models.CharField(max_length=250)
    
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('quote', blocks.BlockQuoteBlock()),
    ], use_json_field=True)
    
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('author'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('feed_image'),
    ]

class EventPage(Page):
    """Esports event or tournament page."""
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    prize_pool = models.CharField(max_length=100, blank=True)
    registration_link = models.URLField(blank=True)
    
    details = RichTextField()
    
    content_panels = Page.content_panels + [
        FieldPanel('start_date'),
        FieldPanel('end_date'),
        FieldPanel('location'),
        FieldPanel('prize_pool'),
        FieldPanel('registration_link'),
        FieldPanel('details'),
    ]

class LeaderboardPage(Page):
    """Ranking page for games or players."""
    game = models.ForeignKey(
        'home.GamePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # Simple JSON field for storing ranking data until a more complex relation is needed
    rankings_data = models.JSONField(default=list, help_text="List of {rank, player, score}")
    
    content_panels = Page.content_panels + [
        FieldPanel('game'),
        FieldPanel('rankings_data'),
    ]
