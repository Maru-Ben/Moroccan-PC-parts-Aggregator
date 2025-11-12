"use client"

import { useState } from "react"
import { Star, Heart, Share2, ShoppingCart, ArrowLeft } from "lucide-react"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { ProductGallery } from "@/components/product-gallery"
import { PriceComparisonTable } from "@/components/price-comparison-table"
import { ProductSpecifications } from "@/components/product-specifications"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"
import Link from "next/link"
import { useLanguage } from "@/contexts/language-context"

// Mock product data
const mockProduct = {
  id: "1",
  name: "NVIDIA GeForce RTX 4080 SUPER Gaming X Trio",
  brand: "MSI",
  model: "RTX 4080 SUPER Gaming X Trio",
  images: [
    "/nvidia-rtx-4080.png",
    "/placeholder.svg?height=400&width=400&text=RTX+4080+Side",
    "/placeholder.svg?height=400&width=400&text=RTX+4080+Back",
    "/placeholder.svg?height=400&width=400&text=RTX+4080+Ports",
  ],
  rating: 4.8,
  reviewCount: 124,
  description:
    "The MSI GeForce RTX 4080 SUPER Gaming X Trio delivers exceptional 4K gaming performance with advanced ray tracing and DLSS 3 technology. Featuring a robust triple-fan cooling system and premium build quality.",
  features: [
    "NVIDIA Ada Lovelace Architecture",
    "16GB GDDR6X Memory",
    "Ray Tracing & DLSS 3",
    "Triple Fan Cooling System",
    "RGB Mystic Light",
    "Metal Backplate",
  ],
  specifications: [
    { label: "GPU", value: "NVIDIA GeForce RTX 4080 SUPER" },
    { label: "Memory", value: "16GB GDDR6X" },
    { label: "Memory Interface", value: "256-bit" },
    { label: "Base Clock", value: "2230 MHz" },
    { label: "Boost Clock", value: "2550 MHz" },
    { label: "CUDA Cores", value: "10,240" },
    { label: "RT Cores", value: "80 (3rd Gen)" },
    { label: "Tensor Cores", value: "320 (4th Gen)" },
    { label: "Interface", value: "PCIe 4.0 x16" },
    { label: "Display Outputs", value: "3x DisplayPort 1.4a, 1x HDMI 2.1" },
    { label: "Power Consumption", value: "320W" },
    { label: "Recommended PSU", value: "750W" },
    { label: "Dimensions", value: "336 x 140 x 61 mm" },
    { label: "Weight", value: "1.7 kg" },
  ],
  stores: [
    {
      name: "TechnoMarket",
      price: 12500,
      originalPrice: 13000,
      availability: "in-stock" as const,
      shipping: "Free shipping",
      rating: 4.7,
      url: "https://technomarket.ma",
      lastUpdated: "2 hours ago",
    },
    {
      name: "PCGamer Morocco",
      price: 12800,
      availability: "in-stock" as const,
      shipping: "Free shipping",
      rating: 4.5,
      url: "https://pcgamer.ma",
      lastUpdated: "4 hours ago",
    },
    {
      name: "ElectroShop",
      price: 13200,
      availability: "limited" as const,
      shipping: "50 MAD shipping",
      rating: 4.3,
      url: "https://electroshop.ma",
      lastUpdated: "1 hour ago",
    },
    {
      name: "Digital Store",
      price: 13500,
      availability: "out-of-stock" as const,
      shipping: "Free shipping",
      rating: 4.6,
      url: "https://digitalstore.ma",
      lastUpdated: "6 hours ago",
    },
  ],
}

export default function ProductDetailPage() {
  const [isWishlisted, setIsWishlisted] = useState(false)
  const { t } = useLanguage()
  const bestPrice = Math.min(...mockProduct.stores.filter((s) => s.availability !== "out-of-stock").map((s) => s.price))
  const formatPrice = (price: number) => `${price.toLocaleString()} ${t.mad}`

  return (
    <div className="min-h-screen">
      <Header />

      <main className="container mx-auto px-4 py-8">
        {/* Breadcrumb */}
        <div className="mb-6">
          <Link
            href="/search"
            className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            {t.backToSearch}
          </Link>
        </div>

        <div className="grid lg:grid-cols-2 gap-8 mb-12">
          {/* Product Images */}
          <div>
            <ProductGallery images={mockProduct.images} productName={mockProduct.name} />
          </div>

          {/* Product Info */}
          <div className="space-y-6">
            <div>
              <p className="text-muted-foreground mb-2">{mockProduct.brand}</p>
              <h1 className="text-3xl font-bold text-balance mb-4">{mockProduct.name}</h1>

              <div className="flex items-center gap-4 mb-4">
                <div className="flex items-center">
                  <Star className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                  <span className="ml-1 font-semibold">{mockProduct.rating}</span>
                  <span className="ml-1 text-muted-foreground">
                    ({mockProduct.reviewCount} {t.reviews})
                  </span>
                </div>
                <Badge variant="secondary">{t.bestSeller}</Badge>
              </div>

              <p className="text-muted-foreground text-pretty leading-relaxed">{mockProduct.description}</p>
            </div>

            {/* Price */}
            <div className="border rounded-lg p-6 bg-muted/30">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <p className="text-sm text-muted-foreground">{t.startingFrom}</p>
                  <p className="text-3xl font-bold text-accent">{formatPrice(bestPrice)}</p>
                  <p className="text-sm text-muted-foreground">
                    {t.availableAt} {mockProduct.stores.filter((s) => s.availability !== "out-of-stock").length}{" "}
                    {t.stores}
                  </p>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="icon" onClick={() => setIsWishlisted(!isWishlisted)}>
                    <Heart className={`h-4 w-4 ${isWishlisted ? "fill-red-500 text-red-500" : ""}`} />
                  </Button>
                  <Button variant="outline" size="icon">
                    <Share2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              <Button size="lg" className="w-full">
                <ShoppingCart className="mr-2 h-5 w-5" />
                {t.compareAllStores}
              </Button>
            </div>

            {/* Key Features */}
            <Card>
              <CardContent className="p-6">
                <h3 className="font-semibold mb-4">{t.keyFeatures}</h3>
                <ul className="space-y-2">
                  {mockProduct.features.map((feature, index) => (
                    <li key={index} className="flex items-center text-sm">
                      <div className="w-2 h-2 bg-accent rounded-full mr-3 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Price Comparison Table */}
        <div className="mb-12">
          <PriceComparisonTable stores={mockProduct.stores} />
        </div>

        {/* Specifications */}
        <div className="mb-12">
          <ProductSpecifications specifications={mockProduct.specifications} />
        </div>

        {/* Related Products Section */}
        <div>
          <h2 className="text-2xl font-bold mb-6">{t.relatedProducts}</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <Card key={i} className="group hover:shadow-lg transition-all hover:-translate-y-1">
                <CardContent className="p-4">
                  <div className="aspect-square mb-4 overflow-hidden rounded-lg bg-muted">
                    <img
                      src={`/product-placeholder.png?height=200&width=200&text=Product+${i}`}
                      alt={`Related product ${i}`}
                      className="h-full w-full object-cover transition-transform group-hover:scale-105"
                    />
                  </div>
                  <h3 className="font-semibold text-balance leading-tight mb-2">Related Graphics Card {i}</h3>
                  <p className="text-lg font-bold text-accent">{formatPrice(10000 + i * 1000)}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
