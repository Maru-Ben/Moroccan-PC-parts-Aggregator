"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { Slider } from "@/components/ui/slider"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { X } from "lucide-react"
import { useLanguage } from "@/contexts/language-context"

interface SearchFiltersProps {
  onFiltersChange: (filters: any) => void
  initialCategory?: string
}

export function SearchFilters({ onFiltersChange, initialCategory }: SearchFiltersProps) {
  const { t } = useLanguage()
  const [priceRange, setPriceRange] = useState([0, 50000])
  const [selectedBrands, setSelectedBrands] = useState<string[]>([])
  const [selectedAvailability, setSelectedAvailability] = useState<string[]>([])
  const [selectedCategories, setSelectedCategories] = useState<string[]>(initialCategory ? [initialCategory] : [])
  const [activeFilters, setActiveFilters] = useState<string[]>(initialCategory ? [initialCategory] : [])

  const categories = [
    { name: t.processors, value: "cpu" },
    { name: t.graphicsCards, value: "gpu" },
    { name: t.memory, value: "memory" },
    { name: t.storage, value: "storage" },
    { name: t.motherboards, value: "motherboards" },
    { name: t.powerSupply, value: "power-supply" },
  ]

  const brands = [
    { name: "NVIDIA", count: 45 },
    { name: "AMD", count: 38 },
    { name: "Intel", count: 52 },
    { name: "ASUS", count: 67 },
    { name: "MSI", count: 43 },
    { name: "Gigabyte", count: 39 },
    { name: "EVGA", count: 28 },
    { name: "Corsair", count: 34 },
  ]

  const availability = [
    { name: t.inStock, value: "in-stock", count: 234 },
    { name: t.limitedStock, value: "limited", count: 45 },
    { name: t.preOrder, value: "pre-order", count: 12 },
  ]

  useEffect(() => {
    onFiltersChange({
      priceRange,
      brands: selectedBrands,
      availability: selectedAvailability,
      categories: selectedCategories,
    })
  }, [priceRange, selectedBrands, selectedAvailability, selectedCategories])

  const handleCategoryChange = (category: string, categoryName: string, checked: boolean) => {
    const newCategories = checked ? [...selectedCategories, category] : selectedCategories.filter((c) => c !== category)
    setSelectedCategories(newCategories)

    const newActiveFilters = checked ? [...activeFilters, category] : activeFilters.filter((f) => f !== category)
    setActiveFilters(newActiveFilters)
  }

  const handleBrandChange = (brand: string, checked: boolean) => {
    const newBrands = checked ? [...selectedBrands, brand] : selectedBrands.filter((b) => b !== brand)
    setSelectedBrands(newBrands)

    const newActiveFilters = checked ? [...activeFilters, brand] : activeFilters.filter((f) => f !== brand)
    setActiveFilters(newActiveFilters)
  }

  const handleAvailabilityChange = (availability: string, checked: boolean) => {
    const newAvailability = checked
      ? [...selectedAvailability, availability]
      : selectedAvailability.filter((a) => a !== availability)
    setSelectedAvailability(newAvailability)
  }

  const clearAllFilters = () => {
    setPriceRange([0, 50000])
    setSelectedBrands([])
    setSelectedAvailability([])
    setSelectedCategories([])
    setActiveFilters([])
  }

  const removeFilter = (filter: string) => {
    setSelectedBrands(selectedBrands.filter((b) => b !== filter))
    setSelectedCategories(selectedCategories.filter((c) => c !== filter))
    setActiveFilters(activeFilters.filter((f) => f !== filter))
  }

  return (
    <div className="space-y-6">
      {/* Active Filters */}
      {activeFilters.length > 0 && (
        <Card>
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm">{t.activeFilters}</CardTitle>
              <Button variant="ghost" size="sm" onClick={clearAllFilters}>
                {t.clearAll}
              </Button>
            </div>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex flex-wrap gap-2">
              {activeFilters.map((filter) => (
                <Badge key={filter} variant="secondary" className="pr-1">
                  {filter}
                  <button
                    onClick={() => removeFilter(filter)}
                    className="ml-1 hover:bg-muted-foreground/20 rounded-full p-0.5"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle className="text-sm">{t.categories}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {categories.map((category) => (
            <div key={category.value} className="flex items-center space-x-2">
              <Checkbox
                id={category.value}
                checked={selectedCategories.includes(category.value)}
                onCheckedChange={(checked) => handleCategoryChange(category.value, category.name, checked as boolean)}
              />
              <label
                htmlFor={category.value}
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
              >
                {category.name}
              </label>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Price Range */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">{t.priceRange}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Slider value={priceRange} onValueChange={setPriceRange} max={50000} min={0} step={100} className="w-full" />
          <div className="flex items-center justify-between text-sm">
            <span>
              {priceRange[0].toLocaleString()} {t.mad}
            </span>
            <span>
              {priceRange[1].toLocaleString()} {t.mad}
            </span>
          </div>
        </CardContent>
      </Card>

      {/* Brands */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">{t.brand}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {brands.map((brand) => (
            <div key={brand.name} className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id={brand.name}
                  checked={selectedBrands.includes(brand.name)}
                  onCheckedChange={(checked) => handleBrandChange(brand.name, checked as boolean)}
                />
                <label
                  htmlFor={brand.name}
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                >
                  {brand.name}
                </label>
              </div>
              <span className="text-xs text-muted-foreground">({brand.count})</span>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Availability */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">{t.availability}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {availability.map((item) => (
            <div key={item.value} className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id={item.value}
                  checked={selectedAvailability.includes(item.value)}
                  onCheckedChange={(checked) => handleAvailabilityChange(item.value, checked as boolean)}
                />
                <label
                  htmlFor={item.value}
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                >
                  {item.name}
                </label>
              </div>
              <span className="text-xs text-muted-foreground">({item.count})</span>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
