---
name: "Multi-Project Deployment"
description: "Deploy updates across all projects safely"
---

Deploy updates across coreldove, bizoholic, and thrillring with the following protocol:

1. **Pre-deployment validation:**
   - Run tests for each project
   - Verify staging environments
   - Check database backups

2. **Staged deployment:**
   - Deploy to staging first
   - Run integration tests
   - Deploy to production with monitoring

3. **Post-deployment verification:**
   - Health checks for all services
   - Performance monitoring
   - User acceptance validation

Use project-specific sub-agents for each deployment and coordinate through the multi-project coordinator.