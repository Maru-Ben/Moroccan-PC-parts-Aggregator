"use client"

import type React from "react"
import { Search, Menu, Hexagon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { LanguageSwitcher } from "@/components/language-switcher"
import { useLanguage } from "@/contexts/language-context"
import { useState } from "react"
import Link from "next/link"

export function Header() {
  const [searchQuery, setSearchQuery] = useState("")
  const { t, isRTL } = useLanguage()

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      // Navigate to search results
      window.location.href = `/search?q=${encodeURIComponent(searchQuery)}`
    }
  }

  return (
    <header className="sticky top-0 z-50 w-full sleek-card border-b border-white/10 backdrop-blur-md">
      <div className="container mx-auto px-4">
        <div className={`flex h-16 items-center justify-between ${isRTL ? "flex-row-reverse" : ""}`}>
          <Link href="/" className="flex items-center space-x-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-primary/80 to-primary border border-primary/30">
              <Hexagon className="h-6 w-6 text-white" />
            </div>
            <span className="text-2xl font-bold accent-text">{"PC Parts Morocco"}</span>
          </Link>

          {/* Search Bar - Hidden on mobile */}
          <div className="hidden md:flex flex-1 max-w-2xl mx-8">
            <form onSubmit={handleSearch} className="relative w-full"></form>
          </div>

          <nav className={`hidden lg:flex items-center space-x-6 mx-5 ${isRTL ? "space-x-reverse" : ""}`}>
            <a href="#" className="text-sm font-medium hover:text-primary transition-colors duration-200">
              {t.categories}
            </a>
            <a href="#" className="text-sm font-medium hover:text-primary transition-colors duration-200">
              {t.deals}
            </a>
            <a href="#" className="text-sm font-medium hover:text-primary transition-colors duration-200">
              {t.buildGuide}
            </a>
          </nav>

          {/* Right side actions */}
          <div className={`flex items-center space-x-2 ${isRTL ? "space-x-reverse" : ""}`}>
            <div className="hidden sm:flex">
              <LanguageSwitcher />
            </div>

            <Button variant="ghost" size="icon" className="lg:hidden hover:bg-primary/10">
              <Menu className="h-4 w-4" />
              <span className="sr-only">{t.menu}</span>
            </Button>
          </div>
        </div>

        <div className="md:hidden pb-4">
          <form onSubmit={handleSearch} className="relative">
            <Search
              className={`absolute ${isRTL ? "right-3" : "left-3"} top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground`}
            />
            <Input
              type="search"
              placeholder={t.searchPlaceholder}
              className={`w-full bg-white/95 backdrop-blur-sm border-0 shadow-md text-gray-900 placeholder:text-gray-500 ${isRTL ? "pr-10 pl-4" : "pl-10 pr-4"}`}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </form>
        </div>
      </div>
    </header>
  )
}
