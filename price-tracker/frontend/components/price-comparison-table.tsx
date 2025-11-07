"use client"

import { ExternalLink, Check, X, Clock } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { useLanguage } from "@/contexts/language-context"

interface Store {
  name: string
  price: number
  originalPrice?: number
  availability: "in-stock" | "limited" | "out-of-stock"
  shipping: string
  rating: number
  url: string
  lastUpdated: string
}

interface PriceComparisonTableProps {
  stores: Store[]
}

export function PriceComparisonTable({ stores }: PriceComparisonTableProps) {
  const { t } = useLanguage()
  const formatPrice = (price: number) => `${price.toLocaleString()} ${t.mad}`

  const getAvailabilityIcon = (availability: Store["availability"]) => {
    switch (availability) {
      case "in-stock":
        return <Check className="h-4 w-4 text-green-600" />
      case "limited":
        return <Clock className="h-4 w-4 text-yellow-600" />
      case "out-of-stock":
        return <X className="h-4 w-4 text-red-600" />
    }
  }

  const getAvailabilityText = (availability: Store["availability"]) => {
    switch (availability) {
      case "in-stock":
        return t.inStock
      case "limited":
        return t.limitedStock
      case "out-of-stock":
        return t.outOfStock
    }
  }

  const getAvailabilityColor = (availability: Store["availability"]) => {
    switch (availability) {
      case "in-stock":
        return "bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400"
      case "limited":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400"
      case "out-of-stock":
        return "bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400"
    }
  }

  const sortedStores = [...stores].sort((a, b) => {
    // Sort by availability first (in-stock first), then by price
    if (a.availability !== b.availability) {
      const order = { "in-stock": 0, limited: 1, "out-of-stock": 2 }
      return order[a.availability] - order[b.availability]
    }
    return a.price - b.price
  })

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t.priceComparison}</CardTitle>
        <p className="text-sm text-muted-foreground">
          {t.compareFromStores} {stores.length} {t.stores}
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {sortedStores.map((store, index) => (
            <div
              key={store.name}
              className={`flex items-center justify-between p-4 rounded-lg border ${
                index === 0 && store.availability === "in-stock" ? "border-accent bg-accent/5" : "border-border"
              }`}
            >
              <div className="flex items-center gap-4">
                <div className="flex-shrink-0">
                  {index === 0 && store.availability === "in-stock" && <Badge className="mb-1">{t.bestPrice}</Badge>}
                  <h3 className="font-semibold">{store.name}</h3>
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <span>★ {store.rating}</span>
                    <span>•</span>
                    <span>{store.shipping}</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="text-right">
                  <div className="flex items-center gap-2">
                    <span className="text-2xl font-bold text-accent">{formatPrice(store.price)}</span>
                    {store.originalPrice && store.originalPrice > store.price && (
                      <span className="text-sm text-muted-foreground line-through">
                        {formatPrice(store.originalPrice)}
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    {t.updated} {store.lastUpdated}
                  </p>
                </div>

                <div className="flex items-center gap-3">
                  <Badge variant="secondary" className={getAvailabilityColor(store.availability)}>
                    {getAvailabilityIcon(store.availability)}
                    <span className="ml-1">{getAvailabilityText(store.availability)}</span>
                  </Badge>

                  <Button
                    size="sm"
                    disabled={store.availability === "out-of-stock"}
                    asChild={store.availability !== "out-of-stock"}
                  >
                    {store.availability !== "out-of-stock" ? (
                      <a href={store.url} target="_blank" rel="noopener noreferrer">
                        {t.visitStore}
                        <ExternalLink className="ml-2 h-4 w-4" />
                      </a>
                    ) : (
                      <>{t.outOfStock}</>
                    )}
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-4 text-xs text-muted-foreground">
          <p>{t.pricesUpdated}</p>
        </div>
      </CardContent>
    </Card>
  )
}
