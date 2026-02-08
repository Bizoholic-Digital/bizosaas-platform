# Business Directory AI Integration with CrewAI

This document describes the AI-powered features integrated into the Business Directory Service using CrewAI agents.

## 🤖 AI Agents Overview

The system includes 6 specialized CrewAI agents that work together to provide comprehensive AI-powered business directory features:

### 1. **Business Listing Optimizer Agent**
- **Role**: Business Listing Optimization Specialist
- **Purpose**: Enhances business descriptions, optimizes keywords, improves SEO
- **Features**:
  - SEO-optimized description generation
  - Keyword analysis and suggestions
  - Category optimization recommendations
  - Engagement score calculation

### 2. **Lead Scoring Agent**
- **Role**: Lead Scoring and Qualification Specialist  
- **Purpose**: Scores and qualifies leads from directory interactions
- **Features**:
  - Behavioral analysis (clicks, form submissions, website visits)
  - Lead categorization (hot, warm, cold)
  - Follow-up priority recommendations
  - Business fit scoring

### 3. **Content Curator Agent**
- **Role**: Content Curation and Management Specialist
- **Purpose**: Manages events, blog posts, community content curation
- **Features**:
  - Blog post generation
  - Event creation and description
  - Community discussion topics
  - Content quality scoring

### 4. **Review Analysis Agent**
- **Role**: Review Analysis and Sentiment Specialist
- **Purpose**: Analyzes business reviews and provides actionable insights
- **Features**:
  - Sentiment analysis (positive, negative, neutral)
  - Theme extraction from reviews
  - Strengths and improvement identification
  - Response strategy suggestions

### 5. **Search Intelligence Agent**
- **Role**: Search Intelligence and Recommendation Specialist
- **Purpose**: Provides personalized search recommendations and enhanced results
- **Features**:
  - Personalized business recommendations
  - Search intent analysis
  - Semantic search matching
  - Query optimization suggestions

### 6. **Directory SEO Agent**
- **Role**: Directory SEO and Visibility Specialist
- **Purpose**: Optimizes directory listings for search engines
- **Features**:
  - Local SEO optimization
  - Directory-specific optimization
  - Visibility improvement strategies
  - Search ranking enhancements

## 🛠️ AI-Powered API Endpoints

### Core AI Features

#### 1. **Listing Optimization**
```http
POST /ai/optimize-listing
Content-Type: application/json

{
  "business_id": "biz_123",
  "name": "Tech Solutions Pro",
  "category": "technology",
  "description": "We provide IT solutions",
  "address": "123 Main St, San Francisco, CA",
  "services": ["IT Support", "Cloud Services"]
}
```

**Response:**
```json
{
  "status": "success",
  "optimization": {
    "optimized_description": "Enhanced SEO-friendly description",
    "suggested_keywords": ["IT support", "cloud services", "professional"],
    "category_recommendations": ["IT Services", "Technology", "Professional Services"],
    "seo_improvements": ["Add location-specific keywords", "..."],
    "engagement_score": 0.85,
    "ai_confidence": 0.85
  }
}
```

#### 2. **Review Analysis**
```http
POST /ai/analyze-reviews
Content-Type: application/json

{
  "business_id": "biz_123",
  "reviews": [
    {"rating": 5, "text": "Excellent service!", "date": "2024-01-15"},
    {"rating": 4, "text": "Good quality work", "date": "2024-01-10"}
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "analysis": {
    "overall_sentiment": "positive",
    "sentiment_distribution": {"positive": 0.75, "neutral": 0.25, "negative": 0.0},
    "key_themes": ["service", "quality"],
    "strengths": ["High customer satisfaction", "Quality service delivery"],
    "areas_for_improvement": [],
    "recommendation_score": 0.9
  }
}
```

#### 3. **Personalized Recommendations**
```http
GET /ai/recommendations/{user_id}?categories=technology,services&limit=5
```

**Response:**
```json
{
  "status": "success",
  "recommendations": [
    {
      "business_id": "rec_tech_1",
      "name": "Recommended Technology Business 1", 
      "category": "technology",
      "relevance_score": 0.9,
      "reason": "Based on your interest in technology",
      "confidence": 0.85
    }
  ]
}
```

#### 4. **Enhanced Search**
```http
POST /ai/enhance-search
Content-Type: application/json

{
  "query": "IT support services",
  "results": [
    {"business_id": "biz1", "name": "Tech Pro", "rating": 4.5}
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "enhancement": {
    "enhanced_results": [...],
    "search_suggestions": ["IT support near me", "best IT support"],
    "search_intent": "local_search",
    "semantic_matches": [...],
    "result_insights": {"quality_insight": "High quality results"}
  }
}
```

#### 5. **Lead Scoring**
```http
POST /ai/score-leads
Content-Type: application/json

{
  "leads": [
    {
      "lead_id": "lead_001",
      "phone_clicked": true,
      "website_visited": true,
      "form_submitted": false,
      "category_match": true,
      "location_match": true
    }
  ]
}
```

**Response:**
```json
{
  "status": "success", 
  "scored_leads": [
    {
      "lead_id": "lead_001",
      "ai_score": 0.8,
      "lead_category": "hot",
      "follow_up_priority": "high",
      ...
    }
  ]
}
```

#### 6. **Content Generation**
```http
POST /ai/generate-content
Content-Type: application/json

{
  "type": "blog_post",
  "topic": "Digital Marketing for Small Businesses",
  "target_audience": "small business owners"
}
```

**Response:**
```json
{
  "status": "success",
  "generated_content": {
    "content_type": "blog_post",
    "title": "The Ultimate Guide to Digital Marketing for Small Business Owners",
    "content": "Discover everything you need to know...",
    "meta_description": "Expert guide on digital marketing...",
    "tags": ["digital marketing", "small business owners", "guide", "tips"],
    "estimated_read_time": "8 minutes",
    "quality_score": 0.8
  }
}
```

### Enhanced Core Endpoints

The AI integration also enhances existing endpoints:

#### **Enhanced Search** (`GET /search`)
Now includes AI-powered features:
- `ai_insights`: Search intent analysis, semantic matches
- `ai_suggestions`: Intelligent search recommendations  
- `ai_enhanced`: Boolean indicating AI enhancement status

#### **Enhanced Performance Analytics** (`GET /performance/{client_id}`)
Now includes AI insights:
- `ai_insights.review_analysis`: Detailed sentiment analysis
- `ai_insights.ai_recommendations`: AI-generated improvement suggestions
- `ai_insights.predicted_performance`: Performance predictions

## 🚀 Installation & Setup

### 1. Install Dependencies

```bash
# Install AI dependencies
pip install crewai>=0.177.0 langchain>=0.1.0 openai>=1.13.3 langchain-openai>=0.0.2 langchain-community>=0.0.10

# Or install from requirements.txt
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Required for full AI features
export OPENAI_API_KEY=your_openai_api_key_here

# Optional environment variables
export LOG_LEVEL=INFO
export REDIS_URL=redis://localhost:6379
export POSTGRES_URL=postgresql://user:pass@localhost/dbname
```

### 3. Start the Service

#### Option A: Using the AI-enabled startup script
```bash
python start_with_ai.py
```

#### Option B: Standard startup
```bash
python directory_service.py
# or
uvicorn directory_service:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Test the Integration

```bash
# Run comprehensive AI tests
python test_ai_integration.py
```

## 🔧 Configuration Options

### AI Manager Configuration

The `DirectoryAIManager` class can be configured with:

```python
# In ai_agents.py
ai_manager = DirectoryAIManager()

# Custom LLM configuration
ai_manager.llm = ChatOpenAI(
    temperature=0.7,  # Creativity level (0.0 - 1.0)
    model_name="gpt-4-turbo-preview",  # Model selection
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
```

### Agent Customization

Each agent can be customized:

```python
# Example: Customize the listing optimizer
listing_optimizer = Agent(
    role="Business Listing Optimization Specialist",
    goal="Your custom optimization goals",
    backstory="Custom agent backstory",
    verbose=True,  # Enable detailed logging
    allow_delegation=False,  # Prevent agent delegation
    llm=custom_llm
)
```

## 📊 Monitoring & Analytics

### AI Service Status
Check AI service health:
```http
GET /ai/status
```

### Performance Metrics
The AI integration tracks:
- **Optimization Success Rate**: Percentage of successful listing optimizations
- **Review Analysis Accuracy**: Sentiment analysis accuracy metrics  
- **Recommendation Relevance**: User engagement with AI recommendations
- **Lead Scoring Effectiveness**: Conversion rates for AI-scored leads
- **Content Quality Scores**: AI-generated content performance

## 🔍 Troubleshooting

### Common Issues

#### 1. **AI Services Unavailable**
```
Error: AI services are currently unavailable
```
**Solution**: Check dependencies and API keys:
```bash
pip install crewai langchain openai
export OPENAI_API_KEY=your_key_here
```

#### 2. **Agent Initialization Failed**
```
Error: Agent initialization failed
```
**Solutions**:
- Verify OpenAI API key is valid
- Check internet connection
- Ensure sufficient API quota

#### 3. **Performance Issues**
**Symptoms**: Slow AI responses
**Solutions**:
- Use faster models (gpt-3.5-turbo instead of gpt-4)
- Implement caching for frequent requests
- Reduce agent verbosity

### Fallback Behavior

When AI services are unavailable, the system provides:
- Basic recommendation fallbacks
- Mock analysis results
- Error messages with guidance
- Graceful degradation to non-AI features

## 🔐 Security Considerations

### API Key Security
- Never commit API keys to version control
- Use environment variables or secure vaults
- Rotate keys regularly

### Data Privacy
- Review data sent to AI services
- Implement data anonymization when possible
- Follow GDPR/privacy regulations

### Rate Limiting
The AI integration respects:
- OpenAI API rate limits
- Cost management through request optimization
- Timeout handling for long-running tasks

## 📈 Future Enhancements

### Planned Features
1. **Advanced Personalization**: Machine learning-based user preference modeling
2. **Multi-language Support**: Internationalization for global directories
3. **Voice Integration**: Voice-based search and interaction
4. **Predictive Analytics**: Business performance forecasting
5. **Custom Agent Training**: Business-specific agent fine-tuning

### Integration Opportunities
- **CRM Systems**: Enhanced lead management
- **Marketing Automation**: Automated campaign optimization
- **Analytics Platforms**: Advanced business intelligence
- **Social Media**: Social media presence optimization

## 📚 Additional Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [LangChain Guide](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🤝 Contributing

To contribute to the AI integration:

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/ai-enhancement`
3. **Add tests**: Ensure new AI features are tested
4. **Update documentation**: Document new agents/features
5. **Submit pull request**: Include test results and documentation updates

## 📞 Support

For AI integration support:
- **Technical Issues**: Check troubleshooting section
- **Feature Requests**: Submit GitHub issues
- **Configuration Help**: Review configuration options
- **Performance Optimization**: Monitor metrics and adjust accordingly