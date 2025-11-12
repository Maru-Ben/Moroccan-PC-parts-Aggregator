"use client"

import { useState } from "react"
import { Grid3X3, List, SlidersHorizontal } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import { SearchFilters } from "./search-filters"
import { useLanguage } from "@/contexts/language-context" // fixed import to use correct path from language context

interface SearchControlsProps {
  viewMode: "grid" | "list"
  onViewModeChange: (mode: "grid" | "list") => void
  totalResults: number
  currentPage: number
  totalPages: number
}

export function SearchControls({
  viewMode,
  onViewModeChange,
  totalResults,
  currentPage,
  totalPages,
}: SearchControlsProps) {
  const [sortBy, setSortBy] = useState("relevance")
  const { t } = useLanguage()

  return (
    <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex items-center gap-4">
        <p className="text-sm text-muted-foreground">
          {totalResults.toLocaleString()} {t.resultsFoundLabel}
        </p>

        {/* Mobile Filters */}
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="outline" size="sm" className="sm:hidden bg-transparent">
              <SlidersHorizontal className="h-4 w-4 mr-2" />
              {t.mobileFilters}
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-80">
            <SheetHeader>
              <SheetTitle>{t.mobileFilters}</SheetTitle>
            </SheetHeader>
            <div className="mt-6">
              <SearchFilters onFiltersChange={() => {}} />
            </div>
          </SheetContent>
        </Sheet>
      </div>

      <div className="flex items-center gap-2">
        {/* Sort */}
        <Select value={sortBy} onValueChange={setSortBy}>
          <SelectTrigger className="w-40">
            <SelectValue placeholder={t.sortBy} />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="relevance">{t.relevance}</SelectItem>
            <SelectItem value="price-low">{t.priceLowToHigh}</SelectItem>
            <SelectItem value="price-high">{t.priceHighToLow}</SelectItem>
            <SelectItem value="rating">{t.customerRating}</SelectItem>
            <SelectItem value="newest">{t.newestFirst}</SelectItem>
            <SelectItem value="popularity">{t.mostPopular}</SelectItem>
          </SelectContent>
        </Select>

        {/* View Mode Toggle */}
        <div className="flex rounded-lg border">
          <Button
            variant={viewMode === "grid" ? "default" : "ghost"}
            size="sm"
            onClick={() => onViewModeChange("grid")}
            className="rounded-r-none"
          >
            <Grid3X3 className="h-4 w-4" />
            <span className="sr-only">{t.gridView}</span>
          </Button>
          <Button
            variant={viewMode === "list" ? "default" : "ghost"}
            size="sm"
            onClick={() => onViewModeChange("list")}
            className="rounded-l-none"
          >
            <List className="h-4 w-4" />
            <span className="sr-only">{t.listView}</span>
          </Button>
        </div>
      </div>
    </div>
  )
}
