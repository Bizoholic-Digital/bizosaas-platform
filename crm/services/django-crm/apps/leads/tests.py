"""
Tests for leads app
Basic model and API tests
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.tenants.models import Tenant, TenantMembership
from .models import LeadSource, LeadTag, Lead, LeadActivity, LeadNote
from datetime import timedelta

User = get_user_model()


class LeadModelTest(TestCase):
    """Test cases for Lead model"""
    
    def setUp(self):
        """Set up test data"""
        self.tenant = Tenant.objects.create(
            name="Test Company",
            slug="test-company"
        )
        
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        TenantMembership.objects.create(
            tenant=self.tenant,
            user=self.user,
            role='admin'
        )
        
        self.source = LeadSource.objects.create(
            tenant=self.tenant,
            name="Website",
            description="Leads from website"
        )
        
        self.tag = LeadTag.objects.create(
            tenant=self.tenant,
            name="Hot Lead",
            color="#ff0000"
        )
    
    def test_lead_creation(self):
        """Test basic lead creation"""
        lead = Lead.objects.create(
            tenant=self.tenant,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            company="Acme Corp",
            source=self.source
        )
        
        self.assertEqual(lead.full_name, "John Doe")
        self.assertEqual(lead.status, "new")
        self.assertEqual(lead.priority, "medium")
        self.assertEqual(lead.score, 0)
    
    def test_lead_score_calculation(self):
        """Test AI score calculation"""
        lead = Lead.objects.create(
            tenant=self.tenant,
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            company="Big Corp",
            company_size="enterprise",
            budget=100000,
            decision_maker=True
        )
        
        # Update score
        score = lead.update_score()
        
        # Should have score components
        self.assertGreater(score, 0)
        self.assertIsInstance(lead.score_factors, dict)
        self.assertIn('company_size', lead.score_factors)
        self.assertIn('budget', lead.score_factors)
        self.assertIn('decision_maker', lead.score_factors)
    
    def test_lead_status_change(self):
        """Test lead status changes"""
        lead = Lead.objects.create(
            tenant=self.tenant,
            first_name="Bob",
            last_name="Johnson",
            email="bob@example.com"
        )
        
        # Mark as contacted
        lead.mark_as_contacted(self.user)
        
        self.assertEqual(lead.status, "contacted")
        self.assertIsNotNone(lead.first_contact_date)
        self.assertIsNotNone(lead.last_contact_date)
    
    def test_lead_conversion(self):
        """Test lead conversion"""
        lead = Lead.objects.create(
            tenant=self.tenant,
            first_name="Alice",
            last_name="Wilson",
            email="alice@example.com"
        )
        
        # Convert lead
        conversion_value = 50000
        lead.convert(value=conversion_value, user=self.user)
        
        self.assertEqual(lead.status, "converted")
        self.assertEqual(lead.conversion_value, conversion_value)
        self.assertEqual(lead.score, 100)
        self.assertIsNotNone(lead.converted_at)
    
    def test_lead_manager_methods(self):
        """Test custom manager methods"""
        # Create test leads
        Lead.objects.create(
            tenant=self.tenant,
            first_name="Test1",
            last_name="User1",
            email="test1@example.com",
            status="new"
        )
        
        Lead.objects.create(
            tenant=self.tenant,
            first_name="Test2",
            last_name="User2",
            email="test2@example.com",
            status="converted"
        )
        
        Lead.objects.create(
            tenant=self.tenant,
            first_name="Test3",
            last_name="User3",
            email="test3@example.com",
            priority="high"
        )
        
        # Test manager methods
        self.assertEqual(Lead.objects.filter(tenant=self.tenant).new().count(), 1)
        self.assertEqual(Lead.objects.filter(tenant=self.tenant).high_priority().count(), 1)
        self.assertEqual(Lead.objects.filter(tenant=self.tenant).unassigned().count(), 3)


class LeadSourceModelTest(TestCase):
    """Test cases for LeadSource model"""
    
    def setUp(self):
        """Set up test data"""
        self.tenant = Tenant.objects.create(
            name="Test Company",
            slug="test-company"
        )
        
        self.source = LeadSource.objects.create(
            tenant=self.tenant,
            name="Website"
        )
    
    def test_conversion_stats_update(self):
        """Test conversion statistics calculation"""
        # Create leads
        Lead.objects.create(
            tenant=self.tenant,
            first_name="Lead1",
            last_name="Test",
            email="lead1@example.com",
            source=self.source,
            status="new"
        )
        
        Lead.objects.create(
            tenant=self.tenant,
            first_name="Lead2",
            last_name="Test",
            email="lead2@example.com",
            source=self.source,
            status="converted"
        )
        
        # Update stats
        self.source.update_conversion_stats()
        
        self.assertEqual(self.source.total_leads, 2)
        self.assertEqual(self.source.converted_leads, 1)
        self.assertEqual(self.source.conversion_rate, 50.00)


class LeadActivityModelTest(TestCase):
    """Test cases for LeadActivity model"""
    
    def setUp(self):
        """Set up test data"""
        self.tenant = Tenant.objects.create(
            name="Test Company",
            slug="test-company"
        )
        
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        self.lead = Lead.objects.create(
            tenant=self.tenant,
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )
    
    def test_activity_creation(self):
        """Test activity creation"""
        activity = LeadActivity.objects.create(
            tenant=self.tenant,
            lead=self.lead,
            user=self.user,
            activity_type="call",
            description="Called the lead"
        )
        
        self.assertEqual(activity.activity_type, "call")
        self.assertTrue(activity.is_completed)
    
    def test_scheduled_activity(self):
        """Test scheduled activity"""
        future_time = timezone.now() + timedelta(hours=2)
        
        activity = LeadActivity.objects.create(
            tenant=self.tenant,
            lead=self.lead,
            user=self.user,
            activity_type="follow_up",
            description="Follow up call",
            scheduled_at=future_time,
            is_completed=False
        )
        
        # Test manager methods
        upcoming = LeadActivity.objects.filter(tenant=self.tenant).upcoming()
        self.assertIn(activity, upcoming)
        
        overdue = LeadActivity.objects.filter(tenant=self.tenant).overdue()
        self.assertNotIn(activity, overdue)