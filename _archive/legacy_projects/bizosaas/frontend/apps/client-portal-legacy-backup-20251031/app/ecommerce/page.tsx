'use client'

/**
 * Saleor E-commerce Admin Interface - SQLAlchemy Admin Style
 * Manages CorelDove e-commerce operations via FastAPI AI Central Hub
 */

import { useState, useEffect } from 'react'
import { 
  Package, 
  ShoppingCart, 
  Users, 
  DollarSign,
  Search,
  Plus,
  Edit,
  Trash2,
  Eye,
  Filter,
  Download,
  Upload,
  BarChart3,
  TrendingUp,
  AlertCircle,
  Settings,
  RefreshCw,
  FileText,
  Tag,
  Star,
  Truck,
  CreditCard
} from 'lucide-react'
import DashboardLayout from '../../components/ui/dashboard-layout';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

// SQLAlchemy-style table interfaces
interface Product {
  id: string
  name: string
  sku: string
  description: string
  price: number
  cost: number
  stock: number
  category: string
  status: 'active' | 'inactive' | 'out_of_stock'
  created_at: string
  updated_at: string
  sales_count: number
  rating: number
  images: string[]
  variants: number
}

interface Order {
  id: string
  order_number: string
  customer_email: string
  customer_name: string
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'
  total: number
  items_count: number
  created_at: string
  shipping_address: string
  payment_status: 'pending' | 'paid' | 'failed' | 'refunded'
  tracking_number?: string
}

interface Customer {
  id: string
  email: string
  first_name: string
  last_name: string
  phone?: string
  total_orders: number
  total_spent: number
  created_at: string
  last_order: string
  status: 'active' | 'inactive'
  address_count: number
}

interface Category {
  id: string
  name: string
  slug: string
  description: string
  product_count: number
  parent_id?: string
  image_url?: string
  seo_title?: string
  seo_description?: string
}

export default function EcommerceAdminPage() {
  const [activeModel, setActiveModel] = useState<'products' | 'orders' | 'customers' | 'categories'>('products')
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedItems, setSelectedItems] = useState<string[]>([])
  
  // Data states
  const [products, setProducts] = useState<Product[]>([])
  const [orders, setOrders] = useState<Order[]>([])
  const [customers, setCustomers] = useState<Customer[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  
  // Modal states
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [editingItem, setEditingItem] = useState<any>(null)

  // Fetch data from FastAPI Central Hub
  useEffect(() => {
    fetchEcommerceData()
  }, [activeModel])

  const fetchEcommerceData = async () => {
    setLoading(true)
    try {
      const endpoint = `${BRAIN_API_URL}/api/brain/saleor/${activeModel}`
      const response = await fetch(endpoint, {
        headers: { 'Content-Type': 'application/json' }
      })

      if (response.ok) {
        const data = await response.json()
        switch (activeModel) {
          case 'products':
            setProducts(data.products || fallbackProducts)
            break
          case 'orders':
            setOrders(data.orders || fallbackOrders)
            break
          case 'customers':
            setCustomers(data.customers || fallbackCustomers)
            break
          case 'categories':
            setCategories(data.categories || fallbackCategories)
            break
        }
      } else {
        // Use fallback data
        switch (activeModel) {
          case 'products':
            setProducts(fallbackProducts)
            break
          case 'orders':
            setOrders(fallbackOrders)
            break
          case 'customers':
            setCustomers(fallbackCustomers)
            break
          case 'categories':
            setCategories(fallbackCategories)
            break
        }
      }
    } catch (error) {
      console.error('Error fetching ecommerce data:', error)
      // Use fallback data on error
      switch (activeModel) {
        case 'products':
          setProducts(fallbackProducts)
          break
        case 'orders':
          setOrders(fallbackOrders)
          break
        case 'customers':
          setCustomers(fallbackCustomers)
          break
        case 'categories':
          setCategories(fallbackCategories)
          break
      }
    } finally {
      setLoading(false)
    }
  }

  const handleBulkAction = async (action: string) => {
    if (selectedItems.length === 0) return

    try {
      const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/${activeModel}/bulk`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action,
          item_ids: selectedItems
        })
      })

      if (response.ok) {
        await fetchEcommerceData()
        setSelectedItems([])
      }
    } catch (error) {
      console.error('Error performing bulk action:', error)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this item?')) return

    try {
      const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/${activeModel}/${id}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' }
      })

      if (response.ok) {
        await fetchEcommerceData()
      }
    } catch (error) {
      console.error('Error deleting item:', error)
    }
  }

  const getModelStats = () => {
    switch (activeModel) {
      case 'products':
        return {
          total: products.length,
          active: products.filter(p => p.status === 'active').length,
          outOfStock: products.filter(p => p.stock === 0).length,
          lowStock: products.filter(p => p.stock > 0 && p.stock < 10).length
        }
      case 'orders':
        return {
          total: orders.length,
          pending: orders.filter(o => o.status === 'pending').length,
          processing: orders.filter(o => o.status === 'processing').length,
          shipped: orders.filter(o => o.status === 'shipped').length
        }
      case 'customers':
        return {
          total: customers.length,
          active: customers.filter(c => c.status === 'active').length,
          newThisMonth: customers.filter(c => 
            new Date(c.created_at) > new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
          ).length,
          highValue: customers.filter(c => c.total_spent > 1000).length
        }
      case 'categories':
        return {
          total: categories.length,
          withProducts: categories.filter(c => c.product_count > 0).length,
          empty: categories.filter(c => c.product_count === 0).length,
          parent: categories.filter(c => !c.parent_id).length
        }
      default:
        return { total: 0, active: 0, pending: 0, inactive: 0 }
    }
  }

  const getStatusColor = (status: string) => {
    const colors = {
      active: 'bg-green-100 text-green-800',
      inactive: 'bg-gray-100 text-gray-800',
      pending: 'bg-yellow-100 text-yellow-800',
      processing: 'bg-blue-100 text-blue-800',
      shipped: 'bg-purple-100 text-purple-800',
      delivered: 'bg-green-100 text-green-800',
      cancelled: 'bg-red-100 text-red-800',
      paid: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
      refunded: 'bg-orange-100 text-orange-800',
      out_of_stock: 'bg-red-100 text-red-800'
    }
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  const getCurrentData = () => {
    switch (activeModel) {
      case 'products': return products
      case 'orders': return orders
      case 'customers': return customers
      case 'categories': return categories
      default: return []
    }
  }

  const filteredData = getCurrentData().filter((item: any) => 
    Object.values(item).some(value => 
      value?.toString().toLowerCase().includes(searchTerm.toLowerCase())
    )
  )

  const stats = getModelStats()

  if (loading) {
    return (
      <DashboardLayout title="E-commerce Management" description="Manage your Saleor e-commerce operations">
        <div className="flex items-center justify-center h-96">
          <RefreshCw className="w-8 h-8 animate-spin text-blue-600" />
          <span className="ml-2 text-lg text-gray-900 dark:text-white">Loading e-commerce data...</span>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout title="E-commerce Management" description="Manage your Saleor e-commerce operations">
      {/* SQLAlchemy Admin Header */}
      <div className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                Saleor E-commerce Admin
              </h1>
              <p className="text-gray-600 dark:text-gray-300 mt-1">
                SQLAlchemy-style interface for CorelDove store management
              </p>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={fetchEcommerceData}
                className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Refresh
              </button>
              <button
                onClick={() => setShowCreateModal(true)}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <Plus className="w-4 h-4 mr-2" />
                Create New
              </button>
            </div>
          </div>
        </div>

        {/* Model Navigation - SQLAlchemy style tabs */}
        <div className="border-b border-gray-200 dark:border-gray-700">
          <nav className="flex space-x-8 px-6">
            {[
              { key: 'products', label: 'Products', icon: Package, count: products.length },
              { key: 'orders', label: 'Orders', icon: ShoppingCart, count: orders.length },
              { key: 'customers', label: 'Customers', icon: Users, count: customers.length },
              { key: 'categories', label: 'Categories', icon: Tag, count: categories.length }
            ].map((model) => (
              <button
                key={model.key}
                onClick={() => setActiveModel(model.key as any)}
                className={`flex items-center py-4 px-1 border-b-2 font-medium text-sm ${
                  activeModel === model.key
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <model.icon className="w-5 h-5 mr-2" />
                {model.label}
                <span className="ml-2 bg-gray-100 text-gray-900 py-0.5 px-2.5 rounded-full text-xs">
                  {model.count}
                </span>
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="px-6 py-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          {Object.entries(stats).map(([key, value]) => (
            <div key={key} className="bg-white dark:bg-gray-900 overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <BarChart3 className="h-6 w-6 text-gray-400" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate capitalize">
                        {key.replace(/([A-Z])/g, ' $1').toLowerCase()}
                      </dt>
                      <dd className="text-lg font-medium text-gray-900 dark:text-white">{value}</dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* SQLAlchemy Admin Toolbar */}
        <div className="bg-white dark:bg-gray-900 shadow rounded-lg mb-6">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                  <input
                    type="text"
                    placeholder={`Search ${activeModel}...`}
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  />
                </div>
                <button className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                  <Filter className="w-4 h-4 mr-2" />
                  Filter
                </button>
              </div>

              <div className="flex items-center space-x-2">
                {selectedItems.length > 0 && (
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-500">
                      {selectedItems.length} selected
                    </span>
                    <button
                      onClick={() => handleBulkAction('delete')}
                      className="inline-flex items-center px-3 py-1 border border-red-300 text-sm leading-4 font-medium rounded text-red-700 bg-red-50 hover:bg-red-100"
                    >
                      <Trash2 className="w-4 h-4 mr-1" />
                      Delete
                    </button>
                    <button
                      onClick={() => handleBulkAction('export')}
                      className="inline-flex items-center px-3 py-1 border border-gray-300 text-sm leading-4 font-medium rounded text-gray-700 bg-white hover:bg-gray-50"
                    >
                      <Download className="w-4 h-4 mr-1" />
                      Export
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* SQLAlchemy-style Table */}
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-800">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    <input
                      type="checkbox"
                      className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSelectedItems(filteredData.map((item: any) => item.id))
                        } else {
                          setSelectedItems([])
                        }
                      }}
                    />
                  </th>
                  {activeModel === 'products' && (
                    <>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">SKU</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stock</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sales</th>
                    </>
                  )}
                  {activeModel === 'orders' && (
                    <>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Payment</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                    </>
                  )}
                  {activeModel === 'customers' && (
                    <>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Orders</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Spent</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Joined</th>
                    </>
                  )}
                  {activeModel === 'categories' && (
                    <>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Slug</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Products</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Parent</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">SEO</th>
                    </>
                  )}
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                {filteredData.map((item: any) => (
                  <tr key={item.id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <input
                        type="checkbox"
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        checked={selectedItems.includes(item.id)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setSelectedItems([...selectedItems, item.id])
                          } else {
                            setSelectedItems(selectedItems.filter(id => id !== item.id))
                          }
                        }}
                      />
                    </td>
                    
                    {/* Products table rows */}
                    {activeModel === 'products' && (
                      <>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="h-10 w-10 flex-shrink-0">
                              <div className="h-10 w-10 rounded bg-gray-300 flex items-center justify-center">
                                <Package className="w-5 h-5 text-gray-500" />
                              </div>
                            </div>
                            <div className="ml-4">
                              <div className="text-sm font-medium text-gray-900 dark:text-white">{item.name}</div>
                              <div className="text-sm text-gray-500">{item.category}</div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{item.sku}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">${item.price}</td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`text-sm ${item.stock < 10 ? 'text-red-600' : 'text-gray-900 dark:text-white'}`}>
                            {item.stock}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(item.status)}`}>
                            {item.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{item.sales_count}</td>
                      </>
                    )}

                    {/* Orders table rows */}
                    {activeModel === 'orders' && (
                      <>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900 dark:text-white">#{item.order_number}</div>
                          <div className="text-sm text-gray-500">{item.items_count} items</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900 dark:text-white">{item.customer_name}</div>
                          <div className="text-sm text-gray-500">{item.customer_email}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">${item.total}</td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(item.status)}`}>
                            {item.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(item.payment_status)}`}>
                            {item.payment_status}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {new Date(item.created_at).toLocaleDateString()}
                        </td>
                      </>
                    )}

                    {/* Customers table rows */}
                    {activeModel === 'customers' && (
                      <>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900 dark:text-white">
                            {item.first_name} {item.last_name}
                          </div>
                          <div className="text-sm text-gray-500">{item.phone}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{item.email}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{item.total_orders}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">${item.total_spent}</td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(item.status)}`}>
                            {item.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {new Date(item.created_at).toLocaleDateString()}
                        </td>
                      </>
                    )}

                    {/* Categories table rows */}
                    {activeModel === 'categories' && (
                      <>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900 dark:text-white">{item.name}</div>
                          <div className="text-sm text-gray-500">{item.description}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{item.slug}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{item.product_count}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {item.parent_id ? 'Subcategory' : 'Parent'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          {item.seo_title ? (
                            <span className="text-green-600 text-sm">✓ Optimized</span>
                          ) : (
                            <span className="text-red-600 text-sm">✗ Missing</span>
                          )}
                        </td>
                      </>
                    )}

                    {/* Actions column */}
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                      <button
                        onClick={() => {
                          setEditingItem(item)
                          setShowEditModal(true)
                        }}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button className="text-gray-600 hover:text-gray-900">
                        <Eye className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(item.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="bg-white dark:bg-gray-900 px-4 py-3 flex items-center justify-between border-t border-gray-200 dark:border-gray-700 sm:px-6">
            <div className="flex-1 flex justify-between sm:hidden">
              <button className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                Previous
              </button>
              <button className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                Next
              </button>
            </div>
            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-gray-700 dark:text-gray-300">
                  Showing <span className="font-medium">1</span> to <span className="font-medium">{filteredData.length}</span> of{' '}
                  <span className="font-medium">{filteredData.length}</span> results
                </p>
              </div>
              <div>
                <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                  <button className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                    Previous
                  </button>
                  <button className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50">
                    1
                  </button>
                  <button className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                    Next
                  </button>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}

// Fallback data for development/testing
const fallbackProducts: Product[] = [
  {
    id: 'prod-1',
    name: 'Premium Wireless Headphones',
    sku: 'WH-PRE-001',
    description: 'High-quality wireless headphones with noise cancellation',
    price: 199.99,
    cost: 89.99,
    stock: 45,
    category: 'Electronics',
    status: 'active',
    created_at: '2024-01-15T10:30:00Z',
    updated_at: '2024-01-16T14:20:00Z',
    sales_count: 234,
    rating: 4.5,
    images: ['/images/headphones-1.jpg'],
    variants: 3
  },
  {
    id: 'prod-2',
    name: 'Smart Fitness Watch',
    sku: 'SW-FIT-002',
    description: 'Advanced fitness tracking with heart rate monitor',
    price: 299.99,
    cost: 149.99,
    stock: 0,
    category: 'Wearables',
    status: 'out_of_stock',
    created_at: '2024-01-14T15:45:00Z',
    updated_at: '2024-01-16T09:15:00Z',
    sales_count: 156,
    rating: 4.2,
    images: ['/images/smartwatch-1.jpg'],
    variants: 2
  },
  {
    id: 'prod-3',
    name: 'Eco-Friendly Water Bottle',
    sku: 'WB-ECO-003',
    description: 'Sustainable stainless steel water bottle',
    price: 29.99,
    cost: 12.99,
    stock: 8,
    category: 'Lifestyle',
    status: 'active',
    created_at: '2024-01-12T11:20:00Z',
    updated_at: '2024-01-15T16:30:00Z',
    sales_count: 89,
    rating: 4.8,
    images: ['/images/water-bottle-1.jpg'],
    variants: 4
  }
]

const fallbackOrders: Order[] = [
  {
    id: 'ord-1',
    order_number: 'ORD-2024-001',
    customer_email: 'john.doe@example.com',
    customer_name: 'John Doe',
    status: 'processing',
    total: 459.97,
    items_count: 2,
    created_at: '2024-01-16T10:30:00Z',
    shipping_address: '123 Main St, City, State 12345',
    payment_status: 'paid',
    tracking_number: 'TRK123456789'
  },
  {
    id: 'ord-2',
    order_number: 'ORD-2024-002',
    customer_email: 'jane.smith@example.com',
    customer_name: 'Jane Smith',
    status: 'shipped',
    total: 199.99,
    items_count: 1,
    created_at: '2024-01-15T14:20:00Z',
    shipping_address: '456 Oak Ave, City, State 12345',
    payment_status: 'paid',
    tracking_number: 'TRK987654321'
  },
  {
    id: 'ord-3',
    order_number: 'ORD-2024-003',
    customer_email: 'mike.wilson@example.com',
    customer_name: 'Mike Wilson',
    status: 'pending',
    total: 89.97,
    items_count: 3,
    created_at: '2024-01-16T09:15:00Z',
    shipping_address: '789 Pine Rd, City, State 12345',
    payment_status: 'pending'
  }
]

const fallbackCustomers: Customer[] = [
  {
    id: 'cust-1',
    email: 'john.doe@example.com',
    first_name: 'John',
    last_name: 'Doe',
    phone: '+1-555-0123',
    total_orders: 5,
    total_spent: 1245.95,
    created_at: '2023-12-15T10:30:00Z',
    last_order: '2024-01-16T10:30:00Z',
    status: 'active',
    address_count: 2
  },
  {
    id: 'cust-2',
    email: 'jane.smith@example.com',
    first_name: 'Jane',
    last_name: 'Smith',
    phone: '+1-555-0456',
    total_orders: 3,
    total_spent: 567.89,
    created_at: '2024-01-01T14:20:00Z',
    last_order: '2024-01-15T14:20:00Z',
    status: 'active',
    address_count: 1
  },
  {
    id: 'cust-3',
    email: 'mike.wilson@example.com',
    first_name: 'Mike',
    last_name: 'Wilson',
    total_orders: 1,
    total_spent: 89.97,
    created_at: '2024-01-16T09:15:00Z',
    last_order: '2024-01-16T09:15:00Z',
    status: 'active',
    address_count: 1
  }
]

const fallbackCategories: Category[] = [
  {
    id: 'cat-1',
    name: 'Electronics',
    slug: 'electronics',
    description: 'Electronic devices and gadgets',
    product_count: 15,
    seo_title: 'Electronics - High-Tech Gadgets',
    seo_description: 'Discover the latest electronic devices and gadgets'
  },
  {
    id: 'cat-2',
    name: 'Wearables',
    slug: 'wearables',
    description: 'Smart watches and fitness trackers',
    product_count: 8,
    parent_id: 'cat-1',
    seo_title: 'Smart Wearables & Fitness Trackers',
    seo_description: 'Advanced wearable technology for health and fitness'
  },
  {
    id: 'cat-3',
    name: 'Lifestyle',
    slug: 'lifestyle',
    description: 'Lifestyle and everyday products',
    product_count: 12
  }
]