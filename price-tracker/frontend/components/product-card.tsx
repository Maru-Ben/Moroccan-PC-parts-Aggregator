import { Star, ShoppingCart, Eye } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import Link from "next/link"

interface ProductCardProps {
  product: {
    id: string
    name: string
    image: string
    brand: string
    starting_price: number
    availability: "in-stock" | "limited" | "out-of-stock"
    category: string
  }
  viewMode: "grid" | "list"
}

       

export function ProductCard({ product, viewMode }: ProductCardProps) {
  const formatPrice = (price: number) => `${price.toLocaleString()} MAD`

  const availabilityColors = {
    "in-stock": "bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400",
    limited: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400",
    "out-of-stock": "bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400",
  }

  const availabilityText = {
    "in-stock": "In Stock",
    limited: "Limited Stock",
    "out-of-stock": "Out of Stock",
  }

  if (viewMode === "list") {
    return (
      <Card className="hover:shadow-lg transition-shadow">
        <CardContent className="p-6">
          <div className="flex gap-6">
            <div className="shrink-0">
              <Link href={`/product/${product.id}`}>
                <img
                  src={product.image || "/placeholder.svg"}
                  alt={product.name}
                  className="h-24 w-24 rounded-lg object-cover hover:opacity-80 transition-opacity"
                />
              </Link>
            </div>

            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">{product.brand}</p>
                  <Link href={`/product/${product.id}`}>
                    <h3 className="font-semibold text-lg mb-2 text-balance hover:text-accent transition-colors">
                      {product.name}
                    </h3>
                  </Link>
{/* 
                  <div className="flex items-center gap-2 mb-2">
                    <div className="flex items-center">
                      <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                      <span className="ml-1 text-sm font-medium">{product.rating}</span>
                    </div>
                    <span className="text-sm text-muted-foreground">({product.reviewCount} reviews)</span>
                    <Badge className={availabilityColors[product.availability]} variant="secondary">
                      {availabilityText[product.availability]}
                    </Badge>
                  </div> */}
                </div>

                <div className="text-right">
                  <div className="mb-2">
                    <p className="text-2xl font-bold text-accent">{formatPrice(product.starting_price)}</p>
                    {/* {product.minPrice !== product.maxPrice && (
                      <p className="text-sm text-muted-foreground">to {formatPrice(product.maxPrice)}</p>
                    )} */}
                  </div>
                  <p className="text-xs text-muted-foreground mb-3">available in 3 stores</p>

                  <div className="flex gap-2">
                    <Button size="sm" variant="outline">
                      <Eye className="h-4 w-4 mr-1" />
                      Compare
                    </Button>
                    <Button size="sm" asChild>
                      <Link href={`/product/${product.id}`}>
                        <ShoppingCart className="h-4 w-4 mr-1" />
                        View Details
                      </Link>
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="group hover:shadow-lg transition-all hover:-translate-y-1">
      <CardContent className="p-4 py-0">
        <Link href={`/product/${product.id}`}>
          <div className="aspect-square mb-4 overflow-hidden rounded-lg bg-muted">
            <img
              src={product.image || "/placeholder.svg"}
              alt={product.name}
              className="h-full w-full object-cover transition-transform group-hover:scale-105"
            />
          </div>
        </Link>

        <div className="space-y-2">
          <p className="text-sm text-muted-foreground">{product.brand}</p>
          <Link href={`/product/${product.id}`}>
            <h3 className="font-semibold text-balance leading-tight hover:text-accent transition-colors">
              {product.name}
            </h3>
          </Link>
{/* 
          <div className="flex items-center gap-1">
            <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
            <span className="text-sm font-medium">{product.rating}</span>
            <span className="text-xs text-muted-foreground">({product.reviewCount})</span>
          </div> */}

          <Badge className={availabilityColors[product.availability]} variant="secondary">
            {availabilityText[product.availability]}
          </Badge>

          <div className="pt-2">
            <p className="text-xl font-bold text-accent">{formatPrice(product.starting_price)}</p>
            {/* {product.minPrice !== product.maxPrice && (
              <p className="text-sm text-muted-foreground">to {formatPrice(product.maxPrice)}</p>
            )} */}
            <p className="text-xs text-muted-foreground">available in 3 stores</p>
          </div>

          <div className="flex gap-2 pt-2">
            <Button size="sm" variant="outline" className="flex-1 bg-transparent">
              <Eye className="h-4 w-4 mr-1" />
              Compare
            </Button>
            <Button size="sm" className="flex-1" asChild>
              <Link href={`/product/${product.id}`}>View Details</Link>
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
