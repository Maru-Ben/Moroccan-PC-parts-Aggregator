"use client"

import { useState, useEffect } from "react"
import { useSearchParams } from "next/navigation"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { SearchFilters } from "@/components/search-filters"
import { SearchControls } from "@/components/search-controls"
import { ProductCard } from "@/components/product-card"

interface ProductGroup {
  id: string
  name: string
  image: string
  brand: string
  starting_price: number
  availability: "in-stock" | "limited" | "out-of-stock"
  category: string
}
            
interface ApiResponse {
  count: number
  next: string | null
  previous: string | null
  results: Array<{
    id: number
    canonical_name: string
    category: string
    starting_price: string
    brand: string
    representative_image_url: string | null
    created_at: string
    updated_at: string
  }>
}

export default function SearchPage() {
  const searchParams = useSearchParams()
  const queryParam = searchParams.get("q")
  const categoryParam = searchParams.get("category")

  const [viewMode, setViewMode] = useState<"grid" | "list">("grid")
  const [filters, setFilters] = useState<any>({})
  const [products, setProducts] = useState<ProductGroup[]>([])
  const [filteredProducts, setFilteredProducts] = useState<ProductGroup[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Fetch products from API
  useEffect(() => {
    const fetchProducts = async () => {
      if (!queryParam) {
        setProducts([])
        setFilteredProducts([])
        setLoading(false)
        return
      }
      
      setLoading(true)
      setError(null)
      
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/products/search?query=${encodeURIComponent(queryParam)}`
        )
        
        if (!response.ok) {
          throw new Error(`Failed to fetch products: ${response.status}`)
        }
        
        const data: ApiResponse = await response.json()
        
        // Transform API data to match ProductCard interface
        const transformedProducts = data.results.map((item) => {
          const price = parseFloat(item.starting_price)
          
          return {
            id: item.id.toString(),
            name: item.canonical_name,
            image: item.representative_image_url || "/placeholder.svg",
            brand: item.brand,
            starting_price: price,
            availability: "in-stock" as const,
            category: item.category
          }
        })
        
        setProducts(transformedProducts)
        setFilteredProducts(transformedProducts)
      } catch (err) {
        console.error("Error fetching products:", err)
        setError("Failed to load products. Please try again later.")
      } finally {
        setLoading(false)
      }
    }

    fetchProducts()
  }, [queryParam])

  // Apply filters
  useEffect(() => {
    let filtered = [...products]

    if (filters.categories && filters.categories.length > 0) {
      // For now, we'll filter by brand since we don't have category in our transformed data
      filtered = filtered.filter((p) => filters.categories.includes(p.category.toLowerCase()))
    }

    // Filter by price range
    if (filters.priceRange) {
      filtered = filtered.filter((p) => p.starting_price >= filters.priceRange[0] && p.starting_price <= filters.priceRange[1])
    }

    // Filter by brands
    if (filters.brands && filters.brands.length > 0) {
      filtered = filtered.filter((p) => filters.brands.includes(p.brand))
    }

    // Filter by availability
    if (filters.availability && filters.availability.length > 0) {
      filtered = filtered.filter((p) => filters.availability.includes(p.availability))
    }

    setFilteredProducts(filtered)
  }, [filters, products])

  if (loading) {
    return (
      <div className="min-h-screen">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        </main>
        <Footer />
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <div className="text-center py-12">
            <h2 className="text-2xl font-bold mb-4">Error Loading Products</h2>
            <p className="text-muted-foreground mb-6">{error}</p>
            <button 
              className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
              onClick={() => window.location.reload()}
            >
              Try Again
            </button>
          </div>
        </main>
        <Footer />
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      <Header />

      <main className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold mb-2">Search Results</h1>
          <p className="text-muted-foreground">
            {queryParam ? `Showing results for "${queryParam}"` : 'Showing all products'}
          </p>
        </div>

        <div className="flex gap-8">
          {/* Desktop Filters Sidebar */}
          <aside className="hidden lg:block w-80 shrink-0">
            <SearchFilters onFiltersChange={setFilters} initialCategory={categoryParam || undefined} />
          </aside>

          {/* Main Content */}
          <div className="flex-1 min-w-0">
            <div className="mb-6">
              <SearchControls
                viewMode={viewMode}
                onViewModeChange={setViewMode}
                totalResults={filteredProducts.length}
                currentPage={1}
                totalPages={1}
              />
            </div>

            {/* Products Grid/List */}
            {filteredProducts.length > 0 ? (
              <div className={viewMode === "grid" ? "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6" : "space-y-4"}>
                {filteredProducts.map((product) => (
                  <ProductCard key={product.id} product={product} viewMode={viewMode} />
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <h3 className="text-xl font-semibold mb-2">No products found</h3>
                <p className="text-muted-foreground">
                  {queryParam 
                    ? `No products match your search for "${queryParam}". Try a different search term.` 
                    : "No products available at the moment."}
                </p>
              </div>
            )}

            {/* Pagination would go here */}
            <div className="mt-12 text-center">
              <p className="text-sm text-muted-foreground">
                Showing {filteredProducts.length} of {products.length} results
              </p>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
