# Supplier Validation Workflow [P9] - BizOSaaS Platform

## Overview

The Supplier Validation Workflow is a comprehensive Human-in-the-Loop (HITL) approval system designed for the BizOSaaS platform. It provides automated business license verification, AI-powered risk assessment, and multi-step human validation workflow with role-based approvals.

## 🚀 Key Features

### Core Capabilities
- **Human-in-the-Loop (HITL) Approval System**: Multi-step validation with role-based approvals
- **Business License Verification**: Automated verification of Indian business credentials
- **AI-Powered Risk Assessment**: Machine learning-based supplier quality scoring
- **Document Management**: Upload, verification, and storage with OCR capabilities
- **Indian Market Compliance**: GST, PAN, and Aadhaar validation
- **Multi-tenant Architecture**: Secure, scalable multi-tenant design
- **Real-time Dashboard**: Comprehensive management interface

### Advanced Features
- **Comprehensive Validation Engine**: Email, phone, website, and business profile validation
- **Workflow Management**: Configurable approval workflows with audit trails
- **Bulk Operations**: Efficient batch processing for large supplier lists
- **Analytics Dashboard**: Detailed insights and performance metrics
- **Document OCR**: Automated text extraction from uploaded documents
- **Integration Ready**: APIs for seamless integration with other services

## 🏗️ Architecture

### Service Components
```
┌─────────────────────────────────────────────────┐
│                 Frontend Layer                  │
├─────────────────────────────────────────────────┤
│  • Dashboard (HTML/CSS/JS)                     │
│  • API Documentation (FastAPI/Swagger)         │
│  • File Upload Interface                       │
└─────────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────────┐
│                 API Layer                       │
├─────────────────────────────────────────────────┤
│  • FastAPI Application (Port 8027)             │
│  • Authentication & Authorization              │
│  • Request Validation & Response Formatting    │
└─────────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────────┐
│              Business Logic Layer               │
├─────────────────────────────────────────────────┤
│  • Supplier Risk Assessment Engine             │
│  • Document Verification Engine                │
│  • HITL Workflow Manager                       │
│  • Comprehensive Validation Engine             │
└─────────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────────┐
│                 Data Layer                      │
├─────────────────────────────────────────────────┤
│  • PostgreSQL Database                         │
│  • Redis Cache                                 │
│  • File Storage (Local/S3)                     │
│  • Audit Logs                                  │
└─────────────────────────────────────────────────┘
```

### Database Schema
- **suppliers**: Main supplier information
- **supplier_documents**: Document metadata and verification results
- **supplier_workflows**: Workflow state and approval tracking
- **supplier_risk_assessments**: Risk assessment history
- **supplier_audit_log**: Complete audit trail
- **supplier_notifications**: Communication history
- **supplier_validation_results**: Comprehensive validation results

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Installation

1. **Clone and Navigate**
   ```bash
   cd /home/alagiri/projects/bizoholic/bizosaas-platform/services/supplier-validation
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Deploy with Docker Compose**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

4. **Access the Service**
   - Dashboard: http://localhost:8027/dashboard
   - API Docs: http://localhost:8027/docs
   - PgAdmin: http://localhost:8080 (admin@bizosaas.com / admin)

### Manual Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   export DATABASE_URL="postgresql://postgres:password@localhost:5432/bizosaas"
   export REDIS_URL="redis://localhost:6379"
   export BRAIN_API_URL="http://localhost:8001"
   ```

3. **Run the Service**
   ```bash
   python main.py
   ```

## 📋 API Documentation

### Core Endpoints

#### Supplier Management
- `POST /suppliers/register` - Register new supplier
- `GET /suppliers/{supplier_id}` - Get supplier details
- `PUT /suppliers/{supplier_id}` - Update supplier information
- `GET /suppliers` - List suppliers with filtering

#### Document Management
- `POST /suppliers/{supplier_id}/documents/upload` - Upload document
- `GET /suppliers/{supplier_id}/documents` - List supplier documents
- `DELETE /documents/{document_id}` - Delete document

#### Validation & Risk Assessment
- `GET /suppliers/{supplier_id}/risk-assessment` - Get risk assessment
- `POST /suppliers/{supplier_id}/validate-comprehensive` - Comprehensive validation
- `GET /suppliers/{supplier_id}/workflow-history` - Get workflow history

#### Workflow Management
- `POST /suppliers/{supplier_id}/review` - Submit review decision
- `GET /workflows/{workflow_id}` - Get workflow details
- `POST /suppliers/bulk-action` - Bulk operations

#### Analytics & Reporting
- `GET /dashboard/analytics` - Dashboard analytics
- `GET /` or `/dashboard` - Web dashboard

### Request Examples

#### Register Supplier
```bash
curl -X POST "http://localhost:8027/suppliers/register" \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "ABC Electronics Pvt Ltd",
    "contact_person": "Rajesh Kumar",
    "email": "rajesh@abcelectronics.com",
    "phone": "+91-9876543210",
    "address": "123 Electronics Market, Nehru Place",
    "city": "New Delhi",
    "state": "Delhi",
    "pincode": "110019",
    "business_type": "Private Limited Company",
    "industry": "Electronics Manufacturing",
    "products_offered": ["Smartphones", "Laptops", "Accessories"],
    "gst_number": "07AABCA1234M1Z5",
    "pan_number": "AABCA1234M"
  }'
```

#### Upload Document
```bash
curl -X POST "http://localhost:8027/suppliers/{supplier_id}/documents/upload" \
  -H "Authorization: Bearer your-token" \
  -F "document_type=business_license" \
  -F "file=@business_license.pdf"
```

#### Submit Review
```bash
curl -X POST "http://localhost:8027/suppliers/{supplier_id}/review" \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "supplier_id": "supplier-uuid",
    "decision": "approve",
    "comments": "All documents verified, low risk supplier"
  }'
```

## 🔧 Configuration

### Environment Variables

#### Core Configuration
- `SERVICE_PORT`: Service port (default: 8027)
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `BRAIN_API_URL`: Brain API endpoint

#### Indian Government APIs
- `GST_API_KEY`: GST verification API key
- `PAN_API_KEY`: PAN verification API key
- `AADHAAR_API_KEY`: Aadhaar verification API key

#### AI/ML Configuration
- `OPENAI_API_KEY`: OpenAI API key for enhanced analysis
- `AI_MODEL`: AI model to use (default: gpt-3.5-turbo)
- `AI_TEMPERATURE`: AI temperature setting

#### File Storage
- `STORAGE_TYPE`: Storage type (local, s3, gcs)
- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `STORAGE_BUCKET`: Storage bucket name

#### Workflow Configuration
- `AUTO_ASSIGN_ANALYSTS`: Auto-assign to analysts
- `REQUIRE_MANAGER_APPROVAL`: Require manager approval
- `REQUIRE_DIRECTOR_APPROVAL`: Require director approval
- `ENABLE_COMPLIANCE_CHECK`: Enable compliance checking

## 🔄 Workflow Process

### Supplier Validation Workflow

```mermaid
graph TD
    A[Supplier Registration] --> B[Document Upload]
    B --> C[Automated Verification]
    C --> D[AI Risk Assessment]
    D --> E[Analyst Review]
    E --> F{Decision}
    F -->|Approve| G[Manager Approval]
    F -->|Request Info| B
    F -->|Reject| H[Rejected]
    G --> I{Manager Decision}
    I -->|Approve| J[Compliance Check]
    I -->|Reject| H
    I -->|Request Info| B
    J --> K[Director Approval]
    K --> L{Director Decision}
    L -->|Approve| M[Approved]
    L -->|Reject| H
    L -->|Request Info| B
```

### Approval Hierarchy
1. **Document Upload**: Supplier uploads required documents
2. **Automated Verification**: AI/OCR document verification
3. **Risk Assessment**: AI-powered risk scoring
4. **Analyst Review**: Human analyst verification
5. **Manager Approval**: Management level approval
6. **Compliance Check**: Final compliance verification
7. **Director Approval**: Executive level approval
8. **Final Status**: Approved/Rejected/Suspended

### User Roles & Permissions
- **Analyst**: Document review, initial approval/rejection
- **Manager**: Manager-level approvals, workflow oversight
- **Director**: Final approvals, policy decisions
- **Admin**: System administration, all permissions

## 🧪 Testing

### Run Test Suite
```bash
python test_supplier_validation.py
```

### Test Categories
1. **Health Check**: Service availability
2. **Dashboard Access**: Frontend functionality
3. **Supplier Registration**: Registration workflow
4. **Document Upload**: File upload and verification
5. **Risk Assessment**: AI risk analysis
6. **Comprehensive Validation**: Full validation suite
7. **Workflow Management**: Approval workflows
8. **Analytics**: Dashboard analytics
9. **Bulk Operations**: Batch processing

### Integration Testing
```bash
# Test with Product Sourcing Workflow [P8]
curl -X POST "http://localhost:8026/validate-supplier" \
  -H "Content-Type: application/json" \
  -d '{"supplier_id": "uuid-from-validation-service"}'
```

## 📊 Validation Engine

### Indian Business Validation
- **GST Number**: Format validation and state verification
- **PAN Number**: Format validation and entity type extraction
- **Business Registration**: Verification against government databases
- **State Compliance**: State-specific validation requirements

### Comprehensive Validation Components
1. **Email Validation**: Format, domain, deliverability
2. **Phone Validation**: Format, country code, number type
3. **Website Validation**: Accessibility, content analysis
4. **Business Profile**: Industry-product alignment, size consistency

### Risk Assessment Factors
- Document verification status
- Business registration completeness
- Financial indicators
- Industry risk factors
- Compliance issues
- Historical performance

### Confidence Scoring
- **High (80-100%)**: All validations passed, low risk
- **Medium (60-79%)**: Minor issues, manageable risk
- **Low (0-59%)**: Significant issues, high risk

## 🔍 Monitoring & Analytics

### Dashboard Metrics
- Total suppliers by status
- Risk level distribution
- Approval workflow metrics
- Recent activity timeline
- Document verification rates

### Performance Monitoring
- API response times
- Document processing times
- Validation accuracy rates
- User activity patterns
- System resource usage

### Audit Trail
- All supplier actions logged
- Document upload/verification history
- Approval decision tracking
- User access patterns
- Compliance verification records

## 🔗 Integration

### Product Sourcing Integration [P8]
- Supplier validation before sourcing requests
- Automated supplier quality checks
- Shared supplier database
- Real-time validation status

### Brain API Integration
- Centralized routing through port 8001
- Shared authentication and authorization
- Cross-service communication
- Unified logging and monitoring

### External Integrations
- Government API integration (GST, PAN)
- Banking verification services
- Credit rating agencies
- Industry compliance databases

## 🚀 Deployment

### Docker Deployment
```bash
# Build and deploy
./deploy.sh

# Check status
./deploy.sh status

# View logs
./deploy.sh logs

# Stop services
./deploy.sh stop
```

### Production Considerations
- Set up SSL/TLS certificates
- Configure production database
- Set up backup and recovery
- Monitor resource usage
- Configure logging and alerting

### Scaling
- Horizontal scaling with load balancer
- Database read replicas
- Redis clustering
- CDN for file storage
- Background task workers

## 📞 Support

### Troubleshooting
1. Check service health: `curl http://localhost:8027/health`
2. View logs: `docker-compose logs supplier-validation`
3. Check database connection: `docker exec -it supplier-validation-postgres psql -U postgres -d bizosaas`
4. Verify Redis: `docker exec -it supplier-validation-redis redis-cli ping`

### Common Issues
- **Port conflicts**: Change port in docker-compose.yml
- **Database connection**: Check DATABASE_URL in .env
- **File upload issues**: Verify file permissions
- **API authentication**: Check API_KEY configuration

### Contact Information
- **Service**: Supplier Validation Workflow [P9]
- **Port**: 8027
- **Repository**: BizOSaaS Platform
- **Team**: BizOSaaS Platform Team

## 📝 License

Part of the BizOSaaS Platform - All Rights Reserved

---

**Note**: This service is part of the comprehensive BizOSaaS platform and integrates with other platform services for complete business workflow automation.