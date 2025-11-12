"use client"

import type React from "react"

import { Search } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useLanguage } from "@/contexts/language-context"
import { useState } from "react"
import { useRouter } from "next/navigation"

export function HeroSection() {
  const [searchQuery, setSearchQuery] = useState("")
  const { t, isRTL } = useLanguage()
  const router = useRouter()

  const handleSearch = () => {
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery.trim())}`)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    handleSearch()
  }

  return (
    <section className="relative py-20 lg:py-32 overflow-hidden">
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: "url('/modern-computer-setup-with-rgb-lighting-and-multip.jpg')",
        }}
      />
      <div className="absolute inset-0 opacity-50 bg-gray-950" />

      {/* Content */}
      <div className="w-full px-4 relative z-10">
        <div className="mx-auto max-w-4xl text-center">
          <div className="mb-6">
            <div className="inline-flex items-center text-sm text-gray-300">
              <span className="inline-flex items-center gap-2 bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-cyan-500/30 rounded-full px-4 py-2 text-cyan-300 font-medium backdrop-blur-sm">
                <div className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></div>
                {t.compareTopRetailers}
              </span>
            </div>
          </div>

          <h1 className="mb-6 text-5xl font-bold tracking-tight text-white lg:text-6xl">
            {t.heroTitle}
            <br />
            {t.heroSubtitlePart1} <span className="text-cyan-400">{t.heroSubtitlePart2}</span>
          </h1>

          <p className="mb-8 text-lg max-w-2xl mx-auto text-gray-200 font-normal">{t.heroDescription}</p>

          <div className="mx-auto mb-8 max-w-2xl">
            <form onSubmit={handleSubmit} className="flex gap-0">
              <div className="relative flex-1">
                <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 !text-gray-400 pointer-events-none z-10" />
                <Input
                  type="search"
                  placeholder={t.searchPlaceholder2}
                  className="h-12 pl-12 pr-4 text-base gaming-input border-0 rounded-r-none focus:ring-0 focus:border-0 rounded-xl mx-0 bg-[rgba(247,250,252,0.9565217391304348)] text-input"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
              <Button
                type="submit"
                className="h-12 px-6 gaming-button text-white font-medium rounded-l-none border-0 rounded-xl mx-3 bg-border"
                onClick={handleSearch}
              >
                {t.searchParts}
              </Button>
            </form>
          </div>

          <div className="flex flex-wrap justify-center gap-3 text-sm items-center">
            <span className="text-foreground text-base font-semibold">{t.popular}</span>
            {["RTX 4090", "Ryzen 7 7900X3D", "DDR5 32GB", "RTX 4800"].map((term) => (
              <button
                key={term}
                className="bg-secondary/80 hover:bg-primary/20 border border-border hover:border-primary/40 rounded-full px-4 py-2 text-foreground hover:text-primary transition-all duration-200 hover:shadow-lg hover:shadow-primary/10 hover:-translate-y-0.5"
                onClick={() => setSearchQuery(term)}
              >
                {term}
              </button>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
