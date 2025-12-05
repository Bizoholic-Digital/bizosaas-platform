# Client Portal Quick Start Guide

**Last Updated:** December 4, 2024  
**Version:** 1.0.0  
**Status:** Production Ready

---

## 🚀 Getting Started in 5 Minutes

### Prerequisites

- ✅ Node.js 18+ installed
- ✅ npm or yarn installed
- ✅ Git installed
- ✅ Terminal/Command line access

---

## 📦 Installation

### Step 1: Navigate to Client Portal

```bash
cd /home/alagiri/projects/bizosaas-platform/portals/client-portal
```

### Step 2: Install Dependencies (if not already done)

```bash
npm install
```

### Step 3: Start Development Server

```bash
npm run dev
```

### Step 4: Open in Browser

```
http://localhost:3001
```

**Default Login:**
- Email: `admin@bizoholic.com`
- Password: `admin123`

---

## 🎯 What You Can Do Right Now

### 1. **Content Management (CMS)**

#### View All Pages:
```
1. Login to http://localhost:3001
2. Click "CMS" in sidebar
3. Click "Pages"
4. See all 22 pages
```

#### Edit a Page:
```
1. Click any page (e.g., "Home")
2. Rich text editor opens
3. Use toolbar to format:
   - Bold: Ctrl+B
   - Italic: Ctrl+I
   - Heading: Click H1, H2, or H3
   - List: Click bullet or number icon
   - Link: Select text, click link icon
   - Image: Click image icon, enter URL
4. Click "Save Page"
```

#### Create New Page:
```
1. Click "Create Page" button
2. Fill in:
   - Page Title: "My New Page"
   - Slug: "my-new-page"
   - Status: Published
   - SEO Title: "My New Page - Bizoholic"
   - SEO Description: "Description here"
   - Content: Use rich text editor
3. Click "Create Page"
```

---

### 2. **E-commerce Management**

#### View Products:
```
1. Click "E-commerce" in sidebar
2. Click "Products"
3. See all 12 products with:
   - Product images
   - Prices
   - Categories
   - Stock levels
   - Ratings
```

#### Edit Product:
```
1. Click any product
2. Edit:
   - Name
   - SKU
   - Description
   - Price
   - Stock
   - Category
3. Click "Update Product"
```

#### Create New Product:
```
1. Click "Create Product"
2. Fill in all fields
3. Click "Create Product"
```

---

### 3. **CRM Management**

#### Manage Leads:
```
1. Click "CRM" in sidebar
2. Click "Leads"
3. View all leads
4. Click "Add Lead" to create new
5. Click any lead to edit
```

#### Manage Tasks:
```
1. Click "CRM" → "Tasks"
2. View all tasks
3. Create new task
4. Set priority and due date
```

---

## 🎨 Rich Text Editor Guide

### Toolbar Overview:

```
[B] [I] [U] [S] [</>] | [H1] [H2] [H3] | [•] [1.] ["] | [←] [↔] [→] [≡] | [🔗] [🖼] | [↶] [↷]
```

### Keyboard Shortcuts:

| Action | Shortcut |
|--------|----------|
| Bold | `Ctrl+B` / `Cmd+B` |
| Italic | `Ctrl+I` / `Cmd+I` |
| Underline | `Ctrl+U` / `Cmd+U` |
| Undo | `Ctrl+Z` / `Cmd+Z` |
| Redo | `Ctrl+Shift+Z` / `Cmd+Shift+Z` |

### Common Tasks:

#### Add a Link:
```
1. Select text
2. Click link icon (🔗)
3. Enter URL
4. Press Enter
```

#### Add an Image:
```
1. Click image icon (🖼)
2. Enter image URL
3. Press Enter
```

#### Create a List:
```
1. Click bullet (•) or number (1.) icon
2. Type first item
3. Press Enter for new item
4. Press Enter twice to exit list
```

#### Add a Heading:
```
1. Click H1, H2, or H3 button
2. Type heading text
3. Press Enter to return to paragraph
```

---

## 📊 Available Data

### CMS Pages (22):

**Main Pages:**
- Home
- About Us
- Services
- Contact
- Pricing

**Service Pages:**
- AI Campaign Management
- Content Generation
- Performance Analytics
- Marketing Automation
- Strategy Consulting
- Creative Design
- SEO Optimization
- Email Marketing
- Social Media Marketing

**Additional Pages:**
- Resources
- Case Studies
- Blog
- Privacy Policy
- Terms of Service
- Careers
- Partners
- FAQ

### E-commerce Products (12):

**Digital Services ($199-$799):**
- AI Campaign Management - Starter
- AI Campaign Management - Professional
- Content Generation Package
- SEO Optimization Service
- Social Media Management - Basic

**Software ($39-$79/mo):**
- Marketing Analytics Dashboard
- Email Marketing Platform
- Landing Page Builder

**Education ($149-$199):**
- Digital Marketing Masterclass
- SEO Fundamentals Course

**Consultation ($199-$299):**
- Marketing Strategy Session
- Website Audit Service

---

## 🔧 Development Mode Features

### Fallback Data:
When the backend is not running, the portal uses fallback data:
- ✅ All pages display immediately
- ✅ All products show with details
- ✅ CRM data is available
- ✅ Forms work (data not persisted)

### What Works Without Backend:
- ✅ View all content
- ✅ Edit pages/products (UI updates)
- ✅ Create new items (UI updates)
- ✅ Rich text editor
- ✅ Navigation
- ✅ Search and filters

### What Requires Backend:
- ❌ Data persistence (saves to database)
- ❌ Real-time updates
- ❌ User authentication (uses mock)
- ❌ File uploads
- ❌ Email notifications

---

## 🎯 Common Tasks

### Task 1: Update Homepage Content

```bash
# Steps:
1. Navigate to CMS → Pages
2. Click "Home"
3. Edit content in rich text editor:
   - Update heading
   - Add new sections
   - Insert images
   - Format text
4. Update SEO fields
5. Click "Save Page"
```

### Task 2: Add New Product

```bash
# Steps:
1. Navigate to E-commerce → Products
2. Click "Create Product"
3. Fill in:
   - Name: "New Service Package"
   - SKU: "NEW-SERV-001"
   - Description: "Complete description"
   - Price: 499.00
   - Category: "Digital Services"
   - Stock: 999
4. Click "Create Product"
```

### Task 3: Manage CRM Leads

```bash
# Steps:
1. Navigate to CRM → Leads
2. View all leads
3. Click "Add Lead"
4. Fill in lead details
5. Click "Create Lead"
6. Lead appears in list
```

### Task 4: Create Blog Post

```bash
# Steps:
1. Navigate to CMS → Posts
2. Click "Create Post"
3. Fill in:
   - Title: "10 Marketing Tips"
   - Slug: "10-marketing-tips"
   - Category: "Marketing"
   - Tags: "tips, marketing, growth"
   - Content: Use rich text editor
4. Click "Create Post"
```

---

## 🌓 Dark Mode

### Toggle Dark Mode:
```
1. Click moon/sun icon in header
2. Theme switches automatically
3. Preference saved to localStorage
```

### Dark Mode Features:
- ✅ All pages support dark mode
- ✅ Rich text editor has dark theme
- ✅ Proper contrast for readability
- ✅ Smooth transitions

---

## 📱 Mobile Support

### Responsive Design:
- ✅ Works on all screen sizes
- ✅ Mobile-friendly navigation
- ✅ Touch-optimized controls
- ✅ Responsive tables and grids

### Mobile Testing:
```
1. Open browser DevTools (F12)
2. Click device toolbar icon
3. Select mobile device
4. Test navigation and features
```

---

## 🐛 Troubleshooting

### Issue: Pages Not Loading

**Solution:**
```bash
# Check if dev server is running
npm run dev

# If port 3001 is in use:
lsof -ti:3001 | xargs kill -9
npm run dev
```

### Issue: Rich Text Editor Not Showing

**Solution:**
```bash
# Verify Tiptap packages are installed
npm list @tiptap/react

# If missing, reinstall:
npm install --legacy-peer-deps @tiptap/react @tiptap/starter-kit
```

### Issue: "SSR Hydration Error"

**Solution:**
Already fixed! The editor has `immediatelyRender: false` configured.

### Issue: API Timeout

**Solution:**
This is expected when backend is not running. Fallback data will display automatically after 5 seconds.

---

## 🔐 Authentication

### Current Setup (Development):
- Mock authentication enabled
- Auto-login as admin user
- Session persists in localStorage

### Login Credentials:
```
Email: admin@bizoholic.com
Password: admin123
```

### Future (Production):
- Real SSO authentication via Auth Service (port 8008)
- JWT tokens
- Role-based access control
- Multi-tenant support

---

## 📂 Project Structure

```
portals/client-portal/
├── app/
│   ├── api/brain/          # API routes (proxy to Brain Gateway)
│   │   ├── django-crm/     # CRM endpoints
│   │   ├── wagtail/        # CMS endpoints
│   │   └── saleor/         # E-commerce endpoints
│   ├── dashboard/          # Main dashboard page
│   └── login/              # Login page
├── components/
│   ├── RichTextEditor.tsx  # Tiptap WYSIWYG editor
│   ├── PageForm.tsx        # Page editing form
│   ├── PostForm.tsx        # Blog post form
│   ├── CMSContent.tsx      # CMS management
│   ├── EcommerceContent.tsx # E-commerce management
│   └── CRMContent.tsx      # CRM management
└── public/                 # Static assets
```

---

## 🚀 Performance Tips

### Optimize Loading:
1. Use fallback data for instant UI
2. API calls timeout after 5 seconds
3. Images load from CDN (Unsplash)
4. Client-side rendering for editor

### Best Practices:
- ✅ Keep pages under 100KB
- ✅ Optimize images before upload
- ✅ Use semantic HTML
- ✅ Minimize inline styles
- ✅ Enable caching

---

## 📊 Analytics & Monitoring

### Available Metrics:
- Page views
- User actions
- API response times
- Error rates
- Content updates

### View Analytics:
```
1. Navigate to Analytics tab
2. View real-time dashboards
3. Export reports
```

---

## 🎓 Learning Resources

### Documentation:
1. `CLIENT_PORTAL_CRUD_FIXES.md` - CRUD operations
2. `TIPTAP_EDITOR_IMPLEMENTATION.md` - Editor guide
3. `CMS_PAGES_INVENTORY.md` - Page inventory
4. `CMS_PAGE_BUILDER_STRATEGY.md` - Strategy guide

### External Resources:
- [Tiptap Documentation](https://tiptap.dev)
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com)

---

## ✅ Quick Checklist

### First Time Setup:
- [ ] Install dependencies (`npm install`)
- [ ] Start dev server (`npm run dev`)
- [ ] Login to portal
- [ ] Browse CMS pages
- [ ] Test rich text editor
- [ ] View products
- [ ] Check CRM data

### Daily Workflow:
- [ ] Start dev server
- [ ] Check for updates
- [ ] Create/edit content
- [ ] Test changes
- [ ] Review analytics

---

## 🎯 Next Steps

### Immediate:
1. ✅ Explore all 22 pages
2. ✅ Test rich text editor
3. ✅ Create sample content
4. ✅ Customize to your brand

### This Week:
1. Add more products
2. Create blog posts
3. Upload media
4. Customize pages

### This Month:
1. Connect to backend
2. Enable data persistence
3. Add team members
4. Launch to production

---

## 🆘 Support

### Need Help?
- Check documentation files
- Review error messages
- Test in different browser
- Clear cache and reload

### Common Commands:
```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Run production build
npm start

# Install dependencies
npm install

# Clear cache
rm -rf .next
npm run dev
```

---

## 🎉 You're Ready!

**Everything is set up and ready to use!**

Start by:
1. Opening http://localhost:3001
2. Exploring the CMS pages
3. Testing the rich text editor
4. Creating your first piece of content

**Happy content creating!** 🚀
