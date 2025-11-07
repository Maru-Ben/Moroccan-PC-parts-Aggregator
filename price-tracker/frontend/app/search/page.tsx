"use client"

import { useState, useEffect } from "react"
import { useSearchParams } from "next/navigation"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { SearchFilters } from "@/components/search-filters"
import { SearchControls } from "@/components/search-controls"
import { ProductCard } from "@/components/product-card"

// Mock data for demonstration
const mockProducts = [
  {
    id: "1",
    name: "NVIDIA GeForce RTX 4080 SUPER Gaming X Trio",
    image: "/nvidia-rtx-4080.png",
    brand: "MSI",
    category: "graphics-cards",
    minPrice: 12500,
    maxPrice: 13200,
    rating: 4.8,
    reviewCount: 124,
    availability: "in-stock" as const,
    stores: [
      { name: "TechnoMarket", price: 12500, availability: true },
      { name: "PCGamer", price: 12800, availability: true },
      { name: "ElectroShop", price: 13200, availability: true },
    ],
  },
  {
    id: "2",
    name: "AMD Ryzen 7 7800X3D Processor",
    image: "/amd-ryzen-7-7800x3d-processor.jpg",
    brand: "AMD",
    category: "processors",
    minPrice: 4200,
    maxPrice: 4500,
    rating: 4.9,
    reviewCount: 89,
    availability: "limited" as const,
    stores: [
      { name: "TechnoMarket", price: 4200, availability: true },
      { name: "PCGamer", price: 4500, availability: false },
    ],
  },
  {
    id: "3",
    name: "Corsair Vengeance LPX 32GB DDR4-3200",
    image: "/corsair-vengeance-lpx-ram-memory.jpg",
    brand: "Corsair",
    category: "memory",
    minPrice: 1800,
    maxPrice: 2100,
    rating: 4.7,
    reviewCount: 256,
    availability: "in-stock" as const,
    stores: [
      { name: "TechnoMarket", price: 1800, availability: true },
      { name: "PCGamer", price: 1950, availability: true },
      { name: "ElectroShop", price: 2100, availability: true },
    ],
  },
  {
    id: "4",
    name: "Samsung 980 PRO 2TB NVMe SSD",
    image: "/samsung-980-pro-nvme-ssd.jpg",
    brand: "Samsung",
    category: "storage",
    minPrice: 2200,
    maxPrice: 2400,
    rating: 4.6,
    reviewCount: 178,
    availability: "in-stock" as const,
    stores: [
      { name: "TechnoMarket", price: 2200, availability: true },
      { name: "ElectroShop", price: 2400, availability: true },
    ],
  },
  {
    id: "5",
    name: "ASUS ROG Strix B650E-F Gaming WiFi",
    image: "/asus-rog-strix-motherboard.jpg",
    brand: "ASUS",
    category: "motherboards",
    minPrice: 3200,
    maxPrice: 3500,
    rating: 4.5,
    reviewCount: 92,
    availability: "in-stock" as const,
    stores: [
      { name: "TechnoMarket", price: 3200, availability: true },
      { name: "PCGamer", price: 3500, availability: true },
    ],
  },
  {
    id: "6",
    name: "Corsair RM850x 850W 80+ Gold PSU",
    image: "/corsair-rm850x-power-supply.jpg",
    brand: "Corsair",
    category: "power-supply",
    minPrice: 1600,
    maxPrice: 1800,
    rating: 4.8,
    reviewCount: 145,
    availability: "limited" as const,
    stores: [
      { name: "PCGamer", price: 1600, availability: true },
      { name: "ElectroShop", price: 1800, availability: false },
    ],
  },
]

export default function SearchPage() {
  const searchParams = useSearchParams()
  const categoryParam = searchParams.get("category")

  const [viewMode, setViewMode] = useState<"grid" | "list">("grid")
  const [filters, setFilters] = useState<any>({})
  const [filteredProducts, setFilteredProducts] = useState(mockProducts)

  useEffect(() => {
    let filtered = [...mockProducts]

    if (filters.categories && filters.categories.length > 0) {
      filtered = filtered.filter((p) => filters.categories.includes(p.category))
    }

    // Filter by price range
    if (filters.priceRange) {
      filtered = filtered.filter((p) => p.minPrice >= filters.priceRange[0] && p.minPrice <= filters.priceRange[1])
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
  }, [filters])

  return (
    <div className="min-h-screen">
      <Header />

      <main className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold mb-2">Search Results</h1>
          <p className="text-muted-foreground">
            {categoryParam ? `Showing results for "${categoryParam}"` : 'Showing results for "graphics cards"'}
          </p>
        </div>

        <div className="flex gap-8">
          {/* Desktop Filters Sidebar */}
          <aside className="hidden lg:block w-80 flex-shrink-0">
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
            <div className={viewMode === "grid" ? "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6" : "space-y-4"}>
              {filteredProducts.map((product) => (
                <ProductCard key={product.id} product={product} viewMode={viewMode} />
              ))}
            </div>

            {/* Pagination would go here */}
            <div className="mt-12 text-center">
              <p className="text-sm text-muted-foreground">
                Showing {filteredProducts.length} of {mockProducts.length} results
              </p>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
