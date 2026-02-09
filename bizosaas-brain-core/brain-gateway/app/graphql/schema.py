import strawberry
from typing import List, Optional
from datetime import datetime

from ..services.project_service import ProjectService
from ..dependencies import get_connector_service, get_secret_service
from ..connectors.base import ConnectorType

from .types.project_types import ProjectType, TaskType
from .types.cms_types import CMSPageType, CMSPostType, CMSStatsType, CMSPluginType, CMSPageInput, CMSPostInput
from .types.crm_types import CRMContactType, CRMDealType, CRMStatsType, CRMContactInput, CRMDealInput
from .types.ecommerce_types import ProductType, OrderType, EcommerceStatsType, ProductInput

from ..ports.cms_port import Page as PortPage, Post as PortPost
from ..ports.crm_port import Contact as PortContact, Deal as PortDeal
from ..ports.ecommerce_port import Product as PortProduct

# Service Locator (simplified DI)
def get_project_service():
    return ProjectService()

    # --- Ecommerce Mutations ---
    @strawberry.mutation
    async def create_product(self, tenant_id: str, input: ProductInput) -> ProductType:
        service = get_connector_service(get_secret_service())
        connector = await service.get_active_connector_by_type(tenant_id, ConnectorType.ECOMMERCE)
        if not connector: raise Exception("Ecommerce Connector not found")
        product_obj = PortProduct(**input.__dict__)
        result = await connector.create_product(product_obj)
        return ProductType(**result.dict())

# Import Gaming Types locally to avoid circular imports if any, or just for organization
from .types.gaming_types import GameType, TournamentType, GamingStatsType, LeaderboardEntryType

@strawberry.type
class Query:
    # --- Projects & Tasks ---
    @strawberry.field
    async def projects(self, tenant_id: str) -> List[ProjectType]:
        service = get_project_service()
        domain_projects = await service.get_all_projects(tenant_id)
        return [ProjectType(**p.dict()) for p in domain_projects]

    @strawberry.field
    async def tasks(self, tenant_id: str, project_id: str) -> List[TaskType]:
        service = get_project_service()
        domain_tasks = await service.get_project_tasks(tenant_id, project_id)
        return [
            TaskType(
                **t.dict(exclude={"status", "priority"}),
                status=t.status.value,
                priority=t.priority.value
            ) for t in domain_tasks
        ]

    # --- Gaming (Thrillring) ---
    @strawberry.field
    async def gaming_stats(self, tenant_id: str) -> GamingStatsType:
        # Mock Data
        return GamingStatsType(
            total_players=12543,
            active_tournaments=4,
            total_prize_pool=25000.0,
            live_matches=12
        )

    @strawberry.field
    async def popular_games(self, tenant_id: str, platform: str = "all", limit: int = 20) -> List[GameType]:
        # Mock Data
        return [
            GameType(
                id=1, name="VALORANT", 
                image_url="https://images.contentstack.io/v3/assets/bltb6530b271fddd0b1/blt0f57635c8291c927/5ebf2c6df442436ea3392306/VALORANT_Jett_Red_Crop.jpg",
                active_players=4500, platforms=["PC"], genre=["FPS"]
            ),
            GameType(
                id=2, name="Counter-Strike 2", 
                image_url="https://cdn.cloudflare.steamstatic.com/steam/apps/730/header.jpg",
                active_players=3200, platforms=["PC"], genre=["FPS"]
            ),
            GameType(
                id=3, name="League of Legends", 
                image_url="https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ahri_0.jpg",
                active_players=8900, platforms=["PC"], genre=["MOBA"]
            ),
            GameType(
                id=4, name="Dota 2", 
                image_url="https://cdn.cloudflare.steamstatic.com/steam/apps/570/header.jpg",
                active_players=2100, platforms=["PC"], genre=["MOBA"]
            ),
        ]

    @strawberry.field
    async def tournaments(self, tenant_id: str, status: Optional[str] = "all", game: Optional[str] = "all", limit: int = 20) -> List[TournamentType]:
        # Mock Data
        return [
            TournamentType(
                id=101, title="ThrillRing Valorant Open", game="VALORANT",
                prize_pool=5000.0, status="registration_open",
                participants=12, max_participants=32,
                image_url="https://images.contentstack.io/v3/assets/bltb6530b271fddd0b1/blt0f57635c8291c927/5ebf2c6df442436ea3392306/VALORANT_Jett_Red_Crop.jpg",
                start_date="2026-03-01T14:00:00Z", end_date="2026-03-01T20:00:00Z",
                registration_status="open", platform=["PC"]
            ),
            TournamentType(
                id=102, title="CS2 Weekend Warwick", game="Counter-Strike 2",
                prize_pool=2500.0, status="live",
                participants=64, max_participants=64,
                image_url="https://cdn.cloudflare.steamstatic.com/steam/apps/730/header.jpg",
                start_date="2026-02-06T10:00:00Z", end_date="2026-02-08T18:00:00Z",
                registration_status="closed", platform=["PC"], featured=True
            ),
            TournamentType(
                id=103, title="Midnight Madness", game="League of Legends",
                prize_pool=1000.0, status="upcoming",
                participants=5, max_participants=16,
                image_url="https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ahri_0.jpg",
                start_date="2026-02-14T20:00:00Z", end_date="2026-02-14T23:00:00Z",
                registration_status="open", platform=["PC"]
            )
        ]

    @strawberry.field
    async def leaderboard(self, tenant_id: str, leaderboard_type: str = "global", game: Optional[str] = None, limit: int = 100) -> List[LeaderboardEntryType]:
        # Mock Data
        return [
            LeaderboardEntryType(rank=1, name="ThrillSeeker01", wins=150, points=3200, earnings=4500.0, avatar="👑"),
            LeaderboardEntryType(rank=2, name="BizBot_AI", wins=142, points=3150, earnings=3200.0, avatar="🤖"),
            LeaderboardEntryType(rank=3, name="NoScopePro", wins=120, points=2900, earnings=1500.0, avatar="🎯"),
        ]

    # --- CMS ---
    @strawberry.field
    async def cms_pages(self, tenant_id: str) -> List[CMSPageType]:
        service = get_connector_service(get_secret_service())
        connector = await service.get_active_connector_by_type(tenant_id, ConnectorType.CMS)
        if not connector: return []
        pages = await connector.get_pages()
        return [CMSPageType(**p.dict()) for p in pages]

    @strawberry.field
    async def cms_posts(self, tenant_id: str) -> List[CMSPostType]:
        service = get_connector_service(get_secret_service())
        connector = await service.get_active_connector_by_type(tenant_id, ConnectorType.CMS)
        if not connector: return []
        posts = await connector.get_posts()
        return [CMSPostType(**p.dict()) for p in posts]

    @strawberry.field
    async def cms_stats(self, tenant_id: str) -> Optional[CMSStatsType]:
        service = get_connector_service(get_secret_service())
        connector = await service.get_active_connector_by_type(tenant_id, ConnectorType.CMS)
        if not connector: return None
        stats = await connector.get_stats()
        return CMSStatsType(**stats.dict())

    # --- CRM ---
    @strawberry.field
    async def crm_contacts(self, tenant_id: str) -> List[CRMContactType]:
        service = get_connector_service(get_secret_service())
        connector = await service.get_active_connector_by_type(tenant_id, ConnectorType.CRM)
        if not connector: return []
        contacts = await connector.get_contacts()
        return [CRMContactType(**c.dict()) for c in contacts]

    @strawberry.field
    async def crm_deals(self, tenant_id: str) -> List[CRMDealType]:
        service = get_connector_service(get_secret_service())
        connector = await service.get_active_connector_by_type(tenant_id, ConnectorType.CRM)
        if not connector: return []
        deals = await connector.get_deals()
        return [CRMDealType(**d.dict()) for d in deals]

    @strawberry.field
    async def crm_stats(self, tenant_id: str) -> Optional[CRMStatsType]:
        service = get_connector_service(get_secret_service())
        connector = await service.get_active_connector_by_type(tenant_id, ConnectorType.CRM)
        if not connector: return None
        stats = await connector.get_stats()
        return CRMStatsType(**stats.dict())

    # --- Ecommerce ---
    @strawberry.field
    async def products(self, tenant_id: str) -> List[ProductType]:
        service = get_connector_service(get_secret_service())
        connector = await service.get_active_connector_by_type(tenant_id, ConnectorType.ECOMMERCE)
        if not connector: return []
        products = await connector.get_products()
        return [ProductType(**p.dict()) for p in products]

    @strawberry.field
    async def orders(self, tenant_id: str) -> List[OrderType]:
        service = get_connector_service(get_secret_service())
        connector = await service.get_active_connector_by_type(tenant_id, ConnectorType.ECOMMERCE)
        if not connector: return []
        orders = await connector.get_orders()
        return [OrderType(**o.dict()) for o in orders]

    @strawberry.field
    async def ecommerce_stats(self, tenant_id: str) -> Optional[EcommerceStatsType]:
        service = get_connector_service(get_secret_service())
        connector = await service.get_active_connector_by_type(tenant_id, ConnectorType.ECOMMERCE)
        if not connector: return None
        stats = await connector.get_stats()
        return EcommerceStatsType(**stats.dict())

@strawberry.type
class Mutation:
    # --- CMS Mutations ---
    @strawberry.mutation
    async def create_cms_page(self, tenant_id: str, input: CMSPageInput) -> CMSPageType:
        service = get_connector_service(get_secret_service())
        connector = await service.get_active_connector_by_type(tenant_id, ConnectorType.CMS)
        if not connector: raise Exception("CMS Connector not found")
        page_obj = PortPage(**input.__dict__)
        result = await connector.create_page(page_obj)
        return CMSPageType(**result.dict())

    @strawberry.mutation
    async def create_cms_post(self, tenant_id: str, input: CMSPostInput) -> CMSPostType:
        service = get_connector_service(get_secret_service())
        connector = await service.get_active_connector_by_type(tenant_id, ConnectorType.CMS)
        if not connector: raise Exception("CMS Connector not found")
        post_obj = PortPost(**input.__dict__)
        result = await connector.create_post(post_obj)
        return CMSPostType(**result.dict())

    # --- CRM Mutations ---
    @strawberry.mutation
    async def create_crm_contact(self, tenant_id: str, input: CRMContactInput) -> CRMContactType:
        service = get_connector_service(get_secret_service())
        connector = await service.get_active_connector_by_type(tenant_id, ConnectorType.CRM)
        if not connector: raise Exception("CRM Connector not found")
        contact_obj = PortContact(**input.__dict__)
        result = await connector.create_contact(contact_obj)
        return CRMContactType(**result.dict())

    @strawberry.mutation
    async def create_crm_deal(self, tenant_id: str, input: CRMDealInput) -> CRMDealType:
        service = get_connector_service(get_secret_service())
        connector = await service.get_active_connector_by_type(tenant_id, ConnectorType.CRM)
        if not connector: raise Exception("CRM Connector not found")
        deal_obj = PortDeal(**input.__dict__)
        result = await connector.create_deal(deal_obj)
        return CRMDealType(**result.dict())

    # --- Ecommerce Mutations ---
    @strawberry.mutation
    async def create_product(self, tenant_id: str, input: ProductInput) -> ProductType:
        service = get_connector_service(get_secret_service())
        connector = await service.get_active_connector_by_type(tenant_id, ConnectorType.ECOMMERCE)
        if not connector: raise Exception("Ecommerce Connector not found")
        product_obj = PortProduct(**input.__dict__)
        result = await connector.create_product(product_obj)
        return ProductType(**result.dict())

schema = strawberry.Schema(query=Query, mutation=Mutation)
